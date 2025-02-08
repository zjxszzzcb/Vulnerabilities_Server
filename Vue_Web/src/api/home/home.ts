import request from '../request'
export function getIndexTotalApi() {
    return request({
        url: 'home/get',
        method: 'get'
    })
}
// 获取名言金句
export function getSentenceApi(Url:string) {
    return request({
        url: 'home/getsentence?url='+Url,
        method: 'get'
    })
}