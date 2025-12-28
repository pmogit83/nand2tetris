@echo off 

for /L %%N in (0,2,14) do call :GENLINE %%N

exit /b 0

:GENLINE
set CUR=%1
set /A NEXT=%CUR%+1
echo Or(a=b%CUR%, b=b%NEXT%, out=bb%CUR%);
exit /b 0
