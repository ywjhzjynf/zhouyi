# GitHub 仓库创建指南

## 📋 步骤一：创建 GitHub 仓库

### 1. 访问 GitHub
打开浏览器，访问：https://github.com/new

### 2. 填写仓库信息
- **Repository name:** `zhouyi`
- **Description:** 周易占卜系统 - 传承千年智慧
- **Visibility:** ✅ Public (公开)
- **Initialize this repository with:** ❌ 全部不勾选

### 3. 点击 "Create repository"

---

## 📋 步骤二：推送代码

仓库创建后，在 PowerShell 中执行以下命令：

```powershell
# 切换到项目目录
cd C:\Users\25243\.openclaw\workspace\projects\zhouyi

# 配置 remote（替换 YOUR_USERNAME 为您的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/zhouyi.git

# 切换到 main 分支
git branch -M main

# 推送代码（可能需要输入 GitHub 密码或 Personal Access Token）
git push -u origin main

# 打标签触发 APK 打包
git tag -a v1.0.0 -m "Zhouyi v1.0.0"
git push origin v1.0.0
```

---

## 📋 步骤三：等待 APK 构建

推送成功后：

1. 访问：`https://github.com/YOUR_USERNAME/zhouyi/actions`
2. 等待构建完成（约 20-30 分钟）
3. 点击构建任务
4. 在 **Artifacts** 部分下载 `zhouyi-apk.zip`
5. 解压获得 `zhouyi-1.0.0-debug.apk`

---

## 📋 步骤四：安装 APK

1. 将 APK 文件传输到 Android 手机
2. 在手机上安装 APK
3. 允许"未知来源应用"安装
4. 打开"周易占卜"应用

---

## 🔑 Personal Access Token 配置

如果推送失败，需要创建 Personal Access Token：

1. 访问：https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 填写 Note: `Zhouyi Deploy`
4. 选择 Scopes:
   - ✅ repo
   - ✅ workflow
5. 点击 "Generate token"
6. 复制生成的 token（只显示一次！）
7. 使用 token 推送：

```powershell
git remote set-url origin https://YOUR_TOKEN@github.com/YOUR_USERNAME/zhouyi.git
git push -u origin main
```

---

## ✅ 快速检查清单

- [ ] GitHub 仓库已创建
- [ ] Remote 已配置
- [ ] 代码已推送
- [ ] 标签 v1.0.0 已推送
- [ ] GitHub Actions 已开始运行
- [ ] APK 已下载
- [ ] APK 已安装到手机

---

## 🆘 常见问题

**Q: 推送时提示认证失败？**
A: 使用 Personal Access Token 代替密码

**Q: GitHub Actions 没有运行？**
A: 检查 `.github/workflows/build.yml` 是否存在

**Q: APK 构建失败？**
A: 查看 Actions 日志，通常是依赖问题

**Q: 构建时间太长？**
A: 首次构建需要 30-40 分钟，后续构建会更快

---

**祝部署顺利！** 🎉
