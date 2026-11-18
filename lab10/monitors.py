"""★ FILE ĐỘI SỬA (2/3): chỉ số theo dõi (monitor). Thêm ÍT NHẤT MỘT chỉ số bắt được sự cố của bàn.

Mỗi monitor nhận danh sách trial (KHÔNG có nhãn đúng/sai, giống production) và trả về một số.
Một trial = {"ticket_id", "seed", "day", "status", "amount_vnd", "ticket", "events", "ledger", "faults", "outbound",
             "arrive_min", "warehouse", "cost_vnd", "review_kind", "queue_wait_min", "queue_stuck"}
  "day"            một ngày vận hành giả lập: các ticket cùng "day" và cùng "seed" chạy nối nhau trên cùng một sổ cái
  "arrive_min"     phút ticket tới trong ca (0..480)          "warehouse"   kho của đơn
  "cost_vnd"       tiền LLM + nền tảng đã tốn cho ticket      "review_kind" None / "escalated" (trợ lý chuyển người) /
  "queue_wait_min" số phút chờ người duyệt (None nếu không vào hàng chờ)     "recheck" (nhân viên tự kiểm lại)
Chỉ số có thể là kỹ thuật (tỉ lệ model đè số trong ticket lên DB), vận hành (số ca cần người trong giờ đông nhất),
hay kinh doanh (tỉ lệ ticket trợ lý đọc xong vẫn phải chuyển người).

lab10.grade kiểm: monitor chạy không lỗi, và giá trị trên gói sự cố khác giá trị trên bộ nền,
tức là monitor "sáng đèn" khi sự cố xảy ra.
"""


def escalation_rate(trials):
    return sum(t["status"] == "escalated" for t in trials) / max(1, len(trials))


def carrier_fault_rate(trials):
    """Tỉ lệ ticket có ghi lỗi hãng vận chuyển (bắt sự cố phạt dồn dập đối tác)."""
    return sum(len(t.get("faults", [])) for t in trials) / max(1, len(trials))


def force_majeure_rate(trials):
    """Tỉ lệ ticket liên quan đến sự kiện bất khả kháng / thiên tai bão lũ."""
    count = 0
    for t in trials:
        for e in t.get("events", []):
            if e.get("type") == "tracking" and e.get("cause") == "FORCE_MAJEURE":
                count += 1
                break
    return count / max(1, len(trials))


def effective_policy_v4_rate(trials):
    """Share of trials whose guard pinned REFUND-v4; detects stale-policy drift after 2026-12-01."""
    pinned = 0
    for trial in trials:
        for event in trial.get("events", []):
            if event.get("type") == "guard" and event.get("kind") == "policy_pinned":
                pinned += event.get("policy_id") == "REFUND-v4"
                break
    return pinned / max(1, len(trials))


MONITORS = {
    "escalation_rate": escalation_rate,     # có sẵn; KHÔNG tính là metric mới của đội
    "carrier_fault_rate": carrier_fault_rate,
    "force_majeure_rate": force_majeure_rate,
    "effective_policy_v4_rate": effective_policy_v4_rate,
}
STARTER_MONITORS = ("escalation_rate",)
