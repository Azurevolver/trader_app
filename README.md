---
title: 'Project documentation template'
disqus: hackmd
---

IS439 Final Projects - eTrader
===

## Table of Contents
[TOC]

## About This Project

### Project Name
eTrader

### Tech Stack
1) Back-end: Django v3.2, Python v3.8.8, requests 2.25.1
2) Front-end: Bootstrap v5.0.0
3) IDE: PyCharm


### Set up environment to run this project (Mac user)
1. Install Anaconda Navigator
2. Create new environment with Anaconda Navigator
    a. Open a new terminal by clicking the newly created env
    b. ==In the terminal, install Django & **requests** by using pip==
    > \> pip install Django
    > \> pip install requests

### API usage
Stock API: [iexcloud](https://iexcloud.io/)
Crypto API: [cryptocompare](https://min-api.cryptocompare.com/)


eTrader User story
---

### STOCK NEWS Page
#### Type stock symbol (ticker), then this page will display related news and current transaction details.

![](https://i.imgur.com/BzSezID.png)


![](https://i.imgur.com/yvgjQg4.png)

### My Stock List Page
#### Type stock symbol (ticker), then the stock will be saved to sqlite database. User can check stock's detail, delete the stock.

![](https://i.imgur.com/Ygc9teB.png)
![](https://i.imgur.com/hQIpB8p.png)
![](https://i.imgur.com/xw0y3I7.png)

![](https://i.imgur.com/iscPEbt.png)


### Stock Detail Page
#### This page demonstrates stock detail and its logo
![](https://i.imgur.com/Qi4OOGv.png)

### Crypto NEWS Page
#### This page demonstrates selected crypto news and some detail information

![](https://i.imgur.com/lzZtVgp.png)

![](https://i.imgur.com/UFFsRR8.png)


### To-do item Page
#### This page allow users to record his/ her trading action and navigate to detail.

![](https://i.imgur.com/Hr9Sj1H.png)

![](https://i.imgur.com/azefmW9.png)

### To-do item Detail Page
#### This page show detail of a to-do item
![](https://i.imgur.com/EYwmCQC.png)

![](https://i.imgur.com/NOxYXeg.png)

![](https://i.imgur.com/N42FsD6.png)

