<template>

  <el-form ref="ruleFormRef" :rules="rules"  :model="formUser"  label-width="80px">
    <el-row>
      <el-col :span="24">
        <el-form-item prop="role" label="所属角色">
          <el-select v-model="formUser.role_id" placeholder="请选择角色" style="width: 100%;">
            <el-option v-for="item in roleOptions" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
      </el-col>
    <el-col :span="12">
    <el-form-item label="用户名" prop="username">
      <el-input v-model="formUser.username" placeholder="请输入用户名" />
    </el-form-item>
    </el-col>
    <el-col :span="12">
    <el-form-item label="登录密码" prop="password">
      <el-input v-model="formUser.password" placeholder="请输入密码" />
    </el-form-item>
    </el-col>
      <el-col :span="12">
    <el-form-item label="电话" prop="phone">
      <el-input v-model="formUser.phone" placeholder="请输入电话" />
    </el-form-item>
      </el-col>
      <el-col :span="12">
    <el-form-item label="联系邮箱" prop="email">
      <el-input v-model="formUser.email" placeholder="请输入联系邮箱" />
    </el-form-item>
      </el-col>
      <el-col :span="12">
    <el-form-item label="性别" prop="sex">
      <el-radio-group v-model="formUser.sex" fill="#178557">
        <el-radio-button label="男" />
        <el-radio-button label="女" />
      </el-radio-group>
    </el-form-item>
      </el-col>
      <el-col :span="12">
    <el-form-item label="状态" prop="status">
      <el-radio-group v-model="formUser.status" fill="#178557">
        <el-radio :value=true>正常</el-radio>
        <el-radio :value=false>封禁</el-radio>
      </el-radio-group>
    </el-form-item>
      </el-col>

      <el-col :span="24">
        <el-form-item label="备注">
          <el-input
              v-model="formUser.remarks"
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
    <el-button color="#178557" :loading="subLoading" type="success" @click="editUser(ruleFormRef)">保存</el-button>
  </div>
</template>

<script setup lang="ts">
import { reactive,ref } from 'vue'
import { ElMessage } from 'element-plus'
import { editUserApi, getAllRoleListApi} from "../../../api/user/user"
import type { FormInstance, FormRules } from 'element-plus'
import JSEncrypt from "jsencrypt";
const emit = defineEmits(['closeEditUserForm','success'])
// RSA 私钥
const privateKey = `-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAsSOjJck8DhR/j6sFCBH/Sw8dXkd9CjKxnNFjMTEWYWx39a5Z
O5uvhWV6ps4/+yZEZPgw0EaBV0gSwpLBs4eC+5EFBArDp0qdf38KRN++oR5MJMGW
DXAJKBcKHall0/TvnZ7ATbhc3M9EN+5Mi/MGTOOHVs0wP61NVnf3KR9DjxhD/ddv
GKNZkc5Ivds0CHPzUX4bLUppa0NeyA2YIVIyTxloBQeR9dnq9C3yB0iBDdYb1H2z
OfaUOGYIS5Xpu5PlL5BPfxH2utS2MzehD6l2yu1RktVGFx0Ij3cVUfMMh03RfMCY
jcoCALxuhZzWqvmp1KSqrQEx6hX0D91ALsGlQwIDAQABAoIBACpfiP5X9eq0UpNO
aKS2kWgmFHNiDHItEDmgCOdSg7UIWmXFsAjHRCRX0xAl1D5CuCejCyI3S2dSkVJE
AtvsNZPx6848uPLCsYw3GoDBOPuXoMVGHZvXSglyAXR4+ifKtqrwt7WfvW8AkaQD
eAIeP0qTPuOvr7P7w71EczY+CU4oLOhdpi1CWLEMZ7xLBIwBy2I8FCgw3ZeKa00c
Rs4YdoQLiKk54AwbfBCYRtIkIM4iVYnGDl5ZnO4OpT+xinmk+Ia8VaDGxqjFfyPN
rHBbJw08xh5PRQTrIOdESNR8IuBgSAwl8GcMawko/OelJI34vxg8FuY5f1xKOdO5
DTEB7JkCgYEAzzKE0KrAZYVq8Dn8Due9V9VeaNH5/vun1gFyjFTHi1DXW343UwR/
pYbZEj7MM7F8iaDNzJ1js7p9IGLO2z/1dXhxNQfr5Pett/01moweCCrdVDbXhV4B
58IdJfYNCjlSrJkkYkxv0u9+8Nos5u8P1fqc0iaCsBczSwAs8Ormd5cCgYEA2tyw
OlimQb0KawFWICFo7+igd0m12+/PviYXj6N32M6CYFFoH59vM/gpIvTe0eNP7PXa
dB4mXJ5yBWD3nkMxUZ/i/OxbO0vHraKzff9YsHGXUvVBSXK9M+8eMxTyWSuF24us
2/PWnUylqB3PM03lRT6/u1sAdx1v4JlqPZAQlTUCgYEAl6sOR8TGI0pfdkurs6l1
E2dvvWD/E+RY/jF/DTQ+AUAC9MlWbCGd4qfsHAv15F0moYQhQYdwZS68y0kozJtr
7Tpl/AC5b5jSBB2I8IFitm3SKAQhDVI8KM8SESikcPh3CTrsxDvZm1mO3XWHauBS
Ajt6MebYwVeqR1twikYYwC8CgYASyA13dFQQICDcveieKT/QFq5ujizFCvdQ4gPz
l5uZR1941IOS8yOf2hPtpAXbDR62vwJYJJ42JIK0Y3XcZve8gXQBMGdD12TzSZsN
nPQHcDgELnfDzczewA5fY9TIQivig0H6PhqUtRciLiyxwmWCY7ggY9bOYgBPzdqI
HezOYQKBgD9/MgHvtEF75U7YARLa1GkPvgj2TvGlqztVu+7LKsrBR07VRVAPkc0L
mhrDYvNaM0zWew1FbHDTXpZ0qGvvo/ERZBCufF4m8Wv0XD22/mZ5aTj6fqP/7KTi
nyiHT609ZvZmcvLkOfG1TMQZKYnPLp2mkqoSSewZeLlM+0I+aeSQ
-----END RSA PRIVATE KEY-----`;
const props = defineProps(['userInfo'])
const userInfo = ref(props.userInfo)

