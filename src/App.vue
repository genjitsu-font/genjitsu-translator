<script setup lang="ts">
import { ref } from 'vue'
import YHNTransrator from './components/YHNTransrator.vue'

const randomText = [
  'おかえり ヨハネ',
  'ぬまづ駅',
  'じゃまつ軌道',
  'シュリーレン',
  'マリ様',
]

const text = ref('')

text.value = randomText[Math.floor(Math.random() * randomText.length)]
</script>

<template>
  <div class="container">
    <div class="row justify-content-center my-5">
      <div class="col-lg-6 text-center">
        <h1 class="fw-bold mb-3">現実→幻日変換</h1>
        <textarea v-model="text" rows="2" class="form-control mb-3" />
        <YHNTransrator :text="text" :conversion-table="{}" />
      </div>
    </div>
    <div class="row my-3 justify-content-center">
      <div class="col-lg-6">
        <h4 class="fw-bold">注意事項</h4>
        <ul>
          <li>このツールは公式ではありませんし、公式に教える必要もありません</li>
          <li>データが正しいかどうかは保証できません(一部未出文字については創作)</li>
          <li>権利者とのトラブルを避けるため、直接の画像データの利用はお控えください</li>
        </ul>
      </div>
    </div>
    <div class="row">
      <div class="col text-center">
        &copy; 2023 windyakin
      </div>
    </div>
  </div>
</template>
