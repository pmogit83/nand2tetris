@echo off
REM ---------------------------------------------------------------------------
REM If *.vm.check files exist in the project directory, they are compared with
REM the *.vm files created by the compilation. Otherwise, the last line of the 
REM out file is displayed. It may contain, for example :
REM The lists are different: verify if needed with VMEmulator.bat!
REM
REM ---------------------------------------------------------------------------

if not exist out\nul (mkdir out || exit /b 2)

for %%D in (Average ComplexArrays Seven ConvertToBin Square Pong Exemple_forum) do call :CHECK %%D

exit /b 0

:CHECK
set PRJ=%1
echo Checking %PRJ%...
call JackCompiler.bat Perso\%PRJ% > out\JackCompiler.%PRJ%.out
if exist Perso\%PRJ%\*.vm.check (
	call :LOCALCHECK
) else (
	tail -1 out\JackCompiler.%PRJ%.out
)
echo --------------------------------------------------------------------------
exit /b 0

:LOCALCHECK
set RC=0
for %%V in (Perso\%PRJ%\*.vm.check) do (
	fc %%V %%~dpnV > nul
	if errorlevel 1 (
		echo %%V and %%~dpnV are different !
		set RC=1
	)
)
if %RC% EQU 0 echo Comparison between vm files and vm.check files OK !
exit /b 0
