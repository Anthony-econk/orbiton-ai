# app/services/llama_service.py
# LLaMA API (Ollama) 호출 및 리스크 요약 기능 포함 서비스 모듈

import os
import httpx
import json

# 환경변수에서 LLaMA API URL과 모델명 로드
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")

if not OLLAMA_API_URL:
    raise EnvironmentError("OLLAMA_API_URL 환경변수가 설정되지 않았습니다.")

if not OLLAMA_MODEL:
    raise EnvironmentError("OLLAMA_MODEL 환경변수가 설정되지 않았습니다.")

# 주어진 프롬프트를 LLaMA API에 전달하고 응답을 반환
async def query_llama(prompt: str) -> str:
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(OLLAMA_API_URL, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "응답이 없습니다.")
        except httpx.RequestError as e:
            return f"LLaMA API 요청 오류: {str(e)}"
        except httpx.HTTPStatusError as e:
            return f"LLaMA API 상태 코드 오류: {str(e)}"
        except Exception as e:
            return f"LLaMA API 호출 중 알 수 없는 오류 발생: {str(e)}"

# 프로젝트 리스크 데이터 요약 기능
async def summarize_risks(risk_data: list) -> str:
    prompt = f"""아래는 프로젝트 내 리스크가 감지된 작업들입니다.

{json.dumps(risk_data, ensure_ascii=False, indent=2)}

이 정보를 바탕으로 다음을 판단해서 요약해줘:
1. 어떤 작업이 가장 급한 리스크인가?
2. 어떤 작업은 조치가 필요하며, 어떻게 해야 할까?
3. 전체적인 프로젝트 위험도는 어떤가?

결과를 bullet point로 정리해줘.
"""
    return await query_llama(prompt)