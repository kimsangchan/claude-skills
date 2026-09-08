#!/usr/bin/env python3
"""s4-rpi-ip-camera/ 산출물을 s4-b.md 한 파일로 병합 (0907 런과 같은 순서·구분자)."""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
ORDER = ["00-seed", "01-recon", "02-blindspot-register", "03-prd", "04-architecture",
         "05-api-contract", "06-test-design", "07-ops-design", "08-readiness-report", "decision-log"]
src = HERE / "s4-rpi-ip-camera"
parts, missing = [], []
for name in ORDER:
    p = src / f"{name}.md"
    if p.is_file():
        parts.append(f"<!-- ===== {name}.md ===== -->\n" + p.read_text(encoding="utf-8").rstrip() + "\n")
    else:
        missing.append(name)
out = HERE / "s4-b.md"
out.write_text("\n".join(parts), encoding="utf-8")
print(f"s4-b.md: {out.stat().st_size:,} bytes, {len(parts)} files" + (f", missing: {', '.join(missing)}" if missing else ""))
