
"""
modules/joi_market.py

Market Intelligence & Investment Strategist (hardened)
- Crypto via CoinGecko (safe JSON handling)
- Stocks via Finnhub OR Twelve Data (configurable)
- Better error reporting (no more silent "success")
"""

from __future__ import annotations

import os
import json
import time
import requests
from datetime import datetime
from typing import Any, Dict, List, Optional
from pathlib import Path

import joi_companion
from flask import jsonify, request as flask_req
from modules.joi_memory import require_user

# ============================================================================
# CONFIGURATION
# ============================================================================

MARKET_DATA_DIR = Path("market_data")
PROPOSALS_DIR = Path("investment_proposals")
ALERTS_DIR = Path("price_alerts")
MARKET_LOG = Path("market_log.json")

CRYPTO_API = "https://api.coingecko.com/api/v3"

# Stock providers
FINNHUB_BASE = "https://finnhub.io/api/v1"
TWELVEDATA_BASE = "https://api.twelvedata.com"

DEFAULT_CRYPTO_WATCHLIST = ["bitcoin", "ethereum", "ripple", "cardano", "solana", "dogecoin", "shiba-inu"]
DEFAULT_STOCK_WATCHLIST = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META"]

MIN_SCALP_GAIN = 0.01
MIN_SWING_GAIN = 0.05
RISK_PER_TRADE = 0.01
MAX_POSITIONS = 5

HTTP_TIMEOUT = int(os.getenv("JOI_MARKET_HTTP_TIMEOUT", "15"))
STOCK_PROVIDER = os.getenv("JOI_STOCK_PROVIDER", "finnhub").strip().lower()
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY", "").strip()
TWELVEDATA_API_KEY = os.getenv("TWELVEDATA_API_KEY", "").strip()
STOCK_MAX_PER_RUN = int(os.getenv("JOI_STOCK_MAX_PER_RUN", "25"))

# ============================================================================
# INITIALIZATION
# ============================================================================

def _ensure_dirs():
    MARKET_DATA_DIR.mkdir(exist_ok=True)
    PROPOSALS_DIR.mkdir(exist_ok=True)
    ALERTS_DIR.mkdir(exist_ok=True)

    if not MARKET_LOG.exists():
        MARKET_LOG.write_text(json.dumps({
            "created": time.time(),
            "updates": [],
            "trades": [],
            "alerts_triggered": [],
            "errors": []
        }, indent=2))

_ensure_dirs()

# ============================================================================
# UTILITIES
# ============================================================================

def _log_market_event(kind: str, payload: Dict[str, Any]) -> None:
    try:
        log = json.loads(MARKET_LOG.read_text())
    except Exception:
        log = {"created": time.time(), "updates": [], "trades": [], "alerts_triggered": [], "errors": []}

    payload = dict(payload)
    payload.setdefault("timestamp", time.time())
    payload.setdefault("datetime", datetime.now().isoformat())

    if kind == "error":
        log.setdefault("errors", []).append(payload)
    else:
        log.setdefault("updates", []).append({"kind": kind, **payload})

    MARKET_LOG.write_text(json.dumps(log, indent=2))


