import os
def analyze():
    print("--- Lotus Analyzer: Starting Vulnerability Assessment ---")
    updates = os.popen('apt list --upgradable 2>/dev/null').read()
    with open("/root/Lotus-System/vuln_report.txt", "w") as f:
        f.write("--- SECURITY UPDATE ANALYSIS ---\n")
        f.write(updates if updates else "System is secure.\n")
    print("--- Analysis Complete: Results stored in vuln_report.txt ---")

if __name__ == "__main__":
    analyze()
