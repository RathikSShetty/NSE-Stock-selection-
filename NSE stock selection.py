import yfinance as yf
import pandas as pd

# List of stock symbols from NSE you want to analyze
symbols = ['RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS', 'ITC.NS', 'SBIN.NS', 'LT.NS', 'HINDUNILVR.NS',
           'BHARTIARTL.NS', 'ASIANPAINT.NS']


# Fetch data
def fetch_stock_data(symbols):
    stock_data = []
    for symbol in symbols:
        stock_info = yf.Ticker(symbol).info
        stock_data.append({
            'Symbol': symbol,
            'Name': stock_info.get('shortName', ''),
            'Sector': stock_info.get('sector', ''),
            'Market Cap': stock_info.get('marketCap', 0),
            'P/E Ratio': stock_info.get('trailingPE', 0),
            'Price': stock_info.get('currentPrice', 0)
        })
    return pd.DataFrame(stock_data)


# Calculate sector averages and identify under-valued and over-valued stocks
def evaluate_stocks(stock_data):
    # Calculate sector average P/E ratios
    sector_avg_pe = stock_data.groupby('Sector')['P/E Ratio'].mean()

    # Identify under-valued and over-valued stocks
    stock_data['Sector Avg P/E'] = stock_data['Sector'].map(sector_avg_pe)
    stock_data['Valuation'] = stock_data.apply(
        lambda x: 'Under-valued' if x['P/E Ratio'] < x['Sector Avg P/E'] else 'Over-valued', axis=1)

    return stock_data


# Main execution
stock_data = fetch_stock_data(symbols)
evaluated_stocks = evaluate_stocks(stock_data)

# Separate under-valued and over-valued stocks
under_valued_stocks = evaluated_stocks[evaluated_stocks['Valuation'] == 'Under-valued']
over_valued_stocks = evaluated_stocks[evaluated_stocks['Valuation'] == 'Over-valued']


# Display results
def display_stocks(stock_df, title):
    print(f"{title}:\n")
    if stock_df.empty:
        print("None")
    else:
        print(stock_df[['Symbol', 'Name', 'Sector', 'P/E Ratio', 'Sector Avg P/E', 'Valuation']].to_string(index=False))
    print("\n")


display_stocks(under_valued_stocks, "Under-valued Stocks")
display_stocks(over_valued_stocks, "Over-valued Stocks")