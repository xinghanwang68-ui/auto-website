import os
from google import genai # 導入 Google 2026 最新官方庫

def get_ai_content():
    """調用新版 Google GenAI 免費 API 生成網頁內容"""
    # 1. 密鑰會自動讀取環境變數 GEMINI_API_KEY，直接初始化客戶端
    client = genai.Client()
    
    prompt = "你是一個科技網站總編輯，請用繁體中文撰寫內容。請提供今天的一句科技名人金句、背後的故事背景，以及這句話對當代科技發展的啟示。請用乾淨的 HTML 格式輸出（只需要 <div> 內的標籤，不用給完整的 html 宣告）。"
    
    # 2. 調用最新、免費且速度最快的 gemini-2.5-flash 模型
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )
    return response.text

def create_html(ai_content):
    """將 AI 內容嵌入到完整的 HTML 模板中"""
    html_template = f"""
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI 每日科技情報站</title>
        <style>
            body {{
                font-family: 'PingFang TC', 'Microsoft JhengHei', sans-serif;
                background-color: #f4f7f6;
                color: #333;
                margin: 0;
                padding: 40px 20px;
            }}
            .container {{
                max-width: 800px;
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            }}
            h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
            .footer {{ margin-top: 30px; font-size: 0.85em; color: #7f8c8d; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 AI 每日科技情報站</h1>
            <p style="color: #95a5a6;">更新時間：每日定時自動更新</p>
            <div class="content">
                {ai_content}
            </div>
            <div class="footer">
                本網頁由 Python + GitHub Actions + Google New GenAI API 自動化生成
            </div>
        </div>
    </body>
    </html>
    """
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_template)
    print("網頁更新成功！")

if __name__ == "__main__":
    content = get_ai_content()
    create_html(content)
