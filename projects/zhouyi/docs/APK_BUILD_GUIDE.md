# 周易占卜 - Android APK 打包指南

**版本：** v1.0.0  
**更新时间：** 2026-03-20  
**技术栈：** Python + Flet

---

## 📦 打包方式

### 方式一：Flet 内置打包（推荐）

Flet 提供简单的 APK 打包命令：

```bash
# 安装 Android 打包依赖
pip install flet[all]

# 打包 APK
cd zhouyi
flet build apk
```

### 方式二：手动打包

如需更多控制，可使用以下步骤：

#### 1. 安装 Buildozer（Linux/macOS）

```bash
pip install buildozer
```

#### 2. 创建 buildozer.spec

```bash
buildozer init
```

编辑 `buildozer.spec`:

```ini
[app]
title = 周易占卜
package.name = zhouyi
package.domain = org.zhouyi
source.dir = .
source.include_exts = py,json,html
version = 1.0.0
requirements = python3,flet
orientation = portrait
osx.python_version = 3.11
```

#### 3. 打包

```bash
buildozer -v android debug
```

---

## 📱 APK 输出

打包完成后，APK 文件位于：

- **调试版：** `bin/zhouyi-1.0.0-debug.apk`
- **发布版：** `bin/zhouyi-1.0.0-release.apk`

---

## 🔧 前提条件

### Android SDK

需要安装 Android SDK 和构建工具：

1. 下载 Android Studio
2. 安装 SDK Tools
3. 设置环境变量：
   - `ANDROID_HOME`
   - `PATH` 添加 `$ANDROID_HOME/tools` 和 `$ANDROID_HOME/platform-tools`

### Java JDK

需要 Java 8 或更高版本：

```bash
java -version
```

---

## 📋 功能清单

### v1.0.0 包含功能

- ✅ 铜钱起卦（金钱卦）
- ✅ 蓍草起卦（大衍之数）
- ✅ 数字起卦
- ✅ 时间起卦（梅花易数）
- ✅ 卦象显示（卦名、卦辞、象曰）
- ✅ 64 卦完整数据
- ⏳ 历史记录（开发中）
- ⏳ 卦象详解（开发中）

---

## 🎨 界面预览

主界面包含：
- 标题区域（☯ 周易占卜）
- 四种起卦方式按钮
- 卦象结果显示区
- 历史记录入口

---

## 🐛 常见问题

### Q: 打包时提示 Android SDK 未找到
A: 确保已安装 Android Studio 并设置 ANDROID_HOME 环境变量

### Q: APK 安装后闪退
A: 检查日志：`adb logcat | grep zhouyi`

### Q: 中文显示乱码
A: 确保文件编码为 UTF-8，并在 Android 设备上安装中文字体

---

## 📞 技术支持

如有问题，请联系：
- 工部：负责 APK 打包
- 兵部：负责算法问题
- 户部：负责数据问题

---

**尚书省 & 工部 联合编制**  
2026 年 3 月 20 日
