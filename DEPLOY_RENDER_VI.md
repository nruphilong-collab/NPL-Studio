# NPL Studio Backend – gói chuẩn bị Render

Gói này đã được sắp xếp để triển khai bằng Render Blueprint. Tao chưa thể bấm deploy thay bạn vì cần đăng nhập tài khoản GitHub/Render của bạn.

## Cách triển khai (làm một lần)
1. Tải ZIP và giải nén.
2. Tạo một repository GitHub mới, ví dụ `nplstudio-backend`, rồi upload toàn bộ nội dung thư mục này lên repo (giữ nguyên cấu trúc, đặc biệt `render.yaml`, `backend/` và `capcut-tts-api-main/`).
3. Trên Render chọn **New → Blueprint**, kết nối repo GitHub vừa tạo và chọn `render.yaml`.
4. Render sẽ tạo web service. Chờ trạng thái Live. Mở URL Render kèm `/health`; kết quả đúng có dạng JSON với `ok: true`.
5. Trong Render → service → Environment, thêm `CAPCUT_COOKIE` hoặc `CAPCUT_BEARER` nếu SDK/tài khoản CapCut của bạn yêu cầu thông tin phiên hợp lệ. Không gửi các giá trị này cho người khác, không commit vào GitHub.
6. Lấy `NPL_API_KEY` trong Environment của Render. Trong NPL Studio nhập URL service làm API endpoint và giá trị `NPL_API_KEY` làm API key.

## Quan trọng
- `NPL_API_KEY` bảo vệ API của riêng NPL Studio; nó KHÔNG phải cookie CapCut.
- Cookie/Bearer CapCut (nếu cần) chỉ đặt trong biến môi trường bí mật của máy chủ. Không dán vào HTML/APK.
- `CORS_ORIGINS` đang để `*` để thử nghiệm; trước khi phát hành cần đổi thành origin chính xác của frontend.
- Gói SDK CapCut là dự án cộng đồng không chính thức. Deploy thành công không đảm bảo CapCut chấp nhận request. Cần kiểm thử `/tts/voices` và `/tts/preview`.
- Render Free có thể ngủ khi không dùng và filesystem tạm có thể bị xóa khi restart/deploy; file MP3 được tạo chỉ nên coi là tạm thời.
- Chưa có URL máy chủ thật cho tới khi bạn triển khai trong tài khoản Render.
