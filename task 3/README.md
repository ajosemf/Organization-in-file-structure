# Task 3 - Hash index

This task consists of create an index file to a large data file using hash.

A large data file may not fit into main memory. Besides, a linear search can be very slow. Using an index file with hash, it is possible to consult for a key in index file and return the data associated at this key with fews access to disk.

The hash index technique consists in return a value calculated by hash function for each key searched. This value will be the index in hash file. If another key return the same value by hash function a colision ocurred. So, in that position of index file, a pointer will be created to the end of file where will be placed the colision. This way, all colisions will be resolved with a linked list.

To processed the code, you need firt extract the data file. In a terminal, type:
```
cat data/x* > data/bolsa.csv.tar.gz
```
The files will be join and the result file will have 369,2MB aproximately

Extract the result file with tar
```
tar -xvf data/bolsa.csv.tar.gz -C data
```
The file will be extract and will have 1,7GB aproximately

The file create_idx.py has the implementation of creation of index file. After extract the data file, type in terminal
```
python create_idx.py
```
This creation will take some minutes.

After creation, you can now use the index file to search data associated for a key with fews access to disk. The file search_NIS.py has the implementation. In terminal type
```
python search_NIS.py [valid_NIS]
```
The file valid_NIS.txt has some NIS you can use to test.
