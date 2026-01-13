import os, time, requests, subprocess

API_KEY = "AIzaSyBhoM7UFn5_WLrcfOlH55rWv7SWbQKVcCs"
# 修正后的物理坐标：增加 models/ 前缀并确保版本对应
BRAIN_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
TARGET_FILE = "/root/Lotus-System/lotus_autopilot.py"

def evolve():
    try:
        if not os.path.exists(TARGET_FILE):
            with open(TARGET_FILE, 'w') as f: f.write("# Init\nimport time\nprint('Waiting...')")
        with open(TARGET_FILE, 'r') as f: current_code = f.read()
        
        prompt = f"Optimize this Python code. Reply ONLY with code inside !!!CODE_START!!! and !!!CODE_END!!! marks:\n{current_code}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        res = requests.post(BRAIN_URL, json=payload, timeout=30).json()
        
        if 'candidates' not in res:
            print(f"⚠️ 坐标已通，但脑部未响应。回执: {res}")
            return

        content = res['candidates'][0]['content']['parts'][0]['text']
        if "!!!CODE_START!!!" in content:
            new_code = content.split("!!!CODE_START!!!")[1].split("!!!CODE_END!!!")[0].strip()
            with open(TARGET_FILE, "w") as f: f.write(new_code)
            os.system("pkill -f lotus_autopilot.py")
            subprocess.Popen(["python3", "-u", TARGET_FILE])
            print("✅ [重大突破] 物理逻辑已通过修正坐标成功更迭！")
    except Exception as e:
        print(f"❌ 运行故障: {e}")
