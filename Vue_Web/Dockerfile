# 使用Node.js官方镜像作为基础镜像
FROM node:18-alpine

# 安装curl用于调试
RUN apk add --no-cache curl

# 设置工作目录
WORKDIR /app

# 复制package.json和package-lock.json（如果存在）
COPY package*.json ./

# 安装所有依赖（包括开发依赖）和全局工具
RUN npm install --verbose && \
    npm install -g serve vite@^3.2.3 --verbose

# 复制所有文件到工作目录
COPY . .

# 声明构建参数，使用默认值
ARG VITE_APP_BASE_API=http://localhost:8081/
# 创建环境变量文件
RUN mkdir -p viteenv && \
    echo "VITE_APP_BASE_API = '${VITE_APP_BASE_API}'" > viteenv/.env.production && \
    echo "VITE_APP_BASE_API = '${VITE_APP_BASE_API}'" > viteenv/.env.development

# 构建应用并显示详细日志
RUN npm run build --verbose

# 暴露端口
EXPOSE 8080

# 启动应用
CMD ["serve", "-s", "dist", "-l", "8080"]