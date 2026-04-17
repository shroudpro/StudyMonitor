"""
状态抽象服务 — 对应概要设计 2.3.2

NOTE: 这是系统从「视觉检测」走向「行为推理」的桥梁。
将 YOLO 低层检测结果转换为高层语义状态。
"""

import logging

from app.schema.schemas import DetectionItem, AbstractedState

logger = logging.getLogger(__name__)


class StateService:
    """
    状态抽象模块

    将目标检测结果转为结构化语义状态：
    - is_present: 是否检测到人
    - using_phone: 手机是否与人体区域存在高关联
    - using_laptop: 是否存在电脑且处于学习工位区域
    - reading_book: 是否存在书籍并处于有效学习区域
    """

    def abstract(
        self,
        detections: list[DetectionItem],
        stableDuration: float = 0.0,
    ) -> AbstractedState:
        """
        从一帧检测结果中抽象出语义状态

        Args:
            detections: YOLO 检测结果列表
            stableDuration: 当前状态持续时长（由时间序列模块提供）

        Returns:
            结构化的抽象状态
        """
        isPresent = False
        usingPhone = False
        usingLaptop = False
        readingBook = False

        personBoxes: list[list[float]] = []

        # 第一遍：收集所有检测目标
        for det in detections:
            if det.className == "person":
                isPresent = True
                personBoxes.append(det.bbox)
            elif det.className == "cell phone":
                usingPhone = True
            elif det.className == "laptop":
                usingLaptop = True
            elif det.className == "book":
                readingBook = True

        # NOTE: 如果检测到手机但没检测到人，不算正在使用手机
        # 这种情况可能是手机放在桌上但人不在
        if not isPresent:
            usingPhone = False
            usingLaptop = False
            readingBook = False

        # HACK: 简化版的空间关联判断
        # MVP 中只做简单的共现判断，后续可加入 IoU 空间关联
        if usingPhone and personBoxes:
            usingPhone = self._checkProximity(
                personBoxes, detections, "cell phone"
            )

        return AbstractedState(
            isPresent=isPresent,
            usingPhone=usingPhone,
            usingLaptop=usingLaptop,
            readingBook=readingBook,
            stableDuration=stableDuration,
        )

    def _checkProximity(
        self,
        personBoxes: list[list[float]],
        detections: list[DetectionItem],
        targetClass: str,
    ) -> bool:
        """
        检查目标物体是否与人体区域有空间关联

        NOTE: MVP 简化实现 — 判断目标物体中心点是否在人体框的扩展区域内。
        后续可以用更精确的 IoU 或姿态估计替换。
        """
        targetCenters = []
        for det in detections:
            if det.className == targetClass:
                cx = (det.bbox[0] + det.bbox[2]) / 2
                cy = (det.bbox[1] + det.bbox[3]) / 2
                targetCenters.append((cx, cy))

        for personBox in personBoxes:
            # 将人体框扩展 20%，增加容差
            px1, py1, px2, py2 = personBox
            pw = px2 - px1
            ph = py2 - py1
            expandedBox = [
                px1 - pw * 0.2,
                py1 - ph * 0.2,
                px2 + pw * 0.2,
                py2 + ph * 0.2,
            ]

            for cx, cy in targetCenters:
                if (expandedBox[0] <= cx <= expandedBox[2] and
                        expandedBox[1] <= cy <= expandedBox[3]):
                    return True

        return False


# 全局单例
stateService = StateService()
