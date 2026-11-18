# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): `E305HHTP`
- Lớp: `L3A`
- Repo của bàn: `K5-L3A-DAY10-E305HHTP-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): S3

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

## LeMinhPhung-2A202603693

### Phần việc phụ trách

Vận hành và pháp lý. Phiếu B mục B4–B5, B7.5–B7.6. Phiếu C mục C7–C11 và đối chiếu hồ sơ CP5.

### Đóng góp cụ thể

- Rà HAZOP lệnh ghi lỗi hãng, kiểm checklist 9 nhóm việc, viết runbook cho người trực và quy tắc dừng khi có lỗi hãng oan hoặc PII. Đối chiếu bản chốt có một người trực, 6 ca/giờ và SLA 60 phút.
- Phần S3 phụ trách rà trần số lỗi tự động theo hãng, xem tác động tới người duyệt và đối tác, cập nhật risk register và runbook 4–5. Trong phạm vi nộp, S3 đạt 50/50 lượt và 0 lỗi hãng oan. Kiểm riêng đủ 60 lượt để xác nhận cổng vẫn xử lý đúng khi không cắt DN.
- Dùng Codex (AI) để đọc đề và code, soạn thảo Phiếu B và C, hỗ trợ sửa guard và monitor CP4, chạy lệnh đo, đối chiếu tiêu chí, chuẩn bị hồ sơ và kịch bản demo CP5. Số liệu lấy từ report và trace của lab.

### Bằng chứng

- `df2620e`: Phiếu B, phần vận hành và pháp lý. `c9494c6`: kiểm đúng kiện, đọc trần Ops, monitor chạm trần và hồ sơ CP4.
- `R-S3-grade-20261118-193511-540e01` và `R-base-after-20261118-193510-540e01`. Ca ngoài S3 `ADHOC-1@11`: thông báo hãng giảm lộ PII từ 1 xuống 0, vẫn hoàn 25.000đ. Chi tiết tại `submission/evidence/cp5-validation.json`.

### Exit ticket

Gợi ý để Phụng xác nhận. Điều học được: chặn riêng lệnh ghi lỗi giúp bảo vệ hãng trong khi khách vẫn nhận khoản hoàn hợp lệ. Điều còn chưa chắc: khi hai lệnh đến đồng thời và cùng đọc sổ lỗi cũ, cổng có giữ được trần hai lỗi hay không. Bài mô phỏng chạy tuần tự nên cần đo việc này lúc pilot.

## PhamThanhTung-2A202603695

### Phần việc phụ trách

Sản phẩm và kinh doanh. PIC chi phí theo Phiếu B mục B5 và Phiếu C mục C11.

### Đóng góp cụ thể và bằng chứng

Theo hồ sơ của bàn, phần kinh doanh cần đối chiếu chi phí/ticket, ROI, ngân sách LLM và trần hoàn với tiêu chí ký. Xem Phiếu A mục A4 (phần SP-2), Phiếu B mục B7.4 và Phiếu C mục C11. Kết quả bộ nền thu hẹp 4.165đ/ticket, ROI 1,40, trong lần chạy `R-base-after-20261118-193510-540e01`.

### Exit ticket

Gợi ý để Phạm Thanh Tùng xác nhận. Điều học được: chi phí chung đạt ngưỡng vẫn có thể che mất phân khúc đắt hơn làm tay. Điều còn chưa chắc: mức tiết kiệm sau khi chuyển ca DN sang tay sẽ giữ được bao lâu khi số ticket thay đổi. Bổ sung việc đã trực tiếp làm và phần có dùng AI nếu có.

## NguyenCanhHieu-2A202603667

### Phần việc phụ trách

Kỹ sư cổng. PIC chất lượng theo Phiếu B mục B5 và Phiếu C mục C11.

### Đóng góp cụ thể và bằng chứng

Phần kiểm cổng và chất lượng gồm bản chốt vòng 1 `c0c09852`, kiểm hồi quy và report ba mốc. Đối chiếu commit `05a724f` (chốt vòng 1), `1b4448d` (cập nhật hồ sơ) và lần chạy `R-S3-grade-20261118-193511-540e01`.

### Exit ticket

Gợi ý để Nguyễn Cảnh Hiếu xác nhận. Điều học được: chạy đủ phạm vi và chạy phạm vi thu hẹp giúp tách tác dụng của cổng khỏi tác dụng của việc bỏ ticket. Điều còn chưa chắc: bài kiểm tra ẩn và tải đồng thời sẽ phát hiện nhánh nào mà bộ nhìn thấy chưa phủ. Bổ sung việc đã trực tiếp làm và phần có dùng AI nếu có.
