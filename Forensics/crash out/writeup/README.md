# crash-out writeup

1. View registry given in Users/nadia/AppData/ and see HKEY_CURRENT_USER\Software\Microsoft\Powershell\1\PowershellExec (it will show powershell command that reveal the path to security_tool.ps1 and winsec.ps1). Else, if they found it first, players can just read the script directly in \Users\nadia\Scripts.
2. security_tool.ps1 compiles winsec.ps1 into exe to run it. it also imports BLABLA.dll module.
3. first flag can be found in BLABLA.dll
4. second flag is in winsec.ps1
5. last flag is in .WER file located in Users/nadia/AppData/Local/Microsoft/WER
