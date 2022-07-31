# TGVMax_search
A python script that automatically search for TGV Max seats for the selected dates.


## Installation

This script required python 3 to be installed as well as the following pip packages:
- PyYAML
- Urllib
- DateTime

## Script usage

1 - Modify the config.yaml file to include the travels to look for, following this syntax:

```shell
Travels:
  Travel 1:
    origin: RENNES
    destination: PARIS (intramuros)
    date: 2022-08-16

  Travel 2:
    origin: RENNES
    destination: PARIS (intramuros)
    date: 2022-08-17  
```

2 - execute the script:

```shell
python .\TGVmax_Search.py -c .\config.yaml
```
