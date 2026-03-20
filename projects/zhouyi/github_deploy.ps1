Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "        周易占卜系统 v2.0.0 - GitHub 一键部署" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[1/5] 检查 Git 安装..." -ForegroundColor Yellow
git --version
Write-Host ""

Write-Host "[2/5] 切换到项目目录..." -ForegroundColor Yellow
Set-Location $PSScriptRoot
Write-Host "当前目录：$(Get-Location)" -ForegroundColor Green
Write-Host ""

Write-Host "[3/5] 配置 GitHub 信息..." -ForegroundColor Yellow
$githubUsername = Read-Host "请输入 GitHub 用户名"
$repoUrl = "https://github.com/$githubUsername/zhouyi.git"
Write-Host "仓库地址：$repoUrl" -ForegroundColor Green
Write-Host ""

Write-Host "[4/5] 配置 remote 并推送..." -ForegroundColor Yellow
git config user.email "zhouyi@example.com"
git config user.name "Zhouyi Project"
git remote set-url origin $repoUrl
git branch -M main
Write-Host "正在推送代码..." -ForegroundColor Yellow
git push -u origin main --force
Write-Host ""

Write-Host "[5/5] 创建版本标签 v1.0.0..." -ForegroundColor Yellow
git tag -a v1.0.0 -m "Zhouyi v1.0.0"
git push origin v1.0.0 --force
Write-Host ""

Write-Host "============================================================" -ForegroundColor Green
Write-Host "        部署成功！" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "请访问 GitHub Actions 下载 APK:" -ForegroundColor Cyan
Write-Host "$repoUrl/actions" -ForegroundColor Cyan
Write-Host ""
Write-Host "按任意键退出..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
