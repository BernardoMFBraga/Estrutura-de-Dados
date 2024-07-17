def bucket_sort(arr):
    # 1. Criar buckets vazios
    num_buckets = len(arr)  # Define o número de buckets como o tamanho do array
    buckets = [[] for _ in range(num_buckets)] #Cria uma lista de listas vazias (buckets).

    # 2. Distribuir elementos nos buckets
    for value in arr: #Itera sobre cada elemento do array.
        bucket_index = int(value * num_buckets) #Calcula o índice do bucket para o valor atual.
        buckets[bucket_index].append(value) #Adiciona o valor ao bucket correspondente.

    # 3. Ordenar individualmente cada bucket usando sorted()
    for i in range(num_buckets): #Itera sobre cada bucket.
        buckets[i] = sorted(buckets[i]) #Ordena o bucket usando a função sorted().

    # 4. Concatenar todos os buckets em uma lista ordenada
    sorted_array = [] #Inicializa a lista para armazenar o array ordenado.
    for bucket in buckets: #Itera sobre cada bucket.
        sorted_array.extend(bucket) #Adiciona os elementos do bucket ao array ordenado.

    return sorted_array #Retorna o array ordenado.

# Exemplo de uso
arr = [0.42, 0.32, 0.23, 0.52, 0.25, 0.47, 0.51]
sorted_arr = bucket_sort(arr)
print("Array ordenado:", sorted_arr)
