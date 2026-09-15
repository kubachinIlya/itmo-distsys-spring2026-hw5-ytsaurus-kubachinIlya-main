SELECT word, count
FROM `//home/ilyakubashin/mapreduce/result`
WHERE LEN(word) > 5 
LIMIT 30;