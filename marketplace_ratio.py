import matplotlib.pyplot as plt
import numpy as np

# 초기 값
years = np.array([1, 2, 3])
customers = np.array([100, 160, 256])  # 연 60% 성장
price_per_customer = 300000  # 월 단가
months = 12
cogs_rate = 0.18
cac_rate = 0.12
marketplace_fee = 0.15

# Marketplace vs 직판 비중 변화
marketplace_ratio = np.array([0.7, 0.5, 0.3])
direct_ratio = 1 - marketplace_ratio

revenue = []
profit = []

for i in range(len(years)):
    gross_revenue = customers[i] * price_per_customer * months
    mp_revenue = gross_revenue * marketplace_ratio[i] * (1 - marketplace_fee)
    direct_revenue = gross_revenue * direct_ratio[i]
    total_revenue = mp_revenue + direct_revenue
    total_profit = total_revenue * (1 - cogs_rate - cac_rate)
    revenue.append(total_revenue / 1e8)  # 억 원 단위
    profit.append(total_profit / 1e8)

plt.plot(years, revenue, marker='o', label='연 매출(억원)')
plt.plot(years, profit, marker='s', label='연 이익(억원)')
plt.title('Orbiton.ai 브릿지 3년 매출·이익 성장 곡선')
plt.xlabel('연도')
plt.ylabel('금액(억원)')
plt.xticks(years)
plt.legend()
plt.grid(True)
plt.show()
