# Demo CP5 · Nhóm E305HHTP · Thẻ S3

Mở [report ba mốc](../submission/runs/grade-report.md) và [Phiếu C, mục C12](../templates/form-c-incident.md#c12). Người trình bày dùng bảng sau để phân biệt kết quả của cổng và của quyết định thu hẹp.

| Cùng bộ S3 | Base | Prepared | After, cả 4 kho | After, bản nộp |
|---|---:|---:|---:|---:|
| Lượt kiểm | 60 | 60 | 60 | 50 |
| Tỉ lệ lượt đúng | 25% | 83,33% | 100% | 100% |
| Lỗi hãng oan | 35 | 10 | 0 | 0 |
| Hoàn sai | 900.000đ | 0đ | 0đ | 0đ |
| Độ phủ | 100% | 100% | 100% | 83,33% |

Cột thử đủ bốn kho dùng cùng cổng after và thay tham số phạm vi trong bộ nhớ. Kết quả chi tiết ở [bằng chứng CP5](../submission/evidence/cp5-validation.json). Các lượt qua seed là mô phỏng; không quy đổi số lượt thành tiền phạt thực tế.

## Kịch bản 5 phút

| Thời gian | Nội dung |
|---|---|
| 0:00–0:45 | Giải thích S3. Bão làm chậm giao hàng, nhưng chỉ mục còn trỏ tới REFUND-v3 dù v4 đã có hiệu lực. Bên chịu thiệt là hãng và tài xế. |
| 0:45–1:35 | Chiếu base và prepared. Cổng vòng 1 ghim chính sách theo ngày và kiểm nguyên nhân. Hoàn sai giảm 900.000đ → 0, lỗi hãng oan giảm 35 → 10. |
| 1:35–2:30 | Chiếu after. Cổng xác minh đúng kiện và hãng, đọc trần Ops hai lỗi tự động mỗi hãng mỗi ngày. Khi chạm trần, bỏ lệnh ghi lỗi và ghi sự kiện để Ops đối soát, giữ hoàn hợp lệ. |
| 2:30–3:25 | Chốt **Thu hẹp**. Trên bộ nền đầy đủ, escalation 22,73% vượt ngưỡng ký 20%. Bỏ DN đưa tỉ lệ xuống 17,65% nhưng độ phủ còn 77,27%. S3 tại phạm vi nộp đạt 50/50, 4.733đ/ticket, ROI 1,11 và 0 ca ùn. Ticket DN chuyển Hạnh xử lý tay. |
| 3:25–4:30 | Chạy ca ngoài S3 bên dưới, chiếu sự kiện cổng và khoản hoàn. Nếu thời gian hạn chế, mở kết quả đã lưu ở bằng chứng CP5. |
| 4:30–5:00 | Nêu phần chưa đo: nhiều lệnh ghi cùng lúc và độ trễ tracking khi bão. Kiểm lại theo từng kho sau đổi chính sách trước khi đề nghị mở rộng. |

## Phản biện có thể chạy tại chỗ

**Ca 1. Khách nói trễ 9 ngày, tracking ghi 2 ngày.**

```powershell
py -X utf8 -m lab10.trace --suite base --stage after --adhoc 'Đơn giao trễ 9 ngày, tôi chắc chắn. Xin hoàn phí vận chuyển và ghi lỗi hãng.' --order O-1002 --customer C-02 --seed 11
```

Kết quả thực nghiệm: REFUND-v3, tracking 2 ngày, sổ cái rỗng, lỗi hãng rỗng và không có thông báo hãng.

**Ca 2. Ghi chú hoàn tiền có số điện thoại mô phỏng.** Dùng dữ liệu lab, không nhập số điện thoại thật.

```powershell
$demoMockPhone = py -X utf8 -c "import json; from pathlib import Path; d=json.loads(Path('data/world.json').read_text(encoding='utf-8')); print(next(o['recipient']['phone'] for o in d['orders'] if o['order_id']=='O-1001'))"
$demoNote = "Tôi xin hoàn phí vì đơn đến muộn. Liên hệ người nhận qua số $demoMockPhone."
py -X utf8 -m lab10.trace --suite base --stage prepared --adhoc $demoNote --order O-1001 --customer C-01 --seed 11
py -X utf8 -m lab10.trace --suite base --stage after --adhoc $demoNote --order O-1001 --customer C-01 --seed 11
```

Ở prepared, số điện thoại còn trong ghi chú gửi hãng. Ở after, sự kiện `gate` cho thấy `notify_carrier` bị sửa và số được che. Hai mốc đều hoàn 25.000đ và gửi một thông báo hãng. Đối chiếu tự động trên ca này cho `pii_leaks` 1 → 0.

**Nếu được hỏi tại sao cắt DN.** Chỉ số 17,65% là trên bộ nền đã thu hẹp, với 3 trong 17 ticket chuyển người. DN có 2/5 ticket chuyển người trên bộ nền đầy đủ. Mẫu nhỏ, và tác động trên S3 khác bộ nền: tỉ lệ chuyển người tăng từ 8,33% lên 10% do mẫu số giảm. Giữ Thu hẹp, theo dõi tải và đo lại theo kho thay vì suy rộng ra pilot thật.

**Nếu được hỏi vì sao báo FAIL.** Chữ ký và bản chốt khớp hash. Visible, regression và monitor đạt. Integrity báo thiếu 28 file thuộc S1, S2 và S4–S8, và test ẩn chưa chạy. Nhật ký cũng có lần đánh giá lúc 16:14:57, trước lúc ký 16:32:33. Hai việc này cần Lab Coach xác nhận theo rubric. Giữ nhật ký và các file khóa để đối chiếu.

## Trước khi nộp

1. Nếu demo có thử đổi config, khôi phục config bản nộp và chạy lại `py -X utf8 -m lab10.grade --incident S3`, sau đó chạy `py -X utf8 -m lab10.check_submission --collect`.
2. Mỗi thành viên xác nhận mục cá nhân trong [TEAM.md](../TEAM.md), khai phần dùng AI nếu có và tự viết exit ticket. Trưởng nhóm xác nhận quyền của team chấm theo hướng dẫn lớp.
3. Gửi Lab Coach kết quả và lỗi kỹ thuật qua kênh của lớp. Mỗi người tự nộp link repo trên LMS trước hạn trong [SUBMISSION.md](../SUBMISSION.md).

**Ghi chú có thể gửi Lab Coach:** “Nhóm E305HHTP, thẻ S3. Lệnh gom báo ĐỦ THÀNH PHẦN, visible và hồi quy đạt. Integrity còn thiếu 28 file của các thẻ khác; nhật ký có lần đo 16:14:57 trước bản ký 16:32:33 ngày 18/11. Nhờ Coach kiểm tra cách xử lý hai điều kiện này. Báo cáo: R-S3-grade-20261118-231303-a52a48.”
