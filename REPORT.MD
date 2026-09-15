## Обязательно напишите ФИО в свой PR!!!

TODO: здесь ответ на задание, содержащий необходимые артефакты, описанные ранее :)


 # 1. Инсталяция

 # 2. Создание таблицы, запись, чтение (CLI)

### Динамическая таблица — CLI-версия
Питон-скрипты писал, но они капризничали с RPC в kind-кластере. Через CLI - завелось сразу.

bash_src/create_table.sh

bash_src/write_to_table.sh

bash_src/read_table.sh

Схема — составной ключ (user_id, item_id):

```bash
# 1. Создание таблицы
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

# 2. Монтирование (обязательно для динамических таблиц!)
yt mount-table //home/ilyakubashin/ratings_project/my_dynamic_table --sync

# 3. Вставка строки
yt insert-rows //home/ilyakubashin/ratings_project/my_dynamic_table \
  --format json \
  <<< '{"user_id": 1, "item_id": 100, "rating": 5.0, "comment": "great"}'

# 4. Чтение по ключу
yt lookup-rows //home/ilyakubashin/ratings_project/my_dynamic_table \
  --format json \
  <<< '{"user_id": 1, "item_id": 100}'
sort_order="ascending" на ключевых колонках — критично. Без него
unique_keys=true падает с ошибкой key columns are not present.

mount-table — обязательный шаг. Без него таблица создана, но не работает.

Скриншот: https://images_text_src/Create-Write-Read_Table.png

Сбор текстов для MapReduce
Парсер лирики AntiHype лежит тут: python_src/parse_to_get_text.py

Результат: images_text_src/antihype_train_lyrics.txt

Скрипт собирает ссылки со страницы альбома и вытаскивает текст каждого трека через data-lyrics-container.


 # 3. Посчитать количество слов в любимом текстовом документе

 # 4. Разработка своей map-reduce задачи для построения индекса часто встречающися слов

 # 5. YQL-запрос, который по построенной таблице и номеру строки выводит все слова (из этой же таблицы), которые строка содержит 