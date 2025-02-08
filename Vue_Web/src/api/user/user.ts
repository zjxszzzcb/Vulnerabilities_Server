import request from '../request'

// 获取用户列表数据
export function getUserListApi(data:object) {
    return request({
        url: 'user/get',
        method: 'get',
        params: data
    })
}
// 添加用户信息
export function addUserApi(data:object) {
    return request({
        url: 'user/add',
        method: 'post',
        data
    })
}
// 根据ID获取用户详情信息
export function getUserApi(id:number){
    return request({
        url: `user/detail?id=${id}`,
        method: 'get'
    })
}
// 更新用户信息
export function editUserApi(data:object) {
    return request({
        url: 'user/update',
        method: 'put',
        data
    })
}
// 根据ID删除用户信息
export function deleteUserApi(id:number) {
    return request({
        url: `user/delete/${id}`,
        method: 'delete'
    })
}
// 获取所有角色列表
export function getAllRoleListApi() {
    return request({
        url: 'role/get',
        method: 'get'
    })
}



