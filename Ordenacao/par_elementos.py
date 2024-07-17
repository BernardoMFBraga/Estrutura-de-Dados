def tem_par_com_soma(lista, soma_alvo): 
#Função principal que verifica se a lista contém um par de elementos cuja soma seja igual ao valor soma_alvo.
    complementos = set()  # Conjunto para armazenar os complementos
    for numero in lista:
        if soma_alvo - numero in complementos: #Verifica se o complemento necessário para formar a soma_alvo com numero está no conjunto complementos
            return True
        complementos.add(numero) # Adiciona o elemento atual ao conjunto de complementos.
    return False

# Exemplo de uso
lista = [10, 15, 3, 7]
soma_alvo = 17
print(tem_par_com_soma(lista, soma_alvo))  # Saída: True