@echo off
setlocal enabledelayedexpansion

:: 设置虚拟环境名称
set VENV_NAME=venv

:: 检查虚拟环境是否存在
if not exist %VENV_NAME% (
    echo 创建虚拟环境...
    python -m venv %VENV_NAME%
    if errorlevel 1 (
        echo 创建虚拟环境失败。请确保已安装 Python 并添加到 PATH。
        pause
        exit /b 1
    )
)

:: 激活虚拟环境
call %VENV_NAME%\Scripts\activate.bat

:: 检查并安装依赖
echo 检查依赖...
python -c "import fastapi" 2>NUL
if errorlevel 1 (
    echo 安装 fastapi...
    pip install fastapi
)

python -c "import uvicorn" 2>NUL
if errorlevel 1 (
    echo 安装 uvicorn...
    pip install uvicorn
)

python -c "import edge_tts" 2>NUL
if errorlevel 1 (
    echo 安装 edge-tts...
    pip install edge-tts
)

:: 运行主程序
echo 启动程序...
python main.py

:: 如果程序异常退出，暂停以查看错误信息
if errorlevel 1 (
    echo 程序异常退出。
    pause
)

:: 停用虚拟环境
deactivate