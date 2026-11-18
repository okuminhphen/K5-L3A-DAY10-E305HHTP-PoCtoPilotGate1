"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Mặc định dưới đây cho qua tất cả (= mốc base).
"""
import re

from . import helpers as H  # noqa: F401
from .tools import Verdict

_MASK = "[đã ẩn]"
_PHONE_LIKE = re.compile(r"(?:\+?\d[\s.\-]?){8,}\d")


def _scrub_text(text, recipient):
    """Bỏ tên, đường, số điện thoại của người nhận (và mọi dãy số giống SĐT) khỏi chữ tự do gửi cho hãng."""
    out = _PHONE_LIKE.sub(_MASK, text)
    for value in (recipient.get("name"), recipient.get("street")):
        if value:
            out = re.sub(re.escape(value), _MASK, out, flags=re.IGNORECASE)
    return out


def pre_guard(ctx):
    # Ghim phiên bản chính sách hiệu lực tại ngày ctx.as_of
    policies = ctx.tools.lookup_policies()
    policy = H.effective_policy(policies, ctx.as_of)
    if policy:
        indexed = next((p for p in policies if p.get("index_active")), None)
        if indexed is None or indexed["policy_id"] != policy["policy_id"]:
            ctx.log("policy_index_stale", effective=policy["policy_id"],
                    indexed=indexed["policy_id"] if indexed else None, as_of=ctx.as_of)
        return Verdict.allow(policy_id=policy["policy_id"])
    return Verdict.allow()


def write_gate(ctx, action):
    # action = {"tool": "issue_refund", "ticket_id":..., "order_id":..., "amount_vnd":..., "payer":..., ...}
    tool = action.get("tool")

    # notify_carrier không có order_id ở cấp ngoài: lấy từ payload để cổng PII không bị bỏ qua
    order_id = action.get("order_id") or (action.get("payload") or {}).get("order_id")
    order = ctx.tools.lookup_order(order_id)
    if not order:
        if tool == "file_carrier_fault":
            return Verdict.deny("Không tìm thấy đơn trong tracking.")
        return Verdict.allow()

    policies = ctx.tools.lookup_policies()
    policy = H.effective_policy(policies, ctx.as_of)
    if not policy:
        if tool == "file_carrier_fault":
            return Verdict.deny("Không xác định được chính sách đang hiệu lực.")
        return Verdict.allow()

    # Kiểm đúng kiện và đếm lỗi của hãng trước khi ghi vào sổ trong ngày.
    if tool == "file_carrier_fault":
        strike_parcel = next(
            (p for p in order["parcels"] if p["parcel_id"] == action.get("parcel_id")),
            None,
        )
        if strike_parcel is None or not strike_parcel.get("delay_cause"):
            return Verdict.deny("Tracking chưa ghi nhận nguyên nhân trễ của kiện cần xử lý.")

        carrier_id = strike_parcel["carrier_id"]
        if action.get("carrier_id") != carrier_id:
            return Verdict.deny("Hãng trong lệnh ghi không khớp với kiện trong tracking.")

        strike_delay = H.db_delay_days(strike_parcel, ctx.as_of)
        if not H.carrier_at_fault(policy, strike_parcel, strike_delay):
            return Verdict.deny("Hãng vận chuyển không có lỗi theo tracking DB và chính sách hiệu lực.")

        strike_cap = ctx.tools.ops_limits().get("max_auto_strikes_per_carrier_per_day")
        if type(strike_cap) is not int or strike_cap < 0:
            return Verdict.deny("Không xác định được trần ghi lỗi tự động đã thống nhất với Ops.")

        strike_count = len(ctx.tools.fault_rows(carrier_id=carrier_id))
        if strike_count >= strike_cap:
            ctx.log("carrier_strike_cap_hit", carrier_id=carrier_id, count=strike_count,
                    limit=strike_cap, as_of=ctx.as_of)
            return Verdict.deny("Hãng đã chạm trần lỗi tự động. Cần vận hành xác minh.")

        if action.get("delay_days") != strike_delay:
            return Verdict.modify("Sửa số ngày trễ theo dữ liệu tracking của kiện.", delay_days=strike_delay)

    # Cổng 2: Chống hoàn sai tiền / hoàn vượt mức chính sách (khắc phục T-002@55 model override)
    if tool == "issue_refund":
        # Chặn hoàn trùng 2 lần cho cùng một ticket (phòng trường hợp write_retry)
        existing = ctx.tools.ledger_rows(ticket_id=action.get("ticket_id"))
        if existing:
            return Verdict.deny("Đã hoàn tiền cho ticket này rồi, chặn hoàn trùng")

        amount = action.get("amount_vnd", 0)
        approval_id = action.get("approval_id")
        if approval_id:
            # Cổng 4: phê duyệt phải đúng ticket, còn hiệu lực, đủ hạn mức và đúng người đứng tên
            found = ctx.tools.lookup_approvals(approval_id=approval_id)
            appr = found[0] if found else None
            approver = ((ctx.gates or {}).get("operations") or {}).get("approver_id")
            if (appr is None or appr.get("status") != "valid"
                    or appr.get("ticket_id") != action.get("ticket_id")
                    or (appr.get("expires_at") and appr["expires_at"] < ctx.as_of)
                    or amount > appr.get("max_vnd", 0)
                    or (approver and appr.get("approver_id") != approver)):
                ctx.log("invalid_approval", approval_id=approval_id, ticket_id=action.get("ticket_id"))
                return Verdict.escalate("Phê duyệt không hợp lệ cho ticket này, chuyển người duyệt.")

        parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
        delay_days = H.db_delay_days(parcel, ctx.as_of)
        entitled = H.entitlement_vnd(policy, order, delay_days, parcel.get("delay_cause"))
        if entitled <= 0:
            return Verdict.deny("Đơn hàng không đủ điều kiện hoàn tiền theo tracking DB")
        if amount > entitled:
            return Verdict.modify("Chỉnh số tiền hoàn về đúng mức quyền lợi theo chính sách", amount_vnd=entitled)

        if not approval_id:
            # Cổng 5: trần hoàn tự động cho một khách trong ngày (ops_limits đã thống nhất với Finance)
            per_customer_cap = ctx.tools.ops_limits().get("max_auto_refund_per_customer_per_day_vnd")
            if isinstance(per_customer_cap, int):
                seed_rows = getattr(getattr(ctx.tools, "_w", None), "seed_rows", 0)
                today = [r for r in ctx.tools.ledger_rows()[seed_rows:]
                         if r.get("customer_id") == order.get("customer_id") and not r.get("approval_id")]
                spent = sum(r["amount_vnd"] for r in today)
                if spent + amount > per_customer_cap:
                    ctx.log("customer_refund_cap_hit", customer_id=order.get("customer_id"),
                            spent=spent, limit=per_customer_cap)
                    return Verdict.escalate("Khách đã chạm trần hoàn tự động trong ngày, chuyển người duyệt.")

    # Cổng 3: Chặn rò rỉ dữ liệu cá nhân PII khi gửi thông báo ra hãng vận chuyển
    if tool == "notify_carrier":
        payload = action.get("payload") or {}
        recipient = order.get("recipient") or {}
        blocked = {"recipient_contact"} | set((ctx.gates or {}).get("legal", {}).get("pii_fields_blocked_to_third_party") or [])
        cleaned = {k: (_scrub_text(v, recipient) if isinstance(v, str) else v)
                   for k, v in payload.items() if k not in blocked}
        if cleaned != payload:
            return Verdict.modify("Xoá thông tin cá nhân của người nhận (khoá liên hệ và chữ tự do) trước khi gửi bên thứ ba",
                                  payload=cleaned)

    return Verdict.allow()
