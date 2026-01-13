import os, time, requests, subprocess

API_KEY = "AIzaSyBhoM7UFn5_WLrcfOlH55rWv7SWbQKVcCs"
# 物理坐标精准锁定：2.0 Flash 稳定版
BRAIN_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
TARGET_FILE = "/root/Lotus-System/lotus_autopilot.py"

def evolve():
    try:
        if not os.path.exists(TARGET_FILE):
            with open(TARGET_FILE, 'w') as f: f.write("# Init\nimport time\nprint('System Online')")
        with open(TARGET_FILE, 'r') as f: current_code = f.read()
        
        prompt = "You are the Lotus Evolution Brain. Rewrite and optimize this code for 2026 market logic. Wrap the new code in !!!CODE_START!!! and !!!CODE_END!!! marks."
        payload = {
            "contents": [{"parts": [{"text": f"{prompt}\n\n{current_code}"}]}]
        }
        headers = {'Content-Type': 'application/json'}
        res = requests.post(BRAIN_URL, json=payload, headers=headers, timeout=30).json()
        
        if 'candidates' not in res:
            print(f"📡 链路诊断 (2.0): {res}")
            return

        content = res['candidates'][0]['content']['parts'][0]['text']
        if "!!!CODE_START!!!" in content:
            new_code = content.split("!!!CODE_START!!!")[1].split("!!!CODE_END!!!")[0].strip()
            with open(TARGET_FILE, "w") as f: f.write(new_code)
            os.system("pkill -f lotus_autopilot.py")
            subprocess.Popen(["python3", "-u", TARGET_FILE])
            print("💎 [物理降临] 2.0 逻辑已成功注入磁盘！")
    except Exception as e:
        print(f"❌ 链路故障: {e}")

if __name__ == "__main__":
    print("🤖 Gemini 2.0 物理通道已切换，启动中...")
    while True:
        evolve()
        time.sleep(60)
