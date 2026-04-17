<script setup lang="ts">
/**
 * 应用根组件
 *
 * NOTE: 主布局采用左右分栏 —
 * 左侧：视频流 + 统计图表
 * 右侧：状态面板 + 语义面板 + 规则管理
 */
import { ref, onMounted, onUnmounted } from 'vue'
import AppHeader from '@/components/AppHeader.vue'
import VideoStream from '@/components/VideoStream.vue'
import StatusPanel from '@/components/StatusPanel.vue'
import StatsChart from '@/components/StatsChart.vue'
import RuleManager from '@/components/RuleManager.vue'
import SemanticPanel from '@/components/SemanticPanel.vue'
import { useWebSocket } from '@/composables/useWebSocket'
import { useApi } from '@/composables/useApi'
import type { StatsResponse } from '@/types'

// WebSocket 连接 — 实时视频流 + 状态
const wsUrl = `ws://${window.location.hostname}:8000/ws/video`
const {
  isConnected,
  latestFrame,
  latestState,
  connect: wsConnect,
} = useWebSocket(wsUrl)

// API 调用
const { startCamera, getStats, startSession, resetSession, stopSession } = useApi()

// 统计数据与会话
const stats = ref<StatsResponse | null>(null)
let statsTimer: ReturnType<typeof setInterval>
const sessionActive = ref(false)
const finalStats = ref<StatsResponse | null>(null)

/**
 * 启动摄像头并连接 WebSocket
 */
async function handleStartCamera() {
  await startCamera()
  wsConnect()
}

/**
 * 定期拉取统计数据
 */
async function refreshStats() {
  if (sessionActive.value) {
    const result = await getStats()
    if (result) stats.value = result
  }
}

// ─── 会话控制 ───
async function handleStartSession() {
  const result = await startSession()
  if (result) {
    sessionActive.value = true
    finalStats.value = null
    stats.value = null
  }
}

async function handleResetSession() {
  await resetSession()
  stats.value = null
  finalStats.value = null
  sessionActive.value = false
}

async function handleStopSession() {
  const result = await stopSession()
  if (result && result.stats) {
    sessionActive.value = false
    finalStats.value = result.stats
  }
}

onMounted(() => {
  // 自动连接 WebSocket
  wsConnect()
  // 每 3 秒刷新统计数据
  refreshStats()
  statsTimer = setInterval(refreshStats, 3000)
})

onUnmounted(() => {
  clearInterval(statsTimer)
})
</script>

<template>
  <AppHeader :is-connected="isConnected" />

  <div class="app-layout">
    <!-- 左侧主区域 -->
    <div class="main-area">
      <VideoStream
        :frame="latestFrame"
        :is-connected="isConnected"
        @start-camera="handleStartCamera"
      />
      <StatsChart :stats="stats" />
    </div>

    <!-- 右侧边栏 -->
    <div class="side-area">
      <div class="card session-controls" style="margin-bottom: var(--space-4);">
        <div class="card-header">
          <span class="card-title">学习会话控制</span>
        </div>
        <div style="display: flex; gap: var(--space-2); margin-top: var(--space-3)">
            <button v-if="!sessionActive" class="btn btn-primary" @click="handleStartSession" style="flex: 1;">▶ 开始学习</button>
            <template v-else>
              <button class="btn btn-outline" @click="handleResetSession" style="flex: 1;">🔄 重置</button>
              <button class="btn btn-primary" @click="handleStopSession" style="flex: 1; background: var(--color-distracted); border-color: var(--color-distracted);">⏹ 结束并分析</button>
            </template>
        </div>
      </div>
      <StatusPanel :state="latestState" />
      <SemanticPanel :current-state="latestState.state" />
      <RuleManager />
    </div>

    <!-- 弹窗：分析结果 -->
    <div v-if="finalStats" class="modal-overlay" @click.self="finalStats = null">
      <div class="modal card">
        <h2 style="margin-bottom: var(--space-4); color: var(--color-accent); font-family: var(--font-mono);">会话统计报告</h2>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-4); margin-bottom: var(--space-5);">
          <div><strong>总时长:</strong> {{ Math.floor(finalStats.totalDuration) }}s</div>
          <div><strong>专注率:</strong> {{ finalStats.focusRate }}%</div>
          <div><strong>专注时长:</strong> {{ Math.floor(finalStats.focusDuration) }}s</div>
          <div><strong>分心时长:</strong> {{ Math.floor(finalStats.distractedDuration) }}s</div>
          <div><strong>低效时长:</strong> {{ Math.floor(finalStats.lowEfficiencyDuration) }}s</div>
          <div><strong>离开时长:</strong> {{ Math.floor(finalStats.awayDuration) }}s</div>
          <div><strong>分心次数:</strong> {{ finalStats.distractedCount }} 次</div>
        </div>
        <button class="btn btn-primary" style="width: 100%;" @click="finalStats = null">关 闭</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}
.modal {
  width: 400px;
  max-width: 90vw;
  padding: var(--space-6);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
}
</style>
