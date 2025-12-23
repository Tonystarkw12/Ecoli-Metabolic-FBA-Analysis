@echo off
REM 大肠杆菌代谢FBA分析工具 - 快速安装脚本
REM 适用于 Windows 系统

echo ========================================
echo E. coli Metabolic FBA Analysis Setup
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python 3.9+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [✓] Python 已安装

REM 检查pip是否可用
pip --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到pip
    pause
    exit /b 1
)
echo [✓] pip 已安装

REM 创建虚拟环境（推荐）
echo.
echo [提示] 建议创建虚拟环境以避免依赖冲突
set /p create_venv="是否创建虚拟环境? (y/n, 默认y): "
if /i "%create_venv%"=="n" goto install_deps

echo [1/3] 创建虚拟环境...
python -m venv venv
if errorlevel 1 (
    echo [错误] 虚拟环境创建失败
    pause
    exit /b 1
)
echo [✓] 虚拟环境创建成功

REM 激活虚拟环境
call venv\Scripts\activate.bat
echo [✓] 虚拟环境已激活

:install_deps
echo.
echo [2/3] 安装依赖库...
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
if errorlevel 1 (
    echo [错误] 依赖安装失败，请检查网络连接
    pause
    exit /b 1
)
echo [✓] 依赖安装成功

REM 检查数据文件
echo.
echo [3/3] 检查数据文件...
if not exist "data\iJO1366.xml" (
    echo [提示] 未找到数据文件 data\iJO1366.xml
    echo.
    echo 请按以下步骤操作：
    echo 1. 访问 https://bigg.ucsd.edu/models/iJO1366
    echo 2. 点击 "Download SBML" 下载 iJO1366.xml
    echo 3. 将文件放入 data/ 文件夹中
    echo.
    set /p download_now="是否现在打开下载页面? (y/n): "
    if /i "%download_now%"=="y" (
        start https://bigg.ucsd.edu/models/iJO1366
    )
) else (
    echo [✓] 数据文件已存在
)

echo.
echo ========================================
echo 安装完成！
echo ========================================
echo.
echo 下一步：
echo 1. 将 iJO1366.xml 放入 data/ 文件夹（如果还没有）
echo 2. 运行: python src\main.py
echo 3. 查看 results/ 文件夹中的结果
echo.
echo 如果使用虚拟环境，下次运行前请先执行:
echo    call venv\Scripts\activate.bat
echo.
pause