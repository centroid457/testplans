# RELEASE HISTORY

********************************************************************************
## TODO
1. add meta for settings in tcs, it is better then applying in manually in TP!  
2. close all (api_server+tpThreads) on GUI close!  
3. add version for all jsons for future api_server  
4. [RESULTS] try separate  

********************************************************************************
## FIXME
1. TP progress  
2. NEED TESTS!!! TC+TP  

********************************************************************************
## NEWS

0.1.16 (2024/03/26 15:44:34)
------------------------------
- [GUI] fix selection ASYNC  

0.1.15 (2024/03/25 19:14:00)
------------------------------
- [TC] fix _tcs__apply_classes if not have TestCase class in TC file-2  

0.1.14 (2024/03/25 18:46:07)
------------------------------
- [TC] fix _tcs__apply_classes if not have TestCase class in TC file  

0.1.13 (2024/03/21 16:04:27)
------------------------------
- [Devices] ref __getattr__ over _GROUP  

0.1.12 (2024/03/21 15:07:40)
------------------------------
- [Devices] apply connect over CONN  

0.1.11 (2024/03/21 14:45:16)
------------------------------
- [Devices] delete *PRESENT* - use direct connect!  

0.1.10 (2024/03/20 15:37:32)
------------------------------
- [GUI/TC] add+apply result__cls_ready/startup  

0.1.9 (2024/03/20 12:27:52)
------------------------------
- [DevicesIndexed]separate DevicesIndexed_WithDut from DevicesIndexed_Base  

0.1.8 (2024/03/19 12:23:50)
------------------------------
- zero refs*3  

0.1.7 (2024/03/18 15:51:06)
------------------------------
- some refs*2  

0.1.6 (2024/03/18 12:57:17)
------------------------------
- some refs  

0.1.5 (2024/03/15 18:06:19)
------------------------------
- [Tp/Tc] clear rename to TCS__INST/*CLS  

0.1.3 (2024/03/15 17:27:22)
------------------------------
- [Tp/Tc] clear separate DEVICES__CLS/DEVICES__BY_INDEX  

0.1.2 (2024/03/15 15:29:56)
------------------------------
- [DevicesIndexed_WithDut]:  
	- add init__devices,  check_exists__group__/check_present__instance__  
	- TESTS FINISHED! add Test__TpDevicesIndexed   

0.1.1 (2024/03/13 14:12:29)
------------------------------
- [DEVICES] add connect__cls/disconnect  

0.1.0 (2024/03/13 12:07:03)
------------------------------
- BIG REF!!!  
- [devises] keep all in one object + generate  
- [TP] add startup/teardown  
- [HELP] add schema  

0.0.16 (2024/02/14 17:50:52)
------------------------------
- move http_client.py into server_templates  

0.0.15 (2024/02/07 19:31:23)
------------------------------
- add post_tc_results  

0.0.14 (2024/02/06 17:32:43)
------------------------------
- add DutBase.check_present explicitly  
- some fixes  
- move all ServerAiohttp_Example here!  

0.0.13 (2024/02/06 16:06:19)
------------------------------
- add check_present  

0.0.12 (2024/02/06 16:01:40)
------------------------------
- add TpMultyDut_Example  

0.0.11 (2024/02/06 15:45:10)
------------------------------
- add INDEX in DUT  
- add TC results_get/*all  
- add TP results_get (not finished)  

0.0.10 (2024/02/02 10:57:02)
------------------------------
- fix TC.info_get  

0.0.9 (2024/02/02 10:35:40)
------------------------------
- add first step API  
- add TC/TP.info_get  

0.0.8 (2024/01/30 16:50:52)
------------------------------
- add START_API  

0.0.7 (2024/01/26 16:52:34)
------------------------------
- add START_GUI  

0.0.6 (2024/01/25 16:51:48)
------------------------------
- add SETTINGS_BASE  
- add SETTINGS_FILES in TC  

0.0.5 (2024/01/24 15:23:17)
------------------------------
- fix work without any TC (again)  

0.0.4 (2024/01/24 15:06:11)
------------------------------
- fix work without any TC  

0.0.3 (2024/01/24 14:49:10)
------------------------------
- add signal__tp_start and connect all (and stop)  
- add tp progress  

0.0.2 (2024/01/19 12:22:32)
------------------------------
- fix exx without settings  

0.0.1 (2024/01/19 10:46:03)
------------------------------
- run TCS by TC class! TP work only with TC class, not instances on duts  
- try use folders: TESTCASES/TESTPLANS/DEVICES  
- use settings for testcases

********************************************************************************
