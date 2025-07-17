# app/utils/logger.py
# Orbiton.ai 통합 로거 설정

import logging
import sys

# 로거 기본 설정
logger = logging.getLogger("orbiton_logger")
logger.setLevel(logging.INFO)

# 콘솔 핸들러
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
console_handler.setFormatter(formatter)

# 핸들러가 중복 추가되지 않도록 확인
if not logger.handlers:
    logger.addHandler(console_handler)

# 파일 핸들러 설정 (로그 파일 저장)
file_handler = logging.FileHandler("orbiton_ai.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

logger.info("Orbiton.ai Logger initialized")
