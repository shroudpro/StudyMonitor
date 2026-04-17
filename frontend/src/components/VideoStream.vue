<script setup lang="ts">
/**
 * 视频流展示组件
 *
 * 通过 WebSocket 接收后端推送的标注帧，显示实时摄像头画面
 */
defineProps<{
  frame: string
  isConnected: boolean
}>()

const emit = defineEmits<{
  startCamera: []
}>()
</script>

<template>
  <div class="card">
    <div class="card-header">
      <span class="card-title">实时监测画面</span>
      <span v-if="isConnected" class="data-readout">
        <span class="value">LIVE</span>
      </span>
    </div>

    <div class="video-container">
      <!-- 有视频帧时显示 -->
      <img
        v-if="frame"
        :src="'data:image/jpeg;base64,' + frame"
        alt="实时检测画面"
      />

      <!-- 无视频帧时显示占位 -->
      <div v-else class="video-placeholder">
        <span class="video-placeholder-icon">⎚</span>
        <span class="data-readout">等待摄像头连接...</span>
        <button
          class="btn btn-primary"
          @click="emit('startCamera')"
        >
          启动检测
        </button>
      </div>

      <!-- 视频底部覆盖层 -->
      <div v-if="frame" class="video-overlay">
        <span class="data-readout">
          <span class="value">640×480</span>
          <span class="unit"> @ 15fps</span>
        </span>
      </div>
    </div>
  </div>
</template>
