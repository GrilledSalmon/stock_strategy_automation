"""VAA 공격형 전략
강환국 <거인의 포트폴리오>에 나온 VAA 공격형 전략의 ETF를 뽑아주는 코드입니다.
FinanceDataReader API를 활용했으며, 코드를 실행한 날짜 기준으로 ETF를 뽑아줍니다."""

from FinanceDataReader import DataReader
from datetime import timedelta

date_start = '20210101'
AGGRESSIVE_ASSET_LIST = ['SPY', 'EFA', 'EEM', 'AGG']
SAFE_ASSET_LIST = ['LQD', 'IEF', 'SHY']
TOTAL_ASSET_LIST = AGGRESSIVE_ASSET_LIST + SAFE_ASSET_LIST
vaa_etf_data_dict = dict()
for etf_name in TOTAL_ASSET_LIST:
    vaa_etf_data_dict[etf_name] = DataReader(etf_name, date_start)

SPY = vaa_etf_data_dict['SPY']
today = SPY.index[-1]

one_year_ago = today - timedelta(365)
six_month_ago = today - timedelta(365//2)
three_month_ago = today - timedelta(365//4)
one_month_ago = today - timedelta(365//12)
date_list = [one_year_ago, six_month_ago, three_month_ago, one_month_ago]
point = [1, 2, 4, 12]

def momentum_score(etf_name):
    """이름이 etf_name인 ETF의 모멘텀 스코어 리턴"""
    etf_data = vaa_etf_data_dict[etf_name]
    today_price = etf_data.loc[today].Close
    score = 0
    print(f'{etf_name} 과거 수익률', ':', end=' ')
    for i in range(4):
        date = date_list[i]
        past_price = etf_data.loc[etf_data.index > date].iloc[0].Close
        earning_rate = (today_price - past_price) / past_price * 100
        print(f'{earning_rate:.3f}%', end=' | ')
        score += point[i] * earning_rate
    print()
    return score

etf_scores = []

print("공격형 자산")
for etf_name in AGGRESSIVE_ASSET_LIST:
    score = momentum_score(etf_name)
    etf_scores.append(score)
    print("{} 모멘텀 스코어 : {:.2f}".format(etf_name, score))

print('-----------------------------------------------------')
print("안전자산")
for etf_name in SAFE_ASSET_LIST:
    score = momentum_score(etf_name)
    etf_scores.append(score)
    print("{} 모멘텀 스코어 : {:.2f}".format(etf_name, score))


invest_aggressively = True
for i in range(len(AGGRESSIVE_ASSET_LIST)):
    if etf_scores[i] < 0:
        invest_aggressively = False


print()
if invest_aggressively:
    print("모든 공격형 자산의 스코어가 0 이상이므로")
    print("모멘텀 스코어가 가장 높은 \"공격형 자산\"에 투자합니다.")
    aggressive_scores = etf_scores[:len(AGGRESSIVE_ASSET_LIST)]
    selected = AGGRESSIVE_ASSET_LIST[aggressive_scores.index(max(aggressive_scores))]
else:
    print("스코어가 0미만인 공격형 자산이 있으므로")
    print("모멘텀 스코어가 가장 높은 \"안전 자산\"에 투자합니다.")
    safe_scores = etf_scores[len(AGGRESSIVE_ASSET_LIST):]
    selected = SAFE_ASSET_LIST[safe_scores.index(max(safe_scores))]

print(f'투자할 종목 : <{selected}>')