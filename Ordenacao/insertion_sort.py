def insertion_sort(arr):
    # Percorre do segundo elemento até o final da lista
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        # Move os elementos de arr[0..i-1], que são maiores que key, uma posição à frente
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

# Exemplo de uso
arr = [5, 2, 4, 6, 1, 3]
insertion_sort(arr)
print("Lista ordenada:", arr)
