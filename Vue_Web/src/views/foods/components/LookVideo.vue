<template>
    <div :model="formFood" label-width="80px">
        <div style="text-align: center;">
            <video controls style="width: 100%;" :poster="url+formFood.foodicon" :src="url+formFood.video" type="video/mp4">您的浏览器不支持视频标签
            </video>
        </div>
        <div class="dialong__button--wrap">
            <el-button @click="close">关闭</el-button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { reactive,ref } from 'vue'
const emit = defineEmits(['closeLookVideoForm','success'])
const props = defineProps(['foodInfo'])
const foodInfo = ref(props.foodInfo)
const formFood:any = reactive({
    id: 0,
    foodname: '',
    video: '',
    foodicon: '',
})

// 给表单填充数据
for (const key in formFood) {
    formFood[key] = foodInfo.value[key]
}
const url = import.meta.env.VITE_APP_BASE_API
// 关闭视频
const close = ()=> {
    emit('closeLookVideoForm')
}
</script>

<style scoped>
.dialong__button--wrap {
    text-align: center;
    margin-top: 20px;
}
</style>  