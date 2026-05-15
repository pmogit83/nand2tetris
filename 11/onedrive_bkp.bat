@echo off

set FILESPEC=%*

if not defined FILESPEC (
	echo Erreur  : specification de fichiers manquante !
	echo Exemple : %0 *.py
	exit /b 1
)
 
set ODDEST=C:\Perso\OneDriveSrcDir\OneDrive\Work\nand2tetris\projects\11
echo Destination : %ODDEST%

attrib -R %ODDEST%\%*
copy /Y %* %ODDEST% || (
	echo erreur de copie ! [ESPACE]
	pause > nul
)

exit /b 0

