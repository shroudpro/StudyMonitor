# 学习行为视觉规则推理系统 — MVP 实施方案

## 项目概述

基于需求分析和概要设计，构建一个**本地离线运行**的学习行为分析系统 MVP。系统采用 B/S 架构，后端 FastAPI + YOLO 检测 + 规则引擎，前端 **Vue3 + TypeScript + Vite** 实时展示。

---

## 🎨 前端设计方向（frontend-design skill）

### Design Direction: Cyber-Academic（赛博学术风）

融合 **Industrial/Utilitarian** 与 **Retro-futurist** 两种风格。理由：这是一个面向学生的学习监控系统，需要兼具科技感（AI 检测）和学术安静感。

### DFII 评分

| 维度 | 分值 | 说明 |
|------|------|------|
| Aesthetic Impact | 4 | 深色赛博风 + 实时数据流效果独特 |
| Context Fit | 5 | 学习场景 + AI 监控完美匹配 |
| Implementation Feasibility | 4 | Vue3 + CSS 变量可实现 |
| Performance Safety | 4 | 轻量动画，不阻塞主线程 |
| Consistency Risk | 2 | 组件化设计，风险可控 |
| **DFII 总分** | **15** | ✅ Excellent，全力执行 |

### Design System Snapshot

**字体**：
- 展示字体：`JetBrains Mono`（适合代码/数据/科技感场景，非 AI 默认字体）
- 正文字体：`Noto Sans SC`（中文优先，清晰可读）

**配色系统**（CSS 变量）：
- 主色调：深蓝黑 `#0a0e1a` → 深空感
- 强调色：青蓝 `#00d4ff` → 科技/活跃
- 状态色：
  - 专注 `#00e676`（翡翠绿）
  - 分心 `#ff5252`（警报红）
  - 低效 `#ff9100`（琥珀橙）
  - 离开 `#546e7a`（冷灰）
- 表面色：`rgba(255,255,255,0.03)` → 微透玻璃层

**空间节奏**：4px 基准，间距 8/12/16/24/32

**动效哲学**：
- 状态切换：脉冲光晕（pulse glow），0.6s ease
- 数据流入：左滑渐显
- 悬浮态：微发光 + 轻微上浮

### Differentiation Callout

> "This avoids generic dashboard UI by using a **data-stream aesthetic** with glowing state indicators and mono-spaced data readouts, instead of standard card-grid layouts with colorful pie charts."

---

## MVP 范围决策

### ✅ 纳入 MVP（核心功能）

| 模块 | 说明 |
|------|------|
| 摄像头采集 | 后端 OpenCV 实时采集摄像头画面 |
| YOLO 目标检测 | YOLOv8n / ONNX Runtime 检测 person, cell phone, laptop, book |
| 状态抽象 | 将检测结果转为 is_present, using_phone 等结构化状态 |
| 规则推理引擎 | 基于规则判定专注/分心/离开/低效 |
| 时间序列分析 | 滑动窗口平滑状态，降低误判 |
| 前端实时展示 | 实时视频流 + 检测框 + 状态展示 |
| 行为数据统计 | 专注时长、分心次数、手机使用时长等 |
| 规则管理（简化版） | 手动 JSON 方式管理规则（查看/保存/启用/停用） |
| SQLite 存储 | 行为日志、规则配置 |

### ⏳ 暂缓实现（后续迭代）

| 模块 | 原因 |
|------|------|
| Qwen2.5-VL-3B 语义解释 | 大模型本地部署复杂，MVP 预留接口 + UI 占位 |
| 自然语言规则解析 | 依赖 VLM，MVP 预留接口 |

> [!IMPORTANT]
> MVP 中 VLM 相关功能会预留完整的 API 接口和前端 UI 入口，但实际调用逻辑暂时返回模拟数据或提示"功能开发中"，确保后续可无缝接入。

---

## 项目结构

