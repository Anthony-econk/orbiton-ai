# app/summaries/prompts.py
# 프로젝트 태스크 목록을 기반으로 LLaMA에 전달할 요약 프롬프트를 생성하는 모듈

from typing import List

# 태스크 목록을 받아 LLaMA에 전달할 프롬프트 생성
def build_project_summary_prompt(tasks: List[str]) -> str:
    if not tasks:
        return "현재 프로젝트에 등록된 태스크가 없습니다."

    # 프롬프트 시작 문구
    prompt_header = "다음은 프로젝트의 주요 태스크 목록입니다. 중요도와 진행상황을 분석하여 요약해 주세요.\n"

    # 태스크를 리스트 형식의 문자열로 변환
    formatted_tasks = "\n".join([f"- {task}" for task in tasks])

    # 완성된 프롬프트 반환
    return f"{prompt_header}{formatted_tasks}\n요약:"
