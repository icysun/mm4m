import os
import pandas as pd

stock_code_list = []
for root, dirs, files in os.walk('all_trading_data/stock data'):
    if files:
        for f in files:
            if '.csv' in f:
                stock_code_list.append(f.split('.csv')[0])

all_stock = pd.DataFrame()
for code in stock_code_list:
    print(code)

    stock_data = pd.read_csv('all_trading_data/stock data/'+code+'.csv', parse_dates=[1])
    stock_data.sort('date', inplace=True)

    low_list = pd.rolling_min(stock_data['low'], 9)
    low_list.fillna(value=pd.expanding_min(stock_data['low']), inplace=True)
    high_list = pd.rolling_max(stock_data['high'], 9)
    high_list.fillna(value=pd.expanding_max(stock_data['high']), inplace=True)
    rsv = (stock_data['close'] - low_list)/(high_list - low_list) * 100
    stock_data['KDJ_K'] = pd.ewma(rsv, com=2)
    stock_data['KDJ_D'] = pd.ewma(stock_data['KDJ_K'], com=2)
    stock_data['KDJ_J'] = 3 * stock_data['KDJ_K'] - 2 * stock_data['KDJ_D']

    stock_data['KDJ_金叉死叉'] = ''
    kdj_position = stock_data['KDJ_K'] > stock_data['KDJ_D']
    stock_data.loc[kdj_position[(kdj_position == True) & (kdj_position.shitf() == False)].index, 'KDJ_金叉死叉'] = '金叉'
    stock_data.loc[kdj_position[(kdj_position == False) & (kdj_position.shitf() == True)].index, 'KDJ_金叉死叉'] = '死叉'

    for n in (1, 2, 3, 5, 10, 20):
        stock_data['接下来' + str(n) + '个交易日涨跌幅'] = stock_data['adjust_price'].shift(-1*n) / stock_data['adjust_price'] - 1.0

    stock_data.dropna(how='any', inplace=True)

    stock_data = stock_data[(stock_data['KDJ_金叉死叉'] == '金叉')]
    if stock_data.empty:
        continue

    all_stock = all_stock.append(stock_data, ignore_index=True)

print()
print('历史上所有股票出现KDJ金交的次数为%d, 这些股票在:' % all_stock.shape[0])
print()

for n in (1, 2, 3, 5, 10, 20):
    print('金交之后的%d个交易日内,' % n)
    print('平均涨幅为%.2f%%, ' % all_stock['接下来' + str(n) + '个交易日涨跌幅'].mean() * 100)
    print('其中上涨股票的比例为%.2f%%' % (all_stock[all_stock['接下来' + str(n) + '个交易日涨跌幅'] > 0].shape[0]/float(all_stock.shape[0])*100))
