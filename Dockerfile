# Dockerfile —— study-review agent 的镜像配方
#
# 【为什么这个文件在仓库根】构建上下文（context）必须是**仓库根**，因为服务要读整个仓库：
#   review_agent.py: REPO_ROOT = Path(__file__).resolve().parent.parent
#   → git log（cwd=REPO_ROOT）/ REPO_ROOT.glob("stage*") / REPO_ROOT / "LEARNING-ROUTE.md"
#   而 .dockerignore 必须放在**上下文根**。所以三个文件都在这里最省事。
#
# 构建：docker build -t study-review-agent:dev .
# 运行：docker compose up -d   →  http://127.0.0.1:8000/docs

# 1) 基础镜像。
#    slim = 精简版 Debian（约 130 MB），自带 pip，够用。
#    不用 alpine（约 50 MB）：它用 musl libc，装带 C 扩展的包容易编译失败。
#    不用 python:3.11（约 1 GB）：完整系统，没必要 —— 镜像越大，拉取/传输/攻击面都越大。
FROM python:3.11-slim

# 2) 设工作目录。之后所有相对路径都基于它，镜像里就是 /app（= 仓库根）。
WORKDIR /app

# 3) 装系统级依赖 git。
#    git 是**必需**的：review_agent 的 git_log 工具要 subprocess 跑 `git log`，
#    而 python:3.11-slim 里没有 git —— 这是实测发现的，第 ① 层静态检查发现不了。
#
#    为什么换成阿里云镜像（实测，不是拍脑袋）：
#      本机开着 FlClash（fake-ip 模式）时，官方源 deb.debian.org 解析成 198.18.0.x，
#      apt 走 http 拿到 502 Bad Gateway，换 https 又炸 SSL "unexpected eof while reading"。
#      换成 mirrors.aliyun.com 就能下（FlClash 对 CN 域名走直连）。
#      在 GitHub Actions 这类没有代理的环境里，两个源都能用 —— 换镜像不损失通用性。
#
#    末尾删掉 apt 索引是标准做法：包索引没必要留在镜像里（能省几十 MB）。
#    放这一层是因为它很少变，能吃到缓存。
RUN sed -i 's|http://deb.debian.org|https://mirrors.aliyun.com|g' /etc/apt/sources.list.d/debian.sources \
    && apt-get update && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

# 4) ---- 层次缓存：先装依赖，最后才拷代码 ----
#    Docker 从上往下构建，任何一层变了，它**下面所有层**都要重做。
#    所以「很少变的」必须写在「经常变的」上面：依赖清单很少改，代码天天改。
#    顺序若反过来，你每改一行代码，pip 就要重装一遍。
#    注意 COPY 的第二个参数：用相对路径时是相对 WORKDIR，不是相对上下文。
COPY study-review-agent/requirements.txt study-review-agent/requirements.txt
RUN pip install --no-cache-dir -r study-review-agent/requirements.txt

# 5) 代码放最后：以后改代码只会让这一层失效，上面装的依赖全部命中缓存。
#    `.` 是构建上下文的根（仓库根），`.` 是目标（WORKDIR，也就是 /app）。
#    被排除掉的文件由 .dockerignore 决定 —— 那里排掉了 195.9 MB 的上游参考仓库。
COPY . .

# 6) 运行时的环境变量。
#    PYTHONUNBUFFERED=1：让 print 立刻刷出来，不然 `docker logs` 要等缓冲满才看得到输出。
ENV PYTHONUNBUFFERED=1
ENV TZ=Asia/Shanghai

# 7) 声明监听 8000。注意：EXPOSE **只是文档**，不会真的开放端口 ——
#    真正决定能不能从外面访问的是 compose 里的 ports。
EXPOSE 8000

# 8) 启动命令。三处都是刻意的：
#    a) exec 形式（JSON 数组）而不是 shell 形式 —— shell 形式会被包一层 /bin/sh -c，
#       于是容器的 PID 1 变成 sh，`docker stop` 的 SIGTERM 送不到 uvicorn，只能等超时强杀。
#    b) --host 0.0.0.0 而不是 127.0.0.1 —— 绑 127 的话只有容器内部能连，端口映射进不来。
#    c) --app-dir study-review-agent —— uvicorn 默认在 cwd 找 api_server，
#       而它在 study-review-agent/ 里；这个参数会把它加进 PYTHONPATH。
CMD ["python", "-m", "uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000", "--app-dir", "study-review-agent"]
