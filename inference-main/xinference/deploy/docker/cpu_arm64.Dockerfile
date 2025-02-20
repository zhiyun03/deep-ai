# 使用兼容 ARM64 的基础镜像
FROM debian:bullseye	

# 复制项目文件到容器中
COPY . /opt/inference

#定义环境变量
ENV NVM_DIR=/usr/local/nvm
ENV NODE_VERSION=14.21.1

# 安装系统依赖
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list && \
    sed -i 's/security.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list && \
    apt-get -y update && \
    apt install -y build-essential curl procps git libgl1 ffmpeg python3 python3-pip python-is-python3 && \
    mkdir -p $NVM_DIR && \
    # 安装 Node.js 环境
    bash /opt/inference/xinference/deploy/docker/nvm_v0.39.7_install.sh && \
    . $NVM_DIR/nvm.sh && \
    nvm install $NODE_VERSION && \
    nvm alias default $NODE_VERSION && \
    nvm use default && \
    # 清理 apt 缓存
    apt-get -yq clean

# 配置 Node.js 路径
ENV PATH=$NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH

# 设置国内镜像源
ENV PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple \
    PIP_TRUSTED_HOST=mirrors.aliyun.com \
    PYTHONHTTPSVERIFY=0
    
# 安装 Python 依赖
RUN python3 -m pip install --upgrade  pip && \
    # 安装 PyTorch 的 CPU 版本（适配 ARM64）
    pip install torch torchvision torchaudio sentence-transformers  && \    
    # 安装 requirements_cpu.txt 中列出的依赖（仅当需要时）
    #pip install -i "$PIP_INDEX" --upgrade-strategy only-if-needed -r /opt/inference/xinference/deploy/docker/requirements_cpu.txt && \
    # 安装 llama-cpp-python
    #CMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python && \

    #构建项目
    cd /opt/inference && \
    python setup.py build_web && \
    pip install . && \
    #清理 pip 缓存
    pip cache purge

#容器启动命令
ENTRYPOINT []
CMD ["/bin/bash"]