def http_get_json(url: str, *, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """
    Safe JSON fetch:
    - validates status code
    - validates content-type (or attempts JSON if provider lies)
    - gives readable error with body snippet
    """
    h = {
        "User-Agent": "Mozilla/5.0 (JoiMarket/1.0)",
        "Accept": "application/json,text/plain,*/*",
    }
    if headers:
        h.update(headers)

    r = requests.get(url, params=params, headers=h, timeout=HTTP_TIMEOUT)
    ct = (r.headers.get("Content-Type") or "").lower()

    if r.status_code != 200:
        snippet = (r.text or "")[:300]
        raise RuntimeError(f"HTTP {r.status_code} from {url} | CT={ct} | body={snippet!r}")

    # Some APIs return application/json; some return text/plain JSON
    try:
        return r.json()
    except Exception:
        snippet = (r.text or "")[:300]
        raise RuntimeError(f"Non-JSON/invalid JSON from {url} | CT={ct} | body={snippet!r}")


def _provider_ready() -> Optional[str]:
    if STOCK_PROVIDER == "finnhub" and not FINNHUB_API_KEY:
        return "FINNHUB_API_KEY missing while JOI_STOCK_PROVIDER=finnhub"
    if STOCK_PROVIDER == "twelvedata" and not TWELVEDATA_API_KEY:
        return "TWELVEDATA_API_KEY missing while JOI_STOCK_PROVIDER=twelvedata"
    if STOCK_PROVIDER not in ("finnhub", "twelvedata"):
        return f"Unknown JOI_STOCK_PROVIDER={STOCK_PROVIDER!r} (use finnhub or twelvedata)"
    return None

# ============================================================================
# CRYPTO (CoinGecko)
# ============================================================================

def fetch_crypto_price(coin_id: str) -> Optional[Dict[str, Any]]:
    try:
        url = f"{CRYPTO_API}/simple/price"
        params = {
            "ids": coin_id,
            "vs_currencies": "usd",
            "include_24hr_change": "true",
            "include_24hr_vol": "true",
            "include_market_cap": "true"
        }
        data = http_get_json(url, params=params)

        if coin_id not in data:
            return None

        coin_data = data[coin_id]
        return {
            "coin_id": coin_id,
            "price_usd": coin_data.get("usd", 0),
            "change_24h": coin_data.get("usd_24h_change", 0),
            "volume_24h": coin_data.get("usd_24h_vol", 0),
            "market_cap": coin_data.get("usd_market_cap", 0),
            "timestamp": time.time(),
            "datetime": datetime.now().isoformat()
        }
    except Exception as e:
        _log_market_event("error", {"where": "fetch_crypto_price", "asset": coin_id, "error": str(e)})
        return None


def fetch_crypto_history(coin_id: str, days: int = 30) -> Optional[List[Dict[str, Any]]]:
    try:
        url = f"{CRYPTO_API}/coins/{coin_id}/market_chart"
        params = {
            "vs_currency": "usd",
            "days": min(days, 365),
            "interval": "daily" if days > 1 else "hourly"
        }
        data = http_get_json(url, params=params)

        if "prices" not in data:
            return None

        history: List[Dict[str, Any]] = []
        for timestamp_ms, price in data["prices"]:
            ts = timestamp_ms / 1000
            history.append({
                "timestamp": ts,
                "datetime": datetime.fromtimestamp(ts).isoformat(),
                "price": price
            })
        return history
    except Exception as e:
        _log_market_event("error", {"where": "fetch_crypto_history", "asset": coin_id, "error": str(e)})
        return None

# ============================================================================
# STOCKS (Finnhub OR Twelve Data)
# ============================================================================

def fetch_stock_quote(symbol: str) -> Optional[Dict[str, Any]]:
    provider_err = _provider_ready()
    if provider_err:
        _log_market_event("error", {"where": "fetch_stock_quote", "asset": symbol, "error": provider_err})
        return None

    try:
        if STOCK_PROVIDER == "finnhub":
            # https://finnhub.io/api/v1/quote?symbol=AAPL&token=...
            url = f"{FINNHUB_BASE}/quote"
            params = {"symbol": symbol, "token": FINNHUB_API_KEY}
            data = http_get_json(url, params=params)

            # Finnhub returns: c(current), d(change), dp(change%), h, l, o, pc(prev close), t(time)
            price = data.get("c", 0) or 0
            change = data.get("d", 0) or 0
            change_percent = data.get("dp", 0) or 0

            return {
                "symbol": symbol,
                "price": price,
                "change": change,
                "change_percent": change_percent,
                "volume": 0,        # not in /quote
                "market_cap": 0,    # not in /quote
                "timestamp": time.time(),
                "datetime": datetime.now().isoformat(),
                "provider": "finnhub"
            }

        # Twelve Data: https://api.twelvedata.com/quote?symbol=AAPL&apikey=...
        url = f"{TWELVEDATA_BASE}/quote"
        params = {"symbol": symbol, "apikey": TWELVEDATA_API_KEY}
        data = http_get_json(url, params=params)

        # Twelve Data can return {"status":"error","message":"..."}
        if str(data.get("status", "")).lower() == "error":
            raise RuntimeError(f"TwelveData error: {data.get('message') or data}")

        price = float(data.get("close") or data.get("price") or 0)
        change = float(data.get("change") or 0)
        change_percent = float(data.get("percent_change") or 0)
        volume = int(float(data.get("volume") or 0))

        return {
            "symbol": symbol,
            "price": price,
            "change": change,
            "change_percent": change_percent,
            "volume": volume,
            "market_cap": 0,
            "timestamp": time.time(),
            "datetime": datetime.now().isoformat(),
            "provider": "twelvedata"
        }

    except Exception as e:
        _log_market_event("error", {"where": "fetch_stock_quote", "asset": symbol, "provider": STOCK_PROVIDER, "error": str(e)})
        return None


# ============================================================================
# TECHNICAL ANALYSIS (unchanged basics)
# ============================================================================

def calculate_rsi(prices: List[float], period: int = 14) -> float:
    if len(prices) < period + 1:
        return 50.0

    gains: List[float] = []
    losses: List[float] = []

    for i in range(1, len(prices)):
        change = prices[i] - prices[i - 1]
        if change > 0:
            gains.append(change); losses.append(0)
        else:
            gains.append(0); losses.append(abs(change))

    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return round(100 - (100 / (1 + rs)), 2)


def detect_trend(history: List[Dict[str, Any]], period: int = 20) -> str:
    if not history or len(history) < period:
        return "unknown"
    recent_prices = [h["price"] for h in history[-period:]]
    half = period // 2
    sma_early = sum(recent_prices[:half]) / half
    sma_late = sum(recent_prices[half:]) / half
    diff_percent = ((sma_late - sma_early) / sma_early) * 100
    if diff_percent > 2:
        return "uptrend"
    if diff_percent < -2:
        return "downtrend"
    return "sideways"


def calculate_volatility(history: List[Dict[str, Any]], period: int = 14) -> float:
    if not history or len(history) < period + 1:
        return 0.0
    prices = [h["price"] for h in history[-period-1:]]
    returns: List[float] = []
    for i in range(1, len(prices)):
        if prices[i - 1] == 0:
            continue
        returns.append((prices[i] - prices[i - 1]) / prices[i - 1])
    if not returns:
        return 0.0
    mean = sum(returns) / len(returns)
    var = sum((r - mean) ** 2 for r in returns) / len(returns)
    return round((var ** 0.5) * 100, 2)

# ============================================================================
# OPPORTUNITY ANALYSIS
# ============================================================================

def analyze_crypto_opportunity(coin_id: str, capital: float = 100.0) -> Dict[str, Any]:
    current = fetch_crypto_price(coin_id)
    if not current:
        return {"ok": False, "error": f"Failed to fetch {coin_id}"}

    history = fetch_crypto_history(coin_id, days=30)
    if not history:
        return {"ok": False, "error": f"Failed to fetch {coin_id} history"}

    prices = [h["price"] for h in history]
    rsi = calculate_rsi(prices)
    trend = detect_trend(history)
    volatility = calculate_volatility(history)

    current_price = current["price_usd"]
    change_24h = current["change_24h"]

    signals: List[str] = []
    opportunity_type: Optional[str] = None

    # Simple signals (same spirit as your original)
    if volatility > 5 and abs(change_24h) > 2:
        if change_24h > 0 and rsi < 70:
            opportunity_type = "scalp_long"
            signals.append("High volatility with positive momentum")
        elif change_24h < 0 and rsi < 40:
            opportunity_type = "scalp_bounce"
            signals.append("Oversold condition - potential bounce")

    if trend == "uptrend" and rsi < 60:
        opportunity_type = opportunity_type or "swing_long"
        signals.append("Uptrend with room to run")

    # Basic sizing
    entry_price = current_price
    take_profit = current_price * (1.02 if "scalp" in (opportunity_type or "") else 1.10)
    stop_loss = current_price * (0.99 if "scalp" in (opportunity_type or "") else 0.95)

    risk_amount = capital * RISK_PER_TRADE
    price_risk = max(entry_price - stop_loss, 1e-9)
    position_size = risk_amount / price_risk
    potential_profit = (take_profit - entry_price) * position_size

    return {
        "ok": True,
        "coin_id": coin_id,
        "coin_name": coin_id.replace("-", " ").title(),
        "current_price": current_price,
        "analysis": {"rsi": rsi, "trend": trend, "volatility": volatility, "change_24h": change_24h},
        "opportunity": {
            "type": opportunity_type,
            "confidence": "high" if len(signals) >= 2 else "medium" if signals else "low",
            "signals": signals,
            "entry_price": entry_price,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "position_size": round(position_size, 4),
            "capital_required": round(entry_price * position_size, 2),
            "potential_profit": round(potential_profit, 2),
        },
        "timestamp": time.time(),
        "datetime": datetime.now().isoformat()
    }


def analyze_stock_opportunity(symbol: str, capital: float = 100.0) -> Dict[str, Any]:
    quote = fetch_stock_quote(symbol)
    if not quote:
        return {"ok": False, "error": f"Failed to fetch {symbol}"}

    current_price = float(quote["price"] or 0)
    change_percent = float(quote["change_percent"] or 0)

    signals: List[str] = []
    opportunity_type: Optional[str] = None

    if abs(change_percent) > 2:
        if change_percent > 0:
            opportunity_type = "momentum_long"
            signals.append(f"Strong positive momentum: +{change_percent:.2f}%")
        else:
            opportunity_type = "bounce_watch"
            signals.append(f"Significant drop: {change_percent:.2f}% - potential bounce")

    entry_price = current_price
    take_profit = current_price * (1.05 if change_percent > 0 else 1.03)
    stop_loss = current_price * (0.97 if change_percent > 0 else 0.98)

    risk_amount = capital * RISK_PER_TRADE
    price_risk = max(entry_price - stop_loss, 1e-9)
    position_size = risk_amount / price_risk
    potential_profit = (take_profit - entry_price) * position_size

    return {
        "ok": True,
        "symbol": symbol,
        "current_price": current_price,
        "analysis": {
            "change_percent": change_percent,
            "volume": quote.get("volume", 0),
            "market_cap": quote.get("market_cap", 0),
            "provider": quote.get("provider", STOCK_PROVIDER),
        },
        "opportunity": {
            "type": opportunity_type,
            "confidence": "medium" if signals else "low",
            "signals": signals,
            "entry_price": entry_price,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "position_size": round(position_size, 4),
            "capital_required": round(entry_price * position_size, 2),
            "potential_profit": round(potential_profit, 2),
        },
        "timestamp": time.time(),
        "datetime": datetime.now().isoformat()
    }

# ============================================================================
# SCHEDULED FUNCTIONS (hardened)
# ============================================================================

def update_all_market_data() -> Dict[str, Any]:
    updated_crypto = 0
    updated_stocks = 0
    failed_crypto: List[str] = []
    failed_stocks: List[str] = []

    for coin_id in DEFAULT_CRYPTO_WATCHLIST:
        data = fetch_crypto_price(coin_id)
        if data:
            (MARKET_DATA_DIR / f"crypto_{coin_id}.json").write_text(json.dumps(data, indent=2))
            updated_crypto += 1
        else:
            failed_crypto.append(coin_id)

    # provider limits safety
    for symbol in DEFAULT_STOCK_WATCHLIST[:max(1, STOCK_MAX_PER_RUN)]:
        data = fetch_stock_quote(symbol)
        if data:
            (MARKET_DATA_DIR / f"stock_{symbol}.json").write_text(json.dumps(data, indent=2))
            updated_stocks += 1
        else:
            failed_stocks.append(symbol)

    _log_market_event("market_update", {
        "crypto_updated": updated_crypto,
        "stocks_updated": updated_stocks,
        "crypto_failed": failed_crypto,
        "stocks_failed": failed_stocks,
        "stock_provider": STOCK_PROVIDER,
    })

    return {
        "ok": True,
        "status": "updated",
        "crypto_updated": updated_crypto,
        "stocks_updated": updated_stocks,
        "crypto_failed": failed_crypto,
        "stocks_failed": failed_stocks,
        "stock_provider": STOCK_PROVIDER,
        "timestamp": time.time()
    }


def create_price_alert(asset_type: str, asset: str, direction: str, target: float, note: str = "") -> Dict[str, Any]:
    """
    asset_type: "crypto" (coin_id) or "stock" (symbol)
    direction: "above" or "below"
    """
    _ensure_dirs()
    alert_id = f"alert_{int(time.time())}_{asset_type}_{asset}".replace("/", "_")
    payload = {
        "id": alert_id,
        "asset_type": asset_type,
        "asset": asset,
        "direction": direction,
        "target": float(target),
        "note": note,
        "created": time.time(),
        "triggered": False,
        "triggered_ts": None,
    }
    (ALERTS_DIR / f"{alert_id}.json").write_text(json.dumps(payload, indent=2))
    return {"ok": True, "alert": payload}

def _get_current_price(asset_type: str, asset: str) -> Optional[float]:
    if asset_type == "crypto":
        d = fetch_crypto_price(asset)
        return float(d["price_usd"]) if d else None
    if asset_type == "stock":
        d = fetch_stock_quote(asset)
        return float(d["price"]) if d else None
    return None

def check_price_alerts() -> Dict[str, Any]:
    """
    Called by scheduler. Triggers alerts and returns a list of notifications.
    """
    _ensure_dirs()
    triggered = []
    total = 0

    for f in ALERTS_DIR.glob("alert_*.json"):
        total += 1
        try:
            alert = json.loads(f.read_text())
        except Exception:
            continue

        if alert.get("triggered"):
            continue

        asset_type = alert.get("asset_type")
        asset = alert.get("asset")
        direction = alert.get("direction")
        target = float(alert.get("target", 0))

        price = _get_current_price(asset_type, asset)
        if price is None:
            continue

        hit = (direction == "above" and price >= target) or (direction == "below" and price <= target)
        if hit:
            alert["triggered"] = True
            alert["triggered_ts"] = time.time()
            alert["triggered_price"] = price
            f.write_text(json.dumps(alert, indent=2))

            msg = f"[ALERT] {asset_type.upper()} {asset} is {price:.6g} (target {direction} {target})"
            triggered.append({"id": alert["id"], "message": msg, "alert": alert})

            _log_market_event("alert_triggered", {"alert_id": alert["id"], "asset_type": asset_type, "asset": asset, "price": price, "target": target, "direction": direction})

    return {"ok": True, "alerts_total": total, "alerts_triggered": len(triggered), "notifications": triggered}


def scan_crypto_opportunities() -> Dict[str, Any]:
    opportunities: List[Dict[str, Any]] = []
    for coin_id in DEFAULT_CRYPTO_WATCHLIST:
        analysis = analyze_crypto_opportunity(coin_id)
        if analysis.get("ok") and analysis["opportunity"]["type"] and analysis["opportunity"]["confidence"] in ("high", "medium"):
            opportunities.append({
                "coin_id": coin_id,
                "type": analysis["opportunity"]["type"],
                "confidence": analysis["opportunity"]["confidence"],
                "potential_profit": analysis["opportunity"]["potential_profit"]
            })
    return {"ok": True, "opportunities_found": len(opportunities), "opportunities": opportunities}


def scan_stock_opportunities() -> Dict[str, Any]:
    opportunities: List[Dict[str, Any]] = []
    for symbol in DEFAULT_STOCK_WATCHLIST[:max(1, STOCK_MAX_PER_RUN)]:
        analysis = analyze_stock_opportunity(symbol)
        if analysis.get("ok") and analysis["opportunity"]["type"] and analysis["opportunity"]["confidence"] in ("high", "medium"):
            opportunities.append({
                "symbol": symbol,
                "type": analysis["opportunity"]["type"],
                "confidence": analysis["opportunity"]["confidence"],
                "potential_profit": analysis["opportunity"]["potential_profit"]
            })
    return {"ok": True, "opportunities_found": len(opportunities), "opportunities": opportunities}


# ============================================================================
# NOTIFICATIONS (Scheduler compatibility)
# ============================================================================

def check_notification_triggers() -> Dict[str, Any]:
    """
    Check active alerts and trigger when conditions are met.
    Called by scheduler.
    """

    triggered_count = 0

    for alert_file in ALERTS_DIR.glob("alert_*.json"):
        try:
            alert = json.loads(alert_file.read_text())

            if alert.get("triggered"):
                continue

            asset_type = alert.get("asset_type")
            asset_id = alert.get("asset_id")
            target_price = alert.get("target_price")
            direction = alert.get("direction")

            # Fetch current price
            if asset_type == "crypto":
                data = fetch_crypto_price(asset_id)
                current_price = data["price_usd"] if data else None
            else:
                data = fetch_stock_quote(asset_id)
                current_price = data["price"] if data else None

            if current_price is None:
                continue

            hit = False

            if direction == "above" and current_price >= target_price:
                hit = True
            elif direction == "below" and current_price <= target_price:
                hit = True

            if hit:
                alert["triggered"] = True
                alert["triggered_at"] = time.time()
                alert["triggered_datetime"] = datetime.now().isoformat()
                alert["triggered_price"] = current_price

                alert_file.write_text(json.dumps(alert, indent=2))

                _log_market_event("alert", {
                    "alert_id": alert.get("alert_id"),
                    "asset": asset_id,
                    "price": current_price,
                    "message": alert.get("notification_message")
                })

                print(f"[!] ALERT: {alert.get('notification_message')}")

                triggered_count += 1

        except Exception as e:
            _log_market_event("error", {
                "where": "check_notification_triggers",
                "file": str(alert_file),
                "error": str(e)
            })

    return {
        "ok": True,
        "alerts_triggered": triggered_count
    }


# ============================================================================
# LLM TOOLS + ROUTES (kept compatible with your original)
# ============================================================================

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "analyze_crypto",
        "description": "Analyze a cryptocurrency for trading opportunities",
        "parameters": {"type": "object", "properties": {
            "coin_id": {"type": "string"},
            "capital": {"type": "number"}
        }, "required": ["coin_id"]}
    }},
    analyze_crypto_opportunity
)

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "analyze_stock",
        "description": "Analyze a stock for trading opportunities",
        "parameters": {"type": "object", "properties": {
            "symbol": {"type": "string"},
            "capital": {"type": "number"}
        }, "required": ["symbol"]}
    }},
    analyze_stock_opportunity
)

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "create_price_alert",
        "description": "Create a price alert for crypto (coin_id) or stock (symbol).",
        "parameters": {"type": "object", "properties": {
            "asset_type": {"type": "string", "enum": ["crypto", "stock"]},
            "asset": {"type": "string"},
            "direction": {"type": "string", "enum": ["above", "below"]},
            "target": {"type": "number"},
            "note": {"type": "string"},
        }, "required": ["asset_type", "asset", "direction", "target"]}
    }},
    lambda p: create_price_alert(p["asset_type"], p["asset"], p["direction"], p["target"], p.get("note",""))
)

joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "check_price_alerts",
        "description": "Check all alerts and return triggered notifications (scheduler calls this).",
        "parameters": {"type": "object", "properties": {}}
    }},
    lambda p=None: check_price_alerts()
)


joi_companion.register_tool(
    {"type": "function", "function": {
        "name": "get_market_summary",
        "description": "Get summary of current market conditions and active opportunities",
        "parameters": {"type": "object", "properties": {}}
    }},
    lambda params=None: {
        "crypto_opportunities": scan_crypto_opportunities(),
        "stock_opportunities": scan_stock_opportunities(),
        "active_alerts": len(list(ALERTS_DIR.glob("alert_*.json"))),
        "stock_provider": STOCK_PROVIDER
    }
)

def market_route():
    require_user()

    if flask_req.method == "GET":
        return jsonify({
            "crypto_data": [json.loads(f.read_text()) for f in MARKET_DATA_DIR.glob("crypto_*.json")],
            "stock_data": [json.loads(f.read_text()) for f in MARKET_DATA_DIR.glob("stock_*.json")],
            "proposals": [json.loads(f.read_text()) for f in PROPOSALS_DIR.glob("proposal_*.json")],
            "alerts": [json.loads(f.read_text()) for f in ALERTS_DIR.glob("alert_*.json")],
            "stock_provider": STOCK_PROVIDER,
        })

    data = flask_req.get_json(silent=True) or {}
    action = data.get("action")

    if action == "analyze_crypto":
        return jsonify(analyze_crypto_opportunity(data.get("coin_id"), data.get("capital", 100)))
    if action == "analyze_stock":
        return jsonify(analyze_stock_opportunity(data.get("symbol"), data.get("capital", 100)))
    if action == "update_all":
        return jsonify(update_all_market_data())

    return jsonify({"ok": False, "error": "Unknown action"})

joi_companion.register_route("/market", ["GET", "POST"], market_route, "market_route")
