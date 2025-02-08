<template>
  <el-card class="box-card">
    <!--头部 start-->
    <template #header>
      <div class="card-header">
        <h3>
          <el-icon style="margin-right: 10px;"><FoodFilled /></el-icon>菜品管理
        </h3>
  
        <!--搜索区域 start-->
         <div class="card-search">
            <el-row :gutter="10">
              <el-col :span="10">
                <el-input :prefix-icon="Search" v-model="searchValue" @keyup.enter.native="search" placeholder="菜品名搜索（回车）"/>
              </el-col>
              <el-col :span="11">
                <div class="my-button">
                  <el-button plain style="width: 40%;" color="#2fa7b9" @click="addFood">添加菜品</el-button>
                  <el-button @click="exportExcelAction" type="primary">
                    <el-icon style="margin-right: 6px"><Download /></el-icon>导出 Excel
                  </el-button>
                </div>
              </el-col>
              <el-col :span="3" style="display: inline-flex;justify-content: center;align-items: center; cursor: pointer;">
                <el-icon style="font-size: 20px;color: #b3b6bc;" @click="refresh">
                  <Refresh />
                </el-icon>
              </el-col>
            </el-row>
         </div>
        <!--搜索区域 end-->
      </div>
    </template>
    <!--头部 end-->
    <!--表格区域 start-->
    <div class="table-box">
      <el-table element-loading-text="数据加载中..." v-loading="loading" :data="tableData"
      style="width: 100%;text-align: center" :cell-style="{textAlign: 'center'}"
      :header-cell-style="{fontSize: '15px', background: '#178557',color: 'white',textAlign: 'center'}">
  
        <el-table-column label="序号" width="100" type="index" :index="Nindex"/>
        <el-table-column label="菜品名称">
          <template #default="scope">
            <el-tooltip :content="scope.row.foodname" palacement="top" effect="light">
              <span class="highlight">{{scope.row.foodname}}</span>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column label="菜品图片">
          <template #default="scope">
              <img v-if="scope.row.foodicon" :src="url+scope.row.foodicon" style="width: 40px;"/>
              <img v-else  src="../../assets/default_food.png" style="width: 40px;"/>
          </template>
       </el-table-column>
        <el-table-column label="用户名称">
          <template #default="scope">
              <span class="highlight">{{scope.row.user}}</span>
          </template>
        </el-table-column>
        <el-table-column label="步骤">
          <template #default="scope">
            <el-button @click="openprocedure(scope.row.id)" type="primary">
              <el-icon style="margin-right: 6px"><KnifeFork/></el-icon>查看步骤
            </el-button>
          </template>
        </el-table-column>
        <el-table-column label="视频">
          <template #default="scope">
            <el-button v-if="scope.row.video" @click="openlookVideo(scope.row.id)" type="primary">
              <el-icon style="margin-right: 6px"><VideoPlay/></el-icon>播放视频
            </el-button>
            <el-button v-else disabled>
              <el-icon style="margin-right: 6px"><VideoPlay/></el-icon>没有视频
            </el-button>
          </template>
        </el-table-column>
        <el-table-column label="价格">
          <template #default="scope">
            <el-tooltip :content="scope.row.price" palacement="top" effect="light">
              <span class="highlight">{{scope.row.price}}</span>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column label="创建时间">
          <template #default="scope">
            <el-tooltip :content="scope.row.created_at" placement="top" effect="light">
              <span class="highlight">{{formatTime(scope.row.created_at, 'yyyy-MM-dd')}}</span>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column label="更新时间">
          <template #default="scope">
            <el-tooltip :content="scope.row.updated_at" placement="top" effect="light">
              <span class="highlight">{{formatTime(scope.row.updated_at, 'yyyy-MM-dd')}}</span>
            </el-tooltip>
          </template>
        </el-table-column>
  
        <el-table-column label="操作">
          <template #default="scope">
            <el-button size="small"
                       style="margin: 0 0 10px 10px;" @click="editFood(scope.row.id)">编辑</el-button>
            <el-popconfirm confirm-button-text="确定" cancel-button-text="取消" :icon="Delete"
                           icon-color="#626AEF" :title="'确定删除菜品名为“'+scope.row.foodname+'”的菜品吗？'"
                           @confirm="delFood(scope.row.id)">
              <template #reference>
                <el-button size="small" type="danger" style="margin-bottom: 10px;">删除</el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
  
      </el-table>
  
      <!--分页 start-->
      <el-pagination background layout="total, sizes, prev, pager, next, jumper" :total="total"
                     v-model:page-size="pageSize"
                     @current-change="changePage"
                     :page-sizes="[10,30,50,100]"/>
      <!--分页 end-->
    </div>
    <!--表格区域 end-->
  </el-card>
  
    <!--新增菜品弹出框 start-->
    <el-dialog  align-center  v-model="foodDialogFormVisible" width="42%" destroy-on-close>
      <template #header="{ close, titleId, titleClass }">
        <div class="my-header">
          <el-icon size="26px"><EditPen /></el-icon>
          <h1 id="titleId">{{title}}</h1>
        </div>
      </template>
      <!--添加菜品组件 start-->
      <AddFood @closeAddFoodForm="closeAddFoodForm" @success="success"/>
      <!--添加菜品组件 end-->
    </el-dialog>
    <!--新增菜品弹出框 end-->
  
    <!--编辑菜品弹出框 start-->
    <el-dialog  align-center v-model="editFoodDialogFormVisible" width="42%" destroy-on-close>
      <template #header="{ close, titleId, titleClass }">
        <div class="my-header">
          <el-icon size="26px"><EditPen /></el-icon>
          <h1 id="titleId">{{editTitle}}</h1>
        </div>
      </template>
      <!--编辑菜品组件 start-->
      <EditFood :foodInfo="foodInfo" @closeEditFoodForm="closeEditFoodForm" @success="success"/>
      <!--编辑菜品组件 end-->
    </el-dialog>
    <!--编辑菜品弹出框 end-->
    
    <!-- 添加视频弹窗 start -->
    <el-dialog align-center v-model="showVideo" width="50%" destroy-on-close>
      <template #header="{ close, titleId, titleClass }">
        <div class="my-header">
          <el-icon size="26px"><EditPen/></el-icon>
          <h1 id="titleId">{{lookvideo}}</h1>
        </div>
      </template>
      <!--添加视频组件 start-->
      <LookVideo :foodInfo="foodInfo" @closeLookVideoForm="closeLookVideoForm"/>
      <!--添加视频组件 end-->
    </el-dialog>
    <!-- 添加视频弹窗 end -->
  
    <!-- 添加步骤弹窗 start -->
    <el-dialog align-center v-model="showProcedure" width="50%" destroy-on-close>
      <template #header="{ close, titleId, titleClass }">
        <div class="my-header">
          <el-icon size="26px"><EditPen/></el-icon>
          <h1 id="titleId">{{lookprocedure}}</h1>
        </div>
      </template>
      <!--添加步骤组件 start-->
      <LookProcedure :foodInfo="foodInfo" @closeProcedure="closeProcedure"/>
      <!--添加步骤组件 end-->
    </el-dialog>
    <!-- 添加步骤弹窗 end -->
  </template>

