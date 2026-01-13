import sys, json, requests

API_KEY = "AIzaSyBhoM7UFn5_WLrcfOlH55rWv7SWbQKVcCs"

def audit_hunter(address):
    # 提示词：要求 AI 像个链上猎人一样思考
    prompt_text = f"你现在是猎人系统的核心。地址 {address} 正在 Pump.fun 扫货。请根据你对聪明钱的直觉，30字内给出绝杀建议和 1-100 分。不要废话。"
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    headers = {'Content-Type': 'application/json'}
    payload = {"contents": [{"parts": [{"text": prompt_text}]}]}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=5)
        res_data = response.json()
        analysis = res_data['candidates'][0]['content']['parts'][0]['text']
        print(f"\n🧠 【AI 主脑审计 - 实战响应】")
        print(f"👤 目标真神: {address}")
        print(f"📡 猎杀建议: {analysis.strip()}")
        print("------------------------------")
    except Exception as e:
        print(f"⚠️ AI 审计链路微调中... (Error: {e})")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        audit_hunter(sys.argv[1])
