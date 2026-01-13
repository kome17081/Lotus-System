import requests
import json
import time

API_KEY = "9b416239-4b4f-4803-8276-cbd66dc08987"

def check_wallet_quality(address):
    print(f"--- 正在审计地址战绩: {address[:8]}... ---")
    url = f"https://api.helius.xyz/v0/addresses/{address}/transactions?api-key={API_KEY}"
    try:
        res = requests.get(url, timeout=10).json()
        # 统计过去 20 笔交易的简单特征
        tx_count = len(res)
        if tx_count < 5: return False # 交易太少，不是职业猎人
        
        # 简单逻辑：如果 20 笔交易里频繁与 DEX 交互，视为活跃
        dex_interactions = 0
        for tx in res:
            if 'description' in tx and ('Raydium' in tx['description'] or 'Pump.fun' in tx['description']):
                dex_interactions += 1
        
        return dex_interactions > 5 # 至少有一半在冲狗
    except: return False

def filter_all():
    with open("/root/Lotus-System/active_hunters.json", "r") as f:
        raw_list = json.load(f)
    
    verified_hunters = []
    for addr in raw_list:
        if check_wallet_quality(addr):
            verified_hunters.append(addr)
            print(f"✅ 捕食者认证成功: {addr[:8]}")
        time.sleep(0.5) # 防止 Helius 频率限制
    
    with open("/root/Lotus-System/verified_hunters.json", "w") as f:
        json.dump(verified_hunters, f)
    print(f"\n--- 过滤完成！剩余精品猎人: {len(verified_hunters)} 名 ---")

if __name__ == "__main__":
    filter_all()
