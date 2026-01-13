import os, time, requests, subprocess

API_KEY = "AIzaSyBhoM7UFn5_WLrcfOlH55rWv7SWbQKVcCs"
# 物理坐标锁定：Lite 版通常配额最足
BRAIN_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent?key={API_KEY}"
TARGET_FILE = "/root/Lotus-System/lotus_autopilot.py"

def evolve():
    try:
        with open(TARGET_FILE, 'r') as f: current_code = f.read()
        prompt = "Optimize this code. Wrap the new code in !!!CODE_START!!! and !!!CODE_END!!!."
        payload = {"contents": [{"parts": [{"text": f"{prompt}\n\n{current_code}"}]}]}
        headers = {'Content-Type': 'application/json'}
        res = requests.post(BRAIN_URL, json=payload, headers=headers, timeout=30).json()
        if 'candidates' not in res:
            print(f"📡 链路诊断 (Lite): {res}")
            return
        content = res['candidates'][0]['content']['parts'][0]['text']
        if "!!!CODE_START!!!" in content:
            new_code = content.split("!!!CODE_START!!!")[1].split("!!!CODE_END!!!")[0].strip()
            with open(TARGET_FILE, "w") as f: f.write(new_code)
            os.system("pkill -f lotus_autopilot.py")
            subprocess.Popen(["python3", "-u", TARGET_FILE])
            print("💎 [物理降临] Lite 逻辑注入成功！")
    except Exception as e:
        print(f"❌ 链路故障: {e}")
if __name__ == "__main__":
    print("🤖 Gemini 2.0 Lite 通道启动，这是最后的物理突围...")
    while True:
        evolve()
        time.sleep(120) # 延长至2分钟，彻底规避频率限制
