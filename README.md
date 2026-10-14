# kaoyan-notes

給 Claude Code 使用的 Skill：把考研不會的題目解題、分類、寫進 Obsidian，並累積成可做弱點分析的資料庫。

## 功能
- **記錄題目**：貼題目照片或文字，Claude 解題後依「科目、單元、重要性、熟悉度、錯誤原因、狀態」分類，寫成 `{科目}/{單元}/{標題}.md`，圖片複製到 `附件/`。每題一頁，題組才合併。
- **弱點分析**：用 `scripts/stats.py` 統計所有筆記的 frontmatter，輸出優先補強單元、錯誤類型分布與複習順序。

## 安裝
```bash
git clone <此 repo 網址> ~/.claude/skills/kaoyan-notes
```
Windows 路徑為 `C:\Users\<你>\.claude\skills\kaoyan-notes`。需要 Python 3（只用標準函式庫）。

## 首次使用
直接貼一題題目。Skill 找不到 `config.json` 時，會一次問你：科系與科目、筆記根目錄的絕對路徑、熟悉度等級、有無考古題，然後在你確認後建立：
- `config.json`（只存在本機，已列入 `.gitignore`）
- `{筆記根目錄}/考研設定.md`
- `{筆記根目錄}/附件/`

## 使用
- 「幫我解這題並記錄」＋題目圖片或文字
- 「做弱點分析」

## 設計原則
- 熟悉度一律由使用者回答，不替你填。
- 不覆寫、不刪除既有筆記；寫入前先列出檔案等你確認。
- 重要性只是估計，並註明依據；沒有考古題時會標示為通用經驗估計。
- `scripts/stats.py` 唯讀。

## 手動統計
```bash
python scripts/stats.py "<筆記根目錄>"
```
