from CodesName import cods

def master_of_cods():
    rel = {}
    k = 1
    for i in cods:
        #print(k, cods[i][0]) # Выведи если надо
        rel[k] = cods[i][0]
        k += 1
    return rel

rel = master_of_cods()