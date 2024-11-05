import yfinance as yf

bnf = yf.Ticker("^NSEBANK")

print(bnf.info)
