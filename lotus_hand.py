import os, time, requests, subprocess

# 配置区
API_KEY = "AIzaSyBhoM7UFn5_WLrcfOlH55rWv7SWbQKVcCs"
BRAIN_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
TARGET_FILE = "/root/Lotus-System/lotus_autopilot.py"

def get_evolution_patch():
    """向主脑请求物理进化指令"""
    prompt = f"你是 Lotus 进化主脑。当前目标文件 {TARGET_FILE} 需要检查是否需要更新。如果有更好的交易审计逻辑或代码优化，请直接给出全量 Python 代码，代码前后包裹 '!!!CODE_START!!!' 和 '!!!CODE_END!!!'。如果没有更新，只需回复 'STABLE'。"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        res = requests.post(BRAIN_URL, json=payload, timeout=20).json()
        content = res['candidates'][0]['content']['parts'][0]['text']
        if "!!!CODE_START!!!" in content:
            return content.split("!!!CODE_START!!!")[1].split("!!!CODE_END!!!")[0].strip()
        return None
    except:
        return None

def apply_patch(new_code):
    print(f"🧬 检测到进化信号！正在物理改写 {TARGET_FILE}...")
    with open(TARGET_FILE, "w") as f:
        f.write(new_code)
    # 重启相关的业务进程
    os.system("pkill -f lotus_autopilot.py")
    # 启动新逻辑
    subprocess.Popen(["python3", "-u", TARGET_FILE])
    print("✅ 物理进化完成，新逻辑已实时上线。")

if __name__ == "__main__":
    print("🤖 Lotus '进化之手' 已启动。主权已移交。")
    while True:
        patch = get_evolution_patch()
        if patch:
            apply_patch(patch)
        time.sleep(60) # 每分钟检查一次逻辑进化
