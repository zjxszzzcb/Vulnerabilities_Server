package helper

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/des"
	"crypto/rand"
	"crypto/rsa"
	"crypto/x509"
	"encoding/base64"
	"encoding/pem"
	"fmt"
	"strings"
)

// base64解码
func Base64DoubleDecode(ciphertextBase64 string) (string, error) {
	// 编码为Base64
	decodetmp, err := base64.URLEncoding.DecodeString(strings.Replace(string(ciphertextBase64), "-", "=", -1))
	if err != nil {
		return "", err
	}
	decodetmp, err = base64.URLEncoding.DecodeString(strings.Replace(string(decodetmp), "-", "=", -1))
	if err != nil {
		return "", err
	}
	return string(decodetmp), nil
}

// 登录的自定义简单解密方式
func CustomDecrypt(encrypted string) (string, error) {
	// base64解码
	encryptmp, err := base64.StdEncoding.DecodeString(encrypted)
	if err != nil {
		return "", err
	}
	text := string(encryptmp)
	// 自定义简单解密方式：去掉混淆字符
	var result strings.Builder
	runes := []rune(text)
	for i := 0; i < len(runes); i += 2 {
		result.WriteRune(runes[i])
	}
	// 颠倒字符串
	runes = []rune(result.String())
	for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
		runes[i], runes[j] = runes[j], runes[i]
	}
	// 凯撒解密
	result = strings.Builder{}
	// 26个字母-3=23
	shift := 23
	for _, c := range string(runes) {
		if c >= 'A' && c <= 'Z' {
			result.WriteRune('A' + (c-'A'+rune(shift))%26)
		} else if c >= 'a' && c <= 'z' {
			result.WriteRune('a' + (c-'a'+rune(shift))%26)
		} else {
			result.WriteRune(c)
		}
	}
	return result.String(), nil
}

// AESDecrypt使用PKCS7填充进行AES-256-CBC解密
func AESDecrypt(ciphertextBase64 string) (string, error) {
	key := "8ffe7d19cbc24e898b3344d06cf842e2"
	iv := "1cfc13bd74a2"

	// 确保key和IV长度正确
	if len(key) < 32 {
		for len(key) < 32 {
			key += "\x00"
		}
	} else if len(key) > 32 {
		key = key[:32]
	}

	if len(iv) < 16 {
		for len(iv) < 16 {
			iv += "\x00"
		}
	} else if len(iv) > 16 {
		iv = iv[:16]
	}
	// 解码Base64编码的密文
	ciphertext, err := base64.StdEncoding.DecodeString(ciphertextBase64)
	if err != nil {
		return "", fmt.Errorf("failed to decode base64 ciphertext: %v", err)
	}

	// 将key和IV转换为字节片
	keyBytes := []byte(key)
	ivBytes := []byte(iv)

	// 确保key和IV的长度正确
	if len(keyBytes) != 32 {
		return "", fmt.Errorf("key must be 32 bytes (256 bits)")
	}
	if len(ivBytes) != aes.BlockSize {
		return "", fmt.Errorf("IV must be %d bytes", aes.BlockSize)
	}

	// 创建AES分组密码
	block, err := aes.NewCipher(keyBytes)
	if err != nil {
		return "", fmt.Errorf("failed to create AES cipher: %v", err)
	}

	// 使用CBC模式解密密文
	mode := cipher.NewCBCDecrypter(block, ivBytes)
	plaintextPadded := make([]byte, len(ciphertext))
	mode.CryptBlocks(plaintextPadded, ciphertext)

	// 删除 PKCS7 padding
	plaintext, err := removePKCS7Padding(plaintextPadded)
	if err != nil {
		return "", fmt.Errorf("failed to remove padding: %v", err)
	}

	return string(plaintext), nil
}

// 从明文中删除PKCS7填充
func removePKCS7Padding(plaintext []byte) ([]byte, error) {
	paddingLen := int(plaintext[len(plaintext)-1])
	if paddingLen > len(plaintext) || paddingLen == 0 {
		return nil, fmt.Errorf("invalid padding length")
	}

	for _, pad := range plaintext[len(plaintext)-paddingLen:] {
		if int(pad) != paddingLen {
			return nil, fmt.Errorf("invalid padding byte")
		}
	}

	return plaintext[:len(plaintext)-paddingLen], nil
}

// 使用RSA公钥加密并 Base64 编码
func RSAEncrypted(message string) (string, error) {
	// 公钥
	const publicKeyPEM = `-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsSOjJck8DhR/j6sFCBH/
Sw8dXkd9CjKxnNFjMTEWYWx39a5ZO5uvhWV6ps4/+yZEZPgw0EaBV0gSwpLBs4eC
+5EFBArDp0qdf38KRN++oR5MJMGWDXAJKBcKHall0/TvnZ7ATbhc3M9EN+5Mi/MG
TOOHVs0wP61NVnf3KR9DjxhD/ddvGKNZkc5Ivds0CHPzUX4bLUppa0NeyA2YIVIy
TxloBQeR9dnq9C3yB0iBDdYb1H2zOfaUOGYIS5Xpu5PlL5BPfxH2utS2MzehD6l2
yu1RktVGFx0Ij3cVUfMMh03RfMCYjcoCALxuhZzWqvmp1KSqrQEx6hX0D91ALsGl
QwIDAQAB
-----END PUBLIC KEY-----`
	// 解析公钥
	block, _ := pem.Decode([]byte(publicKeyPEM))
	if block == nil {
		return "", fmt.Errorf("公钥解析失败")
	}
	pub, err := x509.ParsePKIXPublicKey(block.Bytes)
	if err != nil {
		return "", err
	}

	// RSA 加密
	ciphertext, err := rsa.EncryptPKCS1v15(rand.Reader, pub.(*rsa.PublicKey), []byte(message))
	if err != nil {
		return "", err
	}

	// Base64 编码
	return base64.StdEncoding.EncodeToString(ciphertext), nil
}

// 3DES 解密
func TripleDESDecrypt(cipherText string) (string, error) {
	key := []byte("3c304f5c5eba944c6ef86a88") // 24字节密钥
	iv := []byte("w2sg62fq")                  // 8字节IV
	cipherData, err := base64.StdEncoding.DecodeString(cipherText)
	if err != nil {
		return "", err
	}

	block, err := des.NewTripleDESCipher(key)
	if err != nil {
		return "", err
	}

	blockMode := cipher.NewCBCDecrypter(block, iv)
	decrypted := make([]byte, len(cipherData))
	blockMode.CryptBlocks(decrypted, cipherData)

	// 去除PKCS7填充
	padLen := int(decrypted[len(decrypted)-1])
	return string(decrypted[:len(decrypted)-padLen]), nil
}
