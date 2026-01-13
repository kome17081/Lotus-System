import httpx
import json

def get_live_hunters():
    url = "https://gmgn.ai/api/v1/rank/wallet/smart_money/sol?orderby=pnl_7d&direction=desc"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://gmgn.ai/",
        "Accept": "application/json"
    }

    print("--- 正在刺探 GMGN 内部数据接口 ---")
    try:
        with httpx.Client(headers=headers, follow_redirects=True) as client:
            res = client.get(url, timeout=10)
            if res.status_code == 200:
                data = res.json()
                wallets = data.get('data', {}).get('rank', [])
                elite = [{"addr": w['address'], "win": w.get('win_rate'), "pnl": w.get('pnl_7d')} 
                        for w in wallets if w.get('win_rate', 0) > 0.6]
                return elite
            else:
                print(f"❌ 接口受阻: {res.status_code}"); return []
    except Exception as e:
        print(f"❌ 物理报错: {e}"); return []

if __name__ == "__main__":
    h_list = get_live_hunters()
    if h_list:
        print(f"✅ 成功穿透！捕获到 {len(h_list)} 个顶级猎人")
        for h in h_list[:3]:
            print(f"猎人: {h['addr'][:8]}... | 胜率: {h['win']:.2%}")
        with open("/root/Lotus-System/active_hunters.json", "w") as f:
            json.dump(h_list, f)
