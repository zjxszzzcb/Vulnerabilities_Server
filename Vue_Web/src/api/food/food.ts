import request from '../request'
// 获取食物菜单信息
export function getFoodListApi(data:object) {
    return request({
        url: 'food/get',
        method: 'get',
        params: data
    })
}
// 添加食物菜单信息
export function addFoodApi(data:object) {
    return request({
        url: 'food/add',
        method: 'post',
        data
    })
}

// 根据ID获取食物菜单信息
export function getFoodApi(id:number) {
    return request({
        url: `food/detail?id=${id}`,
        method: 'get'
    })
}
// 更新食物菜单信息
export function editFoodApi(data:object) {
    return request({
        url: 'food/update',
        method: 'put',
        data
    })
}
// 根据ID删除食物菜单信息
export function deleteFoodApi(id:number) {
    return request({
        url: `food/delete/${id}`,
        method: 'delete'
    })
}
// 更新食物icon
export function upfoodicon(data:object) {
    return request({
        url: 'food/upfoodicon',
        method: 'post',
        data
    })
}
// 更新食物视频
export function upfoodvideo(data:object) {
    return request({
        url: 'food/upfoodvideo',
        method: 'post',
        data
    })
}