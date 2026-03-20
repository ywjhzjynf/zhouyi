# 周易占卜系统 APK 打包文档

**版本：** v1.0.0  
**日期：** 2026 年 3 月 20 日  
**状态：** ✅ 代码适配完成，待打包

---

## 📦 打包方案

### 推荐方案：Kivy + Buildozer（Linux 环境）

由于 Buildozer 仅支持 Linux/Mac 环境，Windows 用户需使用以下方法之一：

#### 方法 A：WSL2（推荐）
1. 安装 WSL2 Ubuntu
2. 在 WSL2 中安装 Buildozer
3. 执行打包

#### 方法 B：Docker 容器
使用预配置的 Buildozer Docker 镜像

#### 方法 C：在线打包服务
使用 GitHub Actions 或云构建服务

---

## 🚀 快速打包指南

### 方法 A：WSL2 打包（推荐）

#### 1. 安装 WSL2

```powershell
# Windows PowerShell（管理员）
wsl --install -d Ubuntu
```

重启电脑后，从 Microsoft Store 安装 Ubuntu。

#### 2. 在 Ubuntu 中安装依赖

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装 Python 和依赖
sudo apt install -y python3 python3-pip python3-venv
sudo apt install -y git zip unzip openjdk-11-jdk
sudo apt install -y autoconf automake build-essential libssl-dev
sudo apt install -y libffi-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
sudo apt install -y libsdl2-dev libsdl2-image-dev libsdl2-ttf-dev libsdl2-gfx-dev
sudo apt install -y libmixer-dev libv4l-dev ffmpeg libportmidi-dev
sudo apt install -y libswscale-dev libavformat-dev libavcodec-dev
sudo apt install -y zlib1g-dev libgstreamer-plugins-base1.0-dev gstreamer1.0-plugins-good

# 安装 Java（Android SDK 需要）
sudo apt install -y openjdk-11-jdk
```

#### 3. 安装 Android SDK 和 NDK

```bash
# 创建 Android 目录
mkdir -p ~/android
cd ~/android

