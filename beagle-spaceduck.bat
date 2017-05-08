@echo off
REM assumes the beagle runtime engine is included in PATH, if not
call beagle 1920 1080 0 60 %~dp0
REM return the user to where they were...
CD /D %~dp0
pause
