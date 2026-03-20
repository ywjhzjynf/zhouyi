# 周易占卜 APK 打包 - 执行清单

**任务 ID：** TASK-20260320-016  
**状态：** ✅ 代码就绪，⏳ 待打包  

---

## 🎯 快速执行（推荐 GitHub Actions）

### 第一步：推送到 GitHub

```powershell
# Windows PowerShell（在项目目录执行）
cd C:\Users\25243\.openclaw\workspace\projects\zhouyi

# 初始化 Git
git init
git add .
git commit -m "Mobile version v1.0.0"

# 创建 GitHub 仓库（在 github.com 创建后）
git remote add origin https://github.com/YOUR_USERNAME/zhouyi.git
git push -u origin main
```

### 第二步：触发打包

```powershell
# 打标签（触发自动打包）
git tag v1.0.0
git push origin v1.0.0
```

### 第三步：下载 APK

1. 访问：https://github.com/YOUR_USERNAME/zhouyi/actions
2. 点击最新的 "Build Android APK" 任务
3. 在底部 "Artifacts" 下载 `zhouyi-apk-debug`
4. 解压得到 APK 文件

**预计耗时：** 20-30 分钟（首次构建）

---

## 🐧 备选方案：WSL2 本地打包

### 第一步：安装 WSL2

```powershell
# Windows PowerShell（管理员）
wsl --install -d Ubuntu
```

重启电脑，完成 Ubuntu 安装（设置用户名密码）。

### 第二步：执行打包脚本

```bash
# 在 Ubuntu 终端执行
cd /mnt/c/Users/25243/.openclaw/workspace/projects/zhouyi

# 执行一键打包脚本
chmod +x QUICK_BUILD.sh
./QUICK_BUILD.sh
```

### 第三步：获取 APK

```bash
# 打包完成后
ls -lh bin/zhouyi-1.0.0-debug.apk

# 复制到 Windows 目录
cp bin/zhouyi-1.0.0-debug.apk /mnt/c/Users/25243/Downloads/
```

**预计耗时：** 30-40 分钟（含下载时间）

---

## 📱 安装测试

### 方法一：USB 连接

```bash
# 手机开启 USB 调试，连接电脑
adb devices
adb install zhouyi-1.0.0-debug.apk
```

### 方法二：直接传输

1. 将 APK 文件发送到手机
2. 在手机上打开 APK
3. 允许"未知来源"安装
4. 完成安装

---

## ✅ 验证清单

安装后验证：

- [ ] App 图标显示正常
- [ ] 启动无闪退
- [ ] 主菜单显示 4 个按钮
- [ ] 铜钱起卦：抛掷 6 次，显示卦象
- [ ] 蓍草起卦：点击演算，显示结果
- [ ] 数字起卦：输入数字，生成卦象
- [ ] 时间起卦：显示当前时间卦象
- [ ] 返回主菜单功能正常
- [ ] 中文显示无乱码

---

## 📂 文件清单

### 已交付（已完成）

```
zhouyi/
├── mobile_main.py              ✅ Kivy 主程序
├── buildozer.spec              ✅ 打包配置
├── requirements_mobile.txt     ✅ 依赖清单
├── QUICK_BUILD.sh              ✅ 打包脚本
├── APK_PACKAGING.md            ✅ 打包指南
├── MOBILE_USER_GUIDE.md        ✅ 用户说明
├── FINAL_DELIVERY_REPORT.md    ✅ 交付报告
├── APK_PROGRESS_REPORT.md      ✅ 进度报告
└── .github/
    └── workflows/
        └── build.yml           ✅ 自动打包配置
```

### 待生成（需执行打包）

```
zhouyi/
└── bin/
    ├── zhouyi-1.0.0-debug.apk     ⏳ 调试版
    └── zhouyi-1.0.0-release.apk   ⏳ 发布版
```

---

## 🆘 常见问题

### Q1: GitHub Actions 失败？

**A:** 查看 Logs 找错误，常见问题：
- 依赖下载失败 → 重试即可
- 磁盘空间不足 → 清理 workspace
- SDK 许可证 → 脚本已自动处理

### Q2: WSL2 安装失败？

**A:** 
```powershell
# 启用 WSL 功能（管理员 PowerShell）
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

# 启用虚拟机平台
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# 重启后重试
wsl --install -d Ubuntu
```

### Q3: APK 安装失败？

**A:** 
- 检查 Android 版本 ≥ 5.0
- 允许"未知来源"安装
- 重新下载完整 APK

### Q4: 中文显示乱码？

**A:** 
- Kivy 自动支持中文
- 如仍乱码，检查系统字体
- 或尝试重启应用

---

## 📞 支持文档

详细文档：

1. **打包指南** - APK_PACKAGING.md
2. **用户说明** - MOBILE_USER_GUIDE.md
3. **交付报告** - FINAL_DELIVERY_REPORT.md
4. **进度报告** - APK_PROGRESS_REPORT.md

---

## 🎉 完成标志

当看到以下内容时，表示任务完成：

```
✓ APK 文件生成：bin/zhouyi-1.0.0-debug.apk (约 30MB)
✓ 安装到手机测试通过
✓ 四种起卦方法正常工作
✓ 中文显示正常
✓ 触摸交互流畅
```

---

**工部 制**  
**2026 年 3 月 20 日 15:30**
