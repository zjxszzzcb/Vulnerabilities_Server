<template>
<el-row :gutter="20">
  <!--左侧信息 start-->
  <el-col :span="18">
     <div class="left_box">
       <h3 class="title">
         <el-icon style="margin-right: 10px;">
           <User />
         </el-icon>
         个人信息设置
       </h3>

       <!--基本设置 start-->
        <div class="set">
          <h4>基础设置</h4>
          <el-form ref="basicFormRef" :rules="basicRules" status-icon :model="basic">
            <el-row :gutter="20">
            <!--用户名-->
            <el-col :span="8">
                <el-form-item prop="username" label="用户名" style="width: 100%;">
                  <el-input v-model="basic.username" placeholder="请输入用户姓名"/>
                </el-form-item>
            </el-col>
            <!--用户性别-->
            <el-col :span="8">
              <el-form-item prop="sex" label="性别" style="width: 100%;">
                  <el-radio v-model="basic.sex" value="男" size="large">男</el-radio>
                  <el-radio v-model="basic.sex" value="女" size="large">女</el-radio>
              </el-form-item>
            </el-col>
            <!--头像-->
            <el-col :span="5">
              <el-form-item label="头像：" style="margin: auto;">
                <el-upload ref="uploadavatar" class="avatar-uploader" name="file" :loading="loading" :show-file-list="false" :on-change="fileChange" :http-request="uploadFile" :limit="1">
                  <img v-if="basic.avatar" :src="url+basic.avatar"
                       style="width: 50px;border-radius: 50px;" />
                  <img v-else src="../../assets/default_avatar.png"
                       style="width: 50px;border-radius: 50px;" />
                  <span style="margin-left: 10px; font-size: 10px; text-decoration: underline;line-height: 20px;">点击更换</span>
                </el-upload>
              </el-form-item>
            </el-col>

            <el-col :span="3">
              <el-form-item>
                <el-button :loading="loading" plain color="#2fa7b9"  style="margin-left: 50px;" @click="onBasicSubmit(basicFormRef)">
                  提交
                </el-button>
              </el-form-item>
            </el-col>
            </el-row>
          </el-form>
        </div>
       <!--基本设置 end-->
       <el-divider border-style="dashed" />
       <!--修改密码 start-->
        <UpdatePwd/>
       <!--修改密码 end-->
     </div>
  </el-col>
  <!--左侧信息 end-->
  <!--右侧个人信息 start-->
  <UserInfo/>
  <!--右侧个人信息 end-->
</el-row>
</template>

<script setup lang="ts">
import {ref,reactive,toRefs,onMounted,computed } from 'vue'
import { useUserStore } from '../../store/modules/user'
import { ElMessage } from 'element-plus'
import { UploadRequestOptions } from "element-plus/lib/components";
import type { FormInstance } from 'element-plus'
import { updateInfoApi, upuseravatar } from "../../api/usersettings/usersettings";
import UpdatePwd from "./components/UpdatePwd.vue"
import UserInfo from "./components/UserInfo.vue"
const loading = ref(false)
const basicFormRef = ref<FormInstance>()
const state = reactive({
  // 基本信息
  basic: {
    id: 0,
    username: '',
    sex: '',
    avatar: ''
  }
})

// 校验基础信息
const basicRules = reactive({
  username: [{ required: true, message: "请输入用户名", trigger: "blur" }],
  sex: [{ required: true, message: "请输入性别", trigger: "blur" }],
  avatar: [{ required: true, message: "请输入头像", trigger: "blur" }],
})

// 服务器路径
const url = import.meta.env.VITE_APP_BASE_API
// 用于设置浏览器文件对象
const uploadavatar = ref();
// 清除文件对象，关于上传第一次正常第二次没反应的问题
const fileChange = async () => {
  uploadavatar.value.clearFiles();
}
// 设置文件上传请求
const uploadFile = async (params: UploadRequestOptions) =>{
  if (!params) return
  loading.value = true
  // 判断上传文件类型
  if ((params.file.type !== 'image/jpeg') && (params.file.type !== 'image/png'))  {
    loading.value = false
    ElMessage.error('仅允许上传png或者jpg文件')
    return false
  } else if (params.file.size / 1024 / 1024 > 5) {
    // 图片大小
    ElMessage.error('不允许上传超过5MB文件')
    loading.value = false
    return false
  }
  let formData = new FormData();
  formData.append('file', params.file);
  
  const { data } = await upuseravatar(formData)
   if(data.code === 200){
    ElMessage({
      message: '头像上传成功~',
      type: 'success',
    })
    state.basic.avatar = data.result;
  }else{
    ElMessage({
      message: data.message,
      type: 'error',
    })
  }
  loading.value = false
}
// 提交基础信息
const userStore = useUserStore()
const onBasicSubmit = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.validate(async(valid) => {
    if (valid) {
      loading.value = true
      state.basic.id = userStore.userInfo.uid
      const { data } = await updateInfoApi({ ...state.basic });
      if(data.code===200){
        // 设置token
        userStore.setUserInfo({
          uid: state.basic.id,
          username: state.basic.username,
          sex: state.basic.sex,
          avatar: state.basic.avatar,
        })
        // 提示
        ElMessage({
          message: '基础信息修改成功~',
          type: 'success',
        })
        loading.value = false
      }else {
        // 提示
        ElMessage({
          message: data.message,
          type: 'error',
        })
        loading.value = false
      }
    } else {
      console.log('error submit!')
      return false
    }
  })
}
const { userInfo } = userStore
//挂载后加载数据
onMounted(() => {
  state.basic.id = userInfo.uid
  state.basic.username = userInfo.username
  state.basic.sex = userInfo.sex
  state.basic.avatar = userInfo.avatar
})
const {basic} = toRefs(state)
</script>

<style scoped>
.left_box {
  width: 100%;
  height: auto;
  background: white;
  padding: 20px;
  /* 添加此属性 padding间距不扩大div */
  box-sizing: border-box;
}
.left_box .title {
  color: #178557;
  margin-bottom: 10px;
  padding: 20px 20px;
  display: inline-flex;
  justify-content: center;
  align-items: center;
}
.left_box .set {
  text-align: left;
  padding: 0px 20px;
  margin-bottom: 10px;
  color: #8f8f8f;
  line-height: 35px;
}
.left_box .set h4 {
  line-height: 45px;
  color: #8f8f8f;
}
</style>: { raw: string | Blob; }: string | any[]
