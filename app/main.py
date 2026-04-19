from fastapi import FastAPI
from app.api.v1 import harness as harness_v1

app = FastAPI(
    title="AI Harness",
    description="AI 에이전트를 안전하게 감싸는 제어 실행 환경",
    version="0.1.0",
)

app.include_router(
    harness_v1.router,
    prefix="/api/v1/harness",
    tags=["harness"],
)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)