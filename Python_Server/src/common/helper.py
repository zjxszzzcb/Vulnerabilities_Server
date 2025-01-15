import jwt, os
import pymysql
from datetime import datetime, timedelta
from Crypto.Cipher import AES, PKCS1_OAEP
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
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

# aes解密
def AesDecrypt(ciphertext_base64):
    key = "8ffe7d19cbc24e898b3344d06cf842e2"  # AES-256 密钥
    iv = "1cfc13bd74a2"
    # 确保密钥和 IV 长度正确
    key = key.encode('utf-8')
    iv = iv.encode('utf-8')
    if len(key) < 32:
        key = key.ljust(32, b'\0')  # 填充到 32 字节
    elif len(key) > 32:
        key = key[:32]  # 截断到 32 字节

    if len(iv) < 16:
        iv = iv.ljust(16, b'\0')  # 填充到 16 字节
    elif len(iv) > 16:
        iv = iv[:16]  # 截断到 16 字节
    try:
        # 将 Base64 格式密文解码为字节
        ciphertext = base64.b64decode(ciphertext_base64)
        
        # 初始化 AES 解密器（CBC 模式，PKCS7 填充）
        cipher = AES.new(key, AES.MODE_CBC, iv)
        
        # 解密
        plaintext_padded = cipher.decrypt(ciphertext)
        
        # 移除 PKCS7 填充
        padding_len = plaintext_padded[-1]
        if padding_len < 1 or padding_len > AES.block_size:
            return "", "Invalid padding length"
        plaintext = plaintext_padded[:-padding_len]
        return plaintext.decode('utf-8'), ""
    except Exception as e:
        return "","解密失败：{}".format(e)

# RSA加密
def RsaEncrypt(plaintext):
    public_key = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoMpovuUbHluQaitXR6bc
+Q92C95ZNHT89SIX8cbKV/dFsY000PObJE5g83gQJO+ARPzKlKEuMp/+j03khjzZ
BQr0nIBhpRKtecMMqyvefR9I+Bv91Ra3qxTJX7LKejbG9lxbQ4HcJyUxNuOuRCVm
5ho0j4gO20MzuTXdfOUCscjh7AsvJAy1bBc/Nuc28/4fpQQZ6+lvkM/4aCkZtisk
yz96GrWEIlpwLjrlWsk8Zg4oRYxBn8g8fY1e7nccRyuF7jFN1D0btiY+6d+DWUzx
2x9jLXtP8HUnjOBg/FAmmL+8ePQOOBJ/CceAgdwOv53k9CBTBc/D6Ldl5F9+ZoW/
jQIDAQAB
-----END PUBLIC KEY-----"""
    public_key_obj = RSA.import_key(public_key.encode())
    cipher_rsa_encrypt = PKCS1_OAEP.new(public_key_obj)
    aaa = "{}".format(plaintext)
    ciphertext = cipher_rsa_encrypt.encrypt(aaa.encode())
    # 密文 Base64 编码
    encoded_ciphertext = base64.b64encode(ciphertext)
    return encoded_ciphertext.decode()

# RSA解密
def RsaDecrypt(base64_ciphertext):
    private_key = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAoMpovuUbHluQaitXR6bc+Q92C95ZNHT89SIX8cbKV/dFsY00
0PObJE5g83gQJO+ARPzKlKEuMp/+j03khjzZBQr0nIBhpRKtecMMqyvefR9I+Bv9
1Ra3qxTJX7LKejbG9lxbQ4HcJyUxNuOuRCVm5ho0j4gO20MzuTXdfOUCscjh7Asv
JAy1bBc/Nuc28/4fpQQZ6+lvkM/4aCkZtiskyz96GrWEIlpwLjrlWsk8Zg4oRYxB
n8g8fY1e7nccRyuF7jFN1D0btiY+6d+DWUzx2x9jLXtP8HUnjOBg/FAmmL+8ePQO
OBJ/CceAgdwOv53k9CBTBc/D6Ldl5F9+ZoW/jQIDAQABAoIBABC0ludmdEfWKY3u
TNYj7wdtZM1c35XEpdduIGC9T56OEU6eJiOje7Xs8sO48Kx1ubTxMrb4fA1EdDU9
WYXc4otUlQ+BgyOcaiuhaTqLh0Umr/UfK2MtRg3fTgDEWacS8976v3ynDFGA2rki
NKPd4u/7PwS+lRSQydnvT8C/JmWEGFHZGhlltxsvFi6p42rAPuyF+feC4P0OAVAw
XUF87L/GrNZxor3PhFrvKWUwMl03tCfq1V2+8a67jEaxfOxtSxY+Cs7FCqVAE8pj
ogpRF2N2xnCacycy8bOvQ/jd0olycooU+8fmYSuli9J25nsZDcgS3OAlGP4UKcab
VuKNZT0CgYEAxo4diBSKCd+1qas5LYgQo1kJ6KE+L8MkTQL1/tJE/V6JliaJ7tV3
GlH4DJjYAJpIro6ezCH3xpyYRGA+AQIASP3ao2ZENxI/isas0jfqht1iF1JD9lDL
buwiV17UEOf0Kov4AXH3JTS+FxWDa1AvoYoiWA2QrLUxbtiuGSx00R8CgYEAz09J
gTgMG13UF33EJBd1j/gGu0sDW8c93x80oTseM+FvJZgdQG0spNXZoxfUc2ylzfJe
inyP2imzFSHqBCarWa481aLNVwAQBYSiYJlQm58Gk7pl3fq4UAvSFv6ucy9ZKXXk
7saNTkBQAH0gBNmV25pkqRUfRzTVVqBsbGl3PdMCgYAi9+hvjN56urFtvkAFqs7z
Vb0PAUbIdp+wCHN2e2W3Ea09inAEZgfh1MnQviJciM+AHpIM9XaDvhR7BlAlMUsH
j92vpVUiNc6HDFJne32MXvTlkpFxke0iDehGZucGSzOPQrNc3cte/Bj2S82nWqno
00EVLN5r7EVWdkbDHDc+lQKBgD4ExEKqF8UgHtEgSMtbUUpOswTY/ho40uOrHD2X
yANRT8T5atbZUl/FsiQ+fspBGKEx/uKDPS3RB8gsqyuuvdhIbd6jo7aBSEm+Ui1/
8EN+IaOUQeFUnkskHifO7TV8Vro2kNR2BdQBHW3oAOoyhch6ud5zeTX+MkyGFamh
K5ENAoGBAJFjT7GVzf82FjBw/EbcIpfN4dCVh1MdHVSJ36bSVVk5dQKVG5F+n0Im
n7HD/zU9iDoPLX+mmvgtgPdvLunbJep9OOac4j+KYTS46JX9UQqZaIiABj+5ULeQ
4QRRdlguQy+XP2EmcT1dT/rfC9djajRIHAX2iwttZErnvDRFQT7S
-----END RSA PRIVATE KEY-----"""
    private_key_obj = RSA.import_key(private_key.encode())
    cipher_rsa_decrypt = PKCS1_OAEP.new(private_key_obj)
    plaintext = cipher_rsa_decrypt.decrypt(base64.b64decode(base64_ciphertext))
    return plaintext.decode()