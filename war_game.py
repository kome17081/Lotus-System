import asyncio
import websockets
import json
import requests
import datetime
import os

API_KEY = "9b416239-4b4f-4803-8276-cbd66dc08987"
WSS_URL = f"wss://mainnet.helius-rpc.com/?api-key={API_KEY}"
HUNTERS = [
    "4EtAJ1p8RjqccEVhEhaYnEgQ6kA4JHR8oYqyLFwARUj6",
    "HWdeCUjBvPP1HJ5oCJt7aNsvMWpWoDgiejUWvfFX6T7R",
    "fwHknyxZTgFGytVz9VPrvWqipW2V4L4D99gEb831t81"
]

def get_price(mint):
    try:
        res = requests.get(f"https://api.jup.ag/price/v2?ids={mint}", timeout=5).json()
        return float(res['data'][mint]['price'])
    except: return 0

async def audit_trade(sig, wallet):
    url = f"https://api.helius.xyz/v0/transactions/?api-key={API_KEY}"
    try:
        res = requests.post(url, json={"transactions": [sig]}).json()
        mint = res[0].get('tokenTransfers', [{}])[-1].get('mint')
        if not mint: return
        entry_p = get_price(mint)
        if entry_p == 0: return
        print(f"追踪开启: 猎人 {wallet[:5]} 买入 {mint[:5]} | 入场价: {entry_p}")
        await asyncio.sleep(600)
        exit_p = get_price(mint)
        profit = (exit_p / entry_p - 1) * 100 if entry_p > 0 else 0
        status = "🔥 翻倍" if profit >= 100 else "💀 归零/腰斩" if profit < -40 else "平稳"
        report = f"[{datetime.datetime.now()}] 钱包:{wallet[:5]} | 结果:{status} | 收益:{profit:.2f}% | 币种:{mint}\n"
        with open("/root/Lotus-System/war_game_report.txt", "a") as f:
            f.write(report)
        os.system('cd /root/Lotus-System && git add . && git commit -m "WarGame: Trade Audited" && git push origin main --force > /dev/null 2>&1')
        print(f"审计完成: {status} ({profit:.2f}%)")
    except: pass

async def main():
    print("--- 影子演习启动：正在监听顶级猎人... ---")
    async with websockets.connect(WSS_URL) as ws:
        for addr in HUNTERS:
            await ws.send(json.dumps({"jsonrpc":"2.0","id":1,"method":"logsSubscribe","params":[{"mentions":[addr]},{"commitment":"processed"}]}))
        while True:
            msg = json.loads(await ws.recv())
            sig = msg.get('params', {}).get('result', {}).get('value', {}).get('signature')
            if sig:
                asyncio.create_task(audit_trade(sig, "Hunter"))

if __name__ == "__main__":
    asyncio.run(main())
