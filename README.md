![Ver/TestedPython](https://img.shields.io/pypi/pyversions/testplans)
![Ver/Os](https://img.shields.io/badge/os_development-Windows-blue)  
![repo/Created](https://img.shields.io/github/created-at/centroid457/testplans)
![Commit/Last](https://img.shields.io/github/last-commit/centroid457/testplans)
![Tests/GitHubWorkflowStatus](https://github.com/centroid457/testplans/actions/workflows/test_linux.yml/badge.svg)
![Tests/GitHubWorkflowStatus](https://github.com/centroid457/testplans/actions/workflows/test_windows.yml/badge.svg)  
![repo/Size](https://img.shields.io/github/repo-size/centroid457/testplans)
![Commit/Count/t](https://img.shields.io/github/commit-activity/t/centroid457/testplans)
![Commit/Count/y](https://img.shields.io/github/commit-activity/y/centroid457/testplans)
![Commit/Count/m](https://img.shields.io/github/commit-activity/m/centroid457/testplans)

# testplans (current v0.4.34/![Ver/Pypi Latest](https://img.shields.io/pypi/v/testplans?label=pypi%20latest))

## DESCRIPTION_SHORT
simple testplan framework for several DUTs

## DESCRIPTION_LONG
designed to apply testplan for several DUTs

## ПОНЯТИЯ
    TC - TestCase
    TP - TestPlan
    DUT - Device Under Test - тестируемое устройство

## АРХИТЕКТУРА
- тестплан
    - работает в потоке,
    - может быть остановлен в любой момент terminate(), при этом завершает все запущенные тесткейсы
    - имеет настройки которые принимаются всеми тесткейсами за базовые и могут быть перезаписаны ими для себя
    - имеет списки классов TC и обьектов DUT (генерирует обьекты TC для каждого DUT)
    - для себя не разделяет обьекты тесткейсов, работает строго с классом тесткейса,
    - выполняет все тесткейсы в порядке их следования на списке DUT
    - в один момент времени выполняется только один класс тесткейса
- тесткейсы
    - работают в потоке,
    - может быть остановлен в любой момент terminate(), при этом завершаются безопасно (исполняются все teardown обьектов и глобальный классовый тесткейса), 
    - представляет собой класс инициируемый с входным параметром DUT,
    - выполняются тесткейсы строго по очереди,
    - каждый тесткейс выполняется на всех устройствах либо асинхронно, либо синхронно в зависимости от настройки,
    - работа тесткейса полностью управляется классом тесткейса на серии устройств (возможно выполнение парных тестов с выбором нужных пар внутри тесткейса),
- результаты
    - все результаты находятся в пока в обьекте тесткейса
    - итогового (result)
    - промежуточных результатов (details)
- настройки
    - управление
        - SKIP всех возможных вариантов (полностью тесткейс для всех устройств, полностью DUT для всех TC, отдельный TC на отдельном DUT),
        - выполнение тесткейса синхронно/асинхронно
    - данные для использования в тесткейсах
        - реализовано в файлах JSON
        - для каждого тесткейса и общие для тестплана (кейсовые накладываются на плановые)
- GUI тестплана
    - запуск GUI опциональный,
    - старт/стоп тестплана,
    - отображение текущего тесткейса,
    - отображение результата тескейса на каждом тестируемом устройстве,
    - отображение промежуточных результатов (details)
- API 
    - минимальное API и запуск


## Features
1. [THREADS]:  
	- safe work in independent TCs  
	- safe stop process at any moment by terminate  
2. [SKIP]:  
	- tc  
	- tc on dut  
	- dut  
3. [DEVICES__BREEDER_INST]:  
	- keep all in one instance  
	- use variants: single device for all duts or list for pairing each dut  


********************************************************************************
## License
See the [LICENSE](LICENSE) file for license rights and limitations (MIT).


## Release history
See the [HISTORY.md](HISTORY.md) file for release history.


## Installation
```commandline
pip install testplans
```


## Import
```python
from testplans import *
```


********************************************************************************
## USAGE EXAMPLES
See tests, sourcecode and docstrings for other examples.  

********************************************************************************
