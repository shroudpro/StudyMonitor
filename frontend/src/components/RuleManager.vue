<script setup lang="ts">
/**
 * 规则管理组件
 *
 * 支持查看/添加/启停/删除行为规则
 * MVP 中使用 JSON 方式配置条件
 */
import { ref, onMounted } from 'vue'
import { useApi } from '@/composables/useApi'
import type { BehaviorRule, RuleCreateRequest } from '@/types'

const { getRules, createRule, deleteRule, toggleRule } = useApi()

const rules = ref<BehaviorRule[]>([])
const showForm = ref(false)
const newRule = ref<RuleCreateRequest>({
  ruleName: '',
  conditionJson: '{"using_phone": true, "duration_sec": {">": 10}}',
  outputState: '分心',
})

async function loadRules() {
  rules.value = await getRules()
}

async function handleCreate() {
  const result = await createRule(newRule.value)
  if (result) {
    showForm.value = false
    newRule.value = {
      ruleName: '',
      conditionJson: '{"using_phone": true, "duration_sec": {">": 10}}',
      outputState: '分心',
    }
    await loadRules()
  }
}

async function handleDelete(id: number) {
  const ok = await deleteRule(id)
  if (ok) await loadRules()
}

async function handleToggle(rule: BehaviorRule) {
  const ok = await toggleRule(rule.id, !rule.enabled)
  if (ok) await loadRules()
}

onMounted(loadRules)
</script>

<template>
  <div class="card">
    <div class="card-header">
      <span class="card-title">行为规则</span>
      <button
        class="btn btn-sm"
        :class="showForm ? 'btn-danger' : 'btn-primary'"
        @click="showForm = !showForm"
      >
        {{ showForm ? '取消' : '+ 添加' }}
      </button>
    </div>

    <!-- 添加规则表单 -->
    <div v-if="showForm" class="rule-form animate-slide-in">
      <input
        v-model="newRule.ruleName"
        class="input"
        placeholder="规则名称，如 phone_distraction_10s"
      />
      <textarea
        v-model="newRule.conditionJson"
        class="input rule-textarea"
        placeholder='JSON 条件，如 {"using_phone": true}'
        rows="3"
      />
      <div class="form-row">
        <select v-model="newRule.outputState" class="input">
          <option value="专注">专注</option>
          <option value="分心">分心</option>
          <option value="低效">低效</option>
          <option value="离开">离开</option>
        </select>
        <button class="btn btn-primary" @click="handleCreate">
          保存规则
        </button>
      </div>
    </div>

    <!-- 规则列表 -->
    <div class="rule-list">
      <div
        v-for="rule in rules"
        :key="rule.id"
        class="rule-item"
        :class="{ disabled: !rule.enabled }"
      >
        <div class="rule-info">
          <div class="rule-name data-readout">
            <span class="value">{{ rule.ruleName }}</span>
          </div>
          <div class="rule-meta">
            <span :class="['tag', rule.enabled ? 'tag-enabled' : 'tag-disabled']">
              {{ rule.enabled ? 'ON' : 'OFF' }}
            </span>
            <span class="tag tag-output">
              → {{ rule.outputState }}
            </span>
          </div>
        </div>
        <div class="rule-actions">
          <button
            class="btn btn-sm"
            @click="handleToggle(rule)"
          >
            {{ rule.enabled ? '停用' : '启用' }}
          </button>
          <button
            class="btn btn-sm btn-danger"
            @click="handleDelete(rule.id)"
          >
            删除
          </button>
        </div>
      </div>

      <div v-if="rules.length === 0" class="no-rules data-readout">
        暂无自定义规则，使用系统默认规则
      </div>
    </div>
  </div>
</template>

<style scoped>
.rule-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  margin-bottom: var(--space-4);
  padding-bottom: var(--space-4);
  border-bottom: 1px solid var(--color-neutral-200);
}

.rule-textarea {
  resize: vertical;
  min-height: 60px;
}

.form-row {
  display: flex;
  gap: var(--space-2);
}

.form-row select {
  flex: 1;
}

.rule-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  max-height: 300px;
  overflow-y: auto;
}

.rule-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-3);
  background: var(--color-bg-body);
  border: 1px solid var(--color-neutral-200);
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
}

.rule-item:hover {
  border-color: var(--color-neutral-300);
}

.rule-item.disabled {
  opacity: 0.5;
}

.rule-info {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.rule-name {
  font-size: var(--text-sm);
  font-weight: 600;
}

.rule-meta {
  display: flex;
  gap: var(--space-2);
}

.rule-actions {
  display: flex;
  gap: var(--space-1);
}

.no-rules {
  text-align: center;
  padding: var(--space-6);
  color: var(--color-neutral-500);
}

.tag-output {
  border-color: var(--color-neutral-300);
  color: var(--color-neutral-900);
}
</style>
