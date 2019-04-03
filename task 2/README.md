# Task 2 - External Sort Merge

This task consists of sorting a zip log file unsorted using External Sort Merge technique.

External Sort Merge is used when the file that will be sorted is too large and does not fit in main memory.

Therefore, the external sorting technique consists of splitting the original file into smaller sorted partitions and then merging them two by two using intercalation.

The file external_sort_merge.py has the implementation of External Sort Merge.

You should uncompress the file cep.dat.tar.gz, wich is the unsorted file.

To run, type in a terminal the command
```
python external_sort_merge.py cep.dat
```

The script will create the cep_ordenado.dat file which is the sorted file.
