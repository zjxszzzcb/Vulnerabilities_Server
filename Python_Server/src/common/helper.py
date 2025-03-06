import jwt, os
import pymysql
from datetime import datetime, timedelta

# 生成JWT
def Generatejwt(uid, rid, name, setting, expiration_minutes=60):
    # 生成 JWT Token
    payload = {
        "Uid": uid,  # 用户 ID
        "Rid": rid,  # 用户角色
        "Name": name,  # 用户名
        "exp": datetime.utcnow() + timedelta(minutes=expiration_minutes),  # 到期时间
    }
    token = jwt.encode(payload, setting.JWT_SECRET_KEY, algorithm=setting.JWT_ALGORITHM)
    return bytes.decode(token)

# 验证JWT
def Validatejwt(token, setting):
    try:
        decoded_payload = jwt.decode(token, setting.JWT_SECRET_KEY, algorithms=[setting.JWT_ALGORITHM])
        return decoded_payload
    except:
        return None

# 通过JWT获取用户信息
def GetAuthorizationUserInfo(authHeader, setting):
    if authHeader:
        token = authHeader.split(" ")[1]
        return Validatejwt(token, setting)
    else:
        return None

# 文件上传
def Uploadfile(filepath, filedata):
    # 判断文件夹是否存在
    if not os.path.exists(filepath):
        # 如果不存在，则创建
        os.makedirs(filepath)
    # 打开特定的文件进行二进制写操作
    f = open(os.path.join(filepath, filedata.name), 'wb+')
    # 分块写入文件
    for chunk in filedata.chunks():
        f.write(chunk)
    f.close()
    return os.path.join(filepath, filedata.name)

# 备份数据库
def Dackupdb(host, username, password, database_name, dbpath):
    # 数据库连接配置
    try:
        # 连接到 MySQL 数据库
        connection = pymysql.connect(
            host=host,
            user=username,
            password=password,
            database=database_name
        )
        cursor = connection.cursor()

        # 获取数据库中的所有表
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        # 判断文件夹是否存在
        if not os.path.exists(dbpath):
            # 如果不存在，则创建
            os.makedirs(dbpath)
        # 备份文件路径
        backup_file = os.path.join(dbpath, 'backup_{}.sql'.format(int(datetime.now().timestamp())))
        
        # 打开备份文件
        with open(backup_file, 'w') as file:
            # 遍历每个表，导出其结构和数据
            for table in tables:
                table_name = table[0]
                file.write(f"DROP TABLE IF EXISTS `{table_name}`;\n")
                # 导出表结构（CREATE TABLE）
                cursor.execute(f"SHOW CREATE TABLE {table_name}")
                create_table_stmt = cursor.fetchone()[1]
                file.write(f"-- Table structure for `{table_name}`\n")
                file.write(f"{create_table_stmt};\n\n")

                # 导出表数据（INSERT INTO）
                cursor.execute(f"SELECT * FROM {table_name}")
                rows = cursor.fetchall()
                for row in rows:
                    placeholders = ", ".join(["%s"] * len(row))
                    insert_stmt = f"INSERT INTO {table_name} VALUES ({placeholders});"
                    file.write(insert_stmt % tuple(row))
                    file.write("\n")
        return backup_file
    except Exception as err:
        return "err：{}".format(err)
    finally:
        # 关闭数据库连接
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# 删除文件
def DeleteFile(dbfile):
    # 检查文件是否存在
    if os.path.exists(dbfile):
        # 删除文件
        os.remove(dbfile)
        return True
    else:
        return False
