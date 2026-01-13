import asyncio, json, websockets

# API 配置
API_KEY = "9b416239-4b4f-4803-8276-cbd66dc08987"
WSS_URL = f"wss://mainnet.helius-rpc.com/?api-key={API_KEY}"
PUMP_PROGRAM = "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"

async def lotus_watch():
    async with websockets.connect(WSS_URL) as ws:
        # 建立订阅：只看 Pump.fun 的程序日志
        await ws.send(json.dumps({
            "jsonrpc": "2.0", "id": 1, "method": "logsSubscribe",
            "params": [{"mentions": [PUMP_PROGRAM]}, {"commitment": "processed"}]
        }))
        print("--- 零式监视：等待混沌破缺 ---")
        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            res = data.get('params', {}).get('result', {}).get('value', {})
            logs = res.get('logs', [])
            sig = res.get('signature')
            
            # 莲图逻辑：寻找 Instruction 为 Create 的特征码
            if any("Instruction: Create" in log for log in logs):
                # 精准匹配：寻找包含 'pump' 结尾的 Mint 地址
                mint = next((l.split()[-1] for l in logs if l.endswith("pump")), None)
                if mint:
                    print(f"🌟 [金狗现身] Mint: {mint}")
                    print(f"🔗 签名: https://solscan.io/tx/{sig}")

if __name__ == "__main__":
    asyncio.run(lotus_watch())
