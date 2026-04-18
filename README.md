# StudyMonitor

一个基于 FastAPI + Vue3 + YOLO11n + Ollama(Qwen) 的智能学习行为监控与分析系统。
**测试版 v1 核心特性**：纯本地全离线执行、极简桌面美学、自然语言规则解析、基于 VLM 的状态行为解释。

## 📦 技术栈

- **前端**：Vue 3 + Vite + TypeScript (Sleek Focus Design System)
- **后端**：FastAPI + SQLite + PyDantic
- **计算机视觉**：OpenCV + YOLO11n-pose (ONNX 格式)
- **语义理解**：Ollama + Qwen2.5-1.5B 

---

## 🚀 快速启动指南

### 1. 环境准备工作

本项目需要至少两层核心环境：Python 后端环境 以及 Ollama 本地模型服务。

**1.1 安装 Python 依赖**
建议使用 Conda 或 Venv 创建虚拟环境（要求 Python >= 3.10），以 Conda 为例：
```bash
conda create -n study-monitor python=3.11
conda activate study-monitor

# 切换到项目下 backend 目录
cd backend
# 如果你使用的是 environment.yml，可以直接 conda env update -f environment.yml
# 或者使用 pip 直接安装：
pip install fastapi uvicorn[standard] opencv-python-headless onnxruntime sqlalchemy pydantic websockets python-multipart httpx
```

### 1.2 准备模型与环境验证

本项目高度依赖 Ollama 提供的本地语义解析。请确保按以下步骤执行：

**A. 安装与启动 Ollama**
1. 前往 [Ollama 官网](https://ollama.com/) 下载并安装。
2. **验证启动状态**：
   - **方式一（视觉）**：检查电脑右下角系统托盘是否有 Ollama 的图标。
   - **方式二（浏览器）**：在浏览器访问 [http://localhost:11434](http://localhost:11434)，若显示 "Ollama is running" 则表示服务正常。
   - **方式三（终端）**：运行 `ollama --version` 检查命令是否可用。

**B. 准备并校验 Qwen 模型**
1. **拉取模型**：在终端运行 `ollama pull qwen2.5:1.5b`。 
2. **检查模型是否就绪**：运行 `ollama list`。
   - **预期结果**：列表中必须包含 `qwen2.5:1.5b`。如果缺失，后续的“状态解释”和“规则解析”将进入降级模板模式。

---

### 2. 运行系统

> [!IMPORTANT]
> **路径注意**：启动后端和前端时，请务必先进入对应的子目录，否则会发生 `ModuleNotFoundError`。

**步骤 A: 启动后端**
```bash
# 1. 进入后端目录 (核心步骤)
cd backend

# 2. 激活环境
conda activate study-monitor

# 3. 运行服务 (必须在 backend 目录下运行)
python -m app.main
```
*注：后端默认运行在 http://localhost:8000*

**步骤 B: 启动前端**
```bash
# 1. 另开一个窗口，进入前端目录
cd frontend

# 2. 启动开发服务器
npm run dev
```

---

## 💡 功能验证与常见问题

### VLM 服务状态检查
你可以通过以下现象判断 VLM 是否工作正常：
1. **自动解释**：当你的学习状态改变（如“专注”变为“分心”）后，查看右侧“行为解释”面板。
   - 显示 **[VLM]** 标签：连接 Ollama 成功，生成了 AI 实时解释。
   - 显示 **[模板]** 标签：无法连接 Ollama，已自动降级。
2. **规则解析**：点击“AI生成”规则，输入一段话并解析。
   - 若返回了 JSON 预览：成功。
   - 若提示“无法解析”：请检查终端中 Ollama 是否正在运行。

---

## 📜 系统默认规则

如果你没有配置任何自定义规则，系统将按以下标准逻辑进行判定：

| 状态 | 判定逻辑 (内置) | 说明 |
| :--- | :--- | :--- |
| **离开** | `!isPresent` 且 持续 > 5s | 防抖防误判：检测不到用户在屏幕前超过5秒 |
| **分心** | `isPresent`, `!headDown`, `headTurnedAway` 且 持续 > 10s | 非低头时的偏头：剔除低头读写，并且允许短暂转头思考 |
| **专注** | `headDown` 且 持续 < 60s<br> 或 `!headDown`, `!headTurnedAway` 且 持续 < 30s | 双轨制判定：支持长时间低头伏案（60s静止），同时支持看课件等屏幕聚焦（30s静止） |
| **低效** | 兜底逻辑 | 只打击真正的极限静止发呆。一旦发生活跃打断，则从兜底跳脱 |

*注：自定义规则的优先级高于默认规则。*
