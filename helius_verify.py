import requests
import json

# 姜晨提供的物理凭证
API_KEY = "9b416239-4b4f-4803-8276-cbd66dc08987"
RPC_URL = f"https://mainnet.helius-rpc.com/?api-key={API_KEY}"

def verify():
    print(f"--- 正在连接 Helius 节点 [Key: {API_KEY[:6]}...] ---")
    
    # 1. 测试节点连通性
    payload = {"jsonrpc": "2.0", "id": 1, "method": "getHealth"}
    try:
        res = requests.post(RPC_URL, json=payload, timeout=5)
        if res.status_code == 200:
            status = res.json().get('result', 'unknown')
            print(f"✅ 物理状态：连接成功 (Health: {status})")
            
            # 2. 测试数据读取（查询目前最活跃的一个聪明钱地址余额）
            # 地址：4EtAJ1p8RjqccEVhEhaYnEgQ6kA4JHR8oYqyLFwARUj6
            balance_payload = {
                "jsonrpc": "2.0", "id": 1, 
                "method": "getBalance", 
                "params": ["4EtAJ1p8RjqccEVhEhaYnEgQ6kA4JHR8oYqyLFwARUj6"]
            }
            bal_res = requests.post(RPC_URL, json=balance_payload).json()
            sol_bal = bal_res['result']['value'] / 10**9
            print(f"✅ 数据回传：成功抓取目标余额 {sol_bal:.2f} SOL")
            print("\n结论：该 Key 完全可用。你的服务器已具备“真实观察”能力。")
            
        elif res.status_code == 401:
            print("❌ 物理阻断：API Key 无效。请检查是否复制完整或已被重置。")
        elif res.status_code == 403:
            print("❌ 物理权限：Key 正确但权限不足（可能额度耗尽）。")
        else:
            print(f"❌ 未知错误：状态码 {res.status_code}")
    except Exception as e:
        print(f"❌ 网络异常：无法穿透到 Solana 主网 ({e})")

if __name__ == "__main__":
    verify()
