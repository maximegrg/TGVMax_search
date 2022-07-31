﻿# TGVMax_search

<div align="center">
  ![TGVMax](https://user-images.githubusercontent.com/57716360/182037565-b0c7f3f2-d449-474e-b0d8-fadc6d066e70.jpg)
</div>


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
