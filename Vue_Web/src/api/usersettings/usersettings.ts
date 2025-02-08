import request from '../request'

// 更新个人信息
export function updateInfoApi(data:object) {
    return request({
        url: 'home/updateInfo',
        method: 'put',
        data
    })
}
// 更改个人密码
export function updatePwdApi(data:object) {
    return request({
        url: 'home/updatePwd',
        method: 'put',
        data
    })
}
// 更新头像
export function upuseravatar(data:object) {
    return request({
        url: 'home/upuseravatar',
        method: 'post',
        data
    })
}

