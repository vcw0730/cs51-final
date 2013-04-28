import random

class BinaryHeap(object):
    def __init__(self):
        self.heap = []

    # * * * * *
    # Pushes an element into the heap
    # * * * * *
    def push(self, x):
        self.heap.append(x)
        self.heapifyUp(self.size() - 1)

    # * * * * *
    # Pops an element out of the heap
    # * * * * *
    def pop(self):
        min = self.heap[0]
        self.heap[0] = self.heap[self.size() - 1]
        self.heap.pop()
        if self.size() > 1:
            self.heapifyDown(0)
        return min

    # * * * * *
    # returns the size of the heap
    # * * * * * 
    def size(self):
        return len(self.heap)

    def smaller_child(self, parent):
        i = (parent << 1) + 2
        if i > (self.size() - 1):
            return i - 1
        elif self.heap[i - 1] < self.heap[i]:
            return i - 1
        else:
            return i
            
    def parent (self, child):
        if (child != 0):
            i = (child - 1) >> 1
            return i
        else:
            return -3

    # * * * * *
    # When you add an element to the heap, we want to
    # insert it in the last spot and then move it upwards
    # by comparing to parent nodes, if smaller then 
    # swapping occurs, this is repeated until in order. 
    # * * * * *
    def heapifyUp (self, current):
        mother = self.parent(current)
        while current > 0 and  mother>= 0 and self.heap[mother] > self.heap[current]:
            self.heap[mother], self.heap[current] = self.heap[current], self.heap[mother]
            current = self.parent(current)
            mother = self.parent(current)
    
    # * * * * *
    # When you remove an element from the heap
    # we want to maintain the structure of the heap
    # so we move everything down a spot by comparing
    # the key of the parent node with the children, if 
    # children have lower priority, it is swapped, and is 
    # repeated for newly swapped nodes until heap is
    # re-established 
    # * * * * *
    
    def heapifyDown (self, current):
        while ((current << 1) + 1) <= (self.size() - 1):
            child = self.smaller_child(current)
            if self.heap[current] > self.heap[child]:
                self.heap[current], self.heap[child] = self.heap[child], self.heap[current]
            current = child
    

    # * * * * *
    # Defines a functional call which allows us to check
    # whether the BinaryHeap is working properly
    # * * * * *

def main():
    a = BinaryHeap()
    for each in range(10):
        a.push(random.randint(0,50))

    print a.heap

    for each in range(10):
        print a.pop()
