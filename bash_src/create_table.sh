#!/bin/bash
# Создание таблицы
yt create table //home/ilyakubashin/ratings_project/my_dynamic_table \
  --attributes '{
    dynamic=%true;
    schema=[
      {name="user_id";type="int64";sort_order="ascending"};
      {name="item_id";type="int64";sort_order="ascending"};
      {name="rating";type="double"};
      {name="comment";type="string"}
    ];
    unique_keys=%true
  }'