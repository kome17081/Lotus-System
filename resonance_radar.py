import asyncio, json, websockets

API_KEY = "9b416239-4b4f-4803-8276-cbd66dc08987"
WSS_URL = f"wss://mainnet.helius-rpc.com/?api-key={API_KEY}"

async def radar_run():
    with open("/root/Lotus-System/hunters_matrix.json", "r") as f:
        hunters = json.load(f)
    resonance_pool = {} 
    async with websockets.connect(WSS_URL) as ws:
        await ws.send(json.dumps({
            "jsonrpc": "2.0", "id": 1, "method": "logsSubscribe",
            "params": [{"mentions": hunters}, {"commitment": "processed"}]
        }))
        print(f"📡 莲图雷达已校准：正在深度监控 {len(hunters)} 个实验对象...")
        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            res = data.get('params', {}).get('result', {}).get('value', {})
            logs = str(res.get('logs', []))
            sig = res.get('signature')
            if "Instruction: Buy" in logs:
                mint = next((l.split()[-1] for l in res.get('logs', []) if l.endswith("pump")), None)
                if mint:
                    if mint not in resonance_pool: resonance_pool[mint] = set()
                    resonance_pool[mint].add(sig)
                    count = len(resonance_pool[mint])
                    print(f"🕵️ 捕获动作！Mint: {mint[:8]}... | 共振值: {count}")
                    if count >= 3:
                        print("\n" + "🔥" * 15 + "\n🚨 【共振破缺】发生！\n🎯 目标: " + mint + "\n🔗 https://gmgn.ai/sol/token/" + mint + "\n" + "🔥" * 15 + "\n")

if __name__ == "__main__":
    asyncio.run(radar_run())
