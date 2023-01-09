import pandas as pd

def read_data(path):

    df = pd.read_csv(f'{path}')
    df.drop(['Unnamed: 0'], axis=1, inplace=True)

    return df

if __name__ == '__main__':

    down_test = read_data('src/output_data/01_down_test.csv')
    up_test = read_data('src/output_data/02_up_test.csv')
    at_time_test = read_data('src/output_data/03_at_time_test.csv')

    down_test = down_test.reset_index(drop=True)
    up_test = up_test.reset_index(drop=True)
    at_time_test = at_time_test.reset_index(drop=True)

    # Print all data
    print_all = False

    if print_all:
        print(down_test.to_string())
        print()
        print(up_test.to_string())
        print()
        print(at_time_test.to_string())

    # Select the results for the following symbol
    symbol = 'Bra50Dec22'

    # Print specific symbol
    look_symbol = True

    if look_symbol:
        down_test = down_test[~(down_test['ticker'] != symbol)]
        up_test = up_test[~(up_test['ticker'] != symbol)]
        at_time_test = at_time_test[~(at_time_test['ticker'] != symbol)]

        print()
        print('==============================================================================')
        print(f'{symbol} data:')
        print()
        print(down_test.to_string())
        print()
        print(up_test.to_string())
        print()
        print(at_time_test.to_string())

        save_symbol = False
        if save_symbol:
            down_test.to_csv(f'/Statistic Data/{symbol}_down_test.csv')
            up_test.to_csv(f'/Statistic Data/{symbol}_up_test.csv')
            at_time_test.to_csv(f'/Statistic Data/{symbol}_at_time_test.csv')
