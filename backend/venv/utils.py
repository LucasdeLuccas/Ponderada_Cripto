def calculate_RSI(series, period=14):
    delta = series.diff(1)
    delta = delta.dropna()
    up = delta.copy()
    down = delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    gain = up.rolling(window=period).mean()
    loss = abs(down.rolling(window=period).mean())
    RS = gain / loss
    RSI = 100.0 - (100.0 / (1.0 + RS))
    return RSI

def calculate_MACD(series, slow=26, fast=12):
    exp1 = series.ewm(span=fast, adjust=False).mean()
    exp2 = series.ewm(span=slow, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd, signal
