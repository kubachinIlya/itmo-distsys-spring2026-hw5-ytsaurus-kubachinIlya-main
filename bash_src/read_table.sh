#!/bin/bash

# Выбор строки из таблицы
yt lookup-rows //home/ilyakubashin/ratings_project/my_dynamic_table \
  --format json \
  <<< '{"user_id": 1, "item_id": 100}'