# 下载 Android SDK 命令行工具
wget https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip
unzip commandlinetools-linux-9477386_latest.zip
mkdir -p cmdline-tools/latest
mv cmdline-tools/* cmdline-tools/latest/ 2>/dev/null || true

# 设置环境变量
export ANDROID_HOME=$HOME/android
export ANDROID_SDK_ROOT=$HOME/android
export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools

# 接受许可证并安装 SDK
yes | sdkmanager --licenses
sdkmanager "platform-tools" "platforms;android-33"
sdkmanager "ndk;25.2.9519653"
```

#### 4. 安装 Buildozer

```bash
# 创建项目虚拟环境
cd ~/workspace/projects/zhouyi
python3 -m venv venv
source venv/bin/activate

# 安装 Kivy 和 Buildozer
pip install --upgrade pip
pip install kivy
pip install buildozer
```

#### 5. 配置 buildozer.spec

```bash
# 初始化 buildozer.spec（如已存在可跳过）
buildozer init

# 编辑 buildozer.spec，确保以下配置正确：
# - requirements = python3,kivy
# - android.minapi = 21
# - android.api = 33
# - android.ndk = 25b
```

#### 6. 执行打包

```bash
# 清理旧构建
buildozer clean

# 下载依赖并编译
buildozer -v android debug

# 打包完成后，APK 位于：
# bin/zhouyi-1.0.0-debug.apk
```

#### 7. 测试 APK

```bash
# 连接 Android 手机（USB 调试模式）
adb devices

# 安装 APK
adb install bin/zhouyi-1.0.0-debug.apk
```

---

### 方法 B：Docker 打包

#### 1. 安装 Docker Desktop

从 https://www.docker.com/products/docker-desktop 下载并安装。

#### 2. 使用 Buildozer Docker 镜像

```bash
# 进入项目目录
cd C:\Users\25243\.openclaw\workspace\projects\zhouyi

# 运行 Docker 容器
docker run --rm -v ${PWD}:/home/user/hostcwd \
    kivy/buildozer:latest android debug
```

#### 3. 获取 APK

打包完成后，APK 文件位于 `bin/` 目录。

---

### 方法 C：GitHub Actions 自动打包

#### 1. 创建 `.github/workflows/build.yml`

```yaml
name: Build APK

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y python3-pip python3-venv
          pip install buildozer
          sudo apt-get install -y autoconf automake build-essential libssl-dev
          sudo apt-get install -y libffi-dev libgstreamer1.0-dev
          sudo apt-get install -y libsdl2-dev libsdl2-image-dev libsdl2-ttf-dev
      
      - name: Build APK
        run: |
          buildozer -v android debug
      
      - name: Upload APK
        uses: actions/upload-artifact@v3
        with:
          name: zhouyi-apk
          path: bin/*.apk
```

#### 2. 推送代码并触发构建

```bash
git add .
git commit -m "Release v1.0.0"
git tag v1.0.0
git push origin v1.0.0
```

#### 3. 下载 APK

在 GitHub Actions 页面下载构建产物。

---

## 📱 移动端 UI 说明

### 界面设计

- **主菜单**：四个起卦方法按钮
- **铜钱起卦**：点击抛掷，逐爻显示
- **蓍草起卦**：一键演算，模拟传统流程
- **数字起卦**：输入数字，即时转换
- **时间起卦**：当前时间自动起卦

### 触摸优化

- 大按钮设计（适合手指点击）
- 竖屏模式（portrait）
- 自适应布局（不同屏幕尺寸）
- 简洁交互（减少输入）

---

## 📊 打包配置说明

### buildozer.spec 关键参数

```ini
[app]
title = 周易占卜              # App 名称
package.name = zhouyi         # 包名
package.domain = org.zhouyi   # 包域名
version = 1.0.0              # 版本号

requirements = python3,kivy   # 依赖包
orientation = portrait        # 屏幕方向

android.minapi = 21          # 最低 Android 版本（5.0）
android.api = 33             # 目标 Android 版本（13）
android.ndk = 25b            # NDK 版本
android.arch = arm64-v8a     # CPU 架构（64 位）
```

### 权限配置

```ini
android.permissions = INTERNET
# 如需保存历史记录，添加：
# android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE
```

---

## 🐛 常见问题

### 1. Buildozer 下载依赖失败

```bash
# 使用国内镜像
export PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
```

### 2. Android SDK 许可证未接受

```bash
yes | sdkmanager --licenses
```

### 3. 编译错误：找不到 SDL2

```bash
sudo apt install -y libsdl2-dev libsdl2-image-dev libsdl2-ttf-dev
```

### 4. APK 太大

优化方法：
- 移除未使用的资源文件
- 使用 `--release` 模式构建
- 启用代码压缩

```bash
buildozer -v android release
```

### 5. 安装失败：解析包错误

检查 `android.minapi` 和 `android.api` 设置，确保与手机兼容。

---

## 📝 打包检查清单

- [ ] 代码适配完成（mobile_main.py）
- [ ] buildozer.spec 配置正确
- [ ] 六十四卦数据完整（hexagrams.json）
- [ ] 测试所有起卦方法
- [ ] 检查 UI 显示（无乱码）
- [ ] APK 签名（发布版本）
- [ ] 编写使用说明

---

## 📦 交付物

| 文件 | 说明 |
|------|------|
| `mobile_main.py` | Kivy 移动端主程序 |
| `buildozer.spec` | Buildozer 配置文件 |
| `bin/zhouyi-1.0.0-debug.apk` | 调试版 APK |
| `bin/zhouyi-1.0.0-release.apk` | 发布版 APK（签名） |
| `APK_PACKAGING.md` | 本文档 |

---

## 🎯 下一步

1. **工部**：完成环境搭建和 APK 打包
2. **兵部**：验证算法在移动端的准确性
3. **礼部**：编写用户使用手册
4. **门下省**：质量审核
5. **尚书省**：最终交付

---

**工部尚书 谨呈**  
**2026 年 3 月 20 日**
