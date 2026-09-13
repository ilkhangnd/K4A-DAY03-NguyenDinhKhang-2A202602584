# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** Nguyễn Đình Khang<br>
> **Mã Sinh Viên / Mã Học viên:** 2A202602584<br>
> **Chủ đề Lựa chọn:** Trợ lý Học vụ và Tra cứu Lịch thi VinUni: Tra cứu điểm GPA, lịch thi và đặt lịch tư vấn học vụ với Cố vấn.

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm |
| :--- | :---: | :--- |
| **1. Multi-step Reasoning** | 4 / 5 | Với yêu cầu "Tra cứu cố vấn của sinh viên có MSSV là SV2026002 rồi đặt lịch với đúng cố vấn đó”, Agent cần thực hiện các bước liên tiếp: Tra cứu hồ sơ, lấy tên cố vấn từ kết quả và dùng thông tin đó để đặt lịch. Tuy nhiên, quy trình này vẫn tương đối rõ ràng, ít nhánh xử lý và chưa cần lập kế hoạch phức tạp. |
| **2. Tool Interaction** | 4 / 5 | GPA, lịch thi, cố vấn học tập và trạng thái lịch hẹn là dữ liệu nghiệp vụ cần lấy từ hệ thống học vụ. Agent cần gọi MCP Server để tra cứu và đặt lịch thay vì tự tạo dữ liệu. Tuy vậy, bài toán hiện chỉ dùng số lượng công cụ giới hạn. |
| **3. Dynamic Decision** | 4 / 5 | Bước tiếp theo phụ thuộc vào Observation: Nếu mã sinh viên không tồn tại thì Agent dừng và báo lỗi; nếu tồn tại thì lấy cố vấn tương ứng rồi đặt lịch. Đây là quyết định dựa trên dữ liệu thực tế, nhưng số tình huống rẽ nhánh chưa nhiều. |
| **4. Long Horizon Goal** | 3 / 5 | Trong một phiên xử lý, Agent cần giữ nhất quán mã sinh viên, mục tiêu tư vấn, thời gian hẹn và cố vấn. Tuy nhiên, hệ thống chưa có bộ nhớ dài hạn giữa nhiều phiên hoặc khả năng theo dõi, đổi và nhắc lịch hẹn sau đó. |
| **TỔNG ĐIỂM AGENTIC FIT** | **15 / 20** | *Đề tài phù hợp để triển khai ReAct Agent vì có dữ liệu động, cần gọi công cụ và có bước xử lý phụ thuộc vào kết quả tra cứu trước đó.* |

---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG (SAU KHI CHẠY TEST SUITE TRÊN API THẬT)

> ⚠️ **YÊU CẦU NGHIỆM THU:** Mở tệp `.env` điền `GEMINI_API_KEY` (hoặc `OPENAI_API_KEY`) để kết nối LLM thật trước khi thực thi `python src/app.py --all`. Bài nộp chỉ dùng Mock Offline Provider sẽ không đạt điểm nghiệm thực tế.

Dán 1 đoạn trích xuất log tiêu biểu từ file `docs/trace_waterfall.json` sinh ra từ phản hồi LLM API thật:

```json
[
  {
    "step": 1,
    "query": "Tôi là sinh viên SV2026002. Hãy tra cứu cố vấn học tập của tôi rồi đặt lịch tư vấn với chính cố vấn đó vào 09:00 ngày 18/09/2026.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "academic_query",
    "arguments": {
      "student_id": "SV2026002"
    },
    "observation": {
      "status": "SUCCESS",
      "student_id": "SV2026002",
      "data": {
        "full_name": "Trần Thị Bình",
        "class": "AI-K4",
        "gpa": 3.6,
        "email": "binh.tt@vinuni.edu.vn",
        "status": "Đang học",
        "advisor": "TS. Lê Thị B",
        "exam_schedule": [
          {
            "course_code": "AISC201",
            "course_name": "Machine Learning",
            "datetime": "08:00 20/09/2026",
            "room": "C202"
          },
          {
            "course_code": "DSCI210",
            "course_name": "Data Visualization",
            "datetime": "09:30 26/09/2026",
            "room": "B304"
          }
        ]
      }
    },
    "latency_ms": 531.5
  },
  {
    "step": 2,
    "query": "Tôi là sinh viên SV2026002. Hãy tra cứu cố vấn học tập của tôi rồi đặt lịch tư vấn với chính cố vấn đó vào 09:00 ngày 18/09/2026.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "schedule_appointment",
    "arguments": {
      "student_id": "SV2026002",
      "datetime_str": "09:00 18/09/2026",
      "advisor_name": "TS. Lê Thị B"
    },
    "observation": {
      "status": "SUCCESS",
      "booking_id": "BK-SV2026002-202609",
      "student_id": "SV2026002",
      "datetime": "09:00 18/09/2026",
      "advisor": "TS. Lê Thị B",
      "message": "Đặt lịch thành công cho sinh viên SV2026002 với TS. Lê Thị B vào lúc 09:00 18/09/2026."
    },
    "latency_ms": 502.2
  },
  {
    "step": 3,
    "query": "Tôi là sinh viên SV2026002. Hãy tra cứu cố vấn học tập của tôi rồi đặt lịch tư vấn với chính cố vấn đó vào 09:00 ngày 18/09/2026.",
    "action_type": "FINAL_ANSWER",
    "thought": "Observation xác nhận lịch hẹn đã được tạo thành công.",
    "output": "Đặt lịch thành công cho sinh viên SV2026002 với TS. Lê Thị B vào lúc 09:00 18/09/2026.",
    "latency_ms": 523.46
  }
]
```

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [X] Đã điền API Key thật trong `.env` và xác nhận Agent chạy mượt mà trên LLM API thật (Gemini/OpenAI).
- **Tổng số Test Cases đã chạy thành công:** 5 / 5 test cases.
- **Số lượt gọi Tool qua MCP Server chính xác:** ___ lượt.
- **Kết quả đẩy Repo nộp bài:** [X] Đã Commit và Push mã nguồn thành công lên GitHub cá nhân.

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!