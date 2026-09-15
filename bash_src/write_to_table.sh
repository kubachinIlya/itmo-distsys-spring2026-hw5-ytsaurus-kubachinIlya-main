#!/bin/bash

# Вставка строки в таблицу
yt insert-rows //home/ilyakubashin/ratings_project/my_dynamic_table \
  --format json \
  <<< '{"user_id": 1, "item_id": 100, "rating": 5.0, "comment": "great"}'