import requests
import json
import time

API_KEY = "9b416239-4b4f-4803-8276-cbd66dc08987"

def get_actual_profit(address):
    print(f"--- 深度审计资产曲线: {address[:8]}... ---")
    url = f"https://api.helius.xyz/v0/addresses/{address}/transactions?api-key={API_KEY}"
    try:
        res = requests.get(url, timeout=10).json()
        # 找最近一笔 Token 交易
        for tx in res:
            transfers = tx.get('tokenTransfers', [])
            if transfers:
                mint = transfers[0].get('mint')
                # 查这个币现在的价格
                p_res = requests.get(f"https://api.jup.ag/price/v2?ids={mint}").json()
                price = p_res.get('data', {}).get(mint, {}).get('price')
                if price: return True # 只要他买的币现在还有价，说明没归零
        return False
    except: return False

def run_harvest():
    # 扩大搜索范围，抓取最近 50 笔 Pump.fun 交易
    url = f"https://mainnet.helius-rpc.com/?api-key={API_KEY}"
    payload = {"jsonrpc":"2.0","id":1,"method":"getSignaturesForAddress","params":["6EF8rrecthR5DkZJ4Nsu9H7y7Sbs6HAbLPyzK7Adu5L6", {"limit":50}]}
    sigs = requests.post(url, json=payload).json().get('result', [])
    
    candidates = []
    for s in sigs:
        tx_info = requests.post(f"https://api.helius.xyz/v0/transactions/?api-key={API_KEY}", json={"transactions":[s['signature']]}).json()
        if tx_info: candidates.append(tx_info[0].get('feePayer'))
    
    unique_candidates = list(set(candidates))
    print(f"找到 {len(unique_candidates)} 个待审账户...")
    
    winners = []
    for c in unique_candidates:
        if get_actual_profit(c):
            winners.append(c)
            print(f"💎 发现优质猎人: {c}")
        if len(winners) >= 3: break # 抓到3个就撤，保证效率
        
    with open("/root/Lotus-System/verified_hunters.json", "w") as f:
        json.dump(winners, f)
if __name__ == "__main__":
    run_harvest()
