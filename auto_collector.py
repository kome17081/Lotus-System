import asyncio, json, websockets, requests

API_KEY = "9b416239-4b4f-4803-8276-cbd66dc08987"
WSS_URL = f"wss://mainnet.helius-rpc.com/?api-key={API_KEY}"
PUMP_PROGRAM = "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"

async def auto_collect():
    hunters_pool = set()
    async with websockets.connect(WSS_URL) as ws:
        await ws.send(json.dumps({"jsonrpc":"2.0","id":1,"method":"logsSubscribe","params":[{"mentions":[PUMP_PROGRAM]},{"commitment":"processed"}]}))
        print("🚀 自动收割机启动：正在监听新币并自动提取真神...")
        while len(hunters_pool) < 33:
            msg = await ws.recv()
            data = json.loads(msg)
            res = data.get('params', {}).get('result', {}).get('value', {})
            logs = res.get('logs', [])
            if any("Instruction: Create" in log for log in logs):
                mint = next((l.split()[-1] for l in logs if l.endswith("pump")), None)
                if mint:
                    print(f"发现新目标 {mint}，正在剥离指纹...")
                    try:
                        sig_res = requests.post(f"https://mainnet.helius-rpc.com/?api-key={API_KEY}", json={"jsonrpc":"2.0","id":1,"method":"getSignaturesForAddress","params":[mint,{"limit":20}]}).json()
                        sigs = [x['signature'] for x in sig_res.get('result', [])]
                        for s in reversed(sigs):
                            tx = requests.post(f"https://api.helius.xyz/v0/transactions/?api-key={API_KEY}", json={"transactions":[s]}).json()
                            if isinstance(tx, list) and len(tx) > 0:
                                hunters_pool.add(tx[0]['feePayer'])
                                if len(hunters_pool) >= 33: break
                        print(f"📊 当前进度: {len(hunters_pool)}/33")
                    except: continue

        with open("/root/Lotus-System/hunters_matrix.json", "w") as f:
            json.dump(list(hunters_pool), f)
        print("✅ 33 个实验对象已集结完毕！hunters_matrix.json 已就绪。")

if __name__ == "__main__":
    asyncio.run(auto_collect())
