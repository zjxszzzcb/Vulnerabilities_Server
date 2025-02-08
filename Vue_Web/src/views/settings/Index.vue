<template>
<el-row :gutter="24">
  <el-col :span="24"> 
     <div class="left_box">
       <h3 class="title">
         <el-icon style="margin-right: 10px;">
           <User />
         </el-icon>
         系统设置
       </h3>
       <!--基本设置 start-->
        <div class="set">
          <h4>数据库配置</h4>
            <el-row :gutter="24">
            <!--备份数据库-->
            <el-col :span="3">
              <el-button plain color="#2fa7b9"  style="margin-left: 50px;" @click="backupsdb">
                  备份数据库文件
                </el-button>
            </el-col>
            <!--选择备份数据库-->
            <el-col :span="8">
              <el-form-item label="备份数据库">
                <el-select v-model="dbvalue" placeholder="请选择备份数据库文件" style="width: 100%;">
                  <el-option v-for="item in dbnames" :key="item" :label="item" :value="item"/>
                </el-select>
              </el-form-item>
            </el-col>
            <!--备份数据库-->
            <el-col :span="3">
              <el-button plain color="#2fa7b9"  style="margin-left: 50px;" @click="downbackupsdb">
                  下载备份数据库文件
                </el-button>
            </el-col>
            <!--备份数据库-->
            <el-col :span="3">
              <el-button plain color="#2fa7b9"  style="margin-left: 50px;" @click="deletebackupsdb">
                  删除备份数据库文件
                </el-button>
            </el-col>
            </el-row>
        </div>
       <!--基本设置 end-->
       <el-divider border-style="dashed" />
       <!--Ping start-->
       <PingAdder/>
       <!--Ping end-->
     </div>
  </el-col>
</el-row>
</template>

<script setup lang="ts">
import { onMounted,ref,reactive, computed} from 'vue'
import PingAdder from "./components/PingAdder.vue";
import { ElMessage } from 'element-plus';
import { getBackupsDbApi, backupsDbApi, downBackupsDbApi, deleteBackupsDbApi } from "../../api/settings/settings";

// 定义备份数据库下拉选择项
const dbnames = ref<object[]>([])
// 获取数据库名
const dbvalue = ref();
// 备份数据库
const backupsdb = async () => {
  const { data } = await backupsDbApi();
  if(data.code===200){
    ElMessage.success(data.message)
    getBackupsDb()
  }else {
    ElMessage.error(data.message)
  }
}
// 获取备份列表数据
async function getBackupsDb() {
  try {
    const { data } = await getBackupsDbApi("./static/backupdb/")
    if (data.code == 200) {
      dbnames.value = data.result
    }
  } catch (e) {
      console.log(e)
  }
}

// 下载备份数据库
const downbackupsdb = async () => {
  try {
    let index = dbnames.value.indexOf(dbvalue.value);
    if (index < 0) {
      ElMessage.error("您选择的元素不存在")
      return
    }
    await downBackupsDbApi(dbvalue.value);
  } catch (e) {
      console.log(e)
  }
}
// 删除备份数据库
const deletebackupsdb = async () => {
  try {
    let index = dbnames.value.indexOf(dbvalue.value);
    if (index < 0) {
      ElMessage.error("您选择的元素不存在")
      return
    }
    const { data } = await deleteBackupsDbApi(dbvalue.value);
    if(data.code===200){
      ElMessage.success(data.message)
      getBackupsDb()
    }else {
      ElMessage.error(data.message)
    }
  } catch (e) {
    console.log(e)
  }
}
getBackupsDb()
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
</style>
