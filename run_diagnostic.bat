@echo off
cd /d "%~dp0"
echo ============================================
echo  TEST 1: Raw OpenAI tool call (no Flask)
echo ============================================
venv311\Scripts\python.exe -X utf8 test_tools.py
echo.
echo ============================================
echo  TEST 2: Live Joi chat endpoint
echo  (Make sure joi_companion.py is running!)
echo ============================================
venv311\Scripts\python.exe -X utf8 test_chat.py
echo.
echo ============================================
echo  OpenAI error log (data\openai_error.log):
echo ============================================
if exist data\openai_error.log (
    type data\openai_error.log
) else (
    echo  No errors logged yet.
)
echo.
pause
