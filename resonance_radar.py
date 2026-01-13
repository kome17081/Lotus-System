import asyncio, json, websockets, requests

API_KEY = "9b416239-4b4f-4803-8276-cbd66dc08987"
WSS_URL = f"wss://mainnet.helius-rpc.com/?api-key={API_KEY}"

# 加载你刚刚抓到的实验对象
def load_hunters():
    try:
        with open("/root/Lotus-System/hunters_matrix.json", "r") as f:
            return set(json.load(f))
    except: return set()

async def radar_run():
    hunters = load_hunters()
    print(f"📡 雷达已启动，正在监控 {len(hunters)} 个实验对象的共振信号...")
    
    track_pool = {} # 格式: {mint: set(买入地址)}
    async with websockets.connect(WSS_URL) as ws:
        # 订阅全链交易日志，寻找这 33 人的踪迹
        await ws.send(json.dumps({"jsonrpc": "2.0", "id": 1, "method": "logsSubscribe", "params": [{"mentions": list(hunters)}, {"commitment": "processed"}]}))
        
        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            res = data.get('params', {}).get('result', {}).get('value', {})
            logs = str(res.get('logs', []))
            # 简单粗暴的逻辑：如果日志里出现了新币购买特征
            if "Program log: Instruction: Buy" in logs:
                # 寻找日志中的 Mint 地址（简化逻辑）
                mint = next((l.split()[-1] for l in res.get('logs', []) if l.endswith("pump")), "Unknown")
                payer = "Unknown" # 实际需解析 innerInstructions，此处暂简化提示
                
                print(f"⚠️ 实验对象介入！目标: {mint}")
                # 真正的破缺：当 3 个人同时指向同一个 mint
                # 这里就是姜晨你要的“真金白银”的信号

if __name__ == "__main__":
    asyncio.run(radar_run())
