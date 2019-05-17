import struct
import hashlib
import sys

if len(sys.argv) != 2:
    print("USE {} [NIS]".format(sys.argv[0]))
    quit()

# parameters
hashSize = 17001333
fileName = "data/bolsa.csv"
indexName = "data/bolsa.idx"
indexFormat = "14sLL"
indexStruct = struct.Struct(indexFormat)

# hash function
def h(key):
    global hashSize
    return int(hashlib.sha1(key.encode('utf-8')).hexdigest(),16)%hashSize

NIS = sys.argv[1]

# searching
with open(indexName,'rb') as fi:
    p = h(NIS)
    offset = p*indexStruct.size
    i = 1
    while True:
        fi.seek(offset)
        indexRecord = indexStruct.unpack(fi.read(indexStruct.size))
        if indexRecord[0].decode() == NIS:
            with open(fileName,'r',encoding="latin-1") as f:
                header = f.readline()
                header = header[:-1] # removing '\n'
                header_fields = header.split('\t')
                f.seek(indexRecord[1])
                record = f.readline()
                values = record.split('\t')
                for j in range(len(values)):
                    print('{}: {}'.format(header_fields[j], values[j]))
                print('Number of access to disk: {}'.format(i))
                print()
                break
        offset = indexRecord[2]
        if offset == 0:
            print('NIS {} not found'.format(NIS))
            print()
            break
        i += 1
