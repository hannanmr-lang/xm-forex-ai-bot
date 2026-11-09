from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="XM Forex AI Bot")

class MarketData(BaseModel):
    symbol: str = "XAUUSD"
    bid: float = 0
    ask: float = 0

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
    return {
        "symbol": data.symbol,
        "action": "HOLD",
        "reason": "Demo testing only. No trading strategy yet.",
        "trading_enabled": False
    }
