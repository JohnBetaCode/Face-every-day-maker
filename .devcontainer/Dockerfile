# -----------------------------------------------------------------------------
# JohnBetaCode (john@kiwibot.com)

# -----------------------------------------------------------------------------
FROM ubuntu:20.04

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

# -----------------------------------------------------------------------------
# Install cmake from source, because latest version not available in apt repos
ENV CMAKE_SOURCE_DIR=/cmake_build
# ----- Cmake 3.15 is required for tkDNN library (later on)
RUN mkdir $CMAKE_SOURCE_DIR \
    && wget https://cmake.org/files/v3.15/cmake-3.15.0.tar.gz -O $CMAKE_SOURCE_DIR/cmake-3.15.0.tar.gz \
    && cd $CMAKE_SOURCE_DIR \
    && tar xf cmake-3.15.0.tar.gz \
    && cd cmake-3.15.0  \
    && ./configure \
    && NUM_CPU=$(nproc) \
    && make install \
    && rm -r $CMAKE_SOURCE_DIR

# -----------------------------------------------------------------------------
# OpenCV Installation with contrib
# https://linuxize.com/post/how-to-install-opencv-on-ubuntu-18-04/
ENV OPENCV_VERSION=4.4.0  \
    OPENCV_CONTRIB_VERSION=4.4.0
# OPENCV_LOG_LEVEL=1
RUN apt update && apt install --no-install-recommends -y \
    # ------------------------------
    # Generic tools
    build-essential \
    # git \
    pkg-config \
    unzip \
    yasm \
    checkinstall \
    udev \
    # ------------------------------
    # Image I/O libs
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libopenjp2-tools \
    # ------------------------------
    # Video/Audio Libs - FFMPEG, GSTREAMER, x264 and so on.
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    # libavresample \
    libgstreamer1.0-dev \
    libgstreamer-plugins-base1.0-dev \
    libxvidcore-dev \
    x264 \
    libx264-dev \
    libfaac-dev \
    libmp3lame-dev \
    libtheora-dev \
    libvorbis-dev \
    libgtk2.0-dev \
    # ------------------------------
    # OpenCore - Adaptive Multi Rate Narrow Band (AMRNB) and Wide Band (AMRWB) speech codec
    # libopencore-amrnb-dev \
    # libopencore-amrwb-dev \
    # ------------------------------
    # Cameras programming interface libs
    libdc1394-22 \
    libdc1394-22-dev \
    libxine2-dev \
    libv4l-dev \
    v4l-utils \
    # ------------------------------
    # GTK lib for the graphical user functionalites coming from OpenCV highghui module
    libgtk-3-dev \
    # ------------------------------
    # Ohters
    openexr \
    # ------------------------------
    # Parallelism library C++ for CPU
    libtbb-dev \
    libtbb2 \
    # ------------------------------
    # Optimization libraries for OpenCV
    libatlas-base-dev \
    gfortran \
    # ------------------------------
    # pip dependencies
    &&  python3 -m pip install  \
    numpy \
    testresources \
    setuptools \
    # ------------------------------
    && rm -rf /var/lib/apt/lists/*

RUN  \
    # ------------------------------
    # Downlaoding and extracting OpenCV
    mkdir ~/opencv_build \
    && cd ~/opencv_build \
    && git clone --branch $OPENCV_VERSION https://github.com/opencv/opencv.git \
    && git clone --branch $OPENCV_CONTRIB_VERSION https://github.com/opencv/opencv_contrib.git \
    && cd ~/opencv_build/opencv \
    && mkdir build && cd build \
    # ------------------------------
    && cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D WITH_GSTREAMER=ON \
    -D BUILD_TIFF=ON \ 
    -D WITH_CUDA=ON \ 
    -D WITH_V4L=ON \    
    -D WITH_TBB=ON \
    -D BUILD_TBB=ON \
    -D WITH_OPENGL=OFF \
    -D WITH_OPENCL=OFF \
    -D WITH_IPP=OFF \
    -D WITH_EIGEN=OFF \
    -D ENABLE_FAST_MATH=1 \        
    -D WITH_QT=OFF \
    -D WITH_VTK=OFF \
    -D BUILD_TESTS=OFF \
    -D BUILD_PERF_TESTS=OFF \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_C_EXAMPLES=OFF \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D PYTHON_DEFAULT_EXECUTABLE=/usr/bin/python3 \
    -D OPENCV_GENERATE_PKGCONFIG=ON \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_build/opencv_contrib/modules \
    # -D BUILD_opencv_world=OFF \
    -D BUILD_EXAMPLES=OFF .. \
    # ------------------------------
    && make -j $(nproc) \
    && make install \
    && rm -r ~/opencv_build \
    # ------------------------------
    # && apt autoremove && apt clean -y \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------------------------------------------------------
# Add Python dependencies in here
RUN pip3 install -U pip \
    black~=20.8b \
    dlib==19.22.0 \
    imutils==0.5.4 \
    gdown==3.13.0 \
    tqdm

# Add System dependencies in here
RUN \
    apt update && apt install -y \ 
    ffmpeg  \ 
    && apt autoremove && apt clean -y \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------------------------------------------------------
# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=
CMD ["/bin/bash"]

# -----------------------------------------------------------------------------