<script setup lang="ts">
import { onMounted,reactive,toRefs,ref } from 'vue'
import {Search, Delete} from '@element-plus/icons-vue'
import {ElMessage} from 'element-plus'
import {deleteFoodApi, getFoodApi, getFoodListApi} from "../../api/food/food"
import { formatTime } from "../../utils/date"
import AddFood from './components/AddFood.vue'
import EditFood from './components/EditFood.vue'
import LookVideo from './components/LookVideo.vue'
import LookProcedure from './components/LookProcedure.vue'
import { exportExcel } from '../../utils/exprotExcel'


// 添加视频弹框
const showVideo = ref(false);
const lookvideo = ref('查看视频')

// 添加做菜步骤弹框
const showProcedure = ref(false);
const lookprocedure = ref('查看步骤')

// 添加菜品弹窗状态
const foodDialogFormVisible = ref(false)
const title = ref('新增菜品')
// 编辑菜品弹窗状态
const editFoodDialogFormVisible = ref(false)
const editTitle = ref('编辑菜品')

const state = reactive({
  // 搜索表单内容
  searchValue: "",
  // 表格全部信息
  tableData: [],
  // 当前点击的编辑信息
  foodInfo:null,
  total: 0, //总条数
  pageSize: 10, //每页显示行数
  pageIndex: 1, //当前页码
  loading: false, // 数据加载
})

