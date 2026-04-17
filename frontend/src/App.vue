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
const { startCamera, getStats } = useApi()

// 统计数据
const stats = ref<StatsResponse | null>(null)
let statsTimer: ReturnType<typeof setInterval>

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
  const result = await getStats()
  if (result) stats.value = result
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
      <StatusPanel :state="latestState" />
      <SemanticPanel :current-state="latestState.state" />
      <RuleManager />
    </div>
  </div>
</template>
