:: The first one may ask for login info
appcfg.py --application=gae0x0000 update .

:: The following will run in parallel
start "upload" appcfg.py --application=gae0x0001 update .
start "upload" appcfg.py --application=gae0x0002 update .
start "upload" appcfg.py --application=gae0x0003 update .
start "upload" appcfg.py --application=gae0x0004 update .
start "upload" appcfg.py --application=gae0x0005 update .
start "upload" appcfg.py --application=gae0x0006 update .
start "upload" appcfg.py --application=gae0x0007 update .
start "upload" appcfg.py --application=gae0x0008 update .
start "upload" appcfg.py --application=gae0x0009 update .
start "upload" appcfg.py --application=gae0x000a update .
start "upload" appcfg.py --application=gae0x000b update .
start "upload" appcfg.py --application=gae0x000c update .
start "upload" appcfg.py --application=gae0x000d update .
start "upload" appcfg.py --application=gae0x000e update .
start "upload" appcfg.py --application=gae0x000f update .
