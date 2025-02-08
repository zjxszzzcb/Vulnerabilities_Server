import request from '../request'

// ping地址
export function pingAddApi(data:string) {
    return request({
        url: 'settings/ping',
        method: 'post',
        data: "addre="+data
    })
}
// 备份数据库
export function backupsDbApi() {
    return request({
        url: 'settings/backupsdb',
        method: 'get',
    })
}
// 获取备份数据库
export function getBackupsDbApi(path:string) {
    return request({
        url: 'settings/getdb',
        method: 'post',
        data:   "dir="+path
    })
}
// 下载备份数据库
export function downBackupsDbApi(data:string) {
    return request({
        url: 'settings/downdb',
        method: 'post',
        data: "dbfile="+data,
        responseType: 'blob'
    }).then(res=>{
        // 下载资料的文件名
        let fileName = res.config.data.split('=')[1]
        let link = document.createElement('a');
        link.download = fileName;
        link.href = URL.createObjectURL(res.data);
        link.target = '_blank';
        link.style.display = 'none';
        document.body.appendChild(link);
        link.click();
        URL.revokeObjectURL(link.href);
        document.body.removeChild(link);
    }
    )
}
// 删除备份数据库
export function deleteBackupsDbApi(data:string) {
    return request({
        url: 'settings/deletedb',
        method: 'post',
        data: "dbfile="+data
    })
}