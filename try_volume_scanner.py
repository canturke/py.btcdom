"""
TRY Pair Volume Scanner
Kullanım: python try_volume_scanner.py
Gereksinim: pip install requests  (veya sadece stdlib kullanır)
Çıktı: try_volumes.html + try_volumes.csv
"""
import json, time, csv
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
try:
    import requests
    def get(url, timeout=20):
        r = requests.get(url, timeout=timeout, headers={'User-Agent':'Mozilla/5.0'})
        r.raise_for_status()
        return r.json()
except ImportError:
    import urllib.request, ssl
    ctx = ssl.create_default_context()
    def get(url, timeout=20):
        req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())
COINS = ['BTC','ETH','USDT','XRP','BNB','USDC','SOL','TRX','DOGE','HYPE','ADA','BCH','LEO','LINK','XMR','USDe','CC','XLM','DAI','USD1','LTC','ZEC','AVAX','HBAR','PYUSD','SUI','SHIB','CRO','TON','TAO','WLFI','XAUt','MNT','DOT','PAXG','M','UNI','OKB','NEAR','AAVE','USDG','ASTER','PI','SKY','RLUSD','BGB','PEPE','ICP','ETC','ONDO','USDD','WLD','KCS','KAS','POL','U','ATOM','ENA','RENDER','QNT','TRUMP','GT','ALGO','NIGHT','APT','MORPHO','FLR','FIL','ZRO','XDC','PUMP','VET','ARB','NEXO','JUP','STABLE','BONK','JST','FET','TUSD','VIRTUAL','RIVER','CAKE','PENGU','DCR','DEXE','STX','SEI','ETHFI','EURC','DASH','XTZ','CHZ','FDUSD','GNO','CRV','BTT','IMX','KITE','KAIA','NFT','SUN','CFX','TIA','INJ','AERO','BSV','LIT','SPX','GRT','JASMY','FLOKI','SYRUP','IOTA','IP','2Z','OP','PYTH','H','LDO','MON','SAND','TEL','ENS','VVV','B','HNT','LUNC','TWT','STRK','XCN','AXS','AB','PENDLE','ZBCN','FARTCOIN','VSN','XPL','CVX','NEO','ZK','COMP','WAL','MANA','BARD','FLUID','THETA','WIF','FF','RAY','GALA','MX','TRAC','DEEP','BAT','RUNE','SENT','AKT','SFP','XEC','BERA','1INCH','GLM','S','COW','EIGEN','A','JTO','STG','WEMIX','BEAT','EGLD','ATH','PIPPIN','SKR','0G','AR','MELANIA','LPT','AMP','ZEN','SNX','AWE','GRASS','RSR','GAS','BEAM','W','YZY','FORM','YFI','QTUM','TFUEL','TOSHI','ROSE','KMNO','FTT','ZRX','RVN','CTC']
NAMES = {'BTC':'Bitcoin','ETH':'Ethereum','USDT':'Tether','XRP':'XRP','BNB':'BNB','USDC':'USDC','SOL':'Solana','TRX':'TRON','DOGE':'Dogecoin','HYPE':'Hyperliquid','ADA':'Cardano','BCH':'Bitcoin Cash','LEO':'UNUS SED LEO','LINK':'Chainlink','XMR':'Monero','XLM':'Stellar','DAI':'Dai','LTC':'Litecoin','ZEC':'Zcash','AVAX':'Avalanche','HBAR':'Hedera','SUI':'Sui','SHIB':'Shiba Inu','CRO':'Cronos','TON':'Toncoin','TAO':'Bittensor','DOT':'Polkadot','UNI':'Uniswap','OKB':'OKB','NEAR':'NEAR Protocol','AAVE':'Aave','BGB':'Bitget Token','PEPE':'Pepe','ICP':'Internet Computer','ETC':'Ethereum Classic','ONDO':'Ondo','WLD':'Worldcoin','KCS':'KuCoin Token','KAS':'Kaspa','POL':'Polygon','ATOM':'Cosmos','ENA':'Ethena','RENDER':'Render','QNT':'Quant','TRUMP':'TRUMP','GT':'Gate Token','ALGO':'Algorand','APT':'Aptos','FIL':'Filecoin','VET':'VeChain','ARB':'Arbitrum','NEXO':'Nexo','JUP':'Jupiter','BONK':'Bonk','FET':'Fetch.ai','CAKE':'PancakeSwap','STX':'Stacks','SEI':'Sei','DASH':'Dash','XTZ':'Tezos','CHZ':'Chiliz','CRV':'Curve','IMX':'Immutable','KAIA':'Kaia','TIA':'Celestia','INJ':'Injective','BSV':'Bitcoin SV','GRT':'The Graph','JASMY':'JasmyCoin','FLOKI':'Floki','IOTA':'IOTA','OP':'Optimism','PYTH':'Pyth Network','LDO':'Lido DAO','SAND':'The Sandbox','ENS':'ENS','HNT':'Helium','LUNC':'Terra Classic','TWT':'Trust Wallet Token','AXS':'Axie Infinity','PENDLE':'Pendle','CVX':'Convex Finance','NEO':'NEO','ZK':'ZKsync','COMP':'Compound','MANA':'Decentraland','THETA':'Theta Network','WIF':'dogwifhat','RAY':'Raydium','GALA':'Gala','BAT':'Basic Attention Token','RUNE':'THORChain','AKT':'Akash Network','XEC':'eCash','BERA':'Berachain','1INCH':'1inch','GLM':'Golem','EGLD':'MultiversX','AR':'Arweave','SNX':'Synthetix','RSR':'Reserve Rights','YFI':'yearn.finance','QTUM':'Qtum','ROSE':'Oasis Network','ZRX':'0x Protocol','RVN':'Ravencoin'}
EXCHANGES = [
    {'id':'btcturk',   'name':'BTCTurk',   'type':'tr'},
    {'id':'paribu',    'name':'Paribu',     'type':'tr'},
    {'id':'binancetr', 'name':'BinanceTR',  'type':'tr'},
    {'id':'bitexen',   'name':'Bitexen',    'type':'tr'},
    {'id':'icrypex',   'name':'ICrypex',    'type':'tr'},
    {'id':'okx',       'name':'OKX',        'type':'global'},
    {'id':'bybit',     'name':'Bybit',      'type':'global'},
    {'id':'gate',      'name':'Gate.io',    'type':'global'},
    {'id':'mexc',      'name':'MEXC',       'type':'global'},
    {'id':'kucoin',    'name':'KuCoin',     'type':'global'},
    {'id':'htx',       'name':'HTX',        'type':'global'},
]
def fetch_btcturk():
    d = get('https://api.btcturk.com/api/v2/ticker')
    r = {}
    for x in d.get('data', []):
        if x.get('pairNormalized','').endswith('_TRY'):
            r[x['pairNormalized'].replace('_TRY','').upper()] = float(x.get('volume',0)) * float(x.get('last',0))
    return r
