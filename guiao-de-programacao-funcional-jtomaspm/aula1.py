#Exercicio 1.1
def comprimento(lista):
	if lista == []:
		return 0
	else :
		return 1 + comprimento(lista[1:])

#Exercicio 1.2
def soma(lista):
	if lista == []:
		return 0
	else:
		return lista[0] + soma(lista[1:])

#Exercicio 1.3
def existe(lista, elem):
	if lista == []:
		return False
	if lista[0] == elem:
		return True
	else:
		return existe(lista[1:], elem)

#Exercicio 1.4
def concat(l1, l2):
	if l2 == []:
		return l1
	else: 
		l1[len(l1):] = [l2[0]]
		return concat(l1, l2[1:])

#Exercicio 1.5
def inverte(lista):
	if lista == []:
		return []
	inv = inverte(lista[1:])
	inv[len(inv):] = [lista[0]]
	return inv

#Exercicio 1.6
def capicua(lista):
	if len(lista) == 1:
		return capicua(lista[1:])
	if lista == []:
		return True
	if not (lista[0] == lista[-1]):
		return False
	return capicua(lista[1:-1])
	#return lista == inverte(lista)

#Exercicio 1.7
def explode(lista):
	if lista == []:
		return []
	return lista[0] + explode(lista[1:])

#Exercicio 1.8
def substitui(lista, original, novo):
	if lista == []:
		return []

	if lista[0] == original:
		return [novo] + substitui(lista[1:], original, novo)
	else:
		return [lista[0]] + substitui(lista[1:], original, novo)

#Exercicio 1.9
def insert(elem, lista):
	if lista == []:
		return 0
	if elem > lista[0]:
		return 1 + insert(elem, lista[1:])
	return insert(elem, lista[1:])

def junta_ordenado(lista1, lista2):
	if lista2 == []:
	    return lista1
	ans = lista1
	ans.insert(insert(lista2[0], ans), lista2[0])
	return junta_ordenado(ans, lista2[1:])

	



#Exercicio 2.1
def separar(lista):
	if lista == []:
		return ([], [])
	prev = separar(lista[1:])
	return ([lista[0][0]] + prev[0] ,[lista[0][1]] + prev[1])

	

#Exercicio 2.2
def remove_e_conta(lista, elem):
	if lista == []:
		return [], 0
	
	prev = remove_e_conta(lista[1:] , elem)
	if lista[0] == elem:
		return prev[0] , prev[1] + 1
	else:
		return [lista[0]] + prev[0], prev[1]

#Exercicio 3.1
def cabeca(lista):
	if lista == []:
		return None
	else:
		return lista[0]

#Exercicio 3.2
def cauda(lista):
	if len(lista) < 2:
		return None
	else:
		return lista[1:]

#Exercicio 3.3
def juntar(l1, l2):
	if not len(l1) == len(l2):
		return None
	if l2 == []:
		return []
	prev = juntar(l1[1:], l2[1:])
	return [(l1[0], l2[0])] + prev



#Exercicio 3.4
def menor(lista):
	if lista == []:
		return None
	prev = menor(lista[1:])
	if prev == None:
		return lista[0]
	if prev < lista[0]:
		return prev
	return lista[0]

#Exercicio 3.6
def max_min(lista):
	if lista == []:
		return (None, None)
	prev = max_min(lista[1:])
	if prev == (None, None):
		return (lista[0], lista[0])
	if prev[0] < lista[0]:
		return (lista[0], prev[1])
	if prev[1] > lista[0]:
		return (prev[0], lista[1])
	return prev