```
e:\Vibe-coding\DATA-Process\
├── backend/                          # 后端服务
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI 入口 + WebSocket
│   │   ├── config.py                 # 配置管理
│   │   ├── database.py               # SQLite 数据库
│   │   ├── api/                      # API 路由层
│   │   │   ├── __init__.py
│   │   │   ├── detection.py          # /detect, /state
│   │   │   ├── stats.py              # /stats
│   │   │   ├── rules.py              # /rules/*
│   │   │   └── semantic.py           # /semantic/*（预留）
│   │   ├── service/                  # 业务逻辑层
│   │   │   ├── __init__.py
│   │   │   ├── camera_service.py     # 摄像头采集
│   │   │   ├── detector_service.py   # YOLO 检测
│   │   │   ├── state_service.py      # 状态抽象
│   │   │   ├── rule_engine.py        # 规则推理引擎
│   │   │   ├── timeline_service.py   # 时间序列分析
│   │   │   ├── stats_service.py      # 统计服务
│   │   │   └── semantic_service.py   # 语义服务（预留）
│   │   ├── model/                    # 数据模型
│   │   │   ├── __init__.py
│   │   │   └── models.py             # SQLAlchemy ORM
│   │   └── schema/                   # 请求/响应 Schema
│   │       ├── __init__.py
│   │       └── schemas.py            # Pydantic 模型
│   ├── models/                       # AI 模型文件
│   │   └── yolov8n.onnx              # （需手动下载）
│   ├── data/                         # 数据目录
│   └── environment.yml               # Conda 环境
├── frontend/                         # Vue3 前端
│   ├── src/
│   │   ├── App.vue
│   │   ├── main.ts
│   │   ├── style.css                 # 设计系统 + 全局样式
│   │   ├── components/
│   │   │   ├── VideoStream.vue       # 视频流展示
│   │   │   ├── StatusPanel.vue       # 状态面板
│   │   │   ├── StatsChart.vue        # 统计图表
│   │   │   ├── RuleManager.vue       # 规则管理
│   │   │   ├── SemanticPanel.vue     # 语义面板（预留）
│   │   │   └── AppHeader.vue         # 顶栏
│   │   ├── composables/              # Vue 组合式函数
│   │   │   ├── useWebSocket.ts       # WebSocket
│   │   │   └── useApi.ts             # API 调用
│   │   └── types/
│   │       └── index.ts              # 类型定义
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
├── 需求分析.md
└── 概要设计.md
```

---

## API 接口设计（前后端对齐）

| 接口 | 方法 | 描述 | MVP 状态 |
|------|------|------|----------|
| `ws://localhost:8000/ws/video` | WebSocket | 实时推送标注帧 + 状态 | ✅ |
| `GET /api/state` | GET | 获取当前行为状态 | ✅ |
| `GET /api/stats` | GET | 获取学习行为统计 | ✅ |
| `GET /api/rules` | GET | 获取规则列表 | ✅ |
| `POST /api/rules` | POST | 保存新规则 | ✅ |
| `PUT /api/rules/{id}` | PUT | 更新规则 | ✅ |
| `DELETE /api/rules/{id}` | DELETE | 删除规则 | ✅ |
| `POST /api/camera/start` | POST | 启动摄像头 | ✅ |
| `POST /api/camera/stop` | POST | 停止摄像头 | ✅ |
| `POST /api/semantic/explain` | POST | 语义解释（预留） | ⏳ |
| `POST /api/rules/parse` | POST | 自然语言规则解析（预留） | ⏳ |

---

## 需要你手动完成的事项

> [!WARNING]
> 以下操作需要你手动完成：

1. **安装 Conda**（如未安装）：确保系统中已安装 Anaconda 或 Miniconda
2. **下载 YOLO 模型**：
   ```bash
   # 激活环境后执行
   conda activate study-monitor
   pip install ultralytics
   python -c "from ultralytics import YOLO; m = YOLO('yolov8n.pt'); m.export(format='onnx')"
   # 将生成的 yolov8n.onnx 移到 backend/models/ 目录
   ```
3. **摄像头**：确保电脑连接了可用的摄像头

---

## Verification Plan

### Automated Tests
1. 启动后端服务，验证所有 API 端点可访问
2. 启动前端开发服务器，验证页面正常渲染
3. WebSocket 连接后可接收视频帧

### Manual Verification
1. 打开浏览器访问前端页面，确认 UI 布局和 Cyber-Academic 风格
2. 确认摄像头画面可以正常显示
3. 模拟检测场景，验证状态切换和统计功能
