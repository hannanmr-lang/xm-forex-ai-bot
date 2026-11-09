
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="XM Forex AI Bot")


class MarketData(BaseModel):
    symbol: str = "GOLD"
    bid: float
    ask: float
    closes: list[float] = Field(default_factory=list)


def calculate_ema(prices, period):
    multiplier = 2 / (period + 1)
    ema = sum(prices[:period]) / period

    for price in prices[period:]:
        ema = (price - ema) * multiplier + ema

    return ema


def calculate_rsi(prices, period=14):
    changes = [
        prices[i] - prices[i - 1]
        for i in range(1, len(prices))
    ]

    gains = [max(change, 0) for change in changes[-period:]]
    losses = [max(-change, 0) for change in changes[-period:]]

    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period

    if avg_loss == 0:
        return 100 if avg_gain > 0 else 50

    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


@app.get("/")
def home():
    return {"message": "XM Forex AI Bot is running"}


@app.get("/health")
def health():
    return {
        "status": "OK",
        "mode": "DEMO",
        "trading_enabled": False
    }


@app.post("/signal")
def signal(data: MarketData):
    if data.ask <= data.bid:
        return {
            "action": "HOLD",
            "reason": "Invalid market price",
            "trading_enabled": False
        }

    if len(data.closes) < 50:
        return {
            "symbol": data.symbol,
            "action": "HOLD",
            "reason": "At least 50 candle closing prices are required",
            "trading_enabled": False
        }

    ema20 = calculate_ema(data.closes, 20)
    ema50 = calculate_ema(data.closes, 50)
    rsi14 = calculate_rsi(data.closes, 14)

    action = "HOLD"
    reason = "No clear trading signal"

    if ema20 > ema50 and 50 < rsi14 < 70:
        action = "BUY"
        reason = "Uptrend confirmed by EMA and RSI"

    elif ema20 < ema50 and 30 < rsi14 < 50:
        action = "SELL"
        reason = "Downtrend confirmed by EMA and RSI"

    return {
        "symbol": data.symbol,
        "timeframe": "M5",
        "ema20": round(ema20, 3),
        "ema50": round(ema50, 3),
        "rsi14": round(rsi14, 2),
        "action": action,
        "reason": reason,
        "mode": "DEMO",
        "trading_enabled": False
    }
