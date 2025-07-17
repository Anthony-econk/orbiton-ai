# Orbiton.ai API

Orbiton.ai는 Slack, ClickUp, LLaMA를 통합하여 프로젝트 관리, 업무 자동화, AI 기반 요약 및 분석 기능을 제공하는 API 서버입니다.

---

## ✅ 주요 기능
- Slack 명령어를 통한 ClickUp 태스크 관리
- LLaMA 연동으로 업무 요약/질문 응답 제공
- PostgreSQL 기반 데이터 저장
- GeoIP 기반 지역 접근 제어
- 글로벌 예외 처리 및 로깅

---

## ✅ 설치 방법
```bash
git clone https://github.com/your-repo/orbiton-ai.git
cd orbiton-ai
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## ✅ 환경 변수 설정
```
cp .env.example .env
```
`.env` 파일을 수정하여 실제 환경변수를 입력합니다.

---

## ✅ 실행 방법
```bash
python run.py
```
또는 uvicorn 직접 실행:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## ✅ API 문서
기본 URL: `http://localhost:8000/api`
- `/health/ping` : 서버 정상 여부 확인
- `/health/db` : DB 연결 확인
- `/health/users` : 사용자 매핑 목록 조회
- `/health/tasks` : 태스크 목록 조회

---

## ✅ Slack 명령어 예시
| 명령어 | 설명 |
|---|---|
| `/orbiton.ask` | LLaMA 질문 응답 |
| `/orbiton.summary` | 프로젝트 요약 |
| `/orbiton.tasklist` | 태스크 목록 조회 |
| `/orbiton.mytask` | 나의 할 일 조회 |
| `/orbiton.assign` | 태스크 담당자 지정 |
| `/orbiton.deadline` | 마감일 설정 |
| `/orbiton.update` | 태스크 내용 업데이트 |
| `/orbiton.status` | 상태 변경 |
| `/orbiton.delete` | 태스크 삭제 |

---

## ✅ 기타
- PostgreSQL 사용 필수
- GeoIP DB 파일 필요 (GeoLite2-Country.mmdb)
- Production에서는 ENV를 `production`으로 설정