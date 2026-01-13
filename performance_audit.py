import json
import requests
import time

# 你的凭证
API_KEY = "9b416239-4b4f-4803-8276-cbd66dc08987"
RPC_URL = f"https://mainnet.helius-rpc.com/?api-key={API_KEY}"

def get_token_price(mint_address):
    # 利用 Jupiter 或 Birdeye 接口获取实时价格
    try:
        url = f"https://api.jup.ag/price/v2?ids={mint_address}"
        res = requests.get(url, timeout=5).json()
        return float(res['data'][mint_address]['price'])
    except:
        return 0

def audit_signal(wallet, mint, entry_price):
    print(f"--- 启动模拟审计: 钱包 {wallet[:6]} 买入 {mint[:6]} ---")
    time.sleep(600) # 模拟10分钟后
    current_price = get_token_price(mint)
    
    if current_price > entry_price * 2:
        result = "🔥 DOUBLE! 翻倍成功"
    elif current_price < entry_price * 0.5:
        result = "💀 RUGGED! 归零/腰斩"
    else:
        result = "⏳ HOLDING/STABLE"
        
    print(f"审计结果: {result} | 当前涨幅: {((current_price/entry_price)-1)*100:.2f}%")

# 简单演示
if __name__ == "__main__":
    print("--- 审计引擎就绪：正在等待雷达捕获的 Signature 转化为 Mint 地址 ---")
