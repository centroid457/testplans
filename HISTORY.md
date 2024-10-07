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

0.4.25 (2024/10/07 11:33:16)
------------------------------
- [TP.GUI] add BTN_clear_all  

0.4.24 (2024/10/03 17:43:36)
------------------------------
- [TP.MiddleGroup] add name in PTE+TV/TM  

0.4.23 (2024/10/03 17:33:02)
------------------------------
- [TP.MiddleGroup] fix groups by add __tc_active/tc_prev  

0.4.22 (2024/10/03 15:33:59)
------------------------------
- [TC.MiddleGroup] try fix groups work2  

0.4.21 (2024/10/03 15:21:09)
------------------------------
- [TC.MiddleGroup] try fix groups work  

0.4.20 (2024/10/03 14:46:56)
------------------------------
- [TC.[MiddleGroup] apply new ver  

0.4.19 (2024/10/01 18:37:04)
------------------------------
- [GUI] DUTs add Address into info  

0.4.18 (2024/09/30 15:32:35)
------------------------------
- [Style]add yellow for ValidNoCum=Fail  

0.4.17 (2024/09/25 15:09:46)
------------------------------
- [gui]apply Highlighter for PTE  

0.4.16 (2024/09/04 14:12:37)
------------------------------
- [TP] fix TCS run sequence on exit last tc (not started teardownCls)  

0.4.15 (2024/09/04 12:39:46)
------------------------------
- [TC] fix faulty double start tcTeardownCls=continue  

0.4.14 (2024/09/04 12:13:12)
------------------------------
- [TC] fix faulty double start tcTeardownCls  

0.4.13 (2024/09/03 16:57:37)
------------------------------
- [GUI] apply on selection TV_reread  

0.4.12 (2024/09/03 15:12:43)
------------------------------
- [GROUPS] full ref to direct compare with methods! stop using MiddleGroup as bad idea  
- [GUI] add separated column SKIP  
- [TC+GUI] add TC_RUN_SINGLE  

0.4.11 (2024/08/13 14:36:53)
------------------------------
- [groups] fix tc run if group is None(not exists)  

0.4.10 (2024/08/13 14:33:52)
------------------------------
- [groups] default result as None  

0.4.9 (2024/08/13 14:27:00)
------------------------------
- [groups] apply new  

0.4.8 (2024/08/08 15:30:05)
------------------------------
- [tcs+gui] apply address__resolve  

0.4.7 (2024/08/07 14:55:26)
------------------------------
- [TCS] add test TC_inst startup fail  

0.4.6 (2024/08/07 14:28:15)
------------------------------
- [GUI] add Pink color for TC_inst startup Fail  

0.4.5 (2024/08/02 10:57:42)
------------------------------
- [requirements] fix  

0.4.4 (2024/08/01 12:56:50)
------------------------------
- [TP] add INFINIT_RUN/*TIMEOUT  
- [TP.GUI]:  
	- add CheckBox for INFINIT_RUN  
	- add BTN_devs_detect  

0.4.3 (2024/07/31 10:54:44)
------------------------------
- [Valid] apply renamed name from title  

0.4.2 (2024/07/30 11:40:19)
------------------------------
- [GROUPS.result] apply correct in PTE  

0.4.1 (2024/07/29 17:30:37)
------------------------------
- zero update version  

0.4.0 (2024/07/29 17:00:22)
------------------------------
- [CICD] fix requirements  
- [results] ref to apply Valid over deprecated ValueExpect*  

0.3.21 (2024/07/23 10:50:40)
------------------------------
- [CICD] zero add GitHubActions directory  

0.3.20 (2024/07/23 10:43:51)
------------------------------
- [all results] apply ResultCum +get_result_or_exx  
- [PRJ] apply new  

0.3.19 (2024/07/04 12:15:26)
------------------------------
- [TP.startUp] use connect all groups  

0.3.18 (2024/07/04 10:56:08)
------------------------------
- [TC] apply finall ClsMiddleGroup and MIDDLE_GROUP_NAME  

0.3.17 (2024/07/02 17:37:59)
------------------------------
- [TC] add groups  

0.3.16 (2024/06/27 14:32:04)
------------------------------
- [TCS] fix execution STOP if only resultStartupCls=True and resultTeardownCls=False  

0.3.15 (2024/06/13 11:58:12)
------------------------------
- [GUI] zero rename headers to STARTUP_CLS/TD*  

0.3.14 (2024/06/13 11:50:55)
------------------------------
- [TC]ref get__info_pretty + add result__startup/teardown in instance!  

0.3.13 (2024/06/11 16:19:50)
------------------------------
- [TC] fix post__tc_results  

0.3.12 (2024/06/11 15:54:33)
------------------------------
- [TC] add details.update results for tc instance on teardown/startup  

0.3.11 (2024/06/06 15:19:32)
------------------------------
- [TC] fix using result in any wrapped method as ResultExpect_Chain without runned before! with run__if_not_finished  

0.3.10 (2024/06/04 16:37:56)
------------------------------
- [TC] DUTs connect on every TP.start()  
- [dev]add DEV_FOUND +mark in gui  

0.3.9 (2024/06/04 15:27:02)
------------------------------
- [TC]:  
	- add TYPE__RESULT_W_EXX/TYPE__RESULT_BASE  
	- fix all wrapped methods in case of EXX (wrap by try!)  

0.3.8 (2024/06/04 10:15:43)
------------------------------
- [TC] zero ref  

0.3.7 (2024/06/04 09:55:24)
------------------------------
- [TC] ref PTB+ATC at last are working!  

0.3.6 (2024/05/28 17:35:05)
------------------------------
- [TC] apply singletons list, serial works good!  

0.3.5 (2024/05/28 09:56:34)
------------------------------
- [TC] some fix  

0.3.4 (2024/05/23 17:37:35)
------------------------------
- [TC] zero extend get__info_pretty  

0.3.3 (2024/05/22 18:05:59)
------------------------------
- [__INIT__.py] fix import  
- apply last pypi template  
- apply all last versions for all moduls  

0.3.2 (2024/05/21 17:25:58)
------------------------------
- zero renames  
- add timeoutStart  

0.3.1 (2024/05/21 15:57:48)
------------------------------
- [DEV] rename to DevicesBreeder  
- [installer]apply upgrade_prj  

0.3.0 (2024/05/21 13:17:28)
------------------------------
- apply new ver BreederStr from pyqt_templates  

0.2.23 (2024/05/20 15:00:34)
------------------------------
- [TC+ClientRequests]:  
	- apply new ver logger  
	- fix send only not None  

0.2.22 (2024/05/20 12:46:50)
------------------------------
- [ObjectListBreeder_Base]:  
	- zero fix tests  

0.2.20 (2024/05/17 14:13:43)
------------------------------
- [ObjectListBreeder_Base]:  
	- add group_call__  

0.2.19 (2024/05/17 13:34:10)
------------------------------
- [ObjectListBreeder_Base] big ref:  
	- add BreederGroupType  
	- add group_get__type/group_check__exists/group_get__objects  

0.2.18 (2024/05/16 18:51:05)
------------------------------
- [GUI]:  
	- apply TM.HEADERS.DUTS.get_listed_index__by_outer  

0.2.17 (2024/05/16 15:13:50)
------------------------------
- [GUI]:  
	- show result as ResultChain/Step in PTE for TC_STARTUP/TEARDOWN/DUT  
	- fix tapping mouse on HEADER in Settings mode!  

0.2.15 (2024/05/16 10:53:42)
------------------------------
- [TC] fix/add cls_clear on run_cls  

0.2.14 (2024/05/15 12:22:28)
------------------------------
- [TC] fix info_pretty  

0.2.13 (2024/05/15 12:15:26)
------------------------------
- [TC] separate _Info  
- [GUI] fix click on TEARDOWN  

0.2.12 (2024/05/13 18:05:56)
------------------------------
- [tc]:  
	- fix timestamp  
	- add result__cls_teardown + apply in gui  
	- add startup__cls__wrapped/teardown*rename all to *__wrapped  

0.2.11 (2024/05/13 17:10:38)
------------------------------
- [models] zero fix  
- [tc] add timestamp  

0.2.10 (2024/05/08 15:16:53)
------------------------------
examples except one!  

0.2.9 (2024/05/08 13:43:50)
------------------------------
- [tc+tp] apply teardown if not startup  

0.2.8 (2024/05/08 13:12:56)
------------------------------
- [tc] add tc4=startup=false  

0.2.7 (2024/05/08 11:21:08)
------------------------------
- [tc] logs add+enable as attempt to find bags in parallel started tc-threads=RUN+RUN__CLS  

0.2.6 (2024/05/02 13:00:30)
------------------------------
- [TP]:  
	- try for Linux change scheme thread+async+threads to async+threads  
	- create START__GUI_AND_API  
	- separate TpInsideApi_Runner for linux  

0.2.5 (2024/05/02 12:11:40)
------------------------------
- [TP]:  
	- try for Linux change scheme thread+async+threads to async+threads  
	- create START__GUI_AND_API  
	- separate TpInsideApi_Runner for linux  

0.2.4 (2024/04/26 17:30:50)
------------------------------
- add some logger_aux  
- fix START_GUI=False  

0.2.3 (2024/04/26 15:20:33)
------------------------------
- [DevicesIndexed_WithDut] fix working COUNT  

0.2.1 (2024/04/22 18:10:50)
------------------------------
- [API] fix working with FastApi  

0.2.0 (2024/04/22 12:58:05)
------------------------------
- [API] apply FastApi  

0.1.17 (2024/03/29 17:15:34)
------------------------------
- [GUI] apply last gui with Headers as NamesIndexed + deprecate Tm.ADDITIONAL_COLUMNS  

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
