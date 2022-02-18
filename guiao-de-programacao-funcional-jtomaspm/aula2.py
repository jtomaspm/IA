import math

#Exercicio 4.1
impar = lambda x : x%2==1

#Exercicio 4.2
positivo = lambda x : x>=0

#Exercicio 4.3
comparar_modulo = lambda x, y : abs(x)<abs(y)

#Exercicio 4.4
cart2pol = lambda x, y: (math.sqrt(x*x + y*y), math.atan2(y, x))

#Exercicio 4.5
ex5 = lambda f, g, h: lambda x, y, z : h(f(x, y),g(y, z))

#Exercicio 4.6
def quantificador_universal(lista, f):
    if lista == []:
        return True
    if not quantificador_universal(lista[1:], f):
        return False
    return f(lista[0])

#Exercicio 4.9
def ordem(lista, f):
        if lista == []:
            return None
        prev = ordem(lista[1:], f)
        if prev == None:
            return lista[0]
        if f(lista[0], prev):
            return lista[0]
        return prev

#Exercicio 4.10
def filtrar_ordem(lista, f):
    if lista == []:
        return (None, [])
    prev = filtrar_ordem(lista[1:], f)
    if prev == (None, []):
        return (lista[0], [])    
    if f(lista[0], prev[0]):
        return (lista[0], prev[1] + [prev[0]])
    return (prev[0], [lista[0]] + prev[1] )

#Exercicio 5.2
def insert(elem, lista, f):
    if lista == []:
        return 0
    if lista == None:
        return 0
    if f(lista[0], elem):
        return 1 + insert(elem, lista[1:], f)
    return insert(elem, lista[1:], f)

def ordenar_seleccao(lista, f):
    if lista == []:
        return []
    prev = ordenar_seleccao(lista[1:], f)
    insert_pos = insert(lista[0], prev, f)
    if prev == []:
        return [lista[0]]
    prev.insert(insert_pos, lista[0])
    return prev
