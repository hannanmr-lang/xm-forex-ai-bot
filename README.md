from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="XM Forex AI Bot")

class MarketData(BaseModel):
    symbol: str = "XAUUSD"
    bid: float
    ask: float

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
    spread = data.ask - data.bid
    mid_price = (data.ask + data.bid) / 2

    if spread <= 0:
        action = "HOLD"
        reason = "Invalid market price"
    else:
        action = "HOLD"
        reason = "Strategy is under development. Demo only."

    return {
        "symbol": data.symbol,
        "bid": data.bid,
        "ask": data.ask,
        "spread": round(spread, 3),
        "mid_price": round(mid_price, 3),
        "action": action,
        "reason": reason,
        "mode": "DEMO",
        "trading_enabled": False
    }
