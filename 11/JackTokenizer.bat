@echo off

set ARG1=%1

if not defined ARG1 (
	echo echo Jack file or directory name required !
	exit /b 1
)

if not exist %ARG1% (
	echo %ARG1% not found !
	exit /b 2
)

call python.exe JackTokenizer.py %ARG1%
set RC=%ERRORLEVEL%

if %RC% NEQ 0 echo Conversion failure, rc = %RC% !

exit /b %RC%