// 获取食物菜单数据
const loadData = async (state: any)=> {
  state.loading = true
  // 先清空数据
  state.tableData=[]
  const params = {
    'page':state.pageIndex,
    'size': state.pageSize,
    'keyword': state.searchValue
  }
  const { data } = await getFoodListApi(params)
  state.tableData = data.result.list
  state.total = data.result.count
  state.loading = false
}
// 分页序号不乱
const Nindex = (index:any) => {
  // 当前页数 - 1 * 每页数据条数 + 1
  const page = state.pageIndex // 当前页码
  const pagesize = state.pageSize // 每页条数
  return index + 1 + (page - 1) * pagesize
}
// 刷新按钮
const refresh = () => {
  // 搜索表单内容
  state.searchValue = ""
  // 更新数据
  loadData(state);
}
// 搜索
const search = () => {
  if (state.searchValue !== null) {
    ElMessage({
      type: 'success',
      message: `关键字“${state.searchValue}”搜索内容如下`,
    })
    loadData(state)
  }
}
// 切换页面的执行事件，  val 当前页码
const changePage = (val:any) => {
  state.pageIndex = val
  loadData(state)
}

const foodInfo = ref()
// 打开视频
const openlookVideo = async (id:number)=> {
  const { data } = await getFoodApi(id)
  foodInfo.value = data.result
  showVideo.value = true
}
// 打开做菜步骤
const openprocedure = async (id:number)=> {
  const { data } = await getFoodApi(id)
  foodInfo.value = data.result
  showProcedure.value = true
}
// 编辑菜品信息
const editFood = async (id:number)=> {
  const { data } = await getFoodApi(id)
  foodInfo.value = data.result
  editFoodDialogFormVisible.value = true
}
// 添加菜品
const addFood = ()=> {
  foodDialogFormVisible.value = true
}

// 关闭新增视频弹出框
const closeLookVideoForm = ()=> {
  showVideo.value = false
}
// 关闭新增菜品弹出框
const closeProcedure = ()=> {
  showProcedure.value = false
}
// 关闭编辑菜品弹出框
const closeEditFoodForm = ()=> {
  editFoodDialogFormVisible.value = false
}
// 关闭新增菜品弹出框
const closeAddFoodForm = ()=> {
  foodDialogFormVisible.value = false
}

// 提交表单回调函数
const success = ()=> {
  loadData(state);
  foodDialogFormVisible.value = false
  editFoodDialogFormVisible.value = false
}

// 删除菜品信息
const delFood = async (id:number)=> {
  const { data } = await deleteFoodApi(id)
  if(data.code===200){
    ElMessage.success('删除成功')
    await loadData(state);
  }else {
    ElMessage.error(data.message)
  }
}
const column = [
  {name: 'id',label: '菜品id'},
  {name: 'foodname',label: '菜品名称'},
  {name: 'user',label: '用户名'},
  {name: 'price',label: '价格'},
  {name: 'remarks',label: '备注'}
]
const exportExcelAction = () => {
  exportExcel({
    column,
    data:state.tableData,
    filename: '菜品信息数据',
    format: 'xlsx',
    autoWidth: true,
  })
}

//挂载后加载数据
onMounted(() => {
  loadData(state);
})

// 服务器路径
const url = import.meta.env.VITE_APP_BASE_API

const {tableData,pageSize,loading,total,searchValue} = toRefs(state)
</script>

<style scoped>
.card-header {
  display: flex; /* 弹性布局 */
  justify-content: space-between; /*内容对齐方式 */
  align-items: center; /*设置或检索弹性盒子元素在侧轴（纵轴）方向上的对齐方式*/
}
.card-header h3 {
  display: inline-flex; /*行内块元素*/
  justify-content: center;
  align-items: center;
}

:deep(.el-card__header) {
  border-bottom: 1px solid rgb(238 238 238);
  color: #178557;
}

.text {
  font-size: 14px;
}

.item {
  margin-bottom: 18px;
}

.el-card {
  border-radius: 0px;
  border: none;
}

/*分页样式*/
:deep(.el-pagination.is-background .el-pager li:not(.is-disabled).is-active) {
  background-color: #178557;
}

.el-pagination {
  margin-top: 20px;
  justify-content: center;
}

/*新增用户弹出框自定义头部样式*/
.my-header {
  display: flex;
  justify-content: flex-start;
}
/*自定义按钮样式*/
.my-button {
  display: flex;
  justify-content:space-between;
}

/*修改v-loading样式*/
:deep(.el-loading-spinner .el-loading-text){
  color: #178557;
}
:deep(.el-loading-spinner .path){
  stroke: #178557;
}
</style>