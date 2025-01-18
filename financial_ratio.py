import yfinance as yf

def calculate_ratios(ticker_symbol):
    # fetch data
    ticker = yf.Ticker(ticker_symbol)
    financials = ticker.financials
    balance_sheet = ticker.balance_sheet
    info = ticker.info

    if financials.empty or balance_sheet.empty:
        return False

    # Ensure we're accessing scalar values, not Series
    operating_income = financials.loc['Operating Income'].values[0]  # Ensure scalar value
    total_revenue = financials.loc['Total Revenue'].values[0]  # Ensure scalar value
    net_income = financials.loc['Net Income'].values[0]  # Ensure scalar value
    ebit = financials.loc['EBIT'].values[0]  # Ensure scalar value
    interest_expense = financials.loc['Interest Expense'].values[0]  # Ensure scalar value
    total_debt = balance_sheet.loc['Total Debt'].values[0]  # Ensure scalar value
    equity = balance_sheet.loc['Share Issued'].values[0]  # Ensure scalar value
    sales = financials.loc['Total Revenue'].values[0]  # Ensure scalar value
    price_per_share = info['currentPrice']  # Ensure scalar value
    shares_outstanding = info['sharesOutstanding']  # Ensure scalar value
    book_value_per_share = equity / shares_outstanding  # Scalar value calculation
    pe_ratio = info['trailingPE']  # Ensure scalar value
    
    # Calculate ratios
    operating_margin = operating_income / total_revenue * 100
    pat_margin = net_income / total_revenue * 100
    roe = net_income / equity * 100
    interest_coverage = ebit / interest_expense
    debt_to_equity = total_debt / equity
    p_s_ratio = info['marketCap'] / sales
    p_b_ratio = price_per_share / book_value_per_share
    
    return {
        "operating_margin": operating_margin,
        "pat_margin": pat_margin,
        "return_on_equity": roe,
        "interest_coverage": interest_coverage,
        "debt_to_equity": debt_to_equity,
        "price_to_sales_ratio": p_s_ratio,
        "price_to_bookvalue_ratio": p_b_ratio,
        "price_to_earning_ratio": pe_ratio
    }

def stock_verdict(ratios):
    # Define verdict logic based on threshold values for each ratio
    verdict = {"Buy": 0, "Sell": 0, "Hold": 0}
    
    if ratios["operating_margin"] > 10:
        verdict["Buy"] += 1
    else:
        verdict["Sell"] += 1
        
    if ratios["pat_margin"] > 5:
        verdict["Buy"] += 1
    else:
        verdict["Sell"] += 1
        
    if ratios["return_on_equity"] > 25:
        verdict["Buy"] += 1
    else:
        verdict["Sell"] += 1
        
    if ratios["interest_coverage"] > 3:
        verdict["Buy"] += 1
    else:
        verdict["Sell"] += 1
        
    if ratios["debt_to_equity"] < 1:
        verdict["Buy"] += 1
    else:
        verdict["Sell"] += 1
        
    if ratios["price_to_sales_ratio"] < 3:
        verdict["Buy"] += 1
    else:
        verdict["Sell"] += 1
        
    if ratios["price_to_bookvalue_ratio"] < 1:
        verdict["Buy"] += 1
    else:
        verdict["Sell"] += 1
        
    if ratios["price_to_earning_ratio"] < 20:  # Assuming P/E ratio under 20 is attractive
        verdict["Buy"] += 1
    else:
        verdict["Sell"] += 1
        
    # Final verdict
    if verdict["Buy"] > verdict["Sell"]:
        return "Buy"
    elif verdict["Sell"] > verdict["Buy"]:
        return "Sell"
    else:
        return "Hold"