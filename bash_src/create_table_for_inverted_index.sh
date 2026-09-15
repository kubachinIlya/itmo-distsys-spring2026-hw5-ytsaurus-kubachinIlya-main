#!/bin/bash
# Создание таблицы
yt create table //home/ilyakubashin/mapreduce/word_index \
  --attributes '{schema = [{name = word; type = string}; {name = lines; type = string}]}'