"""
Binance — tüm listelemeleri (market + varlık) kategori bazlı çeker.

Kullanım:
    1) .env.example dosyasını .env olarak kopyalayın ve anahtarlarınızı girin:
           cp .env.example .env
    2) Bağımlılıkları kurun:
           pip install -r requirements.txt
    3) Çalıştırın:
           python binance_all_listings.py

Çıktı:
    binance_symbols.csv   -> tüm işlem çiftleri (spot/margin/futures/options) + kategori
    binance_assets.csv    -> tüm coin/varlık listesi (network detayları ile)
"""

import os, time, hmac, hashlib, urllib.parse, requests, pandas as pd
from dotenv import load_dotenv

# .env dosyasındaki değişkenleri ortam değişkenlerine yükler (varsa).
load_dotenv()

try:
    KEY    = os.environ["BINANCE_API_KEY"]
    SECRET = os.environ["BINANCE_API_SECRET"]
except KeyError as e:
    raise SystemExit(
        f"Eksik ortam değişkeni: {e.args[0]}. "
        "'.env.example' dosyasını '.env' olarak kopyalayıp anahtarlarınızı girin "
        "veya ilgili değişkenleri export edin."
    )

SPOT = "https://api.binance.com"
UM   = "https://fapi.binance.com"    # USDⓈ-M futures
CM   = "https://dapi.binance.com"    # COIN-M futures
EO   = "https://eapi.binance.com"    # Options

S = requests.Session()
S.headers.update({"X-MBX-APIKEY": KEY})


def signed(base, path, **params):
    """İmzalı (SIGNED) endpoint çağrısı — sadece /sapi/ uçları için gerekli."""
    params["timestamp"] = int(time.time() * 1000)
    params["recvWindow"] = 5000
    q = urllib.parse.urlencode(params)
    sig = hmac.new(SECRET.encode(), q.encode(), hashlib.sha256).hexdigest()
    r = S.get(f"{base}{path}?{q}&signature={sig}", timeout=20)
    r.raise_for_status()
    return r.json()


def public(base, path, **params):
    r = S.get(f"{base}{path}", params=params, timeout=20)
    r.raise_for_status()
    return r.json()


# ---------------------------------------------------------------- MARKETLER

def spot_symbols():
    rows = []
    for s in public(SPOT, "/api/v3/exchangeInfo")["symbols"]:
        rows.append(dict(
            market="SPOT", symbol=s["symbol"], base=s["baseAsset"], quote=s["quoteAsset"],
            status=s["status"],
            spot_allowed="SPOT" in s.get("permissions", []),
            margin_allowed=s.get("isMarginTradingAllowed", False),
            contract_type=None, expiry=None,
        ))
    return rows


def margin_pairs():
    rows = []
    for p in signed(SPOT, "/sapi/v1/margin/allPairs"):
        rows.append(dict(market="MARGIN_CROSS", symbol=p["symbol"], base=p["base"],
                         quote=p["quote"], status="TRADING" if p["isBuyAllowed"] else "OFF",
                         spot_allowed=None, margin_allowed=True,
                         contract_type=None, expiry=None))
    for p in signed(SPOT, "/sapi/v1/margin/isolated/allPairs"):
        rows.append(dict(market="MARGIN_ISOLATED", symbol=p["symbol"], base=p["base"],
                         quote=p["quote"], status="TRADING" if p["isBuyAllowed"] else "OFF",
                         spot_allowed=None, margin_allowed=True,
                         contract_type=None, expiry=None))
    return rows


def futures_symbols():
    rows = []
    for s in public(UM, "/fapi/v1/exchangeInfo")["symbols"]:
        rows.append(dict(market="FUTURES_USDM", symbol=s["symbol"], base=s["baseAsset"],
                         quote=s["quoteAsset"], status=s["status"], spot_allowed=False,
                         margin_allowed=None, contract_type=s.get("contractType"),
                         expiry=s.get("deliveryDate")))
    for s in public(CM, "/dapi/v1/exchangeInfo")["symbols"]:
        rows.append(dict(market="FUTURES_COINM", symbol=s["symbol"], base=s["baseAsset"],
                         quote=s["quoteAsset"], status=s["contractStatus"], spot_allowed=False,
                         margin_allowed=None, contract_type=s.get("contractType"),
                         expiry=s.get("deliveryDate")))
    return rows


def options_symbols():
    rows = []
    for s in public(EO, "/eapi/v1/exchangeInfo")["optionSymbols"]:
        rows.append(dict(market="OPTIONS", symbol=s["symbol"], base=s["underlying"],
                         quote=s["quoteAsset"], status="TRADING", spot_allowed=False,
                         margin_allowed=None, contract_type=s.get("side"),
                         expiry=s.get("expiryDate")))
    return rows


# --------------------------------------------------------------- VARLIKLAR

def all_assets():
    """Hesabınızın gördüğü tüm coin/varlıklar + network (chain) detayları."""
    rows = []
    for c in signed(SPOT, "/sapi/v1/capital/config/getall"):
        rows.append(dict(
            asset=c["coin"], name=c["name"], is_legal_money=c["isLegalMoney"],
            trading=c["trading"], deposit=c["depositAllEnable"], withdraw=c["withdrawAllEnable"],
            networks=",".join(n["network"] for n in c.get("networkList", [])),
        ))
    return pd.DataFrame(rows)


# ------------------------------------------------------------ KATEGORİLEME
# Binance REST API'de resmi bir "kategori" alanı YOK. Sınıflandırmayı kendimiz kuruyoruz.

FIAT = {"TRY","EUR","BRL","ARS","RUB","UAH","ZAR","PLN","RON","GBP","USD","JPY","MXN","COP","CZK","IDRT","NGN"}
STABLE = {"USDT","USDC","FDUSD","TUSD","DAI","BUSD","USDP","EURI","AEUR","USD1","PYUSD"}

# bStocks = Binance'in tokenize hisseleri (BTech Holdings ihraçlı, 2026'da başladı).
# Sembol formatı: <TICKER>B/USDT  (NVDAB, TSLAB, CRCLB, MUB, SNDKB, AAPLB, AMZNB, GSB, PYPLB ...)
# Kesin liste API'de tag'li gelmediği için burada tutuluyor, periyodik güncelleyin.
BSTOCKS = {"NVDAB","TSLAB","CRCLB","MUB","SNDKB","SPCXB","AAPLB","AMZNB","GSB","PYPLB",
           "GOOGLB","METAB","MSFTB","COINB","QQQB","MSTRB"}


def classify(row):
    b, q = row["base"], row["quote"]
    if row["market"] == "OPTIONS":
        return "option"
    if b in BSTOCKS or q in BSTOCKS:
        return "tokenized_stock"
    if b.endswith(("UPUSDT","DOWNUSDT")) or b.endswith(("UP","DOWN")) and len(b) > 4:
        return "leveraged_token"
    if q in FIAT or b in FIAT:
        return "fiat_pair"
    if b in STABLE and q in STABLE:
        return "stable_stable"
    if b in STABLE:
        return "stablecoin"
    return "crypto"


def main():
    df = pd.DataFrame(spot_symbols() + margin_pairs() + futures_symbols() + options_symbols())
    df["category"] = df.apply(classify, axis=1)
    df.to_csv("binance_symbols.csv", index=False)

    assets = all_assets()
    assets.to_csv("binance_assets.csv", index=False)

    print(df.pivot_table(index="category", columns="market", values="symbol",
                         aggfunc="count", fill_value=0))
    print(f"\nToplam sembol: {len(df)} | Toplam varlık: {len(assets)}")


if __name__ == "__main__":
    main()
