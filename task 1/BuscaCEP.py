import struct
import sys

if len(sys.argv) != 2:
	print("USO {} [CEP]".format(sys.argv[0]))
	quit()

registroCEP = struct.Struct("72s72s72s72s2s8s2s")
cepColumn = 5
#print("Tamanho da Estrutura: {}".format(registroCEP.size))
f = open("cep_ordenado.dat","rb")
f.seek(0,2) # move para o final do arquivo
posicao = f.tell()
f.seek(0) # move para o início do arquivo
inicio = 0
fim = (posicao // registroCEP.size) - 1
counter = 0

while inicio <= fim:
	meio = (inicio + fim) // 2
	f.seek(meio * registroCEP.size)
	line = f.read(registroCEP.size)
	counter += 1
	record = registroCEP.unpack(line)
	cep = record[cepColumn].decode('latin1')
	if  cep == sys.argv[1]:
		for i in range(0,len(record)-1):
			print(record[i].decode('latin1')) # .decode('latin1')
		break
	elif sys.argv[1] > cep:
		inicio = meio + 1
	else:
		fim = meio - 1

print("Total de Registros Lidos: {}".format(counter))
f.close()