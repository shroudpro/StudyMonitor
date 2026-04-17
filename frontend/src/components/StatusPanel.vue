<script setup lang="ts">
/**
 * 状态面板组件
 *
 * 展示当前学习状态（脉冲光晕指示器）和状态抽象详情
 */
import { computed } from 'vue'
import type { BehaviorState } from '@/types'
import { STATE_CSS_CLASS } from '@/types'

const props = defineProps<{
  state: BehaviorState
}>()

const stateClass = computed(() => {
  return STATE_CSS_CLASS[props.state.state] || 'state-unknown'
})

/**
 * 格式化持续时长为可读字符串
 */
function formatDuration(seconds: number): string {
  if (seconds < 60) return `${Math.floor(seconds)}s`
  const min = Math.floor(seconds / 60)
  const sec = Math.floor(seconds % 60)
  return `${min}m ${sec}s`
}
</script>

<template>
  <div class="card">
    <div class="card-header">
      <span class="card-title">当前状态</span>
    </div>

    <!-- 主状态指示器 -->
    <div class="status-main">
      <div class="state-indicator" :class="stateClass">
        <span class="dot" />
        <span>{{ state.state }}</span>
      </div>
      <div class="status-duration data-readout">
        持续 <span class="value">{{ formatDuration(state.stableDuration) }}</span>
      </div>
    </div>

    <!-- 状态抽象详情 -->
    <div class="abstract-grid">
      <div
        class="abstract-item"
        :class="{ active: state.abstractedState.isPresent }"
      >
        <span class="abstract-icon">👤</span>
        <span class="abstract-label">在场</span>
      </div>
      <div
        class="abstract-item"
        :class="{ active: state.abstractedState.usingLaptop }"
      >
        <span class="abstract-icon">💻</span>
        <span class="abstract-label">电脑</span>
      </div>
      <div
        class="abstract-item"
        :class="{ active: state.abstractedState.usingPhone, warn: state.abstractedState.usingPhone }"
      >
        <span class="abstract-icon">📱</span>
        <span class="abstract-label">手机</span>
      </div>
      <div
        class="abstract-item"
        :class="{ active: state.abstractedState.readingBook }"
      >
        <span class="abstract-icon">📖</span>
        <span class="abstract-label">书籍</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.status-main {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-3);
  margin-bottom: var(--space-5);
}

.status-duration {
  font-size: 0.8rem;
}

.abstract-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-2);
}

.abstract-item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-sm);
  background: var(--color-void);
  border: 1px solid var(--color-border);
  opacity: 0.4;
  transition: all var(--transition-normal);
}

.abstract-item.active {
  opacity: 1;
  border-color: var(--color-accent);
  background: var(--color-accent-dim);
}

.abstract-item.warn {
  border-color: var(--color-distracted);
  background: var(--color-distracted-dim);
}

.abstract-icon {
  font-size: 1rem;
}

.abstract-label {
  font-family: var(--font-mono);
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--color-text-secondary);
}
</style>
