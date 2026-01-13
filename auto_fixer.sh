#!/bin/bash
echo "--- Lotus Engine: Starting Targeted Security Patching ---"
# 仅针对安全更新进行静默升级
apt-get update
apt-get install --only-upgrade -y $(apt-get -s dist-upgrade | awk '/^Inst/ {print $2}')
echo "--- Patching Complete. Updating status... ---"
python3 /root/Lotus-System/vuln_analyzer.py
