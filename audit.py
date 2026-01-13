with open("/root/Lotus-System/vuln_report.txt", "r") as f:
    lines = f.readlines()
    pending = [l.strip() for l in lines if "/" in l]
    print("\n--- 物理审计报告 (Real-World Audit) ---")
    if not pending:
        print("状态：所有安全更新已成功注入。")
    else:
        print(f"状态：尚有 {len(pending)} 个漏洞未修复。")
        print("待办列表：")
        for p in pending[:5]: print(f" - {p}")
    print("--------------------------------------\n")
