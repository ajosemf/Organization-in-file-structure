import struct
import hashlib
import time

# parameters
hashSize = 17001333
fileName = "data/bolsa.csv"
indexName = "data/bolsa.idx"
indexFormat = "14sLL"
keyColumnIndex = 7
indexStruct = struct.Struct(indexFormat)
buffer = 50000

# hash function
def h(key):
    global hashSize
    # %hashSize to keep result smaller then 17001333
    return int(hashlib.sha1(key.encode('utf-8')).hexdigest(),16)%hashSize

# creating an empty index file
with open(indexName,'wb') as fi:
    emptyIndexRecord = indexStruct.pack(b'',0,0)
    for i in range(hashSize):
        fi.write(emptyIndexRecord)
    fileIndexSize = fi.tell()
print('IndexFileSize: {}'.format(fileIndexSize))

# empty record representation
emptyField = indexStruct.unpack(emptyIndexRecord)[0]

# controllers
count = 1
proc = 0

# indexing
with open(fileName, 'r', encoding="latin-1") as f:
    with open(indexName, 'r+b') as fi:
        print('Starting Indexing...')
        start = time.time()
        line = f.readline() # discarding header
        p = f.tell()  # csv file position
        lines = f.readlines(buffer)
        proc += len(lines)
        while (lines):
            count += 1
            if count % 2000 == 0:
                print('Records processed: {}'.format(proc))
            for line in lines:
                record = line.split('\t')  # csv record
                pi = h(record[keyColumnIndex])  # hash of NIS
                fi.seek(pi * indexStruct.size)  # search idx record by hash
                indexRecord = indexStruct.unpack(fi.read(indexStruct.size))  # read record
                fi.seek(pi * indexStruct.size)  # return pointer
                # if empty field
                if indexRecord[0] == emptyField:
                    fi.write(indexStruct.pack(record[keyColumnIndex].encode(), p, 0))  # write new idx
                # if not empty field
                else:
                    nextPointer = indexRecord[2]  # get pointer
                    fi.write(indexStruct.pack(indexRecord[0], indexRecord[1],
                                              fileIndexSize))  # rewrite new idx with new pointer
                    fi.seek(0, 2)  # move to end of file
                    fi.write(indexStruct.pack(record[keyColumnIndex].encode(), p, nextPointer))  # rewrite new idx
                    fileIndexSize = fi.tell()  # update file size
                p += len(line) + 1  # calc new position in csv file
            lines = f.readlines(buffer)
            proc += len(lines)

print('Indexing completed')
print('Estimated time: {} minutes'.format(int((time.time() - start) // 60)))