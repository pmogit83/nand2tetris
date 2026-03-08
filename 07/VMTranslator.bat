@echo off

set ARG1=%1

if not defined ARG1 (
	echo VM file or VM files directory expected !
	exit /b 1
)

if not exist %ARG1% (
	echo %ARG1% was not found !
	exit /b 2
)

call python.exe VMTranslator.py %ARG1%
set RC=%ERRORLEVEL%

if %RC% NEQ 0 echo Conversion failure, rc = %RC% !

exit /b %RC%
