@echo off
REM ---------------------------------------------------------------------------
REM JackTokenizer.bat Perso\ArrayTest > JackTokenizer.out
REM JackParser.bat Perso\ArrayTest > JackParser.out
REM call ..\..\tools\TextComparer.bat ArrayTest\Main.xml Perso\ArrayTest\Main.xml
REM Comparison ended successfully
REM call ..\..\tools\TextComparer.bat ArrayTest\MainT.xml Perso\ArrayTest\MainT.xml
REM Comparison ended successfully
REM ---------------------------------------------------------------------------

set COMPTOOL=..\..\tools\TextComparer.bat

for %%D in (ArrayTest ExpressionLessSquare Square) do call :VALIDATE %%D

exit /b 0

:VALIDATE
set TSTDIR=%1
set WRKDIR=Perso\%TSTDIR%

set OUTFILE=JackTokenizer.%TSTDIR%.out
echo Calling JackTokenizer.bat on %WRKDIR%...
call JackTokenizer.bat %WRKDIR% > %OUTFILE%
if errorlevel 1 (
	echo At least one error : see %OUTFILE% !
	exit /b 1
)

set OUTFILE=JackParser.%TSTDIR%.out
echo Calling JackParser.bat on %WRKDIR%...
call JackParser.bat %WRKDIR% > %OUTFILE%
if errorlevel 1 (
	echo At least one error : see %OUTFILE% !
	exit /b 1
)

for %%T in (%TSTDIR%\*.xml) do (
	echo Comparing %%T and Perso\%%T...
	call %COMPTOOL% %%T Perso\%%T
	if errorlevel 1 (
		echo Comparison error between %%T and Perso\%%T !
		exit /b 2
	)
)

exit /b 0
