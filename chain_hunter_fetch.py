import requests
import json

API_KEY = "9b416239-4b4f-4803-8276-cbd66dc08987"
RPC_URL = f"https://mainnet.helius-rpc.com/?api-key={API_KEY}"

def get_onchain_smarts():
    print("--- 正在从 Solana 链上原始数据中挖掘捕食者 ---")
    # 逻辑：查询 Raydium 资金池地址的最新大额交易
    payload = {
        "jsonrpc": "2.0", "id": 1,
        "method": "getSignaturesForAddress",
        "params": ["675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8", {"limit": 10}]
    }
    try:
        res = requests.post(RPC_URL, json=payload).json()
        signatures = [x['signature'] for x in res.get('result', [])]
        
        # 简单提取：从最近的交易中抓取活跃钱包
        hunters = []
        for sig in signatures:
            tx_url = f"https://api.helius.xyz/v0/transactions/?api-key={API_KEY}"
            tx_data = requests.post(tx_url, json={"transactions": [sig]}).json()
            if tx_data:
                # 抓取交易的发起者
                hunters.append(tx_data[0].get('feePayer'))
        
        return list(set(hunters)) # 去重
    except Exception as e:
        print(f"❌ 挖掘失败: {e}"); return []
if __name__ == "__main__":
    found_hunters = get_onchain_smarts()
    if found_hunters:
        print(f"✅ 挖掘成功！捕获到 {len(found_hunters)} 个链上活跃地址")
        with open("/root/Lotus-System/active_hunters.json", "w") as f:
            json.dump(found_hunters, f)
        print(f"第一个活跃地址: {found_hunters[0]}")
