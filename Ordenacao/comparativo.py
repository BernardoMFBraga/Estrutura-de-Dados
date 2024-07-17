import random
import time
import matplotlib.pyplot as plt

# Algoritmos de ordenação

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j >= 0 and key < arr[j]:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = key
    return arr

def selection_sort(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        merge_sort(L)
        merge_sort(R)

        i = j = k = 0

        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
    return arr

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return quick_sort(left) + middle + quick_sort(right)

def bucket_sort(arr):
    num_buckets = len(arr)
    buckets = [[] for _ in range(num_buckets)]

    for value in arr:
        bucket_index = int(value * num_buckets)
        buckets[bucket_index].append(value)

    for i in range(num_buckets):
        buckets[i] = sorted(buckets[i])

    sorted_array = []
    for bucket in buckets:
        sorted_array.extend(bucket)

    return sorted_array

# Função para medir o tempo de execução
def measure_time(sort_func, arr):
    start_time = time.time()
    sort_func(arr.copy())
    end_time = time.time()
    return end_time - start_time

# Tamanhos das listas
sizes = [1000, 10000, 20000, 30000, 40000, 50000]

# Dicionário para armazenar os tempos de execução
times = {
    "Bubble Sort": [],
    "Insertion Sort": [],
    "Selection Sort": [],
    "Merge Sort": [],
    "Quick Sort": [],
    "Bucket Sort": []
}

# Medir o tempo de execução para listas randômicas
for size in sizes:
    arr = [random.random() for _ in range(size)]
    times["Bubble Sort"].append(measure_time(bubble_sort, arr))
    times["Insertion Sort"].append(measure_time(insertion_sort, arr))
    times["Selection Sort"].append(measure_time(selection_sort, arr))
    times["Merge Sort"].append(measure_time(merge_sort, arr))
    times["Quick Sort"].append(measure_time(quick_sort, arr))
    times["Bucket Sort"].append(measure_time(bucket_sort, arr))

# Plotar os resultados
plt.figure(figsize=(12, 8))
for sort_alg in times:
    plt.plot(sizes, times[sort_alg], label=sort_alg)
plt.xlabel('Tamanho da lista')
plt.ylabel('Tempo de execução (s)')
plt.title('Comparação de Tempo dos Algoritmos de Ordenação para Listas Randômicas')
plt.legend()
plt.grid(True)
plt.show()

# Comparação com lista decrescente
descending_arr = list(range(50000, 0, -1))
descending_times = {
    "Bubble Sort": measure_time(bubble_sort, descending_arr),
    "Insertion Sort": measure_time(insertion_sort, descending_arr),
    "Selection Sort": measure_time(selection_sort, descending_arr),
    "Merge Sort": measure_time(merge_sort, descending_arr),
    "Quick Sort": measure_time(quick_sort, descending_arr),
    "Bucket Sort": measure_time(bucket_sort, descending_arr)
}

# Plotar os resultados para lista decrescente
plt.figure(figsize=(12, 8))
plt.bar(descending_times.keys(), descending_times.values())
plt.xlabel('Algoritmo de Ordenação')
plt.ylabel('Tempo de execução (s)')
plt.title('Comparação de Tempo dos Algoritmos de Ordenação para Lista Decrescente')
plt.grid(True)
plt.show()
