# backend/utils/geoip_policy.py
# 확장 가능한 접근 제어 정책 모듈 (기본 차단 정책)
# 모든 국가 차단 후 허용 국가만 선택
ALLOW_ALL_COUNTRIES = False

# 허용 국가 목록 (ISO 3166-1 alpha-2 코드)
ALLOWED_COUNTRIES = [
    # 아시아
    "KR", "JP", "SG", "TH", "MY", "VN", "ID", "PH", "TW", "HK",
    # 유럽
    "DE", "FR", "GB", "IT", "ES", "NL", "SE", "NO", "FI", "CH", "PL",
    # 북미
    "US", "CA"
]

def is_country_blocked(country_code: str) -> bool:
    if ALLOW_ALL_COUNTRIES:
        return False  # 전체 허용
    return country_code not in ALLOWED_COUNTRIES
