"""
🔌 MULTI-PROVIDER LLM ADAPTER (Google Gemini, OpenAI & Offline Mock)
Hỗ trợ Native Tool Calling và chuyển đổi linh hoạt qua biến môi trường LLM_PROVIDER.
"""

import os
import sys
import json
import re
from typing import Dict, Any, List
from dotenv import load_dotenv

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

load_dotenv()

class BaseLLMProvider:
    """Interface cơ sở cho các LLM Provider hỗ trợ Native Tool Calling"""
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        raise NotImplementedError

    def generate_with_tools(self, prompt: str, tools_schema: List[Dict[str, Any]], system_prompt: str = "") -> Dict[str, Any]:
        raise NotImplementedError


class MockOfflineProvider(BaseLLMProvider):
    """Offline Mock Provider dùng để chạy thử mà không tốn API Key"""
    def __init__(self):
        self.model_name = "Offline-Mock-Model-2026"

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        return f"[Mock Chatbot Response]: Xin chào! Tôi đã nhận được câu hỏi '{prompt}'. (Chế độ Chatbot không có Tool tra cứu dữ liệu thời gian thực)."

    @staticmethod
    def _student_id(prompt: str) -> str:
        match = re.search(r"\bSV\d{7}\b", prompt, flags=re.IGNORECASE)
        return match.group(0).upper() if match else "SV2026001"

    @staticmethod
    def _datetime(prompt: str) -> str:
        match = re.search(r"\b\d{1,2}:\d{2}\s*(?:ngày\s*)?\d{1,2}/\d{1,2}/\d{4}\b", prompt)
        if not match:
            return "14:00 15/09/2026"
        return re.sub(r"\s*ngày\s*", " ", match.group(0)).strip()

    @staticmethod
    def _advisor(prompt: str, fallback: str = "PGS.TS Nguyễn Văn A") -> str:
        for advisor in ("PGS.TS Nguyễn Văn A", "TS. Lê Thị B"):
            if advisor.lower() in prompt.lower():
                return advisor
        return fallback

    @staticmethod
    def _observation(prompt: str) -> Dict[str, Any]:
        marker = "Observation từ MCP Server:\n"
        if marker not in prompt:
            return {}
        raw = prompt.split(marker, 1)[1].split("\n\nDựa duy nhất", 1)[0]
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {}

    def generate_with_tools(self, prompt: str, tools_schema: List[Dict[str, Any]], system_prompt: str = "") -> Dict[str, Any]:
        prompt_lower = prompt.lower()
        student_id = self._student_id(prompt)
        observation = self._observation(prompt)

        # Mô phỏng lượt suy luận sau khi Agent nhận Observation từ MCP Server.
        if observation:
            if observation.get("tool") == "academic_query":
                data = observation.get("data", {})
                if "đặt lịch" in prompt_lower:
                    advisor = data.get("advisor", "PGS.TS Nguyễn Văn A")
                    return {
                        "type": "tool_call",
                        "tool_name": "schedule_appointment",
                        "arguments": {
                            "student_id": observation.get("student_id", student_id),
                            "datetime_str": self._datetime(prompt),
                            "advisor_name": advisor,
                        },
                        "thought": "Observation đã cung cấp cố vấn học tập. Tôi sẽ dùng đúng cố vấn này để đặt lịch."
                    }
                exams = data.get("exam_schedule", [])
                exam_text = "; ".join(
                    f"{exam['course_code']} – {exam['datetime']} tại phòng {exam['room']}"
                    for exam in exams
                ) or "chưa có lịch thi"
                return {
                    "type": "text",
                    "content": (
                        f"Sinh viên {observation.get('student_id')}, {data.get('full_name')}, có GPA {data.get('gpa')}. "
                        f"Cố vấn học tập: {data.get('advisor')}. Lịch thi: {exam_text}."
                    ),
                    "thought": "Observation đã có đủ GPA, cố vấn và lịch thi để trả lời."
                }
            if observation.get("tool") == "schedule_appointment":
                return {
                    "type": "text",
                    "content": observation.get("message", "Đặt lịch tư vấn học vụ thành công."),
                    "thought": "Observation xác nhận lịch hẹn đã được tạo thành công."
                }

        # Mô phỏng nhận diện intent gọi Tool ở lượt đầu tiên.
        needs_lookup = any(keyword in prompt_lower for keyword in ("tra cứu", "gpa", "lịch thi", "cố vấn"))
        if needs_lookup:
            return {
                "type": "tool_call",
                "tool_name": "academic_query",
                "arguments": {"student_id": student_id},
                "thought": f"Người dùng cần dữ liệu học vụ của {student_id}. Tôi sẽ gọi academic_query."
            }
        if "đặt lịch" in prompt_lower:
            return {
                "type": "tool_call",
                "tool_name": "schedule_appointment",
                "arguments": {
                    "student_id": student_id,
                    "datetime_str": self._datetime(prompt),
                    "advisor_name": self._advisor(prompt),
                },
                "thought": f"Người dùng yêu cầu đặt lịch tư vấn cho {student_id}. Tôi sẽ gọi schedule_appointment."
            }
        else:
            return {
                "type": "text",
                "content": f"[Mock Agent Response]: Xin chào! Quy chế học vụ VinUni yêu cầu sinh viên tích lũy tối thiểu 120 tín chỉ và duy trì GPA trên 2.0 để tốt nghiệp.",
                "thought": "Câu hỏi chung về quy chế học vụ, trả lời trực tiếp không cần gọi Tool."
            }


