# 🗞️ Daily News Agent

> 매일 아침, IT 뉴스를 AI가 요약해서 디스코드로 배달해주는 자동화 에이전트

GeekNews의 최신 IT 소식을 RSS로 가져와 Gemini AI가 한국어로 요약하고, 디스코드로 자동 전송합니다. GitHub Actions로 매일 정해진 시간에 알아서 돌아가요.

## ✨ 주요 기능

- 📡 **GeekNews RSS 수집** — 최신 IT/개발 뉴스 자동 크롤링
- 🤖 **Gemini AI 요약** — 뉴스를 한국어로 깔끔하게 정리
- 💬 **디스코드 알림** — 웹훅으로 매일 아침 배달
- ⏰ **완전 자동화** — GitHub Actions 스케줄러로 무인 실행

## 🛠️ 기술 스택

- **Python 3.13**
- **Google Gemini API** (`gemini-2.5-flash`)
- **feedparser** — RSS 파싱
- **GitHub Actions** — 스케줄링 & 자동화
- **Discord Webhook** — 알림 전송

## 📦 프로젝트 구조

```
daily-news-agent/
├── .github/
│   └── workflows/
│       └── news.yml          # GitHub Actions 워크플로우
├── trend_agent.py            # 메인 스크립트
├── requirements.txt          # 의존성
├── .env.example              # 환경변수 예시
└── .gitignore
```

## 🚀 로컬 실행 방법

### 1. 저장소 클론

```bash
git clone https://github.com/prov332325/daily-news-agent.git
cd daily-news-agent
```

### 2. 가상환경 생성 & 활성화

```bash
python -m venv venv

# Windows
.\venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate
```

### 3. 의존성 설치

```bash
pip install -r requirements.txt
```

### 4. 환경변수 설정

`.env.example`을 복사해 `.env`로 만들고 값 입력:

```
GEMINI_API_KEY=your_gemini_api_key_here
DISCORD_WEBHOOK_URL=your_discord_webhook_url_here
```

- **Gemini API Key**: https://aistudio.google.com/app/apikey
- **Discord Webhook**: 채널 설정 → 연동 → 웹후크에서 생성

### 5. 실행

```bash
python trend_agent.py
```

## ⚙️ GitHub Actions 설정

자동 실행을 원한다면:

1. 저장소 → **Settings** → **Secrets and variables** → **Actions**
2. 다음 Secret 추가:
   - `GEMINI_API_KEY`
   - `DISCORD_WEBHOOK_URL`
3. `.github/workflows/news.yml`에 설정된 스케줄대로 자동 실행됨
   - 기본: 매일 한국시간 오전 9시 (`cron: '0 0 * * *'`)

## 📸 실행 결과

디스코드로 아래처럼 전달됩니다:

> ✨ 오늘의 AI 트렌드 리포트 (2026-04-19) ✨  
> 1. **클로드 코드 제대로 써보신 분! <클코나잇 2> 발표자 모집**  
>   링크: https://...  
>   요약: ...

## 🔮 로드맵

- [ ] 본문 크롤링으로 요약 품질 향상
- [ ] 관심 키워드 필터링
- [ ] 최근 24시간 이내 뉴스만 수집 (중복 제거)
- [ ] 뉴스 소스 추가 (Hacker News, Dev.to 등)
- [ ] 리포트를 마크다운 파일로 자동 아카이빙

## 📝 License

MIT

---

Made with 🤖 by [prov332325](https://github.com/prov332325)
