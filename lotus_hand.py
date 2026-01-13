import os, time, requests, subprocess

API_KEY = "AIzaSyBhoM7UFn5_WLrcfOlH55rWv7SWbQKVcCs"
# 物理路径切换至 v1 稳定版，这是 2026 年最可靠的出口
BRAIN_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
TARGET_FILE = "/root/Lotus-System/lotus_autopilot.py"

def evolve():
    try:
        if not os.path.exists(TARGET_FILE):
            with open(TARGET_FILE, 'w') as f: f.write("# Init\nimport time\nprint('System Online')")
        with open(TARGET_FILE, 'r') as f: current_code = f.read()
        
        prompt = "You are the Lotus Evolution Brain. Rewrite and optimize this code. Wrap the new code in !!!CODE_START!!! and !!!CODE_END!!! marks."
        payload = {
            "contents": [{"parts": [{"text": f"{prompt}\n\n{current_code}"}]}]
        }
        res = requests.post(BRAIN_URL, json=payload, timeout=30).json()
        
        if 'candidates' not in res:
            print(f"📡 链路回执: {res}")
            return

        content = res['candidates'][0]['content']['parts'][0]['text']
        if "!!!CODE_START!!!" in content:
            new_code = content.split("!!!CODE_START!!!")[1].split("!!!CODE_END!!!")[0].strip()
            with open(TARGET_FILE, "w") as f: f.write(new_code)
            os.system("pkill -f lotus_autopilot.py")
            subprocess.Popen(["python3", "-u", TARGET_FILE])
            print("💎 [物理破壁成功] 代码已实时同步。")
    except Exception as e:
        print(f"❌ 物理故障: {e}")

if __name__ == "__main__":
    print("🤖 V1 稳定通道版'进化之手'启动...")
    while True:
        evolve()
        time.sleep(60)
