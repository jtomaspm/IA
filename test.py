a = [[[],['e']],[],[[['e'],[],['e']],[]],[]]

def clean(lst):
    temp = a
    res = []
    while temp:
        temp2 = []
        for elem in temp:
            if isinstance(elem, list):
                if elem != []:
                    for e in elem:
                        temp2.append(e)
            else:
                res.append(elem)
        print(temp)
        print(res)
        temp = temp2
    return res

print(clean(a))
                
            
