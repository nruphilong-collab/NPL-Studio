# Báo cáo mổ xẻ NPL Studio APK — nhánh CapCut TTS

Ngày kiểm tra: 2026-11-10
Tệp được kiểm tra: `laziostudio.apk` (39,988,340 bytes)

## Kết quả có bằng chứng từ APK

Trong `classes.dex` có các chuỗi/lớp sau:

- `com/lazio/studio/CapCut`
- `CapCut$AuthorizedIntegration`
- `CapCut$Compatibility`
- `CapCut$RateLimitException`
- `CapCut.java`
- `capcut-voice-v1`
- `capcut_bearer`, `capcut_cookie`, `capcut_compatibility_install_id`
- `capcut_voice`, `capcut_voice_name`, `capcut_voice_resource`
- `https://editor-api-sg.capcutapi.com`
- URL catalog giọng đọc GitHub được ghim theo commit:
  `https://raw.githubusercontent.com/K07VN/capcut-tts-api/7ab87fbd12cbafa60bea4a48903eddf42a939b07/capcut_tts_api/Voice.json`

APK cũng chứa:
- Android `TextToSpeech` / `Voice` classes (có khả năng có TTS hệ thống/fallback).
- FFmpeg Kit native libraries (`libffmpegkit.so`, `libavcodec.so`, `libavfilter.so`, ...), phù hợp cho xử lý/ghép audio-video.
- Tesseract Chinese trained data (`chi_sim.traineddata`).

## Kết luận chính xác

**Có dấu vết rõ ràng của một module CapCut integration/TTS trong APK.** Các lớp `AuthorizedIntegration`, `Compatibility`, `RateLimitException` và các trường cookie/bearer/voice-resource cho thấy ứng dụng có cấu trúc để quản lý tích hợp, xác thực/compatibility, giới hạn tốc độ và lựa chọn giọng.

Nhưng chỉ đọc chuỗi trong DEX không chứng minh được:
1. request TTS thực sự chạy thành công;
2. endpoint còn hoạt động tại thời điểm hiện tại;
3. tài khoản/session nào được chấp nhận;
4. audio artifact có được tải về và ghép đúng timeline hay không.

Không tìm thấy chuỗi JWT rõ ràng trong phần string table đã quét. Đây **không** phải bảo đảm rằng APK không chứa bất kỳ bí mật nào; chỉ có nghĩa là không thấy token JWT dạng văn bản hiển nhiên trong lượt quét này.

## Đặc điểm API tham khảo từ dự án công khai

Repo `K07VN/capcut-tts-api` mô tả luồng TTS:
1. tạo task;
2. truy vấn/poll task;
3. tải audio artifact từ URL trả về.

Repo nêu các route nội bộ dạng `POST /lv/v1/common_task/new` và `POST /lv/v1/common_task/query`. Một repo client khác cảnh báo đây là private/unofficial API, không được CapCut công bố/chứng nhận, có thể thay đổi hoặc bị thu hồi và việc sử dụng có thể vi phạm điều khoản dịch vụ. Vì vậy không nên coi nó là API chính thức hay cam kết ổn định.

## Những gì cần có để ghép thực sự vào NPL Studio

- Mã nguồn Android gốc của NPL Studio (hoặc repo Gradle), không chỉ APK đã biên dịch.
- Một luồng xác thực được phép dùng; không nhúng cookie/bearer cá nhân vào APK phát hành.
- Adapter phía server để giữ credential và xử lý rate-limit/timeout.
- Danh sách voice có thời điểm cập nhật; kiểm tra lại voice/resource ID với dịch vụ trước khi dùng.
- Worker tạo audio theo từng cue SRT, lưu thời gian bắt đầu/kết thúc, sau đó dùng FFmpeg đặt audio vào đúng timestamp và mix với audio gốc.
- Kiểm tra quyền sử dụng, điều khoản và giới hạn của dịch vụ trước khi phát hành.

## Trạng thái

- [x] Xác định dấu vết CapCut TTS/integration trong APK.
- [x] Xác định host API và URL catalog giọng đọc được nhúng.
- [x] Xác định FFmpeg và Android TTS libraries.
- [ ] Decompile đầy đủ `CapCut.java` để xác nhận request body/header và nhánh xử lý audio.
- [ ] Kiểm thử live bằng tài khoản/session được phép.
- [ ] Ghép vào mã nguồn NPL Studio và build APK ký mới.

## Nguồn tham khảo

- https://github.com/K07VN/capcut-tts-api
- https://github.com/jutlyne/capcut-tts
- https://raw.githubusercontent.com/K07VN/capcut-tts-api/7ab87fbd12cbafa60bea4a48903eddf42a939b07/capcut_tts_api/Voice.json
