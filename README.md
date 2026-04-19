# 🐴 AI Harness

> A personal project to build a control & execution environment that wraps AI agents safely.

---

## Why I Built This

While building RAG-based chatbots, I noticed AI would sometimes give completely off-topic responses.
Then I learned about the concept of a "Harness" — a control and execution environment that wraps AI agents to make them behave safely and reliably.
Just like putting a harness on a horse to control its direction, AI needs the same kind of structure.
I decided to learn by building it myself.

---

## How It Works

```
User Request
    ↓
[Auth Middleware]
Local  → X-Harness-Key validation
Prod   → Skip (Kubernetes ClusterIP internal network)
    ↓
[Harness Core]
① Build system prompt from config.yaml (topic + context if RAG)
② Single LLM call → guard + answer at once
③ Check if response starts with BLOCKED:
    ↓
[Response]
blocked: true  → return blocked_reason + token_usage
blocked: false → return answer + token_usage
```

**RAG Support**

```
RAG Project
① Vector search → top 3~5 chunks
② Send chunks as context to Harness
Harness
③ Answer based only on provided context
```

---

## Project Structure

```
harness/
├── app/
│   ├── api/v1/
│   │   └── harness.py        # API router
│   ├── core/
│   │   ├── config.py         # Environment & model config
│   │   ├── harness.py        # Main harness class
│   │   └── prompts.py        # config.yaml loader
│   ├── adapters/
│   │   ├── base.py           # Abstract base adapter
│   │   ├── claude.py         # Claude adapter
│   │   └── openai.py         # OpenAI adapter
│   ├── middleware/
│   │   └── auth.py           # Local API key auth middleware
│   ├── schemas/
│   │   └── harness.py        # Request / Response models
│   └── main.py               # FastAPI entry point
├── config.yaml               # Prompt & model config (gitignored)
├── config.example.yaml       # Config template
├── .env                      # API keys (gitignored)
├── .env.example
├── requirements.txt
└── README.md
```

---

## Tech Stack

| | |
|---|---|
| Language | Python 3.12 |
| Framework | FastAPI |
| LLM | Claude (Anthropic) + GPT (OpenAI) |
| Auth | X-Harness-Key (local) / ClusterIP (k8s) |

## API

### `POST /api/v1/harness/run`

**Request**
```json
{
  "provider": "openai",
  "model": "gpt-4o",
  "topic": "기차",
  "topic_desc": "기차 운행, 요금, 노선, 예약과 관련된 내용",
  "query": "서울에서 부산 요금이 얼마야?",
  "context": "KTX 서울-부산 요금은 59,800원..."
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| provider | string | ✅ | `claude` or `openai` |
| model | string | ❌ | 없으면 config.yaml 기본값 사용 |
| topic | string | ✅ | 하네스 주제 |
| topic_desc | string | ✅ | 주제 설명 |
| query | string | ✅ | 사용자 질문 |
| context | string | ❌ | RAG 검색 결과 (없으면 LLM 자체 지식으로 답변) |

**Response**
```json
{
  "success": true,
  "provider": "openai",
  "topic": "기차",
  "query": "서울에서 부산 요금이 얼마야?",
  "answer": "KTX 서울-부산 요금은 59,800원입니다...",
  "blocked": false,
  "blocked_reason": null,
  "token_usage": {
    "input_tokens": 221,
    "output_tokens": 28,
    "total_tokens": 249
  }
}
```

### `GET /health`

```json
{ "status": "ok" }
```

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | ❌ | Claude 사용시 필요 |
| `OPENAI_API_KEY` | ❌ | OpenAI 사용시 필요 |
| `ENV` | ✅ | `local` or `production` |
| `HARNESS_API_KEYS` | ❌ | 로컬 인증 키 (쉼표로 구분) |
| `CONFIG_FILE` | ❌ | config 파일명 (기본값: `config.yaml`) |

---

> 🐣 *This is a learning-by-doing project. The process matters more than the result.*