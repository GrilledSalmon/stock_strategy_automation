from FinanceDataReader import DataReader
from datetime import timedelta

# Dual Momentum 전략
date_start = '20210101'
etf_names = ['SPY', 'BIL', 'EFA']
data_dict = {}
for etf_name in etf_names:
    data_dict[etf_name] = DataReader(etf_name, date_start)

SPY = data_dict['SPY']
today = SPY.index[-1]

one_year_ago = today - timedelta(365)

def get_earning_rate(etf_name):
    """이름이 etf_name인 ETF의 12개월간 수익률 리턴"""
    etf_data = data_dict[etf_name]
    today_price = etf_data.loc[today].Close
    score = 0
    print(f'{etf_name} 12개월간 수익률', ':', end=' ')
    
    date = one_year_ago
    past_price = etf_data.loc[etf_data.index > date].iloc[0].Close
    earning_rate = (today_price - past_price) / past_price * 100
    print(f'{earning_rate:.3f}%')
    return earning_rate
    
er_SPY = get_earning_rate('SPY')
er_BIL = get_earning_rate('BIL')
er_EFA = get_earning_rate('EFA')

if er_SPY > er_BIL:
    if er_SPY > er_EFA:
        print("SPY를 매수하세요.")
    else:
        print("EFA를 매수하세요.")
else:
    print("AGG를 매수하세요.")