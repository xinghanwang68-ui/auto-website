import os
import glob
from datetime import datetime
from google import genai

def get_ai_content():
    """調用 Google GenAI API 生成內容"""
    client = genai.Client()
    prompt = "你是一個科技網站總編輯，請用繁體中文撰寫內容。請提供今天的一句科技名人金句、背後的故事背景，以及這句話對當代科技發展的啟示。請用乾淨的 HTML 格式輸出（只需要 <div> 內的標籤，不用給完整的 html 宣告）。"
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )
    return response.text

def process_daily_content():
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    # 1. 生成今天的獨立網頁文章
    ai_content = get_ai_content()
    page_template = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>科技情報 - {today_str}</title>
    <style>
        body {{ font-family: 'PingFang TC', sans-serif; background-color: #f4f7f6; color: #333; padding: 40px 20px; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
        h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        .back-btn {{ display: inline-block; margin-bottom: 20px; color: #3498db; text-decoration: none; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="container">
        <a href="index.html" class="back-btn">⬅ 回到首頁</a>
        <h1>📅 科技情報：{today_str}</h1>
        <div class="content">{ai_content}</div>
    </div>
</body>
</html>"""

    # 寫入當天檔案 (如: 2026-07-24.html)
    with open(f"{today_str}.html", "w", encoding="utf-8") as f:
        f.write(page_template)

    # 2. 抓取所有日期 HTML 檔案（直接排除 index.html，不使用複雜正則）
    all_files = [f for f in glob.glob("*.html") if f != "index.html"]
    
    # 依檔名倒序排序（檔名為 YYYY-MM-DD.html，字串排序即為日期排序）
    all_files.sort(reverse=True)
    
    # 3. 超過 5 天的檔案進行清理
    if len(all_files) > 5:
        files_to_delete = all_files[5:]
        for old_file in files_to_delete:
            if os.path.exists(old_file):
                os.remove(old_file)
                print(f"清理歷史檔案: {old_file}")
        # 更新保留列表
        all_files = all_files[:5]

    # 4. 重新建構 index.html 首頁選單
    links_html = ""
    for file_name in all_files:
        date_display = file_name.replace(".html", "")
        links_html += f'<li><a class="date-link" href="{file_name}">📌 瀏覽 {date_display} 的科技情報</a></li>\n'

    homepage_template = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI 每日科技情報站</title>
    <style>
        body {{ font-family: 'PingFang TC', sans-serif; background-color: #f4f7f6; color: #333; padding: 40px 20px; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
        h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        ul {{ list-style: none; padding: 0; }}
        li {{ margin: 15px 0; }}
        .date-link {{ display: block; padding: 15px; background: #ecf0f1; color: #2c3e50; text-decoration: none; border-radius: 8px; font-weight: bold; transition: 0.2s; }}
        .date-link:hover {{ background: #3498db; color: white; transform: translateX(5px); }}
        .footer {{ margin-top: 50px; font-size: 0.85em; color: #7f8c8d; text-align: center; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 AI 每日科技情報站</h1>
        <p style="color: #95a5a6;">本站僅保留最近 5 日內的動態內容以供追蹤：</p>
        <ul>
            {links_html}
        </ul>
        <div class="footer">
            本網頁由 Python + GitHub Actions + Google New GenAI API 自動化生成
        </div>
    </body>
    </html>"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(homepage_template)

if __name__ == "__main__":
    process_daily_content()
