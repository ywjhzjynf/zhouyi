# 周易占卜 APK 快速打包脚本

**使用说明：** 在 Linux 环境（WSL2/Ubuntu）中执行

---

## 快速开始（一键打包）

```bash
#!/bin/bash
# quick_build.sh - 一键打包周易占卜 APK

set -e

echo "=========================================="
echo "  周易占卜系统 APK 打包脚本 v1.0"
echo "=========================================="

# 1. 检查环境
echo "[1/6] 检查环境..."
if ! command -v python3 &> /dev/null; then
    echo "错误：未找到 Python3"
    exit 1
fi

if ! command -v java &> /dev/null; then
    echo "错误：未找到 Java"
    exit 1
fi

echo "✓ Python3: $(python3 --version)"
echo "✓ Java: $(java -version 2>&1 | head -1)"

# 2. 安装依赖
echo ""
echo "[2/6] 安装 Python 依赖..."
python3 -m pip install --upgrade pip
pip3 install kivy buildozer

# 3. 配置 Android SDK
echo ""
echo "[3/6] 配置 Android SDK..."
export ANDROID_HOME=$HOME/android
export ANDROID_SDK_ROOT=$HOME/android

if [ ! -d "$ANDROID_HOME" ]; then
    echo "下载 Android SDK..."
    mkdir -p $ANDROID_HOME
    cd $ANDROID_HOME
    wget -q https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip
    unzip -q commandlinetools-linux-9477386_latest.zip
    mkdir -p cmdline-tools/latest
    mv cmdline-tools/* cmdline-tools/latest/ 2>/dev/null || true
fi

export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools

# 4. 安装 SDK 组件
echo ""
echo "[4/6] 安装 Android SDK 组件..."
yes | sdkmanager --licenses > /dev/null 2>&1 || true
sdkmanager "platform-tools" "platforms;android-33" "ndk;25.2.9519653"

# 5. 编译 APK
echo ""
echo "[5/6] 编译 APK..."
cd -  # 返回项目目录
buildozer clean
buildozer -v android debug

# 6. 完成
echo ""
echo "[6/6] 打包完成！"
echo "=========================================="
echo "APK 文件位置：bin/zhouyi-1.0.0-debug.apk"
echo "=========================================="

# 显示文件信息
if [ -f "bin/zhouyi-1.0.0-debug.apk" ]; then
    ls -lh bin/zhouyi-1.0.0-debug.apk
    echo ""
    echo "安装命令：adb install bin/zhouyi-1.0.0-debug.apk"
else
    echo "警告：APK 文件未生成"
    exit 1
fi
```

---

## 使用方法

### 在 WSL2 Ubuntu 中执行

```bash
# 1. 保存脚本
cd ~/workspace/projects/zhouyi
nano quick_build.sh
# 粘贴上述脚本内容，保存退出

# 2. 添加执行权限
chmod +x quick_build.sh

# 3. 执行打包
./quick_build.sh
```

### 手动分步执行

如果自动脚本失败，可以手动执行每一步：

```bash
# 步骤 1：更新系统
sudo apt update && sudo apt upgrade -y

# 步骤 2：安装依赖
sudo apt install -y python3 python3-pip python3-venv
sudo apt install -y git zip unzip openjdk-11-jdk
sudo apt install -y autoconf automake build-essential libssl-dev
sudo apt install -y libffi-dev libgstreamer1.0-dev
sudo apt install -y libsdl2-dev libsdl2-image-dev libsdl2-ttf-dev

# 步骤 3：安装 Kivy 和 Buildozer
pip3 install kivy
pip3 install buildozer

# 步骤 4：设置 Android SDK
export ANDROID_HOME=$HOME/android
export ANDROID_SDK_ROOT=$HOME/android
export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools

# 步骤 5：初始化 SDK
mkdir -p $ANDROID_HOME
cd $ANDROID_HOME
wget https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip
unzip commandlinetools-linux-9477386_latest.zip
mkdir -p cmdline-tools/latest
mv cmdline-tools/* cmdline-tools/latest/
yes | sdkmanager --licenses
sdkmanager "platform-tools" "platforms;android-33" "ndk;25.2.9519653"

# 步骤 6：打包 APK
cd ~/workspace/projects/zhouyi
buildozer init  # 如已有 buildozer.spec 可跳过
buildozer -v android debug
```

---

## 故障排查

### 问题 1：WSL2 未安装

**解决：**
```powershell
# Windows PowerShell（管理员）
wsl --install -d Ubuntu
```
重启电脑后完成安装。

### 问题 2：磁盘空间不足

Buildozer 需要约 5GB 空间。

**解决：**
```bash
# 清理 WSL2 磁盘
wsl --shutdown
wsl --export Ubuntu ubuntu.tar
wsl --unregister Ubuntu
wsl --import Ubuntu C:\WSL\ubuntu.tar --version 2
```

### 问题 3：下载速度慢

**解决：** 使用国内镜像
```bash
export PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
```

### 问题 4：Java 版本错误

需要 Java 11。

**解决：**
```bash
sudo apt install -y openjdk-11-jdk
sudo update-alternatives --config java
```

---

## 预期输出

成功打包后，您将看到：

```
# (many build logs...)
# PACKAGE SUCCESSFULLY

APK created at: bin/zhouyi-1.0.0-debug.apk
```

APK 文件大小：约 25-35MB

---

**工部 制**  
**2026 年 3 月 20 日**
