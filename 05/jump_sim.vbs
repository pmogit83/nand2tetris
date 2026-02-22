' =============================================================================
' Description : 
' =============================================================================
Option Explicit

Dim j1, j2, j3, ng, zr, J, strMsg, nArg, strArg, nVal
Dim e1, e2, e3, e4, e5, e6, e7

If WScript.Arguments.Count <> 5 Then
    WScript.Echo WScript.ScriptName & " : erreur de syntaxe !"
    displaySyntaxe
    WScript.Quit(1)
End If

For nArg = 0 To WScript.Arguments.Count - 1
	strArg = WScript.Arguments(nArg)
	If Not IsNumeric(strArg) Then
		WScript.Echo WScript.ScriptName & " : " & strArg & " n'est pas numérique !"
	    displaySyntaxe
	    WScript.Quit(2)
	Else
		nVal = CInt(strArg)
		If nVal <> 0 And nVal <> 1 Then
			WScript.Echo WScript.ScriptName & " : " & nVal & " ni 0 ni 1 !"
		    displaySyntaxe
		    WScript.Quit(3)
		End If
		Select Case nArg:
		Case 0 : j1 = nVal
		Case 1 : j2 = nVal
		Case 2 : j3 = nVal
		Case 3 : ng = nVal
		Case 4 : zr = nVal
		End Select
	End If
Next

J = 4 * j1 + 2 * j2 + j3

WScript.StdOut.Write "Evaluation logique : "
strMsg = "(j1=" & j1 & ", j2=" & j2 & ", j3=" & j3 & ", ng=" & ng & ", zr=" & zr & ") "  
Select Case J:
Case 0 : strMsg = strMsg & "pas de saut (j1=j2=j3=0) !"
Case 1 :
	strMsg = strMsg & "JGT, "
	' __ If ALU out > 0, jump 
	If zr = 0 And ng = 0 Then
		strMsg = strMsg & "sortie ALU > 0 => saut"
	Else
		strMsg = strMsg & "sortie ALU <= 0 => pas de saut"
	End If
Case 2 : 
	strMsg = strMsg & "JEQ, "
	' __ If ALU out = 0, jump 
	If zr = 1 And ng = 0 Then
		strMsg = strMsg & "sortie ALU = 0 => saut"
	Else
		strMsg = strMsg & "sortie ALU <> 0 => pas de saut"
	End If
Case 3 : 
	strMsg = strMsg & "JGE, "
	' __ If ALU out >= 0, jump 
	If ng = 0 Then
		strMsg = strMsg & "sortie ALU >= 0 => saut"
	Else
		strMsg = strMsg & "sortie ALU < 0 => pas de saut"
	End If
Case 4 : 
	strMsg = strMsg & "JLT, "
	' __ If ALU out < 0, jump 
	If ng = 1 And zr = 0 Then
		strMsg = strMsg & "sortie ALU < 0 => saut"
	Else
		strMsg = strMsg & "sortie ALU < 0 => pas de saut"
	End If
Case 5 : 
	strMsg = strMsg & "JNE, "
	' __ If ALU out <> 0, jump 
	If zr = 0 Then
		strMsg = strMsg & "sortie ALU <> 0 => saut"
	Else
		strMsg = strMsg & "sortie ALU = 0 => pas de saut"
	End If
Case 6 : 
	strMsg = strMsg & "JLE, "
	' __ If ALU out <= 0, jump 
	If zr = 1 Or ng = 1 Then
		strMsg = strMsg & "sortie ALU <= 0 => saut"
	Else
		strMsg = strMsg & "sortie ALU > 0 => pas de saut"
	End If
Case 7 : strMsg = strMsg & "saut inconditionnel (j1=j2=j3=1) !"	
End Select

WScript.Echo strMsg

WScript.StdOut.Write "Evaluation hdl : "


' 	// __ JGT ?
' 	And(a=JGT, b=notzr, out=and1);
' 	And(a=and1, b=notng, out=e1);
' 	// __ JEQ ?
' 	And(a=JEQ, b=zr, out=and2);
' 	And(a=and2, b=notng, out=e2);
' 	// __ JGE ?
' 	And(a=JGE, b=notng, out=e3);
' 	// __ JLT ?
' 	And(a=JLT, b=notzr, out=and3);
' 	And(a=and3, b=ng, out=e4);
' 	// __ JNE ?
' 	And(a=JNE, b=notzr, out=e5);
' 	// __ JLE ?
' 	Xor(a=zr, b=ng, out=zrXorng);
' 	And(a=JLE, b=zrXorng, out=e6);
' 
' 	// __ Jump ?
' 	Or(a=e1, b=e2, out=or1);
' 	Or(a=or1, b=e3, out=or2);
' 	Or(a=or2, b=e4, out=or3);
' 	Or(a=or3, b=e5, out=or4);
' 	Or(a=or4, b=e6, out=or5);
' 	Or(a=or5, b=JMP, out=jump);



e1 = j3 And Not(zr) And Not(ng)
strMsg = "(e1 = " & e1
e2 = j2 And zr
strMsg = strMsg & ", e2 = " & e2
e3 = j2 And j3 And Not(ng)
strMsg = strMsg & ", e3 = " & e3
e4 = j1 And Not(zr) And ng
strMsg = strMsg & ", e4 = " & e4
e5 = j1 And j3 And Not(zr)
strMsg = strMsg & ", e5 = " & e5
e6 = j1 And j2 And ng
strMsg = strMsg & ", e6 = " & e6
e7 = j1 And j2 And j3
strMsg = strMsg & ", e7 = " & e7 & ")"
If e1 Or e2 Or e3 Or e4 Or e5 Or e6 Or e7 Then
	strMsg = strMsg & " saut"
Else
	strMsg = strMsg & " pas de saut"
End If
WScript.Echo strMsg

WScript.Echo ""

WScript.Quit(0)

' Evaluation logique : (j1=0, j2=1, j3=0, ng=1, zr=1) JEQ, sortie ALU <> 0 => pas de saut
' Evaluation hdl : (e1 = 0, e2 = 1, e3 = 0, e4 = 0, e5 = 0, e6 = 0, e7 = 0) saut
' Evaluation logique : (j1=0, j2=1, j3=1, ng=1, zr=1) JGE, sortie ALU < 0 => pas de saut
' Evaluation hdl : (e1 = 0, e2 = 1, e3 = 0, e4 = 0, e5 = 0, e6 = 0, e7 = 0) saut

' __ Affichage syntaxe
Private Sub displaySyntaxe()
    WScript.Echo ""
    WScript.Echo "Syntaxe : cscript " & WScript.ScriptName & " j1 j2 j3 zr ng"
    WScript.Echo "Avec j1 j2 j3 zr ng = 0 ou 1"
End Sub
