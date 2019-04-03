import os
import sys
import struct
from queue import Queue

if len(sys.argv) != 2:
	print("USO {} [source_filename]".format(sys.argv[0]))
	quit()

src = sys.argv[1]

def compara(a,b):
    r1 = registroCEP.unpack(a)
    r2 = registroCEP.unpack(b)
    return r1[cepColumn] < r2[cepColumn]

def ordena(a):
    r = registroCEP.unpack(a)
    return r[cepColumn]

registroCEP = struct.Struct("72s72s72s72s2s8s2s")
cepColumn = 5

f = open(src,"rb")
f.seek(0,2) # move para o final do arquivo
posicao = f.tell() # tamanho do arquivo em bytes
f.seek(0) # move para o início do arquivo
qtd = int(posicao/registroCEP.size) # qtd total de registros

# tamanho do buffer e registros finais
buffer = qtd//8*registroCEP.size
resto = qtd%8

os.mkdir('tmp') # cria diretório tmp para as partições

print('parametros calculados')

q = Queue()  # fila de partições que serão intercaladas
for i in range(8):
    if i == 7:
        buffer = buffer + resto * registroCEP.size  # ultimo buffer agrega o resto

    lines = f.read(buffer)

    # split do buffer em list
    r_in_buffer = buffer // registroCEP.size  # quantidade de registros no buffer
    start = 0
    end = registroCEP.size
    lista = list()
    for _ in range(r_in_buffer):
        # print(lines[start:end])
        lista.append(lines[start:end])
        start = start + registroCEP.size
        end = end + registroCEP.size

    # ordena
    lista.sort(key=ordena)

    # prepara para escrita no disco
    out = b''.join(lista)

    # escreve no disco o buffer ordenado
    path = 'tmp/cep{}.dat'.format(i)
    fout = open(path, "wb")
    fout.write(out)
    fout.close()
    q.put(path)  # add na queue a partição
    print('particao {} criada'.format(path))

f.close()

print('particoes criadas')

num = 8

# intercalação 2 a 2
while q.qsize() > 1:
    path1 = q.get()
    path2 = q.get()
    print('intercalando {} e {}'.format(path1,path2))
    f1 = open(path1,"rb")
    f2 = open(path2, "rb")

    pathout = 'tmp/cep{}.dat'.format(num)
    num = num + 1
    fout = open(pathout,"wb")

    line1 = f1.read(registroCEP.size)
    line2 = f2.read(registroCEP.size)

    while(line1 and line2):
        if(compara(line1,line2)):
            fout.write(line1)
            line1 = f1.read(registroCEP.size)
        else:
            fout.write(line2)
            line2 = f2.read(registroCEP.size)

    while(line1):
        fout.write(line1)
        line1 = f1.read(registroCEP.size)

    while(line2):
        fout.write(line2)
        line2 = f2.read(registroCEP.size)

    f1.close()
    f2.close()
    fout.close()

    os.remove(path1)
    os.remove(path2)

    q.put(pathout)

print('preparando arquivo final')
# prepara path do arquivo final
pieces = src.split('.')
final_file = '{}_ordenado.{}'.format(pieces[0],pieces[1])

# move e renomeia o arquivo final
os.rename(pathout,final_file)
os.removedirs('tmp')

print('arquivo final: {}'.format(final_file))
