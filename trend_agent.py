import feedparser
import time
import requests
from google import genai
from google.genai import types
import sys, os
from dotenv import load_dotenv

load_dotenv()  # .env 파일 읽어오기


# ============================================
# ⚙️ 가져올 뉴스 설정
# ============================================
NEWS_COUNT = 10  
# ============================================

# 1. 제미나이 설정
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("❌ GEMINI_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")
    sys.exit(1)
    
client = genai.Client(api_key=GEMINI_API_KEY)

def fetch_news(count=NEWS_COUNT):
    print(f"🔍 GeekNews에서 최신 {count}개 소식을 가져오는 중...")
    # url = "https://news.hada.io/rss/news"
    url = "https://yozm.wishket.com/magazine/feed/"
    headers = {'User-Agent': 'Mozilla/5.0'} # 사람임을 나타냄
    
    try:
        response = requests.get(url, headers=headers)
        feed = feedparser.parse(response.content)
        
        if not feed.entries:
            print("⚠️ 뉴스를 찾지 못했습니다. (데이터가 비어있음)")
            return "현재 뉴스 데이터가 없습니다."
            
        news_list = [f"제목: {entry.title}\n링크: {entry.link}" for entry in feed.entries[:count]]
        print(f"✅ 뉴스 {len(news_list)}개 수집 완료!")
        return "\n\n".join(news_list)
        
    except Exception as e:
        print(f"❌ 뉴스 수집 중 에러 발생: {e}")
        return "뉴스 수집 실패"

def analyze_with_gemini(news, count=NEWS_COUNT):
    print("🚀 제미나이가 은실님을 위해 뉴스를 분석하고 있습니다... (발열 걱정 NO!)")
    
    prompt = f"""
    [지침: 엄격한 사실 기반 요약]
    당신은 제공된 '뉴스 리스트'의 내용만 사용하여 리포트를 작성하는 비서입니다.
    당신이 미리 알고 있는 지식이나 루머를 절대 섞지 마세요.
    
    1. 오직 아래 제공된 '뉴스 리스트'에 있는 실제 뉴스 {count} 개만 요약할 것.
    2. 각 뉴스의 제목과 [원본 링크]를 뉴스 리스트에 있는 그대로 출력할 것.
    3. 만약 뉴스 리스트의 내용이 은실님의 관심사(NestJS 등)와 관련이 없더라도, 
       리스트에 있는 실제 뉴스를 그대로 전달할 것. (억지로 연결하지 마세요.)
    4. 제공된 링크가 가짜라고 판단되면 요약하지 마세요.

    [뉴스 리스트]:
    {news}
    
    위 데이터를 바탕으로 은실님을 위한 한국어 리포트를 작성해줘.
    """
    
    start_time = time.time()
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    end_time = time.time()
    
    print(f"✅ 분석 완료! (소요시간: {end_time - start_time:.2f}초)")
    return response.text

if __name__ == "__main__":
    # 뉴스 가져오기
    news_data = fetch_news()
    
    # 제미나이 요약
    report = analyze_with_gemini(news_data)
    
    # 결과 출력
    print("\n" + "="*50)
    print("✨ 은실님을 위한 오늘의 AI 트렌드 리포트 ✨")
    print("="*50)
    print(report)
    print("="*50)