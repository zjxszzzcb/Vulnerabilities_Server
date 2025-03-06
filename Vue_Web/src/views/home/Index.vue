<template>
<div class="home">
  <!--顶部背景图和内容 start-->
  <div class="top_bg">
    <h1>吃好饭，做好菜</h1>
    <p>{{ sentence }}</p>
  </div>
  <!--顶部背景图和内容 end-->
  <!--本站数据统计 start-->
  <div style="margin-bottom:15px;color: #144b9f;">
  <div style="width: 12px;height:12px;background-color:#f9a332;border-radius: 50%;float: left;margin-top: 5px; margin-right: 8px;"></div>管理系统数据统计</div>
  <el-row :gutter="40" class="data_row" :model="basic">
    <el-col :xs="24" :sm="12" :md="12" :lg="6" :xl="6">
      <div style="background: linear-gradient(to right, #6D80FE, #23D2FD);">
        <div class="data_left">
          <el-icon>
            <Avatar />
          </el-icon>
        </div>
        <div class="data_right">
          <h1>{{basic.usernum}}人</h1>
          <p>用户人数</p>
        </div>
      </div>
    </el-col>
    <el-col :xs="24" :sm="12" :md="12" :lg="6" :xl="6">
      <div style="background: linear-gradient(to right, #FF988B, #FF6B88);">
        <div class="data_left">
          <el-icon>
            <Reading />
          </el-icon>
        </div>
        <div class="data_right">
          <h1>{{basic.foodnum}}个</h1>
          <p>菜品个数</p>
        </div>
      </div>
    </el-col>
    <el-col :xs="24" :sm="12" :md="12" :lg="6" :xl="6">
      <div style="background: linear-gradient(to right, #717CFE, #FC83EC);">
        <div class="data_left">
          <el-icon>
            <Clock />
          </el-icon>
        </div>
        <div class="data_right">
          <h1>{{basic.ordernum}}条</h1>
          <p>订单</p>
        </div>
      </div>
    </el-col>
    <el-col :xs="24" :sm="12" :md="12" :lg="6" :xl="6">
      <div style="background: linear-gradient(to right, rgb(35, 32, 34), rgb(255, 0, 0))">
        <div class="data_left">
          <el-icon>
            <Clock />
          </el-icon>
        </div>
        <div class="data_right">
          <h1>{{city}}</h1>
          <p>地址</p>
        </div>
      </div>
    </el-col>
  </el-row>
  <!--本站数据统计 end-->
  <!--显示菜品 start-->
  <div style="margin-bottom:15px;color: #144b9f;">
  <div style="width: 12px;height:12px;background-color:#f9a332;border-radius: 50%;float: left;margin-top: 5px; margin-right: 8px;"></div>菜品信息介绍</div>
  <el-row :gutter="40" class="data_row" >
    <el-col :xs="24" :sm="12" :md="12" :lg="6" :xl="6" v-for="(item, index) in basic.foodinfos" :key="index" :title="item">
      <div style="background: linear-gradient(to right, #6D80FE, #23D2FD);">
        <div class="data_left">
          <el-icon>
            <img v-if="item.foodicon === null || item.foodicon === ''" src="../../assets/default_food.png"  style="width: 70px; border-radius: 50px;"/>
            <img v-else :src="url+item.foodicon"  style="width: 70px; border-radius: 50px;"/>
          </el-icon>
        </div>
        <div class="data_right">
          <h1>{{item["foodname"].substr(0, 8)}}</h1>
          <p>厨师<span>{{item["user"].substr(0, 10)}}</span></p>
        </div>
      </div>
    </el-col>
  </el-row>
  <!--显示菜品 end-->
</div>
</template>

<script setup lang="ts">
import { ref,reactive,onMounted,toRefs } from 'vue'
import { getIndexTotalApi, getSentenceApi } from "../../api/home/home";
// 服务器路径
const url = import.meta.env.VITE_APP_BASE_API
// 定义响应式数据来存储定位信息
const city = ref("北京市"); // 默认城市名
const key = "Y7ABA-RDAYJ-TKSFM-KPSXB-3ASPJ-QHAD4"; // 替换为你的 Key，靶场环境，该key不可用
const sentence = ref();
const state = reactive({
  // 基本信息
  basic: {
    usernum: '',
    foodnum: '',
    ordernum: '',
    foodinfos: [],
  }
})
//挂载后加载数据
onMounted(() => {
  getSentence();
  getIndexTotal();
  getLocationByIP();
})
// 获取信息
const getIndexTotal = async ()=> {
  const { data } = await getIndexTotalApi()
  if(data.code===200){
    basic.value.usernum = data.result.usernum
    basic.value.foodnum = data.result.foodnum
    basic.value.ordernum = data.result.ordernum
    basic.value.foodinfos = data.result.foodinfos
  }
}
// 获取金句
const getSentence = async ()=> {
  const { data } = await getSentenceApi(url+"static/sentence/sentence.txt")
  if(data.code===200){
    sentence.value = data.result.replace("。", "");
  }
}

// 获取 IP 定位
const getLocationByIP = () => {
  const url1 = `https://apis.map.qq.com/ws/location/v1/ip?key=${key}&output=jsonp&callback=handleLocation`;
  // 动态创建 script 标签
  const script = document.createElement("script");
  script.src = url1;
  document.body.appendChild(script);
};

// 将 handleLocation 函数挂载到 window 对象上，使其成为全局函数
window.handleLocation = (data: any) => {
  if (data.status === 0) {
    city.value = data.result.ad_info.city; // 获取城市名称
  } else {
    console.error("定位失败", data.message);
  }
};

const {basic} = toRefs(state)
</script>

<style scoped>
.home {
  width: 100%;
}
.top_bg {
  width: 100%;
  height: 200px;
  background-image: url(../../assets/banner01.jpg);
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  color: white;
  line-height: 60px;
  text-align: center;
  margin: 0 auto 10px;
}

.top_bg h1 {
  font-size: 60px;
  text-shadow: 3px 3px 0px #515151;
  padding-top: 50px;
}

.top_bg p {
  font-weight: lighter;
  font-size: 18px;
}

.data_row .el-col {
  height: 100px;
  margin-bottom: 20px;
  overflow: hidden;
}

.data_row .el-col>div {
  width: 100%;
  height: 100%;
  border-radius: 10px;
  color: white;
}
.data_left {
  float: left;
  width: 40%;
  height: 100%;
  display: inline-flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}
.data_left .el-icon {
  font-size: 60px;
}
.data_right {
  width: 60%;
  float: right;
  margin-top: 20px;
}

.data_right h1 {
  font-size: 30px;
}

.data_right h1 span {
  font-size: 1px;
  margin-left: 10px;
}

.data_right p {
  font-size: 16px;
  font-weight: 600;
  margin-left: 3px;
}
.data_right p span {
  font-size: 14px;
  margin-left: 10px;
}

</style>
