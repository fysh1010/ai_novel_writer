@echo off
title AI小说创作引擎
echo ========================================
echo   AI小说创作引擎 v5.0
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未检测到Python环境
    echo 请先安装Python 3.8或更高版本
    echo.
    pause
    exit /b 1
)

REM 检查依赖是否安装
python -c "import lazyllm" >nul 2>&1
if %errorlevel% neq 0 (
    echo 正在安装依赖...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo 错误: 依赖安装失败
        pause
        exit /b 1
    )
)

echo 启动AI小说创作引擎...
echo.
python main.py

if %errorlevel% neq 0 (
    echo.
    echo 程序运行出错，请检查错误信息
)

echo.
echo 程序已退出
pause