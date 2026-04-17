"""
语义服务（预留） — 对应概要设计 2.3.5

NOTE: MVP 中暂不接入 Qwen2.5-VL-3B，
返回占位数据以保证前端 UI 可以正常展示。
后续迭代时替换为真实 VLM 调用。
"""

import logging

from app.schema.schemas import SemanticExplainResponse

logger = logging.getLogger(__name__)


class SemanticService:
    """
    语义增强服务（预留）

    TODO: 后续接入 Qwen2.5-VL-3B 实现：
    1. 状态解释生成
    2. 自然语言规则解析
    """

    def __init__(self) -> None:
        self._modelLoaded: bool = False

    @property
    def isAvailable(self) -> bool:
        return self._modelLoaded

    def explain(self, state: str, context: str = "") -> SemanticExplainResponse:
        """
        生成当前状态的语义解释

        NOTE: MVP 中返回预设的模板化解释，后续替换为 VLM 生成
        """
        templates = {
            "专注": "系统检测到用户正在使用电脑或阅读书籍，且未发现分心行为，判定为专注状态。",
            "分心": "系统检测到用户正在使用手机，且持续时间较长，因此判定为分心状态。",
            "低效": "系统检测到用户在座位上，但未检测到明显的学习行为（如使用电脑或阅读），判定为低效状态。",
            "离开": "系统未检测到用户在摄像头画面中，判定为离开状态。",
        }

        explanation = templates.get(
            state,
            f"当前状态为「{state}」，语义解释功能将在后续版本中接入 Qwen2.5-VL-3B 模型。"
        )

        return SemanticExplainResponse(
            state=state,
            explanation=explanation,
        )

    def parseRule(self, ruleText: str) -> dict:
        """
        将自然语言规则解析为结构化规则

        TODO: 后续接入 VLM 实现真正的自然语言解析
        """
        logger.info(f"自然语言规则解析（预留）: {ruleText}")
        return {
            "status": "unavailable",
            "message": "自然语言规则解析功能将在后续版本中接入 Qwen2.5-VL-3B 模型。",
            "rawText": ruleText,
        }


# 全局单例
semanticService = SemanticService()
