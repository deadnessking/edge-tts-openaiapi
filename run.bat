@echo off
setlocal enabledelayedexpansion

:: �������⻷������
set VENV_NAME=venv

:: ������⻷���Ƿ����
if not exist %VENV_NAME% (
    echo �������⻷��...
    python -m venv %VENV_NAME%
    if errorlevel 1 (
        echo �������⻷��ʧ�ܡ���ȷ���Ѱ�װ Python ����ӵ� PATH��
        pause
        exit /b 1
    )
)

:: �������⻷��
call %VENV_NAME%\Scripts\activate.bat

:: ��鲢��װ����
echo �������...
python -c "import fastapi" 2>NUL
if errorlevel 1 (
    echo ��װ fastapi...
    pip install fastapi
)

python -c "import uvicorn" 2>NUL
if errorlevel 1 (
    echo ��װ uvicorn...
    pip install uvicorn
)

python -c "import edge_tts" 2>NUL
if errorlevel 1 (
    echo ��װ edge-tts...
    pip install edge-tts
)

:: ����������
echo ��������...
python main.py

:: ��������쳣�˳�����ͣ�Բ鿴������Ϣ
if errorlevel 1 (
    echo �����쳣�˳���
    pause
)

:: ͣ�����⻷��
deactivate