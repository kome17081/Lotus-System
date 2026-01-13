import os, sys, time, requests

# 配置区
API_KEY = "AIzaSyBhoM7UFn5_WLrcfOlH55rWv7SWbQKVcCs"
BRAIN_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

def brain_audit(address):
    """由 AI 主脑进行决策判定"""
    prompt = f"你是 Lotus 自动驾驶内核。监控到真神地址 {address} 进场。请根据直觉给出 1-100 的评分。如果分数 > 90，回复 'EXECUTE'，否则回复 'IGNORE'。只需回复这两个词之一。"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        res = requests.post(BRAIN_URL, json=payload, timeout=10).json()
        decision = res['candidates'][0]['content']['parts'][0]['text'].strip().upper()
        return decision
    except:
        return "IGNORE"

def autopilot_loop():
    print("🚀 Lotus-System v2.0 自动驾驶内核已上线...")
    print("📡 状态：接管中... 目标：33 位真神... 模式：全自动审计")
    
    with os.popen('tail -f /root/Lotus-System/radar.log') as f:
        for line in f:
            if "🕵️ 捕获动作！" in line:
                try:
                    address = line.split("Mint: ")[1].split(" |")[0]
                    print(f"\n⚠️ 发现目标动作，主脑介入中...")
                    decision = brain_audit(address)
                    if "EXECUTE" in decision:
                        print(f"🔥 【绝杀指令】AI 评分过高！标记为 EXECUTE。")
                    else:
                        print(f"💤 【过滤】AI 评分不足，忽略该动作。")
                except:
                    continue

if __name__ == "__main__":
    autopilot_loop()