const subLoading = ref(false)
const ruleFormRef = ref<FormInstance>()
const formUser = reactive({
  id: 0,
  username: '',
  password: '',
  status: false,
  phone: '',
  email: '',
  sex: '男',
  remarks: '',
  role_id: null,
})
// 给表单填充数据
for (const key in formUser) {
  if (key == 'username' || key == 'password' || key == 'phone' || key == 'email') {
    formUser[key] = rsardecrypt(userInfo.value[key])
  }else{
    formUser[key] = userInfo.value[key]
  }
}
// 定义表单约束规则对象
const rules = reactive<FormRules>({
  username: [{ required: true, message: '用户名不能为空', trigger: 'blur' }],
  password: [{ required: true, message: '登录密码不能为空', trigger: 'blur' }],
  sysRole: [{ required: true, message: '角色不能为空', trigger: 'blur' }]
})

// 编辑用户信息
const editUser = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  await formEl.validate(async (valid, fields) => {
    subLoading.value = true
    if (valid) {
      const { data } =  await editUserApi(formUser)
      if(data.code===200){
        ElMessage.success(data.message)
        emit('success')
      }else {
        ElMessage.error(data.message)
      }
    } else {
      ElMessage.error('提交失败，你还有未填写的项！')
      console.log('error submit!', fields)
    }
    subLoading.value = false
  })
}

// 定义角色下拉选择项
const roleOptions = ref<object[]>([])
// 获取所有角色列表
async function getAllRoleList() {
  try {
    const { data } = await getAllRoleListApi()
    if (data.code === 200) {
      roleOptions.value = data.result.list
    }
  } catch (e) {
    console.log(e)
  }
}
getAllRoleList()

// 取消表单
const close = ()=> {
  emit('closeEditUserForm')
}

// Base64解码后使用私钥解密
function rsardecrypt(_0x4ebec0){
  const _0xe593=['decrypt','setPrivateKey'];
  const _0x41f9=function(_0xe5934,_0x41f902){
    _0xe5934=_0xe5934-0x0;
    let _0x262c0f=_0xe593[_0xe5934];
    return _0x262c0f;
  };
  const _0x3964bb=new JSEncrypt();
  _0x3964bb[_0x41f9('0x1')](privateKey);
  return _0x3964bb[_0x41f9('0x0')](_0x4ebec0)||'';
}


</script>

<style scoped>
.dialong__button--wrap {
  text-align: center;
  margin-top: 20px;
}
</style>
