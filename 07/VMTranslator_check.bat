@echo off

REM ------------------------------------------------------------- Description :
REM Calls VMTranslator.bat for each VM file located in the 5 test 
REM sub-directories : 
REM 	MemoryAccess\BasicTest\BasicTest.vm
REM 	MemoryAccess\PointerTest\PointerTest.vm
REM 	MemoryAccess\StaticTest\StaticTest.vm
REM 	StackArithmetic\SimpleAdd\SimpleAdd.vm
REM 	StackArithmetic\StackTest\StackTest.vm
REM 
REM If the call is ok, an asm file corresponding to the VM file must be 
REM created. For example : MemoryAccess\BasicTest\BasicTest.asm
REM 
REM The xxx.asm file is then compared to xxx.asm.check located in the same 
REM sub-directory.
REM ---------------------------------------------------------------------------
 

setlocal

set LOGFILE=%TEMP%\VMTranslator_check.log

if exist %LOGFILE% (del %LOGFILE% 1>nul || exit /b 1) 

call :VMCHECK MemoryAccess\BasicTest\BasicTest.vm
call :VMCHECK MemoryAccess\PointerTest\PointerTest.vm
call :VMCHECK MemoryAccess\StaticTest\StaticTest.vm
call :VMCHECK StackArithmetic\SimpleAdd\SimpleAdd.vm
call :VMCHECK StackArithmetic\StackTest\StackTest.vm

exit /b 0

:VMCHECK
set VMFILE=%1
set PREFIX=%~dpn1
set RESFILE=%PREFIX%.asm
set CHECKFILE=%RESFILE%.check
echo Output to validate : %RESFILE%
echo Check file         : %CHECKFILE%
call VMTranslator.bat %VMFILE% >> %LOGFILE%
echo. >> %LOGFILE%
if errorlevel 1 (
	echo RC VMTranslator.bat = %ERRORLEVEL%, see %LOGFILE%
	exit /b 1
)
fc %RESFILE% %CHECKFILE% 1>nul && exit /b 0
echo Error : %RESFILE% and %CHECKFILE% are not the same !
exit /b 1