def fetch_paribu():
    d = get('https://www.paribu.com/ticker')
    r = {}
    for p, v in d.items():
        if p.endswith('_TL') or p.endswith('_TRY'):
            base = p.replace('_TL','').replace('_TRY','').upper()
            r[base] = float(v.get('volume',0)) * float(v.get('last',0))
    return r
def fetch_binancetr():
    d = get('https://data-api.binance.vision/api/v3/ticker/24hr')
    r = {}
    for x in (d if isinstance(d, list) else []):
        if x.get('symbol','').endswith('TRY'):
            sym = x['symbol'][:-3].upper()
            if sym == 'BUSD': continue  # skip stablecoin
            r[sym] = float(x.get('quoteVolume',0))
    return r
def fetch_bitexen():
    d = get('https://www.bitexen.com/api/v1/ticker/')
    r = {}
    items = d.get('data', d)
    if isinstance(items, dict):
        for p, v in items.items():
            if p.endswith('TRY') or p.endswith('_TL'):
                base = p.replace('TRY','').replace('_TL','').replace('_','').upper()
                r[base] = float(v.get('volume',v.get('volume_24h',0))) * float(v.get('last_price',v.get('last',0)))
    return r
def fetch_icrypex():
    d = get('https://api.icrypex.com/v1/tickers')
    # ICrypex only has USDT pairs; convert to TRY using USDTTRY rate
    usdttry = 1.0
    try:
        rate_data = get('https://data-api.binance.vision/api/v3/ticker/price?symbol=USDTTRY')
        usdttry = float(rate_data.get('price', 44))
    except Exception:
        usdttry = 44.0
    r = {}
    items = d if isinstance(d, list) else d.get('data', [])
    for x in items:
        s = (x.get('symbol') or '').upper()
        if s.endswith('USDT') and '/P' not in s:
            base = s[:-4]
            vol = float(x.get('volume') or 0) * float(x.get('last') or 0)
            r[base] = vol * usdttry
    return r
