import datetime as dt
import pandas as pd
import csv
from stat_functions import Stat
import time

pd.options.mode.chained_assignment = None


if __name__ == '__main__':

    # ===============================================
    # ===============================================
    # INPUT PARAMETERS
    # ===============================================
    # ===============================================

    # Read .csv file with all the symbols to be analysed or use the tickers list below
    with open('ana_statistics/src/data/all_symbols.csv', newline='') as f:
        reader = csv.reader(f)
        tickers = list(reader)[0]
    
    tickers = ['HKInd', 'Usa500', 'UsaTec', 'UsaInd', 'UsaRus', 'Ger40', 'Bra50', 'Jp225', 'Aus200']
    tickers = ['Ger40']

    # Timeframes 
    tfs = ['M5', 'M15', 'M30', 'H1', 'H12', 'D1']     #'M3', 'M5',  'H1', 'H2', 'H4', 'D1', 'W1'
    tfs = ['M5']

    # Candles 
    times = [f"{hour:02d}:{minute:02d}" for hour in range(24) for minute in range(0, 60, 5)]

    # Initial date to analyse the data
    dates = [dt.date(2023, 1, 1), dt.date(2023, 10, 27), dt.date(2024,1,1), dt.date(2023, 7, 1)]
    dates = [dt.date(2023, 11, 1)]
    # Minimum number of trades per strategy tested
    min_trade = 10

    # Maximum loss acceptable per strategy tested
    max_sl = -0.03

    # Type of analysis    
    down_up = True
    at_time = True
    range_at_time = True

    save_files = False
    
    # ===============================================
    # ===============================================

    print('============================================')
    # Create dataframe results for the 4 strategy types
    down_test = pd.DataFrame(columns = ['ticker', 'timeframe', 'pct_down', 'date_0', 'No_Trades', '%_tp', 'Max_tp', 'Max_sl', 'Average_result', 'System_result'])
    up_test = pd.DataFrame(columns   = ['ticker', 'timeframe', 'pct_up', 'date_0', 'No_Trades', '%_tp', 'Max_tp', 'Max_sl', 'Average_result', 'System_result'])
    at_time_test = pd.DataFrame(columns = ['ticker', 'timeframe', 'date_0', 'time','No_Trades', '%_tp', 'Max_tp', 'Max_sl', 'Average_result', 'System_result'])
    range_at_time_test = pd.DataFrame(columns = ['ticker', 'timeframe', 'date_0', 'time', 'No_bars_shift', 'No_Trades', '%_tp', 'Max_tp', 'Max_sl', 'Average_result', 'System_result'])   

    total = len(tickers)

    for ticker in tickers:

        for tf in tfs:

            # Get the dataframe with the candles information
            df = Stat.compile_data(ticker, tf)
            #df = Stat.read_data(ticker, tf)

            for date_0 in dates:
                
                # Up/Down Strategy
                if down_up:
                    for i in range(1, 101):
                        a = i
                        percentage_down = -a / 1000
                        percentage_up = a / 1000

                        down_test = pd.concat([down_test, Stat.ana_down_statistics(df, percentage_down, date_0, ticker, tf, min_trade)])
                        up_test   = pd.concat([up_test, Stat.ana_up_statistics(df, percentage_up, date_0, ticker, tf, min_trade)])
                
                
                # Time Strategy
                for time in times:
                    if at_time:
                        at_time_test = pd.concat([at_time_test, Stat.ana_at_time(df, date_0, time, ticker, tf, min_trade)])

                    # Range time Strategy
                    if range_at_time:
                        for bar_shift in range(144):
                            range_at_time_test = pd.concat([range_at_time_test, Stat.ana_range_time(df, date_0, time, bar_shift , ticker, tf, min_trade)])

        # 



        total = total-1
        print(f'{total} remaining symbols...')

    if down_up:
        # Create Pandas dataframe headers
        down_test = Stat.organise_output(down_test, max_sl)
        up_test = Stat.organise_output(up_test, max_sl)
        print(down_test.to_string())
        print()
        print(up_test.to_string())
        print()    

    if at_time:
        print('========================================================================')
        at_time_test = Stat.organise_output(at_time_test, max_sl)
        print(at_time_test.to_string())
        print()

    if range_at_time:
        range_at_time_test = Stat.organise_output(range_at_time_test, max_sl)
        print(range_at_time_test.to_string())

    # Save the data frames to a .csv file

    
    if save_files == True:
        down_test.to_csv(         f'src/output_data/01_down_test.csv')
        up_test.to_csv(           f'src/output_data/02_up_test.csv')
        at_time_test.to_csv(      f'src/output_data/03_at_time_test.csv')
        range_at_time_test.to_csv(f'src/output_data/04_range_at_time_test.csv')
    