class GeminiProvider(BaseLLMProvider):
    """Google Gemini Provider (Native Tool Calling với Google GenAI SDK)"""
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model_name = model or os.getenv("LLM_MODEL") or "gemini-2.5-flash"

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        if not self.api_key or self.api_key == "your_gemini_api_key_here":
            return "[Gemini Error]: Chưa cấu hình GEMINI_API_KEY trong file .env! Đang sử dụng chế độ Mock."
        try:
            from google import genai
            client = genai.Client(api_key=self.api_key)
            contents = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            response = client.models.generate_content(model=self.model_name, contents=contents)
            return response.text
        except Exception as e:
            return f"[Gemini Exception]: {str(e)}"

    def generate_with_tools(self, prompt: str, tools_schema: List[Dict[str, Any]], system_prompt: str = "") -> Dict[str, Any]:
        if not self.api_key or self.api_key == "your_gemini_api_key_here":
            print("ℹ️ [Gemini Provider]: Chưa tìm thấy GEMINI_API_KEY hợp lệ. Tự động chuyển sang Mock Offline.")
            return MockOfflineProvider().generate_with_tools(prompt, tools_schema, system_prompt)
        
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=self.api_key)
            
            # Chuẩn hóa function declarations cho Gemini SDK
            function_declarations = []
            for tool in tools_schema:
                # Bỏ qua các tool schema chưa được định nghĩa hoàn chỉnh
                if not tool.get("name") or not tool.get("parameters"):
                    continue
                function_declarations.append({
                    "name": tool["name"],
                    "description": tool.get("description", ""),
                    "parameters": tool.get("parameters", {})
                })

            config = types.GenerateContentConfig(
                system_instruction=system_prompt if system_prompt else None,
                tools=[{"function_declarations": function_declarations}] if function_declarations else None,
                temperature=0.2
            )

            response = client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=config
            )

            # Kiểm tra xem Gemini có trả về Tool Call không
            if response.function_calls:
                call = response.function_calls[0]
                args = dict(call.args) if hasattr(call, 'args') and call.args else {}
                return {
                    "type": "tool_call",
                    "tool_name": call.name,
                    "arguments": args,
                    "thought": f"Gemini quyết định gọi công cụ '{call.name}' với tham số: {json.dumps(args, ensure_ascii=False)}"
                }
            else:
                return {
                    "type": "text",
                    "content": response.text or "",
                    "thought": "Gemini phản hồi trực tiếp bằng văn bản (không cần gọi công cụ)."
                }

        except Exception as e:
            print(f"⚠️ [Gemini API Warning]: Không thể kết nối live API ({str(e)}). Tự động fallback về Mock.")
            return MockOfflineProvider().generate_with_tools(prompt, tools_schema, system_prompt)


class OpenAIProvider(BaseLLMProvider):
    """OpenAI Provider (Native Tool Calling với OpenAI SDK)"""
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model_name = model or os.getenv("LLM_MODEL") or "gpt-4o-mini"

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        if not self.api_key or self.api_key == "your_openai_api_key_here":
            return "[OpenAI Error]: Chưa cấu hình OPENAI_API_KEY trong file .env! Đang sử dụng chế độ Mock."
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            response = client.chat.completions.create(model=self.model_name, messages=messages)
            return response.choices[0].message.content or ""
        except Exception as e:
            return f"[OpenAI Exception]: {str(e)}"

    def generate_with_tools(self, prompt: str, tools_schema: List[Dict[str, Any]], system_prompt: str = "") -> Dict[str, Any]:
        if not self.api_key or self.api_key == "your_openai_api_key_here":
            print("ℹ️ [OpenAI Provider]: Chưa tìm thấy OPENAI_API_KEY hợp lệ. Tự động chuyển sang Mock Offline.")
            return MockOfflineProvider().generate_with_tools(prompt, tools_schema, system_prompt)

        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)

            tools = []
            for tool in tools_schema:
                if not tool.get("name"):
                    continue
                tools.append({
                    "type": "function",
                    "function": {
                        "name": tool["name"],
                        "description": tool.get("description", ""),
                        "parameters": tool.get("parameters", {})
                    }
                })

            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            response = client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                tools=tools if tools else None,
                tool_choice="auto" if tools else None
            )

            msg = response.choices[0].message
            if msg.tool_calls:
                call = msg.tool_calls[0]
                args = json.loads(call.function.arguments) if call.function.arguments else {}
                return {
                    "type": "tool_call",
                    "tool_name": call.function.name,
                    "arguments": args,
                    "thought": f"OpenAI quyết định gọi công cụ '{call.function.name}' với tham số: {json.dumps(args, ensure_ascii=False)}"
                }
            else:
                return {
                    "type": "text",
                    "content": msg.content or "",
                    "thought": "OpenAI phản hồi trực tiếp bằng văn bản (không cần gọi công cụ)."
                }
        except Exception as e:
            print(f"⚠️ [OpenAI API Warning]: Không thể kết nối live API ({str(e)}). Tự động fallback về Mock.")
            return MockOfflineProvider().generate_with_tools(prompt, tools_schema, system_prompt)


def get_llm_provider() -> BaseLLMProvider:
    """Factory function khởi tạo Provider theo LLM_PROVIDER env variable"""
    provider_type = os.getenv("LLM_PROVIDER", "gemini").lower()
    
    if provider_type == "gemini":
        key = os.getenv("GEMINI_API_KEY")
        if key and key != "your_gemini_api_key_here":
            return GeminiProvider()
        else:
            return MockOfflineProvider()
    elif provider_type == "openai":
        key = os.getenv("OPENAI_API_KEY")
        if key and key != "your_openai_api_key_here":
            return OpenAIProvider()
        else:
            return MockOfflineProvider()
    elif provider_type == "mock":
        return MockOfflineProvider()
    else:
        return MockOfflineProvider()