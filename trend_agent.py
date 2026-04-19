import feedparser
import time
import requests
from google import genai
from google.genai import types
import sys, os
from dotenv import load_dotenv
from datetime import datetime

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
    url = "https://news.hada.io/rss/news"
    # headers = {'User-Agent': 'Mozilla/5.0'}
    # url = "https://yozm.wishket.com/magazine/feed/"
    # headers는 위에서 말한 보강된 버전으로 사용하세요!
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }
    
    max_retries = 3 #최대 3번 시도
    for i in range (max_retries):
        try:
            print(f"🔍 뉴스 가져오는 중... (시도 {i+1}/{max_retries})")
            response = requests.get(url, headers=headers, timeout=10)
            
            # 403 에러 등이 발생하면 여기서 바로 Exception으로 넘어갑니다.
            response.raise_for_status()
            
            feed = feedparser.parse(response.content)
            if feed.entries:
                news_items = [{"title": entry.title, "link": entry.link} for entry in feed.entries[:count]]
                print(f"✅ 뉴스 {len(news_items)}개 수집 완료!")
                return news_items, True
            else:
                print("⚠️ 데이터가 비어있습니다. 잠시 후 재시도합니다.")
                return [], True

        except Exception as e:
            print(f"❌ 시도 {i+1}번째 실패, 뉴스 수집 중 에러 발생: {e}")
        
        # 마지막 시도가 아니면 5초 쉬었다가 다시 시도
        if i < max_retries - 1:
            time.sleep(5)
            
    return [], False # 결국 다 실패하면 빈 리스트 반환

def analyze_with_gemini(news_items, count=NEWS_COUNT):
    print("🚀 제미나이가 은실님을 위해 뉴스를 분석하고 있습니다...")

    news_text = "\n\n".join(
        f"제목: {item['title']}\n링크: {item['link']}" for item in news_items
    )

    prompt = f"""
    [지침: 엄격한 사실 기반 요약]
    당신은 제공된 '뉴스 리스트'의 내용만 사용하여 리포트를 작성하는 비서입니다.
    당신이 미리 알고 있는 지식이나 루머를 절대 섞지 마세요.

    1. 오직 아래 제공된 '뉴스 리스트'에 있는 실제 뉴스 {count} 개만 요약할 것.
    2. 각 뉴스를 한두 문장으로 간략하게 요약할 것. (링크는 출력하지 않아도 됨)
    3. 만약 뉴스 리스트의 내용이 은실님의 관심사(NestJS 등)와 관련이 없더라도,
       리스트에 있는 실제 뉴스를 그대로 전달할 것. (억지로 연결하지 마세요.)

    [뉴스 리스트]:
    {news_text}

    위 데이터를 바탕으로 은실님을 위한 한국어 요약 리포트를 작성해줘.
    """

    start_time = time.time()
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    end_time = time.time()

    print(f"✅ 분석 완료! (소요시간: {end_time - start_time:.2f}초)")
    return response.text


# ============================================
# 디스코드로 전송하는 함수
# ============================================

_EMBED_DESCRIPTION_LIMIT = 4096
_EMBED_FIELD_NAME_LIMIT = 256
_EMBED_FIELDS_MAX = 25
_EMBED_COLOR_BLUE = 0x3B82F6

def send_to_discord(news_items, report):
    print("💬 디스코드로 전송 중...")

    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("⚠️ DISCORD_WEBHOOK_URL이 없습니다. 전송을 건너뜁니다.")
        return

    today = datetime.now().strftime("%Y-%m-%d")

    # description: Gemini 요약 (4096자 초과 시 말줄임)
    description = report
    if len(description) > _EMBED_DESCRIPTION_LIMIT:
        description = description[:_EMBED_DESCRIPTION_LIMIT - 3] + "..."

    # fields: 뉴스 아이템당 1개 (최대 25개)
    fields = []
    for item in news_items[:_EMBED_FIELDS_MAX]:
        title = item["title"]
        if len(title) > _EMBED_FIELD_NAME_LIMIT:
            title = title[:_EMBED_FIELD_NAME_LIMIT - 3] + "..."
        fields.append({
            "name": title,
            "value": item["link"],
            "inline": False,
        })

    embed = {
        "title": f"🗞️ 오늘의 IT 트렌드 리포트 ({today})",
        "description": description,
        "color": _EMBED_COLOR_BLUE,
        "fields": fields,
        "footer": {"text": "Powered by Gemini AI  •  yozm.wishket.com"},
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    try:
        response = requests.post(
            webhook_url,
            json={"embeds": [embed]},
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        print("✅ 디스코드 전송 완료!")
    except Exception as e:
        print(f"❌ 디스코드 전송 실패: {e}")

# ============================================
# 메인 실행 함수
# ============================================

if __name__ == "__main__":
    news_items, is_success = fetch_news()

    if not is_success:
        print("🚨 서버 차단 또는 네트워크 에러로 뉴스 수집에 실패했습니다!")
        sys.exit(1) # 여기서 에러를 내야 깃허브 액션에 빨간 불이 들어옴

    if not news_items:
        print("📭 접속은 성공했으나, 오늘 올라온 새 뉴스가 없습니다.")
        sys.exit(0) # 이건 정상 상황이므로 초록 불

    report = analyze_with_gemini(news_items)

    print("\n" + "="*50)
    print("✨ 은실님을 위한 오늘의 AI 트렌드 리포트 ✨")
    print("="*50)
    print(report)
    print("="*50)

    send_to_discord(news_items, report)