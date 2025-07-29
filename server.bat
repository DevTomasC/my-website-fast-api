REM SCRIPT .bat PRA WINDOWS XD!
@echo off
cls
echo -------------------------------------
echo Iniciando Server FastAPI local...
echo -------------------------------------

REM Ativa ambiente virtual
call venv\Scripts\activate.bat

REM Inicia o servidor Uvicorn
uvicorn app.main:app --reload

pause