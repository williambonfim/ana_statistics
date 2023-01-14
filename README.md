# ana_statistics

This script is designed to analyze financial data for a given list of tickers within specified timeframes and date ranges. The script utilizes the `pandas` and `csv` libraries to read in and manipulate data, as well as `datetime` for date operations. Additionally, it uses a custom library `stat_functions` which is assumed to have some functions that are useful to the analysis.

## Input Parameters

- `tickers` : a list of tickers to be analyzed. This list can be read in from a `.csv` file or can be manually defined in the script
- `tfs` : a list of timeframes to be analyzed. The options currently available in the script are `M15`, `M30`, `H1`, `D1`
- `times` : a list of times to be analyzed. The options currently available in the script are all the minutes from 00:00 to 23:45
- `dates` : a list of dates to be analyzed. The script uses python's `datetime` library to define these dates
- `min_trade` : the minimum number of trades per strategy to be considered in the analysis
- `max_sl` : the maximum acceptable loss per strategy
- `down_up` : a boolean value that when set to True includes strategy that goes down
- `at_time` : a boolean value that when set to True includes strategy that is at a certain time
- `range_at_time` : a boolean value that when set to True includes strategy that is within a certain range of time
- `save_files` : a boolean value that when set to True saves the analysis output to files

## Output

- The script creates dataframe results for 4 different strategy types (down, up, at_time, range_at_time) and prints them on the console. If the `save_files` option is set to True, these dataframes are also saved to files.

## Additional Information

- It is assumed that the library `stat_functions` is available and contains functions necessary for the analysis.
- The script uses `pandas.options.mode.chained_assignment = None` to prevent a warning message from appearing during the execution of the script.
- The script is intended to be run as a `__main__` script

## How to use

- To use this script, you need to have the following software installed: `python3` and the required libraries which are `pandas`, `csv`, `datetime`, and `stat_functions`
- You need to provide the `all_symbols.csv` file in the `src/data` folder
- Adjust the input parameters as desired
- Run the script by executing `python ana.py` on the command line

## Disclaimer

These scripts are for educational and research purposes only and are not intended for actual trading. It is important to conduct your own research and perform due diligence before making any financial decisions.
