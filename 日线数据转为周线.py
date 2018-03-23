import pandas as pd

stock_data = pd.read_csv('all_trading_data/stock data/sh600000.csv', parse_dates=[1])

period_type = 'W'
stock_data.set_index('date', inplace=True)
period_stock_data = stock_data.resample(period_type, how='last')

period_stock_data['change'] = stock_data['change'].resample(period_type, how=lambda x: (x+1.0).prod() - 1.0)
period_stock_data['open'] = stock_data['open'].resample(period_type, how='first')
period_stock_data['high'] = stock_data['high'].resample(period_type, how='max')
period_stock_data['low'] = stock_data['low'].resample(period_type, how='min')
period_stock_data['volume'] = stock_data['volume'].resample(period_type, how='sum')
period_stock_data['money'] = stock_data['money'].resample(period_type, how='sum')
period_stock_data['turnover'] = period_stock_data['volume']/(period_stock_data['traded_market_value']/period_stock_data['close'])

period_stock_data = period_stock_data[period_stock_data['code'].notnull()]
period_stock_data.reset_index(inplace=True)

period_stock_data.to_csv('week_stock_data.csv', index=False)
