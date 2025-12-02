'''
Дано k відсортованих списків цілих чисел. 
Ваше завдання — об'єднати їх у один відсортований список. 
Тепер при виконанні завдання ви повинні використати мінімальну 
купу для ефективного злиття кількох відсортованих списків 
в один відсортований список. Реалізуйте функцію merge_k_lists, 
яка приймає на вхід список відсортованих списків та повертає 
відсортований список.

Приклад очікуваного результату:

lists = [[1, 4, 5], [1, 3, 4], [2, 6]]
merged_list = merge_k_lists(lists)
print("Відсортований список:", merged_list)

Виведення:

Відсортований список: [1, 1, 2, 3, 4, 4, 5, 6]
'''

# -------------------------------------------------------------------------------------
'''
Знайшов три варіанти вирішення задачі:

Перший:
1. використовуємо списки
2. створюємо купу, куди поміщаємо «верхні» елементи списку
3. у купі крім значення зберігаємо індекс списку та індекс елемента
4. будуємо «мінімальну купу»
5. забираємо верхній з купи - поміщаємо в результат
6. визначаємо номер списку, з якого забрали, і позицію забраного елемента
7. з цього списку беремо наступний за порядком і поміщаємо в купу (якщо він є, якщо ні, пропускаємо цей крок)
8. переходимо до п.5, якщо в купі ще є елементи

Другий:
Все те ж саме, але зі списків робимо черги, тоді не зберігаємо індекс елемента, а просто забираємо з черги перший елемент (popleft). 

Третій:
Такий же, як другий, але без черги: інвертуємо список, щоб сортування було від більшого до меншого, і тоді робимо (pop)

Зробимо досить великий набір тестових даних і виміряємо продуктивність
'''


from typing import Deque, List, Tuple, Callable
from task1 import MinHeap
import random
import time

# -------------------------------------------------------------------------------------
# ------------------------------merge lists--------------------------------------------
# -------------------------------------------------------------------------------------
def merge_k_lists_list(data: List[List[int|float]]) -> List[int|float]:

    heap = MinHeap()
    result = []

    # building list with min value from every list
    min_el_list = []
    for list_idx, list_data in enumerate(data):
        if list_data:
            min_el_list.append((list_data[0], list_idx, 0))

    # convert to heap
    heap.build_heap(min_el_list)
    
    # doing algo
    while heap.heap_size() > 0:
        val, list_idx, el_idx = heap.extract_min()
        result.append(val)
        el_idx += 1
        if len(data[list_idx]) > el_idx:
            heap.insert((data[list_idx][el_idx],list_idx,el_idx))

    return result

def merge_k_lists_deque(data: List[List[int|float]]) -> List[int|float]:
    from collections import deque

    heap = MinHeap()
    result = []

    min_el_list = []
    for list_idx, list_data in enumerate(data):
        if list_data:
            min_el_list.append((list_data[0], list_idx))

    heap.build_heap(min_el_list)

    # convert to deques
    deques: list[Deque] = []
    for list_data in data:
        deques.append(deque(list_data[1:])) # we have to pop first element from deque

    while heap.heap_size() > 0:
        val, deq_idx = heap.extract_min()
        result.append(val)
        if deques[deq_idx]:
            heap.insert((deques[deq_idx].popleft(),deq_idx))

    return result

def merge_k_lists_inverted_list(data: List[List[int|float]]) -> List[int|float]:
    from collections import deque

    heap = MinHeap()
    result = []

    min_el_list = []
    for list_idx, list_data in enumerate(data):
        if list_data:
            min_el_list.append((list_data[0], list_idx))
    
    heap.build_heap(min_el_list)

    # convert to deques
    inverted_lists: list[List] = []
    for list_data in data:
        inverted_lists.append(list_data[:0:-1])

    while heap.heap_size() > 0:
        val, list_idx = heap.extract_min()
        result.append(val)
        if inverted_lists[list_idx]:
            heap.insert((inverted_lists[list_idx].pop(), list_idx))

    return result    

# ---------------------------------------------------------
# Helpers: data generation and baseline implementation
# ---------------------------------------------------------

def generate_sorted_lists(
    k: int,
    min_len: int = 10,
    max_len: int = 100,
    value_min: int = 0,
    value_max: int = 10_000,
) -> List[List[int]]:
    """Generate k sorted lists of random integers."""
    lists = []
    for _ in range(k):
        length = random.randint(min_len, max_len)
        lst = [random.randint(value_min, value_max) for _ in range(length)]
        lst.sort()
        lists.append(lst)
    return lists


def baseline_merge(lists: List[List[int]]) -> List[int]:
    """Simple reference implementation: concatenate and sort."""
    all_items = []
    for lst in lists:
        all_items.extend(lst)
    return sorted(all_items)


# ---------------------------------------------------------
# Benchmark helper
# ---------------------------------------------------------

def benchmark(
    func: Callable[[List[List[int]]], List[int]],
    data: List[List[int]],
    reference: List[int],
    name: str,
    repeat: int = 3,
) -> None:
    """Run func several times, check correctness vs reference, measure time."""
    times = []
    ok = True

    for _ in range(repeat):
        start = time.perf_counter()
        result = func(data)
        end = time.perf_counter()
        times.append(end - start)

        if result != reference:
            ok = False

    avg_time = sum(times) / len(times)
    print(f"{name:30s} | ok={ok} | avg_time={avg_time:.6f} s")


# ---------------------------------------------------------
# Main test runner
# ---------------------------------------------------------

def run_tests():

    # Config: try different sizes
    test_configs = [
        {"k": 5, "min_len": 10, "max_len": 50},
        {"k": 10, "min_len": 50, "max_len": 200},
        {"k": 50, "min_len": 100, "max_len": 300},
        {"k": 100, "min_len": 100, "max_len": 500},
    ]

    for cfg in test_configs:
        print(
            f"\n=== k={cfg['k']}, "
            f"len in [{cfg['min_len']}, {cfg['max_len']}] ==="
        )
        data = generate_sorted_lists(
            k=cfg["k"],
            min_len=cfg["min_len"],
            max_len=cfg["max_len"],
        )

        # Build reference result once
        reference = baseline_merge(data)

        # Run benchmarks
        benchmark(merge_k_lists_list, data, reference, "list+index")
        benchmark(merge_k_lists_deque, data, reference, "deque+popleft")
        benchmark(merge_k_lists_inverted_list, data, reference, "reversed+pop")


if __name__ == "__main__":
    run_tests()