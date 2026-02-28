@echo off

setlocal

set LOGFILE=%TEMP%\asm2bin_check.log

if exist %LOGFILE% (del %LOGFILE% 1>nul || exit /b 1) 

call :ASMCHECK add\Add.asm
call :ASMCHECK max\MaxL.asm
call :ASMCHECK pong\PongL.asm
call :ASMCHECK pong\Pong.asm
call :ASMCHECK rect\RectL.asm
call :ASMCHECK rect\Rect.asm
call :ASMCHECK test_labels.asm
call :ASMCHECK test_vars.asm

exit /b 0

:ASMCHECK
set ASMFILE=%1
set PREFIX=%~dpn1
set RESFILE=%PREFIX%.hack
set CHECKFILE=%PREFIX%Check.hack
echo Checking %ASMFILE% against %CHECKFILE%...
call asm2bin.bat %ASMFILE% >> %LOGFILE%
if errorlevel 1 (
	echo RC asm2bin.bat = %ERRORLEVEL%, see %LOGFILE%
	exit /b 1
)
fc %RESFILE% %CHECKFILE% 1>nul && exit /b 0
echo Error : %RESFILE% and %CHECKFILE% are different !
exit /b 1
