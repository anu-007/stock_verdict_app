from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import yfinance as yf
from cash_flow import analyze_cash_flow
from financial_ratio import calculate_ratios, stock_verdict

class RequestHandler(BaseHTTPRequestHandler):    
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        
        try:
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(file_to_open, 'utf-8'))
        except:
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404 -File not found')
    
    def do_POST(self):
        if self.path == '/process_stock':
            content_lenght = int(self.headers['Content-Length'])

            # read and parse the form data
            post_data = self.rfile.read(content_lenght).decode('utf-8')
            parsed_data = urllib.parse.parse_qs(post_data)

            # get the stock name
            stock_name = parsed_data['stock_name'][0]
            formatted_stock = stock_name.upper() + '.NS'

            try:
                # fetch data
                ticker = yf.Ticker(formatted_stock)

                if ticker == None or ticker.cash_flow.empty:
                    with open('index.html', 'r') as file:
                        template = file.read()
                        response_html = template.format(
                            message = f"404: Stock {stock_name} not found"
                        )
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(response_html.encode('utf-8'))
                    return

                cash_flow = ticker.get_cashflow(None, True)
                financials = ticker.get_financials(None, True)
                balance_sheet = ticker.get_balance_sheet(None, True)
                info = ticker.get_info()

                # get cash flow analysis
                cash_flow_analysis = analyze_cash_flow(cash_flow)

                # get ratios
                ratios = calculate_ratios(financials, balance_sheet, info)

                if cash_flow_analysis == False or ratios == False:
                    with open('index.html', 'r') as file:
                        template = file.read()
                        response_html = template.format(
                            message = f"Not enough data present for {stock_name}"
                        )
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(response_html.encode('utf-8'))
                    return

                # get stock verdict
                verdict_ratios = stock_verdict(ratios)

                # Logic to combine verdicts (simple majority-based decision)
                if verdict_ratios == "Buy" and cash_flow_analysis["verdict"] == "Buy":
                    final_verdict = "Buy"
                elif verdict_ratios == "Sell" and cash_flow_analysis["verdict"] == "Sell":
                    final_verdict = "Sell"
                else:
                    final_verdict = "Hold"

                bot_verdict = ticker.get_recommendations(None, True)

                # Read and render the analysis template
                with open('templates/analysis.html', 'r') as file:
                    template = file.read()
                    response_html = template.format(
                        stock=formatted_stock,
                        operating_cash_flow=cash_flow_analysis["operating_cash_flow"],
                        investing_cash_flow=cash_flow_analysis["investing_cash_flow"],
                        financing_cash_flow=cash_flow_analysis["financing_cash_flow"],
                        free_cash_flow=cash_flow_analysis["free_cash_flow"],
                        score=cash_flow_analysis["score"],
                        operating_margin=ratios["operating_margin"],
                        pat_margin=ratios["pat_margin"],
                        return_on_equity=ratios["return_on_equity"],
                        interest_coverage=ratios["interest_coverage"],
                        debt_to_equity=ratios["debt_to_equity"],
                        price_to_sales_ratio=ratios["price_to_sales_ratio"],
                        price_to_bookvalue_ratio=ratios["price_to_bookvalue_ratio"],
                        price_to_earning_ratio=ratios["price_to_earning_ratio"],
                        verdict=final_verdict,
                        analyst_verdict_strong_buy=bot_verdict.get("strongBuy", [None])[0],
                        analyst_verdict_buy=bot_verdict.get("buy", [None])[0],
                        analyst_verdict_hold=bot_verdict.get("hold", [None])[0],
                        analyst_verdict_sell=bot_verdict.get("sell", [None])[0],
                        analyst_verdict_strongSell=bot_verdict.get("strongSell", [None])[0]
                    )
            except Exception as e:
                response_html = f"Error: {str(e)}"

            # send response
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(response_html.encode('utf-8'))


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    print(f"Server running on port {port}...")
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == "__main__":
    run()