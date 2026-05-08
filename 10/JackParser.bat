@echo off

set ARG1=%1

if not defined ARG1 (
	echo Expecting Jack source file or directory !
	exit /b 1
)

if not exist %ARG1% (
	echo %ARG1% not found !
	exit /b 2
)

call python.exe JackParser.py %ARG1%
set RC=%ERRORLEVEL%

if %RC% NEQ 0 echo Parsing failed, rc = %RC% !

exit /b %RC%
