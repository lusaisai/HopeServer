:: To initially connect to Google, we need to modify hosts file(%SystemRoot%\System32\drivers\etc\hosts) or have an existing proxy like follows
set HTTP_PROXY=http://localhost:1080
set HTTPS_PROXY=http://localhost:1080

:: The first one may ask for login info
appcfg.py --application=app_id1 update .

:: The following will run in parallel
start "upload" appcfg.py --application=app_id2 update .
start "upload" appcfg.py --application=app_id3 update .
