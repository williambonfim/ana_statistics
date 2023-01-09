import datetime as dt
import pandas as pd
import csv
from stat_functions import Stat

pd.options.mode.chained_assignment = None

if __name__ == '__main__':

    # ===============================================
    # ===============================================
    # INPUT PARAMETERS
    # ===============================================
    # ===============================================

    # Read .csv file with all the symbols to be analysed or use the tickers list below
    with open('src/data/all_symbols.csv', newline='') as f:
        reader = csv.reader(f)
        tickers = list(reader)[0]
    
    tickers = ['HKInd','UsaTec','UsaInd', 'Ger40']
    
    # Timeframes 
    tfs = ['M15', 'M30', 'H1', 'D1']     #'M3', 'M5',  'H1', 'H2', 'H4', 'D1', 'W1'

    # Candles 
    times = ['00:00', '00:15', '00:30', '00:45', 
             '01:00', '01:15', '01:30', '01:45', 
             '02:00', '02:15', '02:30', '02:45',
             '03:00', '03:15', '03:30', '03:45', 
             '04:00', '04:15', '04:30', '04:45',
             '05:00', '05:15', '05:30', '05:45',
             '06:00', '06:15', '06:30', '06:45',
             '07:00', '07:15', '07:30', '07:45',
             '08:00', '08:15', '08:30', '08:45',
             '09:00', '09:15', '09:30', '09:45',
             '10:00', '10:15', '10:30', '10:45',
             '11:00', '11:15', '11:30', '11:45',
             '12:00', '12:15', '12:30', '12:45',
             '13:00', '13:15', '13:30', '13:45',
             '14:00', '14:15', '14:30', '14:45',
             '15:00', '15:15', '15:30', '15:45',
             '16:00', '16:15', '16:30', '16:45',
             '17:00', '17:15', '17:30', '17:45',
             '18:00', '18:15', '18:30', '18:45',
             '19:00', '19:15', '19:30', '19:45',
             '20:00', '20:15', '20:30', '20:45',
             '21:00', '21:15', '21:30', '21:45',
             '22:00', '22:15', '22:30', '22:45',
             '23:00', '23:15', '23:30', '23:45']

    # Initial date to analyse the data
    dates = [dt.date(2022, 8, 1), dt.date(2022, 10, 31), dt.date(2022,1,1), dt.date(2022, 6, 1)]

    # Minimum number of trades per strategy tested
    min_trade = 10

    # Maximum loss acceptable per strategy tested
    max_sl = -0.015

    # Type of analysis    
    down_up = True
    at_time = True
    range_at_time = True

    save_files = True
    
    # ===============================================
    # ===============================================

    print('============================================')
    # Create dataframe results for the 4 strategy types
    down_test = pd.DataFrame(columns = ['ticker', 'timeframe', 'pct_down', 'date_0', 'No_Trades', '%_tp', 'Max_tp', 'Max_sl', 'Average_result', 'System_result'])
    up_test = pd.DataFrame(columns   = ['ticker', 'timeframe', 'pct_up', 'date_0', 'No_Trades', '%_tp', 'Max_tp', 'Max_sl', 'Average_result', 'System_result'])
    at_time_test = pd.DataFrame(columns = ['ticker', 'timeframe', 'date_0', 'time','No_Trades', '%_tp', 'Max_tp', 'Max_sl', 'Average_result', 'System_result'])
    range_at_time_test = pd.DataFrame(columns = ['ticker', 'timeframe', 'date_0', 'time', 'No_bars_shift', 'No_Trades', '%_tp', 'Max_tp', 'Max_sl', 'Average_result', 'System_result'])   

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
                        for bar_shift in range(6):
                            range_at_time_test = pd.concat([range_at_time_test, Stat.ana_range_time(df, date_0, time, bar_shift , ticker, tf, min_trade)])

        # Reset index

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
    
