import requests
import json

API_KEY = "9b416239-4b4f-4803-8276-cbd66dc08987"
RPC_URL = f"https://mainnet.helius-rpc.com/?api-key={API_KEY}"

def get_pump_hunters():
    print("--- 正在刺探 Pump.fun 早期猎人 ---")
    # Pump.fun 的程序 ID: 6EF8rrecthR5DkZJ4Nsu9H7y7Sbs6HAbLPyzK7Adu5L6
    payload = {
        "jsonrpc": "2.0", "id": 1,
        "method": "getSignaturesForAddress",
        "params": ["6EF8rrecthR5DkZJ4Nsu9H7y7Sbs6HAbLPyzK7Adu5L6", {"limit": 20}]
    }
    try:
        res = requests.post(RPC_URL, json=payload).json()
        return [x['signature'] for x in res.get('result', [])]
    except: return []
def identify_elites(signatures):
    elites = []
    url = f"https://api.helius.xyz/v0/transactions/?api-key={API_KEY}"
    try:
        res = requests.post(url, json={"transactions": signatures}).json()
        for tx in res:
            # 找到那些在做 Token 交换的真正账户
            fee_payer = tx.get('feePayer')
            if fee_payer: elites.append(fee_payer)
        return list(set(elites))
    except: return []

if __name__ == "__main__":
    sigs = get_pump_hunters()
    if sigs:
        raw_hunters = identify_elites(sigs)
        with open("/root/Lotus-System/active_hunters.json", "w") as f:
            json.dump(raw_hunters, f)
        print(f"✅ 捕获到 {len(raw_hunters)} 个疑似猎人，准备进入二轮审计")
