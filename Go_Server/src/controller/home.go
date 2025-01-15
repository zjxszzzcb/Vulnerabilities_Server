package controller

import (
	"Go_server/define"
	"Go_server/helper"
	"Go_server/models"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"strings"
	"time"

	"math/rand"

	"github.com/gin-gonic/gin"
)

// GetHomeInfo
// @Summary 获取系统数据信息
// @Param Authorization header string true "Authorization"
// @Tags 鉴权接口-首页设置方法
// @Router /home/get [get]
func GetHomeInfo(c *gin.Context) {
	// 初始化变量
	var (
		usernum   int64
		foodnum   int64
		ordernum  int64
		foodinfos []*define.GetFoodListReply
	)
	if err := models.GetFoodList("").Count(&foodnum).Find(&foodinfos).Error; err != nil {
		helper.ErrorResponse(c, "获取系统数据信息", err)
		return
	}
	if err := models.GetUserList("", -1).Count(&usernum).Error; err != nil {
		helper.ErrorResponse(c, "获取系统数据信息", err)
		return
	}
	if err := models.GetOrderList("").Count(&ordernum).Error; err != nil {
		helper.ErrorResponse(c, "获取系统数据信息", err)
		return
	}
	helper.SuccessResponse(c, "获取系统数据信息", struct {
		Usernum   int64                      `json:"usernum"`
		Foodnum   int64                      `json:"foodnum"`
		Ordernum  int64                      `json:"ordernum"`
		FoodInfos []*define.GetFoodListReply `json:"foodinfos"`
	}{
		Usernum:   usernum,
		Foodnum:   foodnum,
		Ordernum:  ordernum,
		FoodInfos: foodinfos,
	})
}

// UpdateInfo
// @Summary 用户自己更新个人信息
// @Tags 鉴权接口-首页设置方法
// @Param Authorization header string true "Authorization"
// @Param UpdateInfoType body define.UpdateInfoType true "用户自己更新个人信息参数"
// @Router /home/updateInfo [put]
func UpdateInfo(c *gin.Context) {
	in := new(define.UpdateInfoType)
	if err := c.ShouldBindJSON(in); err != nil {
		helper.ErrorResponse(c, "参数绑定", err)
		return
	}
	if in.Username == "" || in.Sex == "" {
		helper.ErrorResponse(c, "更新用户个人信息", fmt.Errorf("用户名性别不能为空"))
		return
	}
	// 判断角色是否已存在
	var cnt int64

	if err := models.DB.Model(new(models.SysUser)).Where("id != ? AND username = ?", in.ID, in.Username).Count(&cnt).Error; err != nil {
		helper.ErrorResponse(c, "更新用户个人信息", err)
		return
	}
	if cnt > 0 {
		helper.ErrorResponse(c, "更新用户个人信息", fmt.Errorf("用户名已经存在"))
		return
	}
	if _, err := os.Stat(in.Avatar); in.Avatar != "" && os.IsNotExist(err) {
		helper.ErrorResponse(c, "更新用户个人信息", err)
		return
	}
	// 修改数据
	if err := models.DB.Model(new(models.SysUser)).Where("id = ?", in.ID).Updates(map[string]any{
		"username": in.Username,
		"sex":      in.Sex,
		"avatar":   in.Avatar,
	}).Error; err != nil {
		helper.ErrorResponse(c, "更新用户个人信息", err)
		return
	}
	helper.SuccessResponse(c, "更新用户个人信息", nil)
}

// UpdatePwd
// @Summary 修改个人密码
// @Tags 鉴权接口-首页设置方法
// @accept application/x-www-form-urlencoded
// @Param Authorization header string true "Authorization"
// @Param PwdDataType body define.PwdDataType true "用户自己更新密码和UID"
// @Router /home/updatePwd [put]
func UpdatePwd(c *gin.Context) {
	d := new(define.PwdDataType)
	if err := c.ShouldBindJSON(d); err != nil {
		helper.ErrorResponse(c, "参数绑定", err)
		return
	}
	pwddata, err := helper.AESDecrypt(d.Data)
	if err != nil {
		helper.ErrorResponse(c, "解密", err)
		return
	}
	in := new(define.UpdatePwdType)
	if err = json.Unmarshal([]byte(strings.Replace(pwddata, "'", "\"", -1)), &in); err != nil {
		helper.ErrorResponse(c, "转换", err)
		return
	}
	if in.Newpwd == "" || in.Uid == 0 {
		helper.ErrorResponse(c, "修改密码", fmt.Errorf("ID或新密码不能为空"))
		return
	}
	// 获取用户名的基本信息
	getuser, err := models.GetUserDetail(in.Uid)
	if err != nil {
		helper.ErrorResponse(c, "修改密码", err)
		return
	}
	if err := models.DB.Model(new(models.SysUser)).Where("id = ?", getuser.ID).Updates(map[string]any{
		"password": in.Newpwd,
	}).Error; err != nil {
		helper.ErrorResponse(c, "修改密码", err)
		return
	}
	helper.SuccessResponse(c, "修改密码", nil)
}

// UploadUserAvatar
// @Summary 上传头像
// @Tags 鉴权接口-首页设置方法
// @Param Authorization header string true "Authorization"
// @Param file formData file true "上传头像"
// @Router /home/upuseravatar [post]
func UploadUserAvatar(c *gin.Context) {
	fh, err := c.FormFile("file")
	if err != nil {
		helper.ErrorResponse(c, "上传头像", err)
		return
	}
	// 识别图片
	filepath, err := helper.UploadFile(fh, "user/", fh.Filename)
	if err != nil {
		helper.ErrorResponse(c, "上传头像", err)
		return
	}
	helper.SuccessResponse(c, "上传头像", filepath)
}

// GetSentence
// @Summary 获取每日金句
// @Tags 鉴权接口-首页设置方法
// @Param Authorization header string true "Authorization"
// @Param url query string true "获取每日金句的url" default "http://127.0.0.1:8081/static/sentence/sentence.txt"
// @Router /home/getsentence [get]
func GetSentence(c *gin.Context) {
	url := c.Query("url")
	res, err := http.Get(url)
	if err != nil {
		helper.ErrorResponse(c, "获取每日金句", err)
		return
	}
	body, err := io.ReadAll(res.Body)
	defer res.Body.Close()
	if err != nil {
		helper.ErrorResponse(c, "获取每日金句", err)
		return
	}
	strtmp := strings.Replace(string(body), "\r", "", -1)
	stlist := strings.SplitN(strtmp, "\n", -1)
	rand.Seed(time.Now().UnixNano())
	stsrt := stlist[rand.Intn(len(stlist))]
	if stsrt == "" {
		stsrt = "好好吃饭，天天健康。"
	}
	helper.SuccessResponse(c, "获取每日金句", stsrt)
}
