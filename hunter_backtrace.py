import requests, json, sys

API_KEY = "9b416239-4b4f-4803-8276-cbd66dc08987"
URL = f"https://mainnet.helius-rpc.com/?api-key={API_KEY}"

def get_seeds(mint):
    # 莲图回溯：找最早 50 笔交易
    payload = {"jsonrpc": "2.0", "id": 1, "method": "getSignaturesForAddress", "params": [mint, {"limit": 50}]}
    sigs = [x['signature'] for x in requests.post(URL, json=payload).json().get('result', [])]
    print(f"--- 正在从 {len(sigs)} 笔原始交易中提取真神指纹 ---")
    hunters = []
    for s in reversed(sigs):
        tx = requests.post(f"https://api.helius.xyz/v0/transactions/?api-key={API_KEY}", json={"transactions": [s]}).json()
        if tx and 'feePayer' in tx[0]:
            hunters.append(tx[0]['feePayer'])
            if len(set(hunters)) >= 33: break
    
    with open("/root/Lotus-System/hunters_matrix.json", "w") as f:
        json.dump(list(set(hunters)), f)
    print(f"🎯 成功捕获 {len(set(hunters))} 个实验对象。路径: hunters_matrix.json")

if __name__ == "__main__":
    if len(sys.argv) > 1: get_seeds(sys.argv[1])
