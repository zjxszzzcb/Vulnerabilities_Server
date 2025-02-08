import request from '../request'
// 获取订单列表数据
export function getOrderListApi(data:object) {
    return request({
        url: 'order/get',
        method: 'get',
        params: data
    })
}

// 添加订单信息
export function addOrderApi(data:object) {
    return request({
        url: 'order/add',
        method: 'post',
        data
    })
}

// 根据ID获取订单信息
export function getOrderApi(id:number) {
    return request({
        url: `order/detail?id=${id}`,
        method: 'get'
    })
}
// 更新订单信息
export function editOrderApi(data:object) {
    return request({
        url: 'order/update',
        method: 'put',
        data
    })
}
// 根据ID删除订单信息
export function deleteOrderApi(id:number) {
    return request({
        url: `order/delete/${id}`,
        method: 'delete'
    })
}

// 获取所有菜品列表
export function getAllFoodListApi() {
    return request({
        url: 'food/get',
        method: 'get'
    })
}