import requests, json, sys, time

API_KEY = "9b416239-4b4f-4803-8276-cbd66dc08987"
URL = f"https://mainnet.helius-rpc.com/?api-key={API_KEY}"

def get_seeds(mint):
    payload = {"jsonrpc": "2.0", "id": 1, "method": "getSignaturesForAddress", "params": [mint, {"limit": 50}]}
    res = requests.post(URL, json=payload).json()
    sigs = [x['signature'] for x in res.get('result', [])]
    if not sigs:
        print("❌ 未能获取到签名，请检查 Mint 地址或稍后重试")
        return
    print(f"--- 正在从 {len(sigs)} 笔原始交易中提取真神指纹 ---")
    hunters = []
    for s in reversed(sigs):
        try:
            tx_url = f"https://api.helius.xyz/v0/transactions/?api-key={API_KEY}"
            tx_res = requests.post(tx_url, json={"transactions": [s]})
            tx = tx_res.json()
            # 修正点：增加对列表长度和内容的物理检查
            if isinstance(tx, list) and len(tx) > 0 and 'feePayer' in tx[0]:
                hunters.append(tx[0]['feePayer'])
                print(f"✅ 捕获地址: {tx[0]['feePayer'][:8]}...")
                if len(set(hunters)) >= 33: break
        except Exception: continue # 遇到 API 坏点直接跳过，不准报错崩溃
    
    with open("/root/Lotus-System/hunters_matrix.json", "w") as f:
        json.dump(list(set(hunters)), f)
    print(f"🎯 最终捕获 {len(set(hunters))} 个实验对象。")

if __name__ == "__main__":
    if len(sys.argv) > 1: get_seeds(sys.argv[1])
