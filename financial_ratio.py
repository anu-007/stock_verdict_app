def calculate_ratios(financials, balance_sheet, info):
    financials_latest_timestamp = max(financials.keys())
    balance_sheet_latest_timestamp = max(balance_sheet.keys())
    financials_data = financials[financials_latest_timestamp]
    balance_sheet_data = balance_sheet[balance_sheet_latest_timestamp]

    # Ensure we're accessing scalar values, not Series
    operating_income = financials_data.get('OperatingIncome')
    total_revenue = financials_data.get('TotalRevenue')
    net_income = financials_data.get('NetIncome')
    ebit = financials_data.get('EBIT')
    interest_expense = financials_data.get('InterestExpense')
    total_debt = balance_sheet_data.get('TotalDebt')
    equity = balance_sheet_data.get('ShareIssued')
    sales = financials_data.get('TotalRevenue')
    price_per_share = info.get('currentPrice')
    shares_outstanding = info.get('sharesOutstanding')
    book_value_per_share = equity / shares_outstanding
    pe_ratio = info.get('trailingPE')
    
    # Calculate ratios
    operating_margin = operating_income / total_revenue * 100
    pat_margin = net_income / total_revenue * 100
    roe = net_income / equity * 100
    interest_coverage = ebit / interest_expense
    debt_to_equity = total_debt / equity
    p_s_ratio = info.get('marketCap') / sales
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