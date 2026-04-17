<script setup lang="ts">
/**
 * 应用顶栏组件
 *
 * 展示系统名称、连接状态和当前时间
 */
import { ref, onMounted, onUnmounted } from 'vue'

defineProps<{
  isConnected: boolean
}>()

const currentTime = ref('')
let timer: ReturnType<typeof setInterval>

function updateTime() {
  const now = new Date()
  currentTime.value = now.toLocaleTimeString('zh-CN', { hour12: false })
}

onMounted(() => {
  updateTime()
  timer = setInterval(updateTime, 1000)
})

onUnmounted(() => {
  clearInterval(timer)
})
</script>

<template>
  <header class="app-header">
    <div class="header-left">
      <div class="logo">
        <span class="logo-icon">◈</span>
        <span class="logo-text">StudyLens</span>
      </div>
      <span class="header-subtitle">学习行为分析系统</span>
    </div>

    <div class="header-right">
      <div class="header-status">
        <span
          class="status-dot"
          :class="isConnected ? 'online' : 'offline'"
        />
        <span class="data-readout">
          {{ isConnected ? 'CONNECTED' : 'OFFLINE' }}
        </span>
      </div>
      <div class="header-time data-readout">
        <span class="value">{{ currentTime }}</span>
      </div>
    </div>
  </header>
</template>

<style scoped>
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-3) var(--space-6);
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(12px);
}

.header-left {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.logo {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.logo-icon {
  font-size: 1.2rem;
  color: var(--color-accent);
  text-shadow: 0 0 8px var(--color-accent-glow);
}

.logo-text {
  font-family: var(--font-mono);
  font-size: 1rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: var(--color-text-primary);
}

.header-subtitle {
  font-family: var(--font-sans);
  font-size: 0.75rem;
  color: var(--color-text-muted);
  padding-left: var(--space-4);
  border-left: 1px solid var(--color-border);
}

.header-right {
  display: flex;
  align-items: center;
  gap: var(--space-6);
}

.header-status {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
}

.status-dot.online {
  background: var(--color-focus);
  box-shadow: 0 0 6px var(--color-focus-glow);
  animation: pulse 2s ease-in-out infinite;
}

.status-dot.offline {
  background: var(--color-text-muted);
}

.header-time {
  font-size: 0.85rem;
}
</style>
