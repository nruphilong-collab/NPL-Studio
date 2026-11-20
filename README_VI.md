# NPL Studio – CapCut TTS backend

## Đã nối những gì
- `/tts/voices`: trả danh sách giọng từ catalog SDK.
- `/tts/preview`: tạo một file MP3 thật bằng `CapCutClient`.
- `/tts/srt`: tạo một MP3 cho mỗi cue phụ đề, giữ lại start/end để tầng render ghép đúng thời gian.
- `/audio/{filename}`: phát/tải file MP3 đã tạo.
- `/health`: kiểm tra backend.

## Chạy thử trên máy chủ
Yêu cầu Python 3.10+:
```bash
cd backend
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell:
# .venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -e ../capcut-tts-api-main
cp .env.example .env
# Thiết lập NPL_API_KEY trong môi trường trước khi chạy
uvicorn server:app --host 0.0.0.0 --port 8000
```
Mã nguồn SDK nằm trong `capcut-tts-api-main/`. Nếu cài đặt từ thư mục khác, chạy
`pip install -e /đường/dẫn/capcut-tts-api-main`.

Trong NPL Studio, đặt **API endpoint** thành `https://TEN-MIEN-MAY-CHU/` (không phải
`https://editor-api-sg.capcutapi.com`) và nhập cùng `NPL_API_KEY` vào ô API key.

## Giới hạn quan trọng
- Đây là SDK cộng đồng không chính thức; việc có code không đảm bảo dịch vụ CapCut
  chấp nhận request. Tài khoản/quyền truy cập, chữ ký, giới hạn vùng và thay đổi phía
  CapCut có thể làm request thất bại.
- `Voice.json` là catalog tham khảo, không đảm bảo mọi voice còn dùng được.
- `/tts/srt` tạo audio từng câu, chưa tự ghép MP3 thành một video MP4. Cần FFmpeg/
  Android native renderer để đặt audio vào đúng timestamp và render video.
- Không đưa cookie/bearer Capcut vào HTML, APK hoặc kho mã công khai. Chỉ cấu hình
  thông tin phiên hợp lệ trên máy chủ do bạn kiểm soát.
- Chỉ sử dụng theo điều khoản dịch vụ và quyền truy cập hợp lệ.
