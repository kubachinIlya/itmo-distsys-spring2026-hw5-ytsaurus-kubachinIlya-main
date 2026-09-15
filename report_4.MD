# файлы перекинул
cd C:\Users\kubashinia\Documents\Personal\itmo-distsys-spring2026-hw5-ytsaurus-kubachinIlya-main\images_text_src

scp -i "C:\Users\kubashinia\Documents\Personal\my_keys\ssh-key-1789404872376\ssh-key-1789404872376" antihype_train_lyrics.txt ilyakubashin@84.201.151.66:~/hw5/src/


cd C:\Users\kubashinia\Documents\Personal\itmo-distsys-spring2026-hw5-ytsaurus-kubachinIlya-main\python_src

scp -i "C:\Users\kubashinia\Documents\Personal\my_keys\ssh-key-1789404872376\ssh-key-1789404872376" map_reduce_count_words.py ilyakubashin@84.201.151.66:~/hw5/src/

# Шаг 2. Подготовка TSV
MapReduce-скрипт ожидает входные данные в tab-separated формате с колонками lineno= и text=. Преобразуем текст:

bash
cd ~/hw5/src

awk '{gsub(/\t/, "\\t"); print "lineno="NR"\ttext="$0}' antihype_train_lyrics.txt > antihype.tsv
Проверь, что получилось:

bash
head -5 antihype.tsv


ilyakubashin@compute-vm-4-12-35-ssd-1789461179672:~/hw5/src$ head -5 antihype.tsv
lineno=1        text=### Zamay and slava kpss antihypeintro
lineno=2        text=
lineno=3        text=41 ContributorsAntihypeintro LyricsВступительный трек целиком написан из ключевых слов, которые присылали донатеры во время одного из совместных стримов Славы КПСС и Замая:
lineno=4        text=Е, я сказал маме, что собираюсь заниматься рэпом, она сказала: «Лан, даун»
lineno=5        text=Да, этот трек нам спонсировал Ландаун
ilyakubashin@compute-vm-4-12-35-ssd-1789461179672:~/hw5/src$

# создание таблиц и директории

# загрузка данных в инпут
cat antihype.tsv | yt write-table //home/ilyakubashin/mapreduce/input --format dsv
Проверка — прочитать первые 6 строк:

bash
yt read-table '//home/ilyakubashin/mapreduce/input[:#6]' --format dsv


# запуск map - reduce

Шаг 5. Запуск MapReduce
bash
yt map-reduce \
  --mapper "python3 map_reduce_count_words.py map" \
  --reducer "python3 map_reduce_count_words.py reduce" \
  --map-local-file map_reduce_count_words.py \
  --reduce-local-file map_reduce_count_words.py \
  --src //home/ilyakubashin/mapreduce/input \
  --dst //home/ilyakubashin/mapreduce/result \
  --reduce-by word \
  --format dsv
Что означают флаги:

--mapper — команда для map-фазы (запускает скрипт с аргументом map).

--reducer — команда для reduce-фазы (аргумент reduce).

--map-local-file / --reduce-local-file — файлы, которые нужно доставить на узлы кластера. YTsaurus их сам раздаст по нодам.

--src / --dst — входная и выходная таблицы.

--reduce-by word — ключ, по которому группируются данные перед reduce.

--format dsv — входной формат TSV.

результат фоточка есть)



# своя мап редуска
cd C:\Users\kubashinia\Documents\Personal\itmo-distsys-spring2026-hw5-ytsaurus-kubachinIlya-main\python_src
 

scp -i "C:\Users\kubashinia\Documents\Personal\my_keys\ssh-key-1789404872376\ssh-key-1789404872376" map_reduce_inverted_index.py ilyakubashin@84.201.151.66:~/hw5/src/


таблица -  create_table_for_inverted_index.sh


run map reduce

yt map-reduce \
  --mapper "python3 map_reduce_inverted_index.py map" \
  --reducer "python3 map_reduce_inverted_index.py reduce" \
  --map-local-file map_reduce_inverted_index.py \
  --reduce-local-file map_reduce_inverted_index.py \
  --src //home/ilyakubashin/mapreduce/input \
  --dst //home/ilyakubashin/mapreduce/word_index \
  --reduce-by word \
  --format dsv