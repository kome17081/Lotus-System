import os
import platform
import datetime

def main():
    stats = {
        "time": str(datetime.datetime.now()),
        "uptime": os.popen('uptime -p').read().strip(),
        "load": os.popen("cat /proc/loadavg").read().strip(),
        "memory": os.popen("free -m").read().strip()
    }
    # 强制写入同步文件夹
    with open("/root/Lotus-System/sentinel_report.txt", "w") as f:
        for k, v in stats.items():
            f.write(f"{k}: {v}\n")
    print("--- Physical Scan Complete: Report Generated ---")

if __name__ == "__main__":
    main()
