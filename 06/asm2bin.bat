@echo off

set ASMFILE=%1

if not defined ASMFILE (
	echo The asm file is mandatory !
	exit /b 1
)

if not exist %ASMFILE% (
	echo %ASMFILE% not found !
	exit /b 2
)

call python.exe asm2bin.py %ASMFILE%
set RC=%ERRORLEVEL%

if %RC% NEQ 0 echo Assembly failure, rc = %RC% !

exit /b %RC%
