'''
Уявіть, що вам на технічному інтерв'ю дають наступну задачу, яку треба розв'язати за допомогою купи.

Є декілька мережевих кабелів різної довжини, їх потрібно об'єднати по два за раз в один кабель, 
використовуючи з'єднувачі, у порядку, який призведе до найменших витрат. Витрати на з'єднання двох кабелів 
дорівнюють їхній сумі довжин, а загальні витрати дорівнюють сумі з'єднання всіх кабелів.

Завдання полягає в тому, щоб знайти порядок об'єднання, який мінімізує загальні витрати.
'''

# take heap class from hw-03
# but for this task we need to modificate from max heap to min heap

# idea: pop root = min1, heapify_down, pop root = min2, heapify_down
# connect two minimal length cables (min1 + min2), add new connected cable to end, heapify_up
# repeat until 1 cable left

# -------------------------------------------------------------------------------------
# ------------------------------heap class----------------------------------------------
# -------------------------------------------------------------------------------------
class MinHeap:
    def __init__(self) -> None:
        self.heap = []
    def parent(self, index):
        return (index-1)//2
    def left_child(self, index):
        return 2*index+1
    def right_child(self, index):
        return 2*index+2        
    def heap_size(self):
        return len(self.heap)

    def heapify_up(self, index):
        while index != 0 and self.heap[self.parent(index)] > self.heap[index]:
            self.heap[self.parent(index)], self.heap[index] = self.heap[index], self.heap[self.parent(index)]
            index = self.parent(index)

    def heapify_down(self, index):
        size = len(self.heap)
        while True:
            smallest = index
            left = self.left_child(index)
            right = self.right_child(index)

            if left < size and self.heap[left] < self.heap[smallest]:
                smallest = left
            if right < size and self.heap[right] < self.heap[smallest]:
                smallest = right
            if smallest != index:
                self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
                index = smallest
            else:
                break

    def insert(self, key):
        self.heap.append(key)
        self.heapify_up(len(self.heap)-1)

    def extract_min(self):
        if not self.heap:
            return None 
        if len(self.heap) == 1:
            return self.heap.pop()                       
        minimum = self.heap[0]
        self.heap[0] = self.heap.pop()        
        self.heapify_down(0)
        return minimum

    def build_heap(self, data):
        self.heap = data[:]
        for i in range(len(self.heap)//2-1, -1, -1):
            self.heapify_down(i)


def main():

    # list of cables (sample)
    cables = [1.5, 2.1, 3.3, 4.9, 5.5, 2.4, 3.2]

    # create heap
    heap = MinHeap()
    heap.build_heap(cables)

    cost = 0.0
    heap_size = heap.heap_size()
    # until one cable left
    while heap_size > 1:
        # pop two cables
        min_cable_1 = heap.extract_min()
        min_cable_2 = heap.extract_min()
        # connect
        new_cable = min_cable_1 + min_cable_2
        # add to heap
        heap.insert(new_cable)

        # update cost and size
        cost += new_cable
        heap_size -= 1 # 2 removed, 1 added

    print(f"Minimal connection cost for: {cables} is {cost:.2f}")

if __name__ == "__main__":
    main()