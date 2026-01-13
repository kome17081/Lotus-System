import os
import platform

def sense_reality():
    # 这是一个真正的逻辑感应器，它会抓取你服务器的物理真实情况
    stats = {
        "os": platform.system(),
        "node": platform.node(),
        "engine_status": "Active",
        "purpose": "Nirvana Engine Foundation"
    }
    with open("reality_log.txt", "w") as f:
        for k, v in stats.items():
            f.write(f"{k}: {v}\n")
    print("--- 物理现实已捕获，准备同步至 GitHub ---")

if __name__ == "__main__":
    sense_reality()
