@echo off 


for /L %%N in (3,1,15) do call :GENLINE %%N

exit /b 0

:GENLINE
set CUR=%1
set /A PREV=%CUR%-1
echo FullAdder(a=a[%CUR%], b=b[%CUR%], c=c%PREV%, sum=out[%CUR%], carry=c%CUR%);
exit /b 0
