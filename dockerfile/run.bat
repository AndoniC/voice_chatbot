@echo off
REM run ip:0.0 [media_dir]  [code_dir] [models_dir] [libs_dir] [repos_dir] [build]
setlocal enabledelayedexpansion

for %%x in (%*) do (
   set /A argCount+=1
   set "argVec[!argCount!]=%%~x"
)

if "%argCount%" NEQ "7" (
echo Error: wrong number of parameters
echo:
echo run_cpu [ip/adapter identifier:0.0] [media_dir]  [code_dir] [models_dir] [libs dir] [repos_dir] [build dir]
echo: 
echo Example: run "Ethernet adapter Ethernet"  F:\MEDIA D:\code F:\models F:\libs
echo          HOME:: run 192.168.1.57:0.0 F:\MEDIA D:\andoni\code F:\models D:\libs D:\repos D:\andoni\builds\linux
echo          WORK:: run 192.168.110.102:0.0  D:\media H:\code D:\models H:\libs H:\python_repos H:\builds\x64\linux  
echo          HALK:: ./run.sh   D:\media H:\code D:\models H:\python_repos   
echo:
)else (

	echo input: %~1
	(echo %~1 | findstr /r "[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*"  >Nul && (set ret=true
) || set ret=false)

	if !ret!==true (
		set IP_ADDRESS_TXT=%~1
		echo IP FOUND : !IP_ADDRESS_TXT!
		set DISPLAY_ADDRESS = !IP_ADDRESS_TXT!
		
	) else (

		ECHO Buscando la ip del dispositivo %~1
		CALL :get_ip "%~1",IP_ADDRESS_TXT
		
		set DISPLAY_ADDRESS = !IP_ADDRESS_TXT! 
	)
	ECHO Display Address: !IP_ADDRESS_TXT!
	echo docker run -ti --rm --gpus all  --env NVIDIA_DISABLE_REQUIRE=1 -e CUDA_VISIBLE_DEVICES=0  --name elleanor-assistant -e DISPLAY=!IP_ADDRESS_TXT! -p 5000:5000 -p 8000:8000   -v %4:/hostmodels/ -v %2:/hostmedia/ -v %3:/hostcode/ -v %5:/hostlibs/ -v %6:/hostrepos/ -v %7:/hostbuild/ assistant/elleanor:1.0 bash
	docker run -ti --rm --gpus all  --env NVIDIA_DISABLE_REQUIRE=1 -e CUDA_VISIBLE_DEVICES=0  --name elleanor-assistant -e DISPLAY=!IP_ADDRESS_TXT! -p 5000:5000 -p 8000:8000        --volume="/etc/sudoers.d:/etc/sudoers.d:ro"  --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw"   -v %4:/hostmodels/ -v %2:/hostmedia/ -v %3:/hostcode/ -v %5:/hostlibs/ -v %6:/hostrepos/ -v %7:/hostbuild/ assistant/elleanor:1.0 bash
)

PAUSE
EXIT /B %ERRORLEVEL% 



REM http://www.trytoprogram.com/batch-file-functions/
:get_ip 
	REM just a sample adapter here:
	set adapter=%~1
	REM ~remove quotes from input string

	set adapterfound=false
	echo Network Connection Test
	echo adapter : %adapter%
	REM ::get 1 and 2 string from the line a will be first b will be second
	REM using variables inside a loop
	REM https://stackoverflow.com/questions/13805187/how-to-set-a-variable-inside-a-loop-for-f
	REM https://ss64.com/nt/delayedexpansion.html (delayed expansion)
	for /F "usebackq tokens=1-2 delims=:" %%a in (`ipconfig /all`) do (
		REM this syntax "item=%%a" prevents inadvertent trailing spaces from getting in the value, and also protects against special characters
		set "item=%%a"
		REM echo !item!
		if !adapterfound!==false (	
			if /i !item!==!adapter! (
				set adapterfound=true
				echo Adapter Found !item! 
			)
		) else (
			REM echo !item!
			REM echo !secondstring!
			REM line with Adapter name has been found, therefore ip will be next line with ip address
			REM item contains IPv4 
			REM !item:IPv4=! replace IPv4 if it is in item with empty string
			REM when they are not the same !item! had IPv4 inside
			if not "!item!"=="!item:IPv4=!"  (
				echo IPv4 FOUND :: %%b 
				set "IP_ADDRESS_TXT=%%b"
				goto :found
			)
		)	
	)
REM goto :eof
:found
REM for /f "tokens=* delims= " %%a in ("%IP_ADDRESS%") do set IP_ADDRESS=%%a
call :Trim IP_ADDRESS %IP_ADDRESS_TXT%
set IP_ADDRESS=!IP_ADDRESS:(Preferido)=!
set IP_ADDRESS=!IP_ADDRESS:(Preferred)=!
set  DISPLAY=%IP_ADDRESS%:0.0
SET %~2=%DISPLAY%
REM echo DISPLAY inside the function: %DISPLAY%
REM echo Parametro 2 inside the function: !%~2!
EXIT /B 0

:Trim
SetLocal EnableDelayedExpansion
set Params=%*
for /f "tokens=1*" %%a in ("!Params!") do EndLocal & set %1=%%b
exit /b

