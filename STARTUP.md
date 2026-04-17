# StudyMonitor 项目启动指南

本指南将帮助您快速启动 **StudyMonitor** 学习监控平台的后端与前端系统。

## 环境要求

- **Python**: 3.10+ (推荐使用 Conda 环境)
- **Node.js**: 16.x+ 及 npm
- **摄像头**: 系统默认使用索引为 0 的摄像头（前置单摄像头）

---

## 1. 后端启动 (Python/FastAPI)

后端负责 YOLO11n-pose 姿态检测、状态抽象映射及规则推理。

### 安装依赖
进入 `backend` 目录并安装必要库：
```bash
cd backend
pip install fastapi uvicorn[standard] opencv-python onnxruntime sqlalchemy pydantic python-multipart websockets ultralytics
```

### 运行服务
在 `backend` 目录下执行：
```bash
python -m app.main
```
- 后端将默认运行在 `http://127.0.0.1:8000`
- API 文档可在 `http://127.0.0.1:8000/docs` 查看

---

## 2. 前端启动 (Vue3/Vite)

前端负责实时视频流显示、状态仪表盘及统计图表。

### 安装依赖
进入 `frontend` 目录：
```bash
cd frontend
npm install
```

### 运行服务
在 `frontend` 目录下执行：
```bash
npm run dev
```
- 前端将默认运行在 `http://localhost:3000` (或控制台提示的其他端口)

---

## 3. 使用说明

1. 确保摄像头未被其他应用占用。
2. 先启动后端，再启动前端。
3. 打开前端页面，系统将自动连接 WebSocket 并开启监控。
4. **功能指标**:
   - **专注**: 面部可见且姿态稳定。
   - **分心**: 头部大幅度偏离屏幕方向。
   - **低效**: 长时间低头（趴睡）或姿态频繁剧烈抖动。
   - **离开**: 画面中未检测到人。

---

## 4. 常见问题

- **模型下载**: 首次启动时后端会自动尝试从 Ultralytics 导出 `yolo11n-pose.onnx`。如果导出失败，请手动将模型放置在 `backend/models/` 目录下。
- **跨域问题**: 后端已配置 CORS 允许来源于前端的跨域请求。
