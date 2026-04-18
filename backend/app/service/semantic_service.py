"""
语义服务 — 对应概要设计 2.3.5

NOTE: 接入 Ollama 运行本地 Qwen2.5-1.5B (由于 Qwen3 未出，使用 Qwen2.5 大致相同规模模型)
支持：
1. 状态解释生成
2. 自然语言规则解析
"""

import logging
import json
import httpx
from pydantic import BaseModel

from app.schema.schemas import SemanticExplainResponse, NlRuleParseResponse, AbstractedState

logger = logging.getLogger(__name__)

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:1.5b"
TIMEOUT_SEC = 10.0


class SemanticService:
    """
    语义增强服务
    
    使用本地 Ollama Qwen 模型生成解释和解析规则。
    具备降级能力（网络错误/未启动时）。
    """

    def __init__(self) -> None:
        self._isAvailable = True

    @property
    def isAvailable(self) -> bool:
        return self._isAvailable

    def _callOllama(self, prompt: str) -> str:
        """底层调用 Ollama API"""
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
        try:
            with httpx.Client(timeout=TIMEOUT_SEC) as client:
                response = client.post(OLLAMA_API_URL, json=payload)
                response.raise_for_status()
                data = response.json()
                return data.get("response", "").strip()
        except Exception as e:
            logger.error(f"Ollama 调用失败: {e}")
            raise

    def explain(self, currentState: str, abstractedState: AbstractedState, matchedRule: str | None, context: str = "") -> SemanticExplainResponse:
        """
        生成当前状态的语义解释
        """
        # 降级模板
        templates = {
            "专注": "系统检测到用户正在使用电脑或阅读书籍，且未发现分心行为，判定为专注状态。",
            "分心": "系统检测到用户正在使用手机，或头部严重偏移，因此判定为分心状态。",
            "低效": "系统检测到用户在座位上，但未检测到明显的学习行为或姿势异常，判定为低效状态。",
            "离开": "系统未检测到用户在摄像头画面中，判定为离开状态。",
        }
        template_text = templates.get(currentState, f"当前状态为「{currentState}」。")

        prompt = f"""你是一个智能学习行为分析系统的解释助手。请根据下方的判定规则和实时传感器数据，用一句简洁的中文向用户解释当前为什么被判定为该状态。

系统当前的默认判定规则逻辑（供你参考）：
1. 离开 (AWAY)：不在位 (isPresent=false) 超过 5 秒。
2. 分心 (DISTRACTED)：在位、没有低头且转头 (headTurnedAway=true) 超过 10 秒。
3. 专注 (FOCUS)：
   - 伏案专注：低头 (headDown=true) 且 静止发呆时间 (inactiveDuration) <= 60 秒。
   - 屏幕专注：抬头 (headDown=false)、没转头 且 静止发呆时间内 (inactiveDuration) <= 30 秒。
4. 低效 (LOW)：当上述条件都不满足时触发。通常是因为：
   - 抬头静止(发呆)超过 30 秒。
   - 低头静止(睡着/僵直)超过 60 秒。

当前判定状态：{currentState}
匹配到的规则：{matchedRule or '默认规则'}

传感器数据：
- 是否在场 (isPresent): {abstractedState.isPresent}
- 脸部可见 (faceVisible): {abstractedState.faceVisible}
- 头部转向 (headTurnedAway): {abstractedState.headTurnedAway}
- 是否低头 (headDown): {abstractedState.headDown}
- 姿态是否稳定 (postureStable): {abstractedState.postureStable}
- 发呆/静止时长 (inactiveDuration): {abstractedState.inactiveDuration}秒

要求：
1. 严格按照上述逻辑解释。例如，如果是“低效”，请说明是因为静止时间超过了 30/60 秒。
2. 回答要通俗、简洁、友好，禁止虚构传感器数据中没体现的行为。
3. 纯文本，不要超过 50 字，禁止 Markdown。"""

        try:
            explanation = self._callOllama(prompt)
            # 清理可能的 markdown 等
            explanation = explanation.replace("```", "").replace("\n", "").strip()
            return SemanticExplainResponse(
                state=currentState,
                explanation=explanation,
                source="vlm"
            )
        except Exception:
            return SemanticExplainResponse(
                state=currentState,
                explanation=template_text,
                source="template"
            )

    def parseRule(self, ruleText: str) -> dict:
        """
        将自然语言规则解析为结构化规则
        """
        logger.info(f"自然语言规则解析: {ruleText}")

        prompt = f"""你是一个配置规则转化器。用户的系统支持根据传感器状态监控学习。用户的输入是自然语言描述的规则。你要将它转换为严格的 JSON 格式。

可用的传感器条件参数：
- head_turned_away: 布尔值 (头部是否明显偏离屏幕)
- head_down: 布尔值 (是否低头读写)
- face_visible: 布尔值 (脸部是否可见)
- is_present: 布尔值 (是否在场)
- posture_stable: 布尔值 (姿态是否稳定)
- duration_sec: 比较对象。例如 {{"min": 10}} 对应代码逻辑中的持续时间判断。
  （注：在 conditionJson 中请使用 {{"duration_sec": {{">": 10}}}} 这种格式）

输出的状态种类只能是："专注", "分心", "低效", "离开"。

用户输入："{ruleText}"

请根据输入，猜测规则名称（英文小写加下划线，例如 rule_distracted_10s）、条件和输出状态，并严格且**只输出 JSON 字符串**，不要包含任何前后缀或其他自然语言，不要用```包裹。格式示例：
{{"ruleName": "rule_name", "conditionJson": "{{\\"head_down\\": true, \\"duration_sec\\": {{\\">\\": 5}}}}", "outputState": "低效"}}
"""

        try:
            result_str = self._callOllama(prompt)
            # 尝试修复可能包裹的 ```json
            if result_str.startswith("```"):
                result_str = "\n".join(result_str.split("\n")[1:-1])
            result_str = result_str.strip()
            
            parsed = json.loads(result_str)
            return {
                "success": True,
                "parsedRule": {
                    "ruleName": parsed.get("ruleName", "custom_rule"),
                    "conditionJson": parsed.get("conditionJson", "{}"),
                    "outputState": parsed.get("outputState", "未知"),
                },
                "rawText": ruleText
            }
        except Exception as e:
            logger.error(f"解析规则失败: {e}")
            return {
                "success": False,
                "error": "VLM 无法正确解析规则内容，请检查描述是否清晰或稍后再试。",
                "rawText": ruleText
            }


# 全局单例
semanticService = SemanticService()
