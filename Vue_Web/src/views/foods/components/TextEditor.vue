<template>
    <div style="border: 1px solid;">
      <Toolbar
        style="border-bottom: 1px solid #ccc"
        :editor="editorRef"
        :defaultConfig="toolbarConfig"
      />
      <Editor
        style="height: 400px; overflow-y: hidden;"
        v-model="valueHtml"
        :defaultConfig="editorConfig"
        @onCreated="handleCreated"
      />
    </div>
</template>

<script setup lang="ts">
import '@wangeditor/editor/dist/css/style.css' // 引入 css
import { onBeforeUnmount, ref, shallowRef, onMounted,watchEffect,watch } from 'vue'
import { Editor, Toolbar } from '@wangeditor/editor-for-vue'

// 声明属性
const props = defineProps({
    modelValue: {
        type: String,
        default: "",
    }
})
// 声明事件消息
const emits = defineEmits<{
    (e: "update:modelValue", value: string): void
}>()

// 编辑器实例，必须用 shallowRef
const editorRef = shallowRef()

// 内容 HTML
const valueHtml = ref('<p>hello</p>')
// 当属性变化时，自动赋值给 valueHtml
watchEffect(() => {
    valueHtml.value = props.modelValue
})
// 当 valueHtml 变化时，自动赋值父组件
watch(valueHtml, (newHtml) => {
    emits("update:modelValue", newHtml)
})
// // 模拟 ajax 异步获取内容
// onMounted(() => {
//     setTimeout(() => {
//         valueHtml.value = '<p></p>'
//     }, 1500)
// })
// 配置
const toolbarConfig = {}
const editorConfig = { placeholder: '请输入内容...' }

// 组件销毁时，也及时销毁编辑器
onBeforeUnmount(() => {
    const editor = editorRef.value
    if (editor == null) return
    editor.destroy()
})

const handleCreated = (editor:any) => {
    editorRef.value = editor // 记录 editor 实例，重要！
}

</script>
