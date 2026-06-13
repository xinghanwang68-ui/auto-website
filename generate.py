import os
import glob
from datetime import datetime, timedelta
from google import genai

def get_ai_content():
    """調用新版 Google GenAI 免費 API 生成網頁內容"""
    client = genai.Client()
    prompt = "你是一個科技網站總編輯，請用繁體中文撰寫內容。請提供今天的一句科技名人金句、背後的故事背景，以及這句話對當代科技發展的啟示。請用乾淨的 HTML 格式輸出（只需要 <div> 內的標籤，不用給完整的 html 宣告）。"
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )
    return response.text

def manage_history_pages(ai_content, today_str):
    """1. 生成當天的獨立網頁，並清理超過 5 天的舊網頁"""
    # 當天文章的獨立美化模板
    page_template = f"""
    <!DOCTYPE html>
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
    </html>
    """
    # 寫入當天的日期檔案 (例如: 2026-06-13.html)
    with open(f"{today_str}.html", "w", encoding="utf-8") as f:
        f.write(page_template)
        
    # 【自動清理機制】計算 5 天前的日期
    five_days_ago = datetime.now() - timedelta(days=5)
    
    # 找出所有歷史 HTML 檔案
    all_html_files = glob.glob("20[0-9][0-9]-[0-1][0-9]-[0-3][0-9].html")
    for file_name in all_html_files:
        try:
            # 從檔名解析出日期
            file_date_str = file_name.replace(".html", "")
            file_date = datetime.strptime(file_date_str, "%Y-%m-%d")
            # 如果檔案日期比 5 天前還舊，就刪除
            if file_date < five_days_ago:
                os.remove(file_name)
                print(f"已自動清理過期檔案: {file_name}")
        except ValueError:
            continue # 如果檔名格式不對就跳過

def create_homepage():
    """2. 根據目前留下的檔案，重新動態生成 index.html 首頁選單"""
    # 再次抓取目前資料夾內剩下的日期檔案
    valid_files = glob.glob("20[0-9][0-9]-[0-1][0-9]-[0-3][0-9].html")
    # 排序檔案，讓最新的日期排在最上面
    valid_files.sort(reverse=True)
    
    # 動態產生 5 日內的超連結 HTML 字串
    links_html = ""
    for file_name in valid_files:
        date_display = file_name.replace(".html", "")
        links_html += f'<li><a class="date-link" href="{file_name}">📌 瀏覽 {date_display} 的科技情報</a></li>\n'
    
    # 首頁的 HTML 模板
    homepage_template = f"""
    <!DOCTYPE html>
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
        </div>
    </body>
    </html>
    """
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(homepage_template)
    print("首頁選單更新成功！")

if __name__ == "__main__":
    # 取得今天日期的字串格式 (例如: 2026-06-13)
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 1. 叫 AI 寫今天的新文章
    ai_content = get_ai_content()
    
    # 2. 把文章存成今日獨立檔案，並刪除第 6 天前的舊檔
    manage_history_pages(ai_content, today)
    
    # 3. 重新掃描現有的檔案，做成首頁的 5 日連結列表
    create_homepage()
