import yfinance as yf

def analyze_cash_flow(ticker_symbol):

    try:
        # fetch data
        ticker = yf.Ticker(ticker_symbol)
        cash_flow = ticker.cashflow

        if cash_flow.empty:
            print(f"No cash flow data for {ticker_symbol}")
            return None

        ocf = cash_flow.loc["Operating Cash Flow"].values[0]
        icf = cash_flow.loc["Investing Cash Flow"].values[0]
        fcf = cash_flow.loc["Financing Cash Flow"].values[0]
        capex = cash_flow.loc["Capital Expenditure"].values[0]
        free_cash_flow = ocf - capex
    except Exception as e:
        print(f"Error fetching cash flow for {ticker_symbol}: {e}")
        return None

    # initialze score
    score = 0

    # Operating cash flow
    if ocf > 0:
        score += 1
    elif ocf < 0:
        score -= 1

    # Investing cash flow
    if icf < 0: # Reinvestment
        score += 1
    elif icf > 0: # asset sales
        score -= 1

    # financing cash flow
    if fcf < 0: # Repayment of debt
        score += 1
    elif fcf > 0: # Excess borrowing
        score -= 1
    
    # Free Cash Flow (FCF)
    if free_cash_flow > 0:
        score += 1
    elif free_cash_flow < 0:
        score -= 1
    
    # Final Verdict
    if score >= 2:
        verdict = "Buy"
    elif score <= -2:
        verdict = "Sell"
    else:
        verdict = "Hold"
    
    # Return detailed results
    return {
        "operating_cash_flow": ocf,
        "investing_cash_flow": icf,
        "financing_cash_flow": fcf,
        "free_cash_flow": free_cash_flow,
        "score": score,
        "verdict": verdict
    }