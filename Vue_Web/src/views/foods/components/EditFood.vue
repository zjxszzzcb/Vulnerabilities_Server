<template>
  <el-form ref="ruleFormRef" :rules="rules"  :model="formFood"  label-width="80px">
    <el-row>
      <el-col :span="12">
    <el-form-item label="菜品名" prop="foodname">
      <el-input v-model="formFood.foodname" placeholder="请输入菜品名" />
    </el-form-item>
    <el-form-item label="价格" prop="price">
      <el-input-number v-model="formFood.price" :precision="2" :step="1" :min="0" />
    </el-form-item>
    <el-form-item label="菜品图片" style="margin: auto;">
      <el-upload ref="upload1" class="icon-uploader" name="file" :show-file-list="false" :on-change="fileChange1" :http-request="uploadFile" :limit="1">
        <img v-if="formFood.foodicon" :src="url+formFood.foodicon" style="width: 70px;border-radius: 10px;" />
        <img v-else src="../../../assets/default_food.png" style="width: 70px;border-radius: 10px;border-style: dashed;border-width: 1px;border-color: #8c939d;" />
        <span style="margin-left: 10px; font-size: 10px; text-decoration: underline;line-height: 20px;">点击更换</span>
      </el-upload>
    </el-form-item>
    </el-col>
    <el-col :span="12">
      <el-form-item label="视频" prop="video">
        <el-upload ref="upload2" class="video-uploader" name="file" :show-file-list="true" :on-change="fileChange2" :http-request="uploadVideo" :limit="1" :auto-upload="true">
          <video v-if="formFood.video" :src="url+formFood.video" controls style="width: 240px; height:171px;"></video>
          <el-icon v-else style="width: 240px; height:171px; border-style: dashed; border-width: 1px; border-color: rgb(140, 147, 157);" class="avatar-uploader-icon"><Plus /></el-icon>
          <span style="margin-left: 10px; font-size: 10px; text-decoration: underline;line-height: 20px;">点击更换</span>
        </el-upload>
      </el-form-item>
    </el-col>
    <el-col :span="24">
        <el-form-item label="做菜步骤">
          <TextEditor v-model="formFood.foodprocedure"/>
        </el-form-item>
      </el-col>
    <el-col :span="24">
      <el-form-item label="备注">
        <el-input
            v-model="formFood.remarks"
            :rows="2"
            type="textarea"
            placeholder="请输入备注"
        />
      </el-form-item>
    </el-col>
    </el-row>
  </el-form>

  <div class="dialong__button--wrap">
    <el-button @click="close">取消</el-button>
    <el-button color="#178557" :loading="subLoading" type="success" @click="editFood(ruleFormRef)">保存</el-button>
  </div>
</template>

<script setup lang="ts">
import { reactive,ref } from 'vue'
import { ElMessage } from 'element-plus'
import { editFoodApi, upfoodicon, upfoodvideo } from "../../../api/food/food"
import type { FormInstance, FormRules } from 'element-plus'
import TextEditor from './TextEditor.vue'
import { UploadRequestOptions } from "element-plus/lib/components";

const emit = defineEmits(['closeEditFoodForm','success'])
const props = defineProps(['foodInfo'])
const foodInfo = ref(props.foodInfo)
const subLoading = ref(false)
const loading1 = ref(false)
const loading2 = ref(false)
const ruleFormRef = ref<FormInstance>()
const formFood:any = reactive({
  id: 0,
  foodname: '',
  foodprocedure: '',
  remarks: '',
  foodicon: '',
  video: '',
  price: ref(),
})
// 给表单填充数据
for (const key in formFood) {
  formFood[key] = foodInfo.value[key]
  
}
// 定义表单约束规则对象
const rules = reactive<FormRules>({
  foodname: [{ required: true, message: '菜品名不能为空', trigger: 'blur' }],
  foodprocedure: [{ required: true, message: '做菜步骤不能为空', trigger: 'blur' }],
})

// 编辑菜品信息
const editFood = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  await formEl.validate(async (valid, fields) => {
    subLoading.value = true
    if (valid) {
      const { data } =  await editFoodApi(formFood)
      if(data.code===200){
        ElMessage.success(data.message)
        emit('success')
      }else {
        ElMessage.error(data.message)
      }
    } else {
      ElMessage.error('提交失败，你还有未填写的项！')
    }
    subLoading.value = false
  })
}

// 取消表单
const close = ()=> {
  emit('closeEditFoodForm')
}
// 服务器路径
const url = import.meta.env.VITE_APP_BASE_API
// 食物icon
// 用于设置浏览器文件对象
const upload1 = ref();
// 清除文件对象，关于上传第一次正常第二次没反应的问题
const fileChange1 = async () => {
  upload1.value.clearFiles();
}
// 视频
// 用于设置浏览器文件对象
const upload2 = ref();
// 清除文件对象，关于上传第一次正常第二次没反应的问题
const fileChange2 = async () => {
  upload2.value.clearFiles();
}
// 设置文件上传请求
const uploadFile = async (params: UploadRequestOptions) =>{
  if (!params) return
  loading1.value = true
  // 判断上传文件类型
  if ((params.file.type !== 'image/jpeg') && (params.file.type !== 'image/png'))  {
    loading1.value = false
    ElMessage.error('仅允许上传png或者jpg文件')
    return false
  } else if (params.file.size / 1024 / 1024 > 5) {
    // 图片大小
    ElMessage.error('不允许上传超过5MB文件')
    loading1.value = false
    return false
  }
  let formData = new FormData();
  formData.append('file', params.file);
  
  const { data } = await upfoodicon(formData)
   if(data.code === 200){
    ElMessage({
      message: '图片上传成功~',
      type: 'success',
    })
    formFood.foodicon = data.result;
  }else{
    ElMessage({
      message: data.message,
      type: 'error',
    })
  }
  loading1.value = false
}
// 设置video文件上传请求
const uploadVideo = async (params: UploadRequestOptions) =>{
  if (!params) return
  loading2.value = true
  // 判断上传文件类型
  if ((params.file.type !== 'video/mp4') && (params.file.type !== 'video/flv') && (params.file.type !== 'video/avi'))  {
    loading2.value = false
    ElMessage.error('仅允许上传mp4/avi/flv文件')
    return false
  } else if (params.file.size / 1024 / 1024 > 20) {
    // 图片大小
    ElMessage.error('不允许上传超过20MB文件')
    loading2.value = false
    return false
  }
  let formData = new FormData();
  formData.append('file', params.file);
  
  const { data } = await upfoodvideo(formData)
   if(data.code === 200){
    ElMessage({
      message: '视频上传成功~',
      type: 'success',
    })
    formFood.video  = data.result;
  }else{
    ElMessage({
      message: data.message,
      type: 'error',
    })
  }
  loading2.value = false
}
</script>

<style scoped>
.dialong__button--wrap {
  text-align: center;
  margin-top: 20px;
}
</style>
