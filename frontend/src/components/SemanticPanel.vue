<script setup lang="ts">
/**
 * 语义解释面板组件（预留）
 *
 * MVP 中展示模板化解释，后续接入 VLM
 */
import { ref } from 'vue'
import { useApi } from '@/composables/useApi'
import type { SemanticExplainResponse } from '@/types'

const props = defineProps<{
  currentState: string
}>()

const { getExplanation } = useApi()

const explanation = ref<SemanticExplainResponse | null>(null)
const loading = ref(false)

async function fetchExplanation() {
  loading.value = true
  explanation.value = await getExplanation(props.currentState)
  loading.value = false
}
</script>

<template>
  <div class="card">
    <div class="card-header">
      <span class="card-title">语义解释</span>
      <span class="tag tag-disabled">VLM 预留</span>
    </div>

    <div v-if="explanation" class="semantic-text animate-fade-in">
      {{ explanation.explanation }}
    </div>

    <div v-else class="semantic-placeholder">
      <p class="data-readout">
        点击下方按钮获取当前状态的 AI 解释
      </p>
      <p class="data-readout" style="margin-top: var(--space-2);">
        <span style="color: var(--color-text-muted); font-size: 0.7rem;">
          // 后续将接入 Qwen2.5-VL-3B
        </span>
      </p>
    </div>

    <button
      class="btn btn-primary semantic-btn"
      :disabled="loading"
      @click="fetchExplanation"
    >
      {{ loading ? '分析中...' : '查看解释' }}
    </button>
  </div>
</template>

<style scoped>
.semantic-placeholder {
  padding: var(--space-4) 0;
}

.semantic-btn {
  margin-top: var(--space-4);
  width: 100%;
}
</style>
