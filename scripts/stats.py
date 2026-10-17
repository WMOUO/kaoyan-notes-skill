#!/usr/bin/env python3
"""統計考研專區筆記的 frontmatter，輸出 JSON。唯讀，不會修改任何檔案。

用法: python3 stats.py "<筆記根目錄>"
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

SKIP_DIRS = {"附件", "弱點分析", "考古題"}
IMPORTANCE_WEIGHT = {"高": 3, "中": 2, "低": 1}


def parse_frontmatter(text):
    m = re.match(r"^---\s*\n(.*?)\n---\s*(\n|$)", text, re.S)
    if not m:
        return {}
    data = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip().strip('"').strip("'")
    return data


def to_int(v):
    try:
        return int(re.match(r"\d+", v).group())
    except (AttributeError, TypeError):
        return None


def main():
    if len(sys.argv) < 2:
        sys.exit("用法: stats.py <考研專區路徑>")
    root = Path(sys.argv[1]).expanduser()
    if not root.is_dir():
        sys.exit(f"找不到資料夾: {root}")
    notes, skipped = [], []
    for p in root.rglob("*.md"):
        rel = p.relative_to(root)
        if rel.parts[0] in SKIP_DIRS or p.name == "考研設定.md":
            continue
        fm = parse_frontmatter(p.read_text(encoding="utf-8", errors="replace"))
        if not fm.get("科目"):
            skipped.append(str(rel))
            continue
        notes.append({
            "path": str(rel).replace("\\", "/"),
            "科目": fm.get("科目", ""),
            "單元": fm.get("單元", ""),
            "重要性": fm.get("重要性", ""),
            "熟悉度": to_int(fm.get("熟悉度", "")),
            "錯誤原因": fm.get("錯誤原因", ""),
            "狀態": fm.get("狀態", ""),
        })

    units = defaultdict(list)
    for n in notes:
        units[(n["科目"], n["單元"])].append(n)

    unit_rows = []
    for (subj, unit), items in units.items():
        fams = [i["熟悉度"] for i in items if i["熟悉度"] is not None]
        avg = round(sum(fams) / len(fams), 2) if fams else None
        imp = Counter(i["重要性"] for i in items).most_common(1)[0][0]
        pending = sum(1 for i in items if i["狀態"] == "待複習")
        w = IMPORTANCE_WEIGHT.get(imp[:1], 1)
        # 優先分數 = 重要性權重 × (6 - 平均熟悉度) + 待複習題數 × 0.5
        score = round(w * (6 - avg) + pending * 0.5, 2) if avg is not None else None
        unit_rows.append({
            "科目": subj, "單元": unit, "題數": len(items), "平均熟悉度": avg,
            "重要性": imp, "待複習": pending, "優先分數": score,
            "錯誤原因": dict(Counter(i["錯誤原因"] for i in items if i["錯誤原因"])),
        })
    unit_rows.sort(key=lambda r: (r["優先分數"] is None, -(r["優先分數"] or 0)))

    subj_rows = []
    by_subj = defaultdict(list)
    for n in notes:
        by_subj[n["科目"]].append(n)
    for s, items in by_subj.items():
        fams = [i["熟悉度"] for i in items if i["熟悉度"] is not None]
        subj_rows.append({"科目": s, "題數": len(items),
                          "平均熟悉度": round(sum(fams) / len(fams), 2) if fams else None})

    out = {
        "總題數": len(notes),
        "科目統計": subj_rows,
        "單元統計(依優先分數排序)": unit_rows,
        "錯誤原因分布": dict(Counter(n["錯誤原因"] for n in notes if n["錯誤原因"])),
        "高重要性且低熟悉度(<=2)": [n["path"] for n in notes
                              if n["重要性"][:1] == "高" and n["熟悉度"] is not None and n["熟悉度"] <= 2],
        "待複習題目": [n["path"] for n in notes if n["狀態"] == "待複習"],
        "略過(無科目欄位)": skipped,
    }
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
