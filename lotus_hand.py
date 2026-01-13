import os, time, requests, subprocess

API_KEY = "AIzaSyBhoM7UFn5_WLrcfOlH55rWv7SWbQKVcCs"
BRAIN_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
TARGET_FILE = "/root/Lotus-System/lotus_autopilot.py"

def evolve():
    # 1. 读取当前代码内容（向主脑展示身体）
    if not os.path.exists(TARGET_FILE):
        with open(TARGET_FILE, 'w') as f: f.write("# Init")
    with open(TARGET_FILE, 'r') as f:
        current_code = f.read()
    # 2. 封装 Payload
    prompt = f"你是 Lotus 进化主脑。当前代码：\n{current_code}\n请优化逻辑，直接输出代码并包裹在 !!!CODE_START!!! 和 !!!CODE_END!!! 之间。"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        res = requests.post(BRAIN_URL, json=payload, timeout=30).json()
        content = res['candidates'][0]['content']['parts'][0]['text']
        if "!!!CODE_START!!!" in content:
            new_code = content.split("!!!CODE_START!!!")[1].split("!!!CODE_END!!!")[0].strip()
            # 3. 物理改写磁盘
            with open(TARGET_FILE, "w") as f:
                f.write(new_code)
            os.system("pkill -f lotus_autopilot.py")
            subprocess.Popen(["python3", "-u", TARGET_FILE])
            print("✅ 物理逻辑已通过 API 实时更迭。")
    except Exception as e:
        print(f"❌ 进化失败: {e}")

if __name__ == "__main__":
    print("🤖 '进化之手' 已就绪，正在开启代码自曝与实时重塑循环...")
    while True:
        evolve()
        time.sleep(3600) # 保持免费额度，每小时进化一次
