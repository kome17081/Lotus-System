import requests
import time
import json

# 凭证
API_KEY = "9b416239-4b4f-4803-8276-cbd66dc08987"
RPC_URL = f"https://mainnet.helius-rpc.com/?api-key={API_KEY}"

def parse_transaction(signature):
    """通过 Signature 解析出买入的 Token 地址和价格"""
    url = f"https://api.helius.xyz/v0/transactions/?api-key={API_KEY}"
    payload = {"transactions": [signature]}
    try:
        res = requests.post(url, json=payload).json()
        tx = res[0]
        # 寻找 Token 转移逻辑
        token_transfers = tx.get('tokenTransfers', [])
        if token_transfers:
            # 简单逻辑：取最后一笔转移的代币作为买入目标
            mint = token_transfers[-1].get('mint')
            return mint
    except:
        return None

def get_price(mint):
    try:
        url = f"https://api.jup.ag/price/v2?ids={mint}"
        res = requests.get(url, timeout=5).json()
        return float(res['data'][mint]['price'])
    except:
        return 0

def run_shadow_test(signature, wallet_name):
    mint = parse_transaction(signature)
    if not mint: return
    
    entry_price = get_price(mint)
    if entry_price == 0: return

    log_start = f"追踪开始: [{wallet_name}] 买入 {mint} | 入场价: {entry_price}"
    print(log_start)
    
    # 模拟等待 10 分钟验证胜率
    print("等待 600 秒进行胜率审计...")
    time.sleep(600)
    
    exit_price = get_price(mint)
    profit = (exit_price / entry_price - 1) * 100 if entry_price > 0 else 0
    
    status = "✅ 翻倍" if profit >= 100 else "❌ 失败" if profit < -30 else "平盘"
    result_log = f"审计结束: {status} | 收益率: {profit:.2f}% | 币种: {mint}"
    print(result_log)
    
    # 存入物理文件供你随时在 GitHub 查阅
    with open("/root/Lotus-System/win_rate_report.txt", "a") as f:
        f.write(f"{result_log}\n")

if __name__ == "__main__":
    # 这里接入之前雷达捕获的真实 Sig 进行测试
    # 姜晨，只要雷达捕获到一个 Sig，你就可以丢进这里测它的含金量
    print("--- 影子追踪引擎已就绪 ---")
