# 周易占卜 - Windows 可执行文件打包脚本
# 使用 PyInstaller 打包为 .exe

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  周易占卜 - Windows 打包工具" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan

# 检查 PyInstaller 是否安装
Write-Host "`n[1/4] 检查 PyInstaller..." -ForegroundColor Yellow
try {
    $pyinstaller = pip show pyinstaller -ErrorAction Stop
    Write-Host "PyInstaller 已安装" -ForegroundColor Green
} catch {
    Write-Host "正在安装 PyInstaller..." -ForegroundColor Yellow
    pip install pyinstaller --quiet
    Write-Host "PyInstaller 安装完成" -ForegroundColor Green
}

# 进入项目目录
Write-Host "`n[2/4] 进入项目目录..." -ForegroundColor Yellow
Set-Location $PSScriptRoot

# 清理旧的构建文件
Write-Host "`n[3/4] 清理旧文件..." -ForegroundColor Yellow
if (Test-Path "build") {
    Remove-Item -Recurse -Force "build"
    Write-Host "清理 build 目录" -ForegroundColor Green
}
if (Test-Path "dist") {
    Remove-Item -Recurse -Force "dist"
    Write-Host "清理 dist 目录" -ForegroundColor Green
}

# 打包
Write-Host "`n[4/4] 开始打包..." -ForegroundColor Yellow
Write-Host "这可能需要几分钟..." -ForegroundColor Yellow

pyinstaller --onefile `
            --windowed `
            --name "周易占卜" `
            --add-data "zhouyi/data/hexagrams.json;zhouyi\data" `
            --hidden-import flet `
            zhouyi/mobile/main.py

# 检查结果
if (Test-Path "dist\周易占卜.exe") {
    Write-Host "`n======================================" -ForegroundColor Green
    Write-Host "  打包成功！" -ForegroundColor Green
    Write-Host "======================================" -ForegroundColor Green
    Write-Host "`n可执行文件位置：" -ForegroundColor Cyan
    Write-Host "  $(Get-Location)\dist\周易占卜.exe" -ForegroundColor White
    Write-Host "`n文件大小：$(Get-Item "dist\周易占卜.exe" | Select-Object -ExpandProperty Length) 字节" -ForegroundColor Cyan
} else {
    Write-Host "`n======================================" -ForegroundColor Red
    Write-Host "  打包失败！" -ForegroundColor Red
    Write-Host "======================================" -ForegroundColor Red
    Write-Host "请检查错误日志" -ForegroundColor Yellow
}

Write-Host "`n按任意键退出..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
