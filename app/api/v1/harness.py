from fastapi import APIRouter, HTTPException
from app.schemas.harness import HarnessRequest, HarnessResponse
from app.core.harness import Harness

router = APIRouter()
harness = Harness()


@router.post("/run", response_model=HarnessResponse)
async def run_harness(request: HarnessRequest) -> HarnessResponse:
    """
    하네스 실행 엔드포인트

    - **provider**: 사용할 LLM (claude or openai)
    - **model**: 모델명 (없으면 provider 기본값 사용)
    - **topic**: 하네스 주제 (예: 기차)
    - **topic_desc**: 주제 설명 (예: 기차 운행, 요금, 노선 관련)
    - **query**: 사용자 질문
    """
    try:
        return await harness.run(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))