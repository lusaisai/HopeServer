:: The first one may ask for login info
appcfg.py --application=app_id1 update .

:: The following will run in parallel
start "upload" appcfg.py --application=app_id2 update .
start "upload" appcfg.py --application=app_id3 update .
