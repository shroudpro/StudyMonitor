# Study Monitor (学习行为视觉规则推理系统) 启动指南

本项目分为前端（Vue3 + Vite）和后端（FastAPI + YOLOv8图像识别），以下是完整启动该 MVP 项目的详细步骤。

## 1. 准备工作

确保你已经将 YOLO 模型文件放置到相应位置：
在 `backend/models` 目录下，必须存在：
- `yolov8n.onnx` （12.3 MB 左右）

## 2. 启动后端 (Backend)

后端提供了 WebSocket 实时视频推送以及相关数据统计 API。

1. **打开终端** 并激活你的 Python 虚拟环境（如：`study-monitor`）：
   ```bash
   conda activate study-monitor
   ```
2. **进入 backend 目录**：
   ```bash
   cd e:\Vibe-coding\DATA-Process\backend
   ```
3. **启动 FastAPI 服务**：
   ```bash
   python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
   ```
   > 启动成功后，控制台会显示 `Uvicorn running on http://127.0.0.1:8000`，表示后端服务正在运行。系统会自动探测默认摄像头以采集画面及启动推理引擎。
   
   健康状态检查（可选）：http://127.0.0.1:8000/api/health

## 3. 启动前端 (Frontend)

前端主要由 Vite 驱动，负责实时展示检测画面和状态推断。

1. **新开一个终端窗口**。
2. **进入 frontend 目录**：
   ```bash
   cd e:\Vibe-coding\DATA-Process\frontend
   ```
3. **安装依赖**（如果还未安装过）：
   ```bash
   npm install
   ```
4. **启动开发服务器**：
   ```bash
   npm run dev
   ```
   > 启动成功后，终端将输出 `Local: http://localhost:3000/`。

## 4. 预览系统

打开浏览器，访问 frontend 提供的地址：
👉 **http://localhost:3000**

此时即可在网页端查看通过 YOLO 推理过的实时视频流及检测数据。

## 常见问题处理
- **依赖/编译器报错问题**：前端如果存在 `useDefineForDefault` 报错或 Node 内置模块不可用（如 `__dirname`，`path` 等）的错误，通常是因为 TypeScript 设置或者未安装 `@types/node`。我们已对其进行了修复。
- **端口冲突**：如果 `8000` 或 `3000` 端口被占用，请在各自的配置中更改默认启动端口（即 backend 中的 `--port` 参数与 frontend `vite.config.ts` 中的 `server.port`）。
