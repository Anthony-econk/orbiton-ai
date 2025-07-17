# run.py
# Orbiton.ai API 실행 스크립트 (운영 및 개발 환경 구분)

import uvicorn
import os

# 운영 환경 설정
def get_settings():
    return {
        "host": os.getenv("HOST", "0.0.0.0"),
        "port": int(os.getenv("PORT", 8000)),
        "reload": os.getenv("ENV", "development") == "development",
        "workers": int(os.getenv("WORKERS", 1)),
    }

if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "app.main:app",
        host=settings["host"],
        port=settings["port"],
        reload=settings["reload"],
        workers=settings["workers"]
    )
