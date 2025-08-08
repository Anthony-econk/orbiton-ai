# Orbiton Slack Bot 
FastAPI AI PMS Slack Bot

| 번호 | 경로(prefix=/api/     | 설명                       | 테스트 대상                          | 예상 응답                                       |
| -- | ----------------------- | --------------------           | --------------------------------    | ----------------------------------------------  |
| 1  | `/health/ping`          | 서버 실행 여부 확인             | FastAPI 자체                        | `{ "status": "ok" }`                             |
| 2  | `/health/db`            | DB 연결 및 사용자/태스크 수 확인 | PostgreSQL 연결 + ORM               | `{ "users": int, "tasks": int }`                 |
| 3  | `/health/users`         | 전체 사용자 조회                | DB(UserMapping)                     | 사용자 리스트                                     |
| 4  | `/health/tasks`         | 전체 태스크 조회                | DB(ClickUpTask)                     | 태스크 리스트                                     |
| 5  | `/health/env`           | 환경변수 설정 점검              | `.env` 또는 Render 환경 설정         | ✅ / ❌                                         |
| 6  | `/health/llm`           | LLM API 연결 테스트             | Ollama 등 LLM 서버                  | `{ "status": "ok" or "error" }`                  |
| 7  | `/health/model`         | 현재 사용 LLM 모델 정보         | `LLM_MODEL`, `LLM_API_URL`          | 모델명, API 경로                                  |
| 8  | `/health/slack`         | Slack 봇 연동 확인              | `SLACK_BOT_TOKEN` 인증              | `{ "status": "ok", "team": str, "user": str }`   |
| 9  | `/health/clickup`       | ClickUp API 연동 확인          | `CLICKUP_API_KEY` 인증               | `{ "status": "ok", "team_count": int }`          |
| 10 | `/health/geoip/test`    | 접속자 IP 기준 국가 확인        | GeoIP DB (`request.client.host`)    | 국가명, ISO코드                                   |
| 11 | `/health/geoip/ip/{ip}` | 특정 IP 국가 정보 확인          | GeoIP DB (`입력된 IP`)              | 국가명, ISO코드                                   |


ex : https://orbiton-slack-bot.onrender.com/health/geoip
prefix= /api/