def fetch_okx():
    d = get('https://www.okx.com/api/v5/market/tickers?instType=SPOT')
    r = {}
    for x in d.get('data', []):
        if x.get('instId','').endswith('-TRY'):
            r[x['instId'].replace('-TRY','').upper()] = float(x.get('volCcy24h',0))
    return r
def fetch_bybit():
    d = get('https://api.bybit.com/v5/market/tickers?category=spot')
    r = {}
    for x in d.get('result',{}).get('list',[]):
        if x.get('symbol','').endswith('TRY'):
            r[x['symbol'][:-3].upper()] = float(x.get('turnover24h',0))
    return r
def fetch_gate():
    d = get('https://api.gateio.ws/api/v4/spot/tickers')
    r = {}
    for x in (d if isinstance(d, list) else []):
        if x.get('currency_pair','').endswith('_TRY'):
            r[x['currency_pair'].replace('_TRY','').upper()] = float(x.get('quote_volume',0))
    return r
def fetch_mexc():
    d = get('https://api.mexc.com/api/v3/ticker/24hr')
    r = {}
    for x in (d if isinstance(d, list) else []):
        if x.get('symbol','').endswith('TRY'):
            r[x['symbol'][:-3].upper()] = float(x.get('quoteVolume',0))
    return r
def fetch_kucoin():
    d = get('https://api.kucoin.com/api/v1/market/allTickers')
    r = {}
    for x in d.get('data',{}).get('ticker',[]):
        if x.get('symbol','').endswith('-TRY'):
            r[x['symbol'].replace('-TRY','').upper()] = float(x.get('volValue',0))
    return r
def fetch_htx():
    d = get('https://api.huobi.pro/market/tickers')
    r = {}
    for x in d.get('data', []):
        if x.get('symbol','').endswith('try'):
            r[x['symbol'][:-3].upper()] = float(x.get('vol',0)) * float(x.get('close',0))
    return r
FETCHERS = {
    'btcturk': fetch_btcturk, 'paribu': fetch_paribu,
    'binancetr': fetch_binancetr, 'bitexen': fetch_bitexen,
    'icrypex': fetch_icrypex, 'okx': fetch_okx,
    'bybit': fetch_bybit, 'gate': fetch_gate,
    'mexc': fetch_mexc, 'kucoin': fetch_kucoin, 'htx': fetch_htx,
}
def fetch_exchange(ex):
    eid = ex['id']
    try:
        data = FETCHERS[eid]()
        print(f"  ✓ {ex['name']:12s} — {len([v for v in data.values() if v>0])} TRY pair bulundu")
        return eid, data, None
    except Exception as e:
        print(f"  ✗ {ex['name']:12s} — HATA: {e}")
        return eid, {}, str(e)
