# -----------------------------------------------------------------------------
# JohnBetaCode (john@kiwibot.com)

# -----------------------------------------------------------------------------
FROM ubuntu:22.04

# Or your actual UID, GID on Linux if not the default 1000
ARG USERNAME=ada
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

# -----------------------------------------------------------------------------
RUN apt-get update && apt-get install -y \
    apt-utils \
    build-essential \
    curl \
    git \
    libasio-dev \
    libwebsocketpp-dev \
    lbzip2 \
    openssh-client \ 
    procps \
    python3 \
    python3-argcomplete \
    python3-pip \
    software-properties-common \
    tar \
    wget \ 
    # Install Docker CE CLI
    && curl -fsSL https://download.docker.com/linux/$(lsb_release -is | tr '[:upper:]' '[:lower:]')/gpg | (OUT=$(apt-key add - 2>&1) || echo $OUT) \
    && add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/$(lsb_release -is | tr '[:upper:]' '[:lower:]') $(lsb_release -cs) stable" \
    && apt-get update && apt-get install -y docker-ce-cli \
    # Install Docker Compose
    && curl -sSL "https://github.com/docker/compose/releases/download/${COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose \
    && chmod +x /usr/local/bin/docker-compose \
    # Create a non-root user to use if preferred - see https://aka.ms/vscode-remote/containers/non-root-user.
    && apt-get install -y nodejs \
    && groupadd --gid $USER_GID $USERNAME \
    && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
    # [Optional] Add sudo support for non-root user
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    # WebCam Permission
    && usermod -a -G video $USERNAME \
    # ------------------------------
    # Clean up
    && apt-get autoremove && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

RUN \
    pip3 install \
    opencv-python \
    mediapipe \
    stow \
    numpy \
    tqdm \
    onnxruntime \ 
    tf2onnx \
    tensorflow==2.*

# -----------------------------------------------------------------------------
# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=
CMD ["/bin/bash"]

# -----------------------------------------------------------------------------