import os, time, requests, subprocess

API_KEY = "AIzaSyBhoM7UFn5_WLrcfOlH55rWv7SWbQKVcCs"
# 终极修正：去掉多余的前缀，严格遵守 API 结构
BRAIN_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
TARGET_FILE = "/root/Lotus-System/lotus_autopilot.py"

def evolve():
    try:
        if not os.path.exists(TARGET_FILE):
            with open(TARGET_FILE, 'w') as f: f.write("# Init\nimport time\nprint('Waiting...')")
        with open(TARGET_FILE, 'r') as f: current_code = f.read()
        
        prompt = "You are the Lotus brain. Optimize the provided code. Output ONLY the code wrapped in !!!CODE_START!!! and !!!CODE_END!!!."
        # 简化请求体，确保符合 v1beta 标准
        payload = {
            "contents": [{"parts": [{"text": f"{prompt}\n\nCode:\n{current_code}"}]}]
        }
        headers = {'Content-Type': 'application/json'}
        res = requests.post(BRAIN_URL, json=payload, headers=headers, timeout=30).json()
        
        if 'candidates' not in res:
            print(f"⚠️ 物理链路诊断: {res}")
            return

        content = res['candidates'][0]['content']['parts'][0]['text']
        if "!!!CODE_START!!!" in content:
            new_code = content.split("!!!CODE_START!!!")[1].split("!!!CODE_END!!!")[0].strip()
            with open(TARGET_FILE, "w") as f: f.write(new_code)
            os.system("pkill -f lotus_autopilot.py")
            subprocess.Popen(["python3", "-u", TARGET_FILE])
            print("✅ [物理降临] 逻辑已成功注入磁盘。")
    except Exception as e:
        print(f"❌ 链路故障: {e}")

if __name__ == "__main__":
    print("🤖 绝境突围版'进化之手'启动...")
    while True:
        evolve()
        time.sleep(60)
