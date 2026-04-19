# AI Harness
- A personal project to build a control & execution environment that wraps AI agents safely.

## Why I Build This
- While building RAG-based chatbots, I noticed AI would sometimes give completely off-topic responses.
Then I learned about the concept of a "Harness" — a control and execution environment that wraps AI agents to make them behave safely and reliably.
Just like putting a harness on a horse to control its direction, AI needs the same kind of structure.
I decided to learn by building it myself.

## Project Structure
```
harness/
├── src/
│   ├── core/
│   │   ├── harness.py        # 하네스 메인 클래스 / Main harness class
│   │   └── types.py          # 공통 타입 정의 / Common type definitions
│   ├── adapters/
│   │   ├── claude.py         # Claude (Anthropic) 연결 / Claude adapter
│   │   └── openai.py         # GPT (OpenAI) 연결 / OpenAI adapter
│   ├── guards/
│   │   ├── topic_guard.py    # 주제 범위 제한 / Topic scope limiter
│   │   └── output_guard.py   # 출력 필터링 / Output filter
│   └── main.py               # FastAPI 진입점 / FastAPI entry point
├── .env                      # API 키 (git 제외) / API keys (gitignored)
├── .gitignore
├── requirements.txt
└── README.md
```

## Tech Stack
- Language: Python 3.12
- Framework: FastAPI
- Agent: LangChain + LangGraph
- Guardrail: GuardrailsAI
- LLM: Claude + GPT

## Get STarted
```
# 1. 클론 / Clone
git clone https://github.com/yourname/harness.git
cd harness

# 2. 가상환경 / Virtual environment
python -m venv .venv-harness
source .venv-harness/bin/activate  # Windows: .venv-harness\Scripts\activate

# 3. 패키지 설치 / Install packages
pip install -r requirements.txt

# 4. 환경변수 설정 / Set environment variables
cp .env.example .env
# .env 파일에 API 키 입력 / Fill in your API keys in .env

# 5. 서버 실행 / Run server
uvicorn src.main:app --reload
```