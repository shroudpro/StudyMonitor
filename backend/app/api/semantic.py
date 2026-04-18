"""
语义解释 API 路由（预留）

NOTE: MVP 中返回模板化解释，后续接入 Qwen2.5-VL-3B
"""

from fastapi import APIRouter

from app.schema.schemas import (
    SemanticExplainRequest,
    SemanticExplainResponse,
    NlRuleParseRequest,
    NlRuleParseResponse,
)
from app.service.semantic_service import semanticService

router = APIRouter(prefix="/api/semantic", tags=["semantic"])


@router.post("/explain", response_model=SemanticExplainResponse)
async def explainState(request: SemanticExplainRequest):
    """
    生成当前状态的语义解释

    使用本地 Ollama VLM/LLM
    """
    return await semanticService.explain(
        currentState=request.currentState,
        abstractedState=request.abstractedState,
        matchedRule=request.matchedRule,
        context=request.context or "",
    )


@router.post("/rules/parse", response_model=NlRuleParseResponse)
async def parseNaturalLanguageRule(request: NlRuleParseRequest):
    """
    将自然语言规则解析为结构化规则
    """
    return await semanticService.parseRule(request.ruleText)
