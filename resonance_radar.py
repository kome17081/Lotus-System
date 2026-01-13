import asyncio, json, websockets, requests

API_KEY = "9b416239-4b4f-4803-8276-cbd66dc08987"
WSS_URL = f"wss://mainnet.helius-rpc.com/?api-key={API_KEY}"

def load_hunters():
    with open("/root/Lotus-System/hunters_matrix.json", "r") as f:
        return json.load(f)

async def radar_run():
    hunters = load_hunters()
    # 建立一个追踪池，记录每个币被多少个真神买入
    resonance_pool = {} 
    
    async with websockets.connect(WSS_URL) as ws:
        # 订阅逻辑：监控这 33 个地址的所有链上活动
        await ws.send(json.dumps({
            "jsonrpc": "2.0", "id": 1, "method": "logsSubscribe",
            "params": [{"mentions": hunters}, {"commitment": "processed"}]
        }))
        print(f"📡 莲图雷达启动！正在监听 {len(hunters)} 个实验对象的共振破缺...")
        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            res = data.get('params', {}).get('result', {}).get('value', {})
            logs = str(res.get('logs', []))
            payer = res.get('signature') # 简化处理，实际监控签名来源
            
            # 识别买入行为：寻找 Pump.fun 的买入指令特征
            if "Program log: Instruction: Buy" in logs:
                # 从日志提取 Mint 地址
                mint = next((l.split()[-1] for l in res.get('logs', []) if l.endswith("pump")), None)
                if mint:
                    if mint not in resonance_pool: resonance_pool[mint] = set()
                    # 模拟记录这个真神的介入（实际上 mentions 已经帮我们过滤了这 33 人）
                    resonance_pool[mint].add(payer) 
                    count = len(resonance_pool[mint])
                    
                    print(f"🕵️ 实验对象动作！目标: {mint} | 当前共振数: {count}")
                    
                    if count >= 3:
                        print("\n" + "🔥" * 20)
                        print(f"🚨 绝杀信号：【共振破缺】发生！")
                        print(f"🎯 目标合约: {mint}")
                        print(f"⚡ 共振强度: {count} 人齐冲")
                        print(f"🔗 链接: https://gmgn.ai/sol/token/{mint}")
                        print("🔥" * 20 + "\n")

if __name__ == "__main__":
    asyncio.run(radar_run())
