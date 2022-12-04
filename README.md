# ASCII-HF-Transplanter <!-- omit in toc -->
[![License](https://img.shields.io/badge/license-GNU-v3.svg?style=flat)](https://www.gnu.org/licenses/gpl-3.0.txt)

A Python script to transfer Heightfield data between ASCII files

# Table of Contents <!-- omit in toc -->
- [Info](#info)
- [Usage](#usage)

# Info
This script was made to transfer data between heightmaps

The goal is to allow enable versioning of heightmaps and/or allow multiple terrain makers to edit the terrain simultaneously by allowing sectioned data transfer between files. 

# Usage
```sh
hfcarrier.py [fromfile] [tofile] [coords] [-o --output output]
```  

| Parameter | Function | Format | Default | |
| ---- | ----- | ---- | ---- | ---- |
| fromfile | path of the file to cut from | ./file.asc | |
| tofile | path of the file to paste to | ./file.asc | |
| coods | Bottom Right and Top Left coordinates of the area to be transfered | brx,bry,trx,try | |
| -o, --output | path and filename of output file | ./file.asc | ./out.asc |
