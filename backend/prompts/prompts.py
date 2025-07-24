# backend/prompts/prompts.py
# 프로젝트 태스크 목록을 기반으로 LLaMA에 전달할 요약 프롬프트를 생성하는 모듈

from typing import List

def build_project_summary_prompt(tasks: List[str]) -> str:
    """
    프로젝트 태스크 목록을 받아 LLaMA에 전달할 요약용 프롬프트를 생성합니다.

    Args:
        tasks (List[str]): 프로젝트 태스크 목록

    Returns:
        str: LLaMA에 전달할 자연어 요약 요청 프롬프트
    """
    if not tasks:
        return "현재 프로젝트에 등록된 태스크가 없습니다."

    prompt = (
        "다음은 프로젝트의 주요 태스크 목록입니다. "
        "각 태스크의 중요도, 진행상태, 연관성을 고려하여 간결하게 요약해 주세요.\n\n"
    )
    prompt += "\n".join(f"- {task}" for task in tasks)
    prompt += "\n\n요약:"
    return prompt
