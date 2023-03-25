@echo off
REM build [docker image name]
setlocal enabledelayedexpansion

set argCount=0
for %%x in (%*) do (
   set /A argCount+=1
   set "argVec[!argCount!]=%%~x"
)
echo nparams = %argCount%
if "%argCount%" NEQ "1" (
	echo Error: wrong number of parameters
	echo:
	echo build.bat username/container_name:version
	echo: 
) else (
	docker build --build-arg NB_UID=8110 --build-arg USER=acortes --build-arg USE_GPU=1 -f Dockerfile_gpu -t %1 .
)
