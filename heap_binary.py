class BinaryHeap(object):
    def __init__(self):
        self.heap = []

    def push(self, x):
        self.heap.append(x)
        if self.size() != 1:
            self.heapifyUp(self.size() - 1)

    def pop(self):
        min = self.heap[0]
        self.heap[0] = self.heap[self.size() - 1]
        self.heap.pop()
        self.heapifyDown(0)
        return min

    def size(self):
        return len(self.heap)

    def left(self, parent):
        i = (parent << 1) + 1
        if (i < self.size()):
            return i
        else:
            return -1

    def right (self, parent):
        i = (parent << 1) + 2
        if (i < self.size()):
            return i
        else:
            return -2

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
        while current > 0 and mother >= 0 and self.heap[mother] > self.heap[current]:
            temp = self.heap[mother]
            self.heap[mother] = self.heap[current]
            self.heap[current] = temp
            current = mother
    
    # * * * * *
    # When you remove an element from the heap
    # we want to maintain the structure of the heap
    # so we move everything down a spot by comparing
    # the key of the parent node with the children, if 
    # children have lower priority, it is swapped, and is 
    # repeated for newly swapped nodes until heap is
    # re-established 
    # * * * * */
    def heapifyDown (self, current):
        lchild = self.left(current)
        rchild = self.right(current)
        if ((lchild > 0) and (rchild > 0) and (self.heap[lchild] > self.heap[rchild])):
            lchild = rchild
        if (lchild > 0):
            temp = self.heap[current]
            self.heap[current] = self.heap[lchild]
            self.heap[lchild] = temp
            self.heapifyDown(lchild)
