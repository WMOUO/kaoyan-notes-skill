# kaoyan-notes

給 Claude Code 與 Codex 使用的 Skill（支援 macOS、Linux）：把考研不會的題目解題、分類、寫進 Obsidian，並累積成可做弱點分析的資料庫。

## 功能
- **記錄題目**：貼題目照片或文字，Claude 解題後依「科目、單元、重要性、熟悉度、錯誤原因、狀態」分類，寫成 `{科目}/{單元}/{標題}.md`，圖片複製到 `附件/`。每題一頁，題組才合併。
- **弱點分析**：用 `scripts/stats.py` 統計所有筆記的 frontmatter，輸出優先補強單元、錯誤類型分布與複習順序。

## 事前準備
- **請先下載並安裝 [Obsidian](https://obsidian.md/)**，並建立（或開啟）一個 vault。本 Skill 的筆記是寫進 vault 的 Markdown 檔，用 Obsidian 才能看到 `![[ ]]` 圖片、frontmatter 屬性與雙向連結。
- 需要 Python 3（只用標準函式庫）。
- 作業系統：macOS、Linux。

## 安裝
依你使用的工具擇一（Skill 資料夾名稱都叫 `kaoyan-notes`）：

**Claude Code**
```bash
git clone <此 repo 網址> ~/.claude/skills/kaoyan-notes
```
Windows 路徑為 `.claude\skills\kaoyan-notes`。

**Codex**
```bash
git clone <此 repo 網址> ~/.codex/skills/kaoyan-notes
```
Codex 沒有自動載入 Skill 時，可在你的專案或 `~/.codex/AGENTS.md` 加一行：「處理考研題目或弱點分析時，先讀 `~/.codex/skills/kaoyan-notes/SKILL.md` 並照做」。

兩者可共用同一份：只 clone 一次，再用 `ln -s` 把另一個目錄指過去。

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
python3 scripts/stats.py "<筆記根目錄>"
```
