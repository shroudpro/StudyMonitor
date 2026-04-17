# StudyMonitor MVP v3 需求分析与概要设计

## 1. 需求分析 (Requirements Analysis)

### 1.1 项目背景
StudyMonitor 旨在通过视觉 AI 技术提供客观的学习状态反馈。经过前两版的迭代，产品已从不切实际的桌面目标检测（如书本、手机检测）进化为基于**上半身姿态关键点**的精准行为分析。

### 1.2 核心痛点
- **误报率高**：前置摄像头视角受限，无法稳定观测桌面。
- **状态跳变**：单帧检测不稳，缺乏时间维度的逻辑过滤。
- **反馈缺失**：用户需要“学习会话”的概念来统计一段完整时间的表现。

### 1.3 关键功能需求 (FM)
- **FM-001: 姿态感知**：利用 YOLO11-pose 提取人脸及肢体 17 个关键点，计算空间坐标与置信度。
- **FM-002: 状态抽象**：计算语义化布尔值：
    - `faceVisible` (正脸可见性)
    - `headTurnedAway` (侧脸/分心检测)
    - `headDown` (低头探测)
    - `postureStable` & `inactiveDuration` (通过关键点位移方差计算是否稳定及是否在发呆)。
- **FM-003: 智能规则引擎**：实行优先级匹配逻辑，解决状态吞噬问题。
- **FM-004: 会话生命周期管理**：提供“开始、重置、结束并结算”的完整会话闭环，支持 Session 数据汇总。
- **FM-005: 离线存储**：所有行为数据写入本地 SQLite。

---

## 2. 概要设计 (System Design)

### 2.1 技术栈 (Technology Stack)
- **后端**: Python 3.10+ / FastAPI / SQLAlchemy / ONNX Runtime (CPU)
- **前端**: Vue 3 / Vite / TypeScript / ECharts
- **AI模型**: YOLO11n-pose (17 Points)
- **数据库**: SQLite (本地)

### 2.2 核心架构 (Core Architecture)

```text
[摄像头] -> [Detector (YOLO11n-pose)] 
          -> [State Service (几何抽象)] 
          -> [Rule Engine (时序判定)] 
          -> [Timeline Service (平滑处理)] 
          -> [Frontend (实时图表/会话控制)]
```

### 2.3 核心数据结构

#### AbstractedState (内存对象)
- `isPresent`: 是否在场
- `faceVisible`: 正脸在看向屏幕
- `inactiveDuration`: 姿态完全不动持续时长（阈值：方差 < 0.01）
- `awayDuration`: 人员缺席累积时长

#### StudySession (数据库表)
- `sessionId`: uuid
- `totalDuration`: 总时长
- `focusRate`: 专注率 (专注时长/总时长)
- `distractedCount`: 分心触发次数

### 2.4 规则匹配逻辑 (Priority Engine)
1. **离开**: `PRESENT == false` 且 `AWAY_TIME > 3s`
2. **分心**: `HEAD_SIDEWAYS == true` 且持续时长达标
3. **专注**: `VISIBLE == true` 且 `STABLE == true` 且 `INACTIVE < 5s` (排除死磕死记/发呆)
4. **低效**: 兜底状态（如长时间一动不动、持续低头、姿态混乱）

### 2.5 接口设计 (API API)
- `POST /api/session/start`: 开启新统计
- `POST /api/session/stop`: 停止、存档并返回结果报告
- `WS /ws/video`: 实时推送 Frame、Keypoints、State

---

## 3. 设计亮点与改进点 (v3 Improvements)
- **高确定性判定**：舍弃不可观测特征，引入基于位移方差的 `postureStable`。
- **演示友好性**：降低了状态切换阈值，使得发呆满 5 秒即可稳定触发“低效”，便于快速验证。
- **数据闭环**：通过本地 Session 持久化，让产品从“实时显示器”转变为“学习分析工具”。
- **性能优化**：采用 ONNX Runtime 纯 CPU 推理，确保中低性能笔记本也能流畅运行。
