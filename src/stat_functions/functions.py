import pandas as pd


class Stat:

    def compile_data(ticker, tf = 'H4'):

        # Read .csv file from a local path based on the ticker name and timeframe name
        df = pd.read_csv('ana_statistics/src/Data_MT5/{}_{}.csv'.format(tf, ticker)) #/Volumes/PiNAS/market/Data_MT5/{}_{}.csv
        # Adjust time column to Pandas datetime and set it as index of the df
        df['time'] = pd.to_datetime(df['time'])
        df.set_index('time', inplace=True)

        # Drop columns that will not be used
        df.drop(['spread', 'real_volume', 'tick_volume'], axis=1, inplace=True)

        # Calculate percentage change based on the last close value
        df['high_pct']  = (df['high']  - df['close'].shift(1)) / df['close'].shift(1)
        df['low_pct']   = (df['low']   - df['close'].shift(1)) / df['close'].shift(1)
        df['close_pct'] = (df['close'] - df['close'].shift(1)) / df['close'].shift(1)
        
        # Create a target column with only 0
        df['target'] = 0

        # Save the df into a .csv file
        df.to_csv(f'ana_statistics/src/Statistic Data/{ticker}_{tf}.csv')

        print(f'{ticker}_{tf}')

        # Return the dataframe
        return df

    def read_data(ticker, tf):

        # Read the .csv file saved from compile_data
        df = pd.read_csv(f'/Volumes/PiNAS/market/1_Statistic_Method/Statistic Data/{ticker}_{tf}.csv')

        # Adjust the time column to Pandas datetime and set it as index of the df
        df['time'] = pd.to_datetime(df['time'])
        df.set_index('time', inplace=True)

        print(f'{ticker}_{tf}')

        # Return the dataframe
        return df

    def symbol_selection(df, ticker, tf, min_trade, date_0):
        
        # Count the number of profit trades
        count_tp = df[df['target'] > 0].count()['target']

        # Count the total number of trades
        count_trades = df.astype(bool).sum(axis=0)['target']

        # Calculate success rate
        if count_tp == 0 or count_trades ==0:
            success_rate = 0
        else: 
            success_rate = count_tp/count_trades

        # Calculate total system result in the time period
        system_result = df.sum()['target']

        # Calculate maximum profit trade
        max_tp = df.max()['target']

        # Calculate maximum loss trade
        max_sl = df.min()['target']

        # Calculate average result in the time period
        if system_result == 0 or count_trades == 0:
            average_result = 0
        else:
            average_result = system_result / count_trades

        # Create a list with the data and the column header
        data = [[ticker, tf, date_0, count_trades, success_rate, max_tp, max_sl, average_result, system_result]]
        df_results = pd.DataFrame(data, columns = ['ticker', 'timeframe', 'date_0', 'No_Trades', '%_tp', 'Max_tp', 'Max_sl', 'Average_result', 'System_result'])
        
        # Drop results with less trades than minimum amount
        df_results.drop(df_results.index[df_results['No_Trades'] < min_trade], inplace=True)

        # Drop results with success_rate between 25 - 75%
        index_drop = df_results[(df_results['%_tp'] > 0.20) & (df_results['%_tp'] < 0.80)].index
        df_results.drop(index_drop, inplace=True)

        return df_results

    def ana_down_statistics(df, target_down, date_0, ticker, tf, min_trade):

        # Get initial time and drop index before the initial date
        date_0 = pd.to_datetime(date_0)
        df = df[~(df.index < date_0)]

        # Set target column to trade result if a condition is met then
        df['target'] = pd.Series(0, index = df.index).mask(df['low_pct'] < target_down, df['close_pct'] - target_down)

        df_results = Stat.symbol_selection(df, ticker, tf, min_trade, date_0)
        df_results['pct_down'] = target_down

        return df_results

    def ana_up_statistics(df, target_up, date_0, ticker, tf, min_trade):

        # Get initial time and drop index before the initial date
        date_0 = pd.to_datetime(date_0)
        df = df[~(df.index < date_0)]

        # Set target column to trade result if a condition is met then
        df['target'] = pd.Series(0, index = df.index).mask(df['high_pct'] > target_up, target_up - df['close_pct'])

        df_results = Stat.symbol_selection(df, ticker, tf, min_trade, date_0)
        df_results['pct_up'] = target_up

        return df_results

    def ana_at_time(df, date_0, initial_time, ticker, tf, min_trade):
        
        # Get initial time and drop index before the initial date
        date_0 = pd.to_datetime(date_0)
        df = df[~(df.index < date_0)]

        df = df.between_time(initial_time, initial_time)

        # Set target column to trade result at close - Buy at open and Sell at close strategy
        df['target'] = df['close_pct']

        df_results = Stat.symbol_selection(df, ticker, tf, min_trade, date_0)
        df_results['time'] = initial_time
        
        return df_results

    def ana_range_time(df, date_0, initial_time, num_bars , ticker, tf, min_trade):
        # Get initial time and drop index before the initial date
        date_0 = pd.to_datetime(date_0)
        df = df[~(df.index < date_0)]

        df['target'] = df['close'].shift(-num_bars)
        df['target'] = (df['target'] - df['open']) / df['open']

        df = df.between_time(initial_time, initial_time)

        df_results = Stat.symbol_selection(df, ticker, tf, min_trade, date_0)
        df_results['time'] = initial_time
        df_results['No_bars_shift'] = num_bars

        return df_results

    def organise_output(df, max_sl):
    
        df = df.reset_index(drop = True)
        index_drop = df[(df['Max_sl'] < max_sl) & (df['%_tp'] >= 0.75)].index
        df.drop(index_drop, inplace=True)
        index_drop = df[(df['Max_tp'] < -max_sl) & (df['%_tp'] <= 0.25)].index
        df.drop(index_drop, inplace=True)
        df = df.sort_values(by=['Average_result'], ascending=False)
        df = df.reset_index(drop = True)
        
        return df