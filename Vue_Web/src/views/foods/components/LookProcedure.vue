<template>
    <div label-width="80px">
        <div v-html="rawHtml"></div>
        <div class="dialong__button--wrap">
            <el-button @click="close">关闭</el-button>
        </div>
    </div>
</template>
<script setup lang="ts">
import { ref } from 'vue'
const emit = defineEmits(['closeProcedure','success'])
const props = defineProps(['foodInfo'])
const foodInfo = ref(props.foodInfo)
const rawHtml = ref(foodInfo.value['foodprocedure']);
// 关闭视频
const close = ()=> {
    emit('closeProcedure')
}
</script>
<style scoped>
.dialong__button--wrap {
    text-align: center;
    margin-top: 20px;
}
</style>
  