"""
语义解释 API 路由（预留）

NOTE: MVP 中返回模板化解释，后续接入 Qwen2.5-VL-3B
"""

from fastapi import APIRouter

from app.schema.schemas import (
    SemanticExplainRequest,
    SemanticExplainResponse,
)
from app.service.semantic_service import semanticService

router = APIRouter(prefix="/api/semantic", tags=["semantic"])


@router.post("/explain", response_model=SemanticExplainResponse)
async def explainState(request: SemanticExplainRequest):
    """
    生成当前状态的语义解释

    NOTE: MVP 阶段返回预设模板，后续替换为 VLM 实时生成
    """
    return semanticService.explain(
        state=request.state,
        context=request.context or "",
    )


@router.post("/rules/parse")
async def parseNaturalLanguageRule(ruleText: str = ""):
    """
    将自然语言规则解析为结构化规则

    NOTE: MVP 阶段返回不可用提示，后续接入 VLM
    """
    return semanticService.parseRule(ruleText)
