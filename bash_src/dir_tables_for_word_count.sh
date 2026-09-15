#!/bin/bash

# Директория для таблиц (если ещё нет)
yt create map_node //home/ilyakubashin/mapreduce --recursive

# Входная таблица: lineno + text
yt create table //home/ilyakubashin/mapreduce/input \
  --attributes '{schema = [{name = lineno; type = string}; {name = text; type = string}]}'

# Выходная таблица: count + word
yt create table //home/ilyakubashin/mapreduce/result \
  --attributes '{schema = [{name = count; type = string}; {name = word; type = string}]}'