<template>
  <el-col class="hidden-md-and-down" :lg="6" :xl="6">
    <div class="right_box">
      <h3 class="title">
        <el-icon style="margin-right: 10px;">
          <Grid />
        </el-icon>
        信息展示
      </h3>
      <div class="info">
        <div class="right_photo">
          <!-- 用户没设置头像的情况下使用系统默认的 -->
          <img v-if="userInfo.avatar === null || userInfo.avatar === ''" src="../../../assets/default_avatar.png">
          <img v-else :src="url+userInfo.avatar">
        </div>
        <h2>Hi，{{userInfo.username}}</h2>
        <br>
        <p class="email">{{userInfo.email}}</p>
      </div>
      <el-divider />
      <h3 class="title">
        <el-icon style="margin-right: 10px;">
          <Sunrise />
        </el-icon>
        系统说明
      </h3>
      <div class="type">
        <br>
        <p>{{userInfo.introduce}}</p>
      </div>
      <el-divider />
      <h3 class="title">
        <el-icon style="margin-right: 10px;">
          <Watch />
        </el-icon>
        本站运行天数（{{calculateDays('2022-12-20 00:00:00')}}）
      </h3>
    </div>
  </el-col>
</template>

<script setup lang="ts">

import { useUserStore } from '../../../store/modules/user'
import {calculateDays} from "../../../utils/date";
const { userInfo } =  useUserStore()
// 服务器路径
const url = import.meta.env.VITE_APP_BASE_API


</script>

<style scoped>
.right_box {
  width: 100%;
  height: auto;
  background: white;
  padding: 20px;
  /* 添加此属性 padding间距不扩大div */
  box-sizing: border-box;
}

.right_photo {
  position: relative;
  text-align: center;
  height: 100px;
  width: 100px;
  margin-left: -50px;
  left: 50%;
}

.info {
  text-align: center;
}

.right_photo img {
  width: 100%;
  border-radius: 50%;
}

.right_box h2 {
  padding-top: 10px;
  letter-spacing: 0;
  font-size: 30px;
}
.right_box .title {
  color: #178557;
}
</style>
