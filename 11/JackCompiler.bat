@echo off

set SELF=%0

set ARG1=%1

if not defined ARG1 (
	echo Jack file or directory name required !
	exit /b 1
)

if not exist %ARG1% (
	echo %ARG1% not found !
	exit /b 2
)

REM Convert ARG1 to a Unix-style path :
set ARG2=%ARG1:\=/%

REM __ If ARG1 is a directory, check if the Jack source has not been modified 
REM after any xml files :
if not exist %ARG1%\nul goto SKIPCTRL

pushd %CD%
cd %ARG1%

if not exist *T.xml (
	popd
	echo XML outputs missing : calling JackTokenizer...
	call JackTokenizer.bat %ARG1%
	if errorlevel 1 exit /b 9
	goto SKIPCTRL
)

for /F %%F in ('dir /b /od *T.xml *.jack') do @set LASTEXT=%%~xF
popd
if "%LASTEXT%"==".jack" (
	echo Jack code is newer than XML outputs : calling JackTokenizer...
	call JackTokenizer.bat %ARG1%
	if errorlevel 1 exit /b 3
)

:SKIPCTRL
echo %SELF%, %DATE%-%TIME%, Calling JackCompiler.py with %ARG2%

call python.exe JackCompiler.py %ARG2%
set RC=%ERRORLEVEL%

if %RC% NEQ 0 (
	echo %SELF%, %DATE%-%TIME%, Compilation failed, rc = %RC% !
	exit /b %RC%
)

for %%I in (%ARG1%) do @set PRJDIR=%%~nI
if not exist %PRJDIR%\nul (
	echo %PRJDIR% is not a provided program =^> no VM file verification...
	exit /b 0
)

if not exist %PRJDIR%\*.vm (
	echo No VM files in %PRJDIR% =^> no result verification...
	exit /b 0
)

set CURCKLST=%TEMP%\%SELF%.Perso.%PRJDIR%.lst
set PRJCKLST=%TEMP%\%SELF%.%PRJDIR%.lst

echo.
echo Calculating checksums of produced VM files in %CURCKLST%...
call :CALCCKSUM %CURCKLST% %ARG1%
echo Calculating checksums of official VM files in %PRJCKLST%...
call :CALCCKSUM %PRJCKLST% %PRJDIR%

fc %CURCKLST% %PRJCKLST% 1>nul
if errorlevel 1 (
	echo The lists are different : verify if needed with VMEmulator.bat !
) else (
	echo OK : the lists are identical !
)

exit /b 0

:CALCCKSUM
set OUTLIST=%1
set VMDIR=%2
if exist %OUTLIST% del %OUTLIST% 1>nul || exit /b 1
for /f %%C in ('cksum %VMDIR%\*.vm') do @echo %%C  >> %OUTLIST%
exit /b 0
