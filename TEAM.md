# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng):
- Lớp: `L3A`
- Repo của bàn: `K5-L3A-DAY10-E305HHTP-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8):

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; thêm dòng nếu cần. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên        | MSSV        | Vai                    | Trưởng nhóm |
| --: | ---------------- | ----------- | ---------------------- | :---------: |
|   1 | Hoàng Hải Nam    | 2A202603694 | Sản phẩm và kinh doanh |             |
|   2 | Phạm Thanh Tùng  | 2A202603695 | Sản phẩm và kinh doanh |             |
|   3 | Nguyễn Cảnh Hiếu | 2A202603667 | Kỹ sư cổng             |             |
|   4 | Lê Minh Phụng    | 2A202603693 | Vận hành và pháp lý    |             |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## HoangHaiNam-2A202603694

### Phần việc phụ trách

Vai **Sản phẩm và kinh doanh**. Phiếu A: câu 1.1, 1.5 và câu 1.6 (5 chỉ số bắt buộc, ranh giới đầu ra, bốn câu soát), mục A5. Phiếu B: B3 (bản đồ dữ liệu và ví dụ drift), hàng Kinh doanh của B6, B7.4, chỉnh B8. Phiếu C: C1, C3.5, C5 (câu 3.2), C12 (quyết định v2). File: `config/operating_gates.json` mục `business` (`daily_refund_cap_vnd`, `cost_budget_per_ticket_vnd`, `pilot_scope`, `roi_min`).

### Đóng góp cụ thể

- Viết mục tiêu hệ thống (câu 1.1) và các câu tiêu chí "Nếu … thì chúng tôi sẽ …" cho `pass_rate_min` 0,97, `pass_k_min` 0,95 và ba chỉ số an toàn bằng 0, cùng hành động Thu hẹp, Cải tiến thêm hoặc Dừng đi kèm; soát chéo với `decision_rule` đã ký.
- B3: phát hiện ví dụ drift chính sách REFUND-v3 sang REFUND-v4 ngày 2026-12-01 (ngưỡng ngày trễ, hạn mức tự động, FORCE_MAJEURE không còn bị ghi lỗi hãng, cờ `index_active` là bản sao chậm). Thẻ S3 xảy ra đúng cơ chế này.
- B7.4: đặt bốn con số `business` kèm lý do từ `ops_limits` và `ops_facts` (trần hoàn 1.000.000đ/ngày, ngân sách LLM 1.500đ/ticket, ROI tối thiểu 0,6).
- Kiểm B8 (quyết định v1) và sửa các dòng sai: phần cắt dựa vào kho `?`, mã lần chạy, chức danh người ký.
- Thẻ S3: viết C1, C3.5, C5 (câu 3.2); chọn quyết định v2 **Thu hẹp** vì `escalation_rate` bộ nền 0,2273 vượt 0,2 (điều kiện của dòng "Tiếp tục" đã ký), thử trên bản sao tạm rồi áp dụng `business.pilot_scope` = HN, HCM, CT (bỏ kho DN): `escalation_rate` xuống 0,1765, độ phủ 77,3%.
- Rà code cùng đồng đội: thấy cổng PII vòng 1 không chạy vì `write_gate` thoát sớm ở `notify_carrier` (lệnh này không có `order_id` ở cấp ngoài) và chữ khách gõ đi nguyên sang hãng; đã sửa trong `lab10/guards.py`.
- Đã dùng Claude Code (AI) để đọc đề và các phiếu, chạy lệnh đo, soát số liệu, viết nháp các mục trên và sửa `lab10/guards.py` (lọc PII); số liệu lấy từ báo cáo `lab10.eval` và `lab10.grade`.

### Bằng chứng

- Commit: `c47fb3b` (ký tiêu chí), `1821019` (A5), `427dc2c` (B3, B6, B7.4, mục `business`), `03cab66` (chỉnh B8).
- Mã lần chạy: base `R-base-before-20261118-164410-bde05c`, prepared `R-base-prepared-20261118-170437-6a25cc`; thẻ S3: grade `R-S3-grade-20261118-190514-a65420`, after (thu hẹp) `R-S3-after-20261118-190039-a65420`, bộ nền sau khi sửa `R-base-after-20261118-190040-a65420`.
- Dòng trong phiếu: Phiếu A mục A1 đến A5; Phiếu B mục B3, B6, B7.4, B8; Phiếu C mục C1, C3.5, C5, C12.

### Exit ticket

Học được: ngưỡng phải ký trước khi xem số, và dòng "được phép cân nhắc Tiếp tục" của report không tính `escalation_rate`, nên phải đối chiếu thêm `decision_rule` đã ký. Còn chưa chắc: hash tiêu chí được tính trên bản CRLF của máy Windows trong khi bản trên GitHub là LF, nên máy chấm có thể báo lệch (đã báo Lab Coach chưa thì cần xác nhận); và việc cắt kho DN chỉ dựa trên mẫu 5 ticket mỗi ngày.