def main():
    print(f"\n{'='*55}")
    print(f"  TRY Volume Scanner — {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
    print(f"{'='*55}")
    print(f"  {len(COINS)} coin, {len(EXCHANGES)} borsa — paralel çekiliyor...\n")
    all_data = {}   # exid -> {coin: vol}
    all_errors = {} # exid -> str
    with ThreadPoolExecutor(max_workers=11) as pool:
        futures = {pool.submit(fetch_exchange, ex): ex for ex in EXCHANGES}
        for f in as_completed(futures):
            eid, data, err = f.result()
            all_data[eid] = data
            if err:
                all_errors[eid] = err
    # Build result table
    rows = []
    for i, sym in enumerate(COINS):
        row = {'rank': i+1, 'symbol': sym, 'name': NAMES.get(sym, '')}
        total = 0
        for ex in EXCHANGES:
            v = all_data.get(ex['id'], {}).get(sym, 0) or 0
            row[ex['id']] = v
            total += v
        row['total'] = total
        rows.append(row)
    # Sort by total descending for summary
    top = sorted(rows, key=lambda r: r['total'], reverse=True)
    print(f"\n{'='*55}")
    print(f"  TOP 20 — Toplam TRY Hacmi")
    print(f"{'='*55}")
    for r in top[:20]:
        if r['total'] > 0:
            t = r['total']
            ts = f"₺{t/1e9:.2f}B" if t>=1e9 else f"₺{t/1e6:.1f}M" if t>=1e6 else f"₺{t/1e3:.0f}K"
            print(f"  {r['rank']:3d}. {r['symbol']:10s} {ts}")
    # CSV export
    csv_file = 'try_volumes.csv'
    with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
        cols = ['rank','symbol','name'] + [ex['id'] for ex in EXCHANGES] + ['total']
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    print(f"\n  ✓ CSV kaydedildi: {csv_file}")
    # XLSX export
    generate_xlsx(rows)
    print(f"  ✓ XLSX kaydedildi: try_volumes.xlsx")
    # HTML export
    generate_html(rows, all_errors)
    print(f"  ✓ HTML kaydedildi: try_volumes.html")
    print(f"\n  Hata veren borsalar: {list(all_errors.keys()) or 'YOK'}")
    print(f"{'='*55}\n")
def generate_xlsx(rows):
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, numbers
    wb = Workbook()
    ws = wb.active
    ws.title = 'TRY Volumes'
    # Headers
    headers = ['#', 'Sembol', 'İsim'] + [ex['name'] for ex in EXCHANGES] + ['TOPLAM']
    hdr_font = Font(bold=True, color='FFFFFF', size=10)
    hdr_fill = PatternFill('solid', fgColor='1a1a2e')
    for c, h in enumerate(headers, 1):
        cell = ws.cell(row=1, column=c, value=h)
        cell.font = hdr_font
        cell.fill = hdr_fill
        cell.alignment = Alignment(horizontal='center')
    # Data rows
    fmt_try = '#,##0'
    green_font = Font(bold=True, color='00AA00')
    yellow_font = Font(bold=True, color='CC8800')
    for ri, r in enumerate(rows, 2):
        ws.cell(row=ri, column=1, value=r['rank'])
        ws.cell(row=ri, column=2, value=r['symbol']).font = Font(bold=True)
        ws.cell(row=ri, column=3, value=r['name'])
        for ci, ex in enumerate(EXCHANGES, 4):
            v = r[ex['id']]
            cell = ws.cell(row=ri, column=ci, value=round(v) if v else None)
            cell.number_format = fmt_try
            if v >= 500e6:
                cell.font = green_font
            elif v >= 50e6:
                cell.font = yellow_font
        tot_cell = ws.cell(row=ri, column=len(EXCHANGES)+4, value=round(r['total']) if r['total'] else None)
        tot_cell.number_format = fmt_try
        tot_cell.font = Font(bold=True, color='0066CC')
    # Totals row
    tr = len(rows) + 2
    ws.cell(row=tr, column=2, value='TOPLAM').font = Font(bold=True, size=11)
    for ci, ex in enumerate(EXCHANGES, 4):
        t = sum(r[ex['id']] for r in rows)
        cell = ws.cell(row=tr, column=ci, value=round(t))
        cell.number_format = fmt_try
        cell.font = Font(bold=True)
    grand = sum(r['total'] for r in rows)
    gc = ws.cell(row=tr, column=len(EXCHANGES)+4, value=round(grand))
    gc.number_format = fmt_try
    gc.font = Font(bold=True, color='0066CC', size=11)
    # Column widths
    ws.column_dimensions['A'].width = 5
    ws.column_dimensions['B'].width = 10
    ws.column_dimensions['C'].width = 20
    for ci in range(4, len(EXCHANGES)+5):
        from openpyxl.utils import get_column_letter
        ws.column_dimensions[get_column_letter(ci)].width = 16
    # Timestamp sheet
    ws2 = wb.create_sheet('Bilgi')
    ws2.cell(row=1, column=1, value='Tarih')
    ws2.cell(row=1, column=2, value=datetime.now().strftime('%d.%m.%Y %H:%M:%S'))
    ws2.cell(row=2, column=1, value='Coin Sayısı')
    ws2.cell(row=2, column=2, value=len(COINS))
    ws2.cell(row=3, column=1, value='Borsa Sayısı')
    ws2.cell(row=3, column=2, value=len(EXCHANGES))
    wb.save('try_volumes.xlsx')
def generate_html(rows, errors):
    ex_headers = ''.join(f'<th class="e{ex["type"]}">{ex["name"]}</th>' for ex in EXCHANGES)
    ts = datetime.now().strftime('%d.%m.%Y %H:%M')
    def fmt(v):
        if not v: return '<span class="v0">—</span>'
        cls = 'vh' if v>=500e6 else 'vm' if v>=50e6 else 'vl'
        if v>=1e9: s=f'{v/1e9:.2f}B'
        elif v>=1e6: s=f'{v/1e6:.1f}M'
        elif v>=1e3: s=f'{v/1e3:.0f}K'
        else: s=f'{v:.0f}'
        return f'<span class="{cls}">₺{s}</span>'
    row_html = ''
    for r in rows:
        cells = ''.join(f'<td>{fmt(r[ex["id"]])}</td>' for ex in EXCHANGES)
        nm = f'<span class="cnm">{r["name"]}</span>' if r["name"] else ''
        row_html += f'<tr><td class="rk">{r["rank"]}</td><td><span class="sym">{r["symbol"]}</span>{nm}</td>{cells}<td class="vtot">{fmt(r["total"])}</td></tr>\n'
    # Totals row
    totals = {ex['id']: sum(r[ex['id']] for r in rows) for ex in EXCHANGES}
    grand = sum(totals.values())
    tot_cells = ''.join(f'<td>{fmt(totals[ex["id"]])}</td>' for ex in EXCHANGES)
    err_note = ''
    if errors:
        err_note = '<div class="errnote">⚠ Hata: ' + ', '.join(f'{k}: {v[:60]}' for k,v in errors.items()) + '</div>'
    html = f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<title>TRY Volume Scanner</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Syne:wght@800&display=swap');
:root{{--bg:#090c10;--surf:#0f1318;--brd:#1e2530;--acc:#00d4ff;--acc2:#ff6b35;--grn:#00ff88;--ylw:#ffd600;--mut:#4a5568;--txt:#e2e8f0;--dim:#718096;}}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{background:var(--bg);color:var(--txt);font-family:'JetBrains Mono',monospace;padding:20px;}}
h1{{font-family:'Syne',sans-serif;font-size:22px;color:var(--acc);}}
.sub{{color:var(--dim);font-size:11px;margin-top:3px;}}
.hdr{{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:16px;flex-wrap:wrap;gap:12px;}}
.ts{{font-size:10px;color:var(--dim);background:var(--surf);padding:6px 10px;border:1px solid var(--brd);border-radius:4px;}}
.filters{{display:flex;gap:8px;margin-bottom:14px;flex-wrap:wrap;align-items:center;}}
input{{font-family:'JetBrains Mono',monospace;font-size:12px;background:var(--surf);border:1px solid var(--brd);color:var(--txt);padding:6px 10px;border-radius:4px;outline:none;width:180px;}}
input:focus{{border-color:var(--acc);}}
label{{font-size:11px;color:var(--dim);display:flex;align-items:center;gap:5px;cursor:pointer;}}
select{{font-family:'JetBrains Mono',monospace;font-size:11px;background:var(--surf);border:1px solid var(--brd);color:var(--txt);padding:6px 8px;border-radius:4px;outline:none;cursor:pointer;}}
.twrap{{overflow-x:auto;border-radius:8px;border:1px solid var(--brd);}}
table{{width:100%;border-collapse:collapse;font-size:11px;min-width:900px;}}
thead{{position:sticky;top:0;z-index:10;}}
th{{background:#111720;color:var(--dim);padding:9px 10px;text-align:right;font-weight:700;font-size:9px;border-bottom:1px solid var(--brd);white-space:nowrap;}}
th:first-child,th:nth-child(2){{text-align:left;}}
td{{padding:7px 10px;text-align:right;border-bottom:1px solid #131820;white-space:nowrap;}}
td:first-child,td:nth-child(2){{text-align:left;}}
tr:hover td{{background:#0f1520;}}
.rk{{color:var(--dim);font-size:9px;}}
.sym{{font-weight:700;font-size:12px;}}
.cnm{{color:var(--dim);font-size:9px;display:block;}}
.v0{{color:var(--mut);}}
.vl{{color:#e2e8f0;}}
.vm{{color:var(--ylw);font-weight:600;}}
.vh{{color:var(--grn);font-weight:700;}}
.vtot{{color:var(--acc);font-weight:700;}}
.etr{{color:var(--acc)!important;}}
.eglobal{{color:var(--acc2)!important;}}
.sumrow td{{background:#111720!important;border-top:2px solid var(--brd);font-weight:700;color:var(--acc);}}
.errnote{{font-size:10px;color:#ff4757;padding:8px 12px;margin-bottom:10px;border:1px solid #ff475733;border-radius:4px;background:#ff475710;}}
.foot{{font-size:10px;color:var(--dim);margin-top:12px;display:flex;justify-content:space-between;}}
</style>
</head>
<body>
<div class="hdr">
  <div><h1>TRY VOLUME SCANNER</h1><p class="sub">200 Coin × 11 Borsa — Son 24 Saat</p></div>
  <span class="ts">📅 {ts}</span>
</div>
{err_note}
<div class="filters">
  <input type="text" id="srch" placeholder="Coin ara... BTC, ETH..." oninput="filt()">
  <label><input type="checkbox" id="hz" onchange="filt()"> Sadece hacimli</label>
  <select id="srt" onchange="filt()">
    <option value="rank">Sıra (CMC)</option>
    <option value="desc">Toplam Hacim ↓</option>
    <option value="az">Sembol A-Z</option>
  </select>
</div>
<div class="twrap">
<table>
<thead><tr><th>#</th><th>Sembol</th>{ex_headers}<th style="color:var(--acc)">TOPLAM</th></tr></thead>
<tbody id="tb">
{row_html}
<tr class="sumrow"><td colspan="2">TOPLAM</td>{tot_cells}<td>{''.join(['<span class="vh">', f'₺{grand/1e9:.2f}B</span>' if grand>=1e9 else f'₺{grand/1e6:.1f}M</span>'])}</td></tr>
</tbody>
</table>
</div>
<div class="foot">
  <span>🟢 &gt;500M ₺ &nbsp;🟡 &gt;50M ₺ &nbsp;⚪ düşük</span>
  <span>Mavi = TR Borsaları &nbsp;|&nbsp; Turuncu = Global</span>
</div>
<script>
const orig = Array.from(document.querySelectorAll('#tb tr:not(.sumrow)'));
const sum = document.querySelector('.sumrow');
function filt() {{
  const q = document.getElementById('srch').value.trim().toUpperCase();
  const hz = document.getElementById('hz').checked;
  const srt = document.getElementById('srt').value;
  let rows = orig.filter(r => {{
    const sym = r.querySelector('.sym')?.textContent || '';
    const nm = r.querySelector('.cnm')?.textContent || '';
    if (q && !sym.includes(q) && !nm.toUpperCase().includes(q)) return false;
    if (hz) {{
      const tot = r.querySelector('.vtot')?.textContent || '';
      if (tot === '—' || tot === '') return false;
    }}
    return true;
  }});
  if (srt === 'desc') rows.sort((a,b) => getTotal(b) - getTotal(a));
  else if (srt === 'az') rows.sort((a,b) => (a.querySelector('.sym')?.textContent||'').localeCompare(b.querySelector('.sym')?.textContent||''));
  else rows.sort((a,b) => parseInt(a.querySelector('.rk')?.textContent||0) - parseInt(b.querySelector('.rk')?.textContent||0));
  const tb = document.getElementById('tb');
  rows.forEach(r => tb.insertBefore(r, sum));
  orig.filter(r => !rows.includes(r)).forEach(r => r.style.display='none');
  rows.forEach(r => r.style.display='');
}}
function getTotal(row) {{
  const t = row.querySelector('.vtot')?.textContent || '';
  if (!t || t==='—') return 0;
  const n = parseFloat(t.replace('₺','').replace('B','e9').replace('M','e6').replace('K','e3')) || 0;
  return n;
}}
</script>
</body>
</html>"""
    with open('try_volumes.html', 'w', encoding='utf-8') as f:
        f.write(html)
if __name__ == '__main__':
    main()
