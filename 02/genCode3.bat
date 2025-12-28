@echo off 

for /L %%N in (0,4,12) do call :GENLINE %%N

exit /b 0

:GENLINE
set CUR=%1
set /A NEXT=%CUR%+2
echo Or(a=bb%CUR%, b=bb%NEXT%, out=bbb%CUR%);
exit /b 0
