# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** Nguyễn Đình Khang<br>
> **Mã Sinh Viên / Mã Học viên:** 2A202602584<br>
> **Chủ đề Lựa chọn:** Trợ lý Học vụ và Tra cứu Lịch thi VinUni: Tra cứu điểm GPA, lịch thi và đặt lịch tư vấn học vụ với Cố vấn.

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm |
| :--- | :---: | :--- |
| **1. Multi-step Reasoning** | 5 / 5 | Với yêu cầu đặt lịch qua cố vấn chưa biết, Agent phải tra cứu hồ sơ, xác định đúng cố vấn, rồi mới đặt lịch và xác nhận kết quả. |
| **2. Tool Interaction** | 5 / 5 | GPA, lịch thi và trạng thái lịch hẹn là dữ liệu nghiệp vụ động; Agent cần gọi MCP Server thay vì suy đoán. |
| **3. Dynamic Decision** | 5 / 5 | Tên cố vấn và việc có thể đặt lịch hay không phụ thuộc trực tiếp vào Observation của lần tra cứu sinh viên trước đó. |
| **4. Long Horizon Goal** | 4 / 5 | Agent phải giữ xuyên suốt mã sinh viên, mục đích tư vấn và thời điểm hẹn qua nhiều bước trong một phiên xử lý. |
| **TỔNG ĐIỂM AGENTIC FIT** | **19 / 20** | *Bài toán rất phù hợp triển khai Agentic System vì vượt ngưỡng 12/20.* |

---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG (SAU KHI CHẠY TEST SUITE TRÊN API THẬT)

> ⚠️ **YÊU CẦU NGHIỆM THU:** Mở tệp `.env` điền `GEMINI_API_KEY` (hoặc `OPENAI_API_KEY`) để kết nối LLM thật trước khi thực thi `python src/app.py --all`. Bài nộp chỉ dùng Mock Offline Provider sẽ không đạt điểm nghiệm thực tế.

Dán 1 đoạn trích xuất log tiêu biểu từ file `docs/trace_waterfall.json` sinh ra từ phản hồi LLM API thật:

```json
[
  {
    "step": 1,
    "action_type": "TOOL_EXECUTION",
    "tool_name": "academic_query",
    "arguments": {
      "student_id": "SV2026001"
    },
    "observation": {
      "status": "SUCCESS",
      "student_id": "SV2026001",
      "data": {
        "full_name": "Nguyễn Văn An",
        "gpa": 3.85
      }
    },
    "latency_ms": 120.5
  }
]
```

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [ ] Đã điền API Key thật trong `.env` và xác nhận Agent chạy mượt mà trên LLM API thật (Gemini/OpenAI).
- **Tổng số Test Cases đã chạy thành công:** ___ / 5 test cases.
- **Số lượt gọi Tool qua MCP Server chính xác:** ___ lượt.
- **Kết quả đẩy Repo nộp bài:** [ ] Đã Commit và Push mã nguồn thành công lên GitHub cá nhân.

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!
