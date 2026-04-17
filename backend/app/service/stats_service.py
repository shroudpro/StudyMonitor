"""
学习行为统计服务

NOTE: 基于时间序列模块记录的状态历史计算统计指标，
不直接依赖数据库查询，保证实时性。
"""

import logging
from collections import Counter

from app.schema.schemas import StatsResponse
from app.service.timeline_service import timelineService

logger = logging.getLogger(__name__)


class StatsService:
    """
    统计服务 — 对应功能模块 FM-005

    从时间序列模块获取状态历史，计算各类统计指标。
    """

    def getStats(self) -> StatsResponse:
        """
        计算当前学习行为统计

        Returns:
            完整的统计数据响应
        """
        history = timelineService.getStateHistory()
        totalDuration = timelineService.totalDuration

        # 各状态累计时长
        focusDuration = 0.0
        distractedDuration = 0.0
        lowEfficiencyDuration = 0.0
        awayDuration = 0.0

        # 分心次数统计
        distractedCount = 0
        prevState = None

        # 状态时间线（用于前端图表）
        stateTimeline: list[dict] = []

        for segment in history:
            state = segment["state"]
            duration = segment["duration"]

            if state == "专注":
                focusDuration += duration
            elif state == "分心":
                distractedDuration += duration
                # 每次从非分心状态进入分心，算一次分心
                if prevState != "分心":
                    distractedCount += 1
            elif state == "低效":
                lowEfficiencyDuration += duration
            elif state == "离开":
                awayDuration += duration

            prevState = state

            stateTimeline.append({
                "state": state,
                "startTime": segment["startTime"],
                "endTime": segment["endTime"],
                "duration": round(duration, 1),
            })

        # 专注率
        focusRate = 0.0
        if totalDuration > 0:
            focusRate = round((focusDuration / totalDuration) * 100, 1)

        return StatsResponse(
            totalDuration=round(totalDuration, 1),
            focusDuration=round(focusDuration, 1),
            distractedDuration=round(distractedDuration, 1),
            lowEfficiencyDuration=round(lowEfficiencyDuration, 1),
            awayDuration=round(awayDuration, 1),
            distractedCount=distractedCount,
            # HACK: MVP 中手机使用时长近似等于分心时长
            phoneUsageDuration=round(distractedDuration, 1),
            focusRate=focusRate,
            stateTimeline=stateTimeline,
        )


# 全局单例
statsService = StatsService()
