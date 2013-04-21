# I have no idea if this works or not what the fuck is this
# TODO: Translate: 

#include <iostream> 
#include <vector>
#include <iterator>
#include <sstream>

#is this correct?
type pair (float, unsigned long)

# TODO: Translate:
# using namespace std;

class BinaryHeap:
	def BinaryHeap ():

	def ~BinaryHeap ():

	def heap:

	def heapID:

	# pushes the element into the heap
	def push (type tuple element):
		if heapID [element.second] != None :
			heapID [element.second] = element.first
		else :
			heap.push_back(element)
			heapifyup(heap.size() - 1)

	# returns the minimum element which is located at the root of the tree
	def pop ():
		min = heap.front().first
		heap[0] = heap[heap.size() - 1]
		heap.pop_back()
		heapifydown(0)
		return min

	def print ():
		# not sure what cout << Heap does
		iterator_pos = heap.begin()
		while pos != heap.eng():
			# cout << (*pos).first << " ";
			++pos
		cout << endl



	def size () :
		return heap.size () 

	def left (parent):
		int i = (parent << 1) + 1
		if i < heap.size() then:
			return i
		else:
			return -1

	def right (parent):
		int i = (parent << 1) + 2
		if i < heap.size() then:
			return i
		else: 
			return -1

	def parent (child):
		if children != 0: 
			int i = (child - 1) >> 1
			return i
		return -1

	def heapifyup (current):
		while (current > 0 && parent[current].first && 
		      heap[parent(current)].first > heap[current].first):
			pair temp = heap[parent(current)]
			heap[parent(current)] = heap[current]
			heap[current] = temp
			current = parent(current)

	def heapifydown (current):
		child = left(current)
		if (child > 0 && right(current) > 0 && 
			heap[child].first > heap[right(current)].first):
			child = right(current)
		if child > 0:
			pair temp = heap[current]
			heap[current] = heap[child]
			heap[child] = temp
			heapifydown(child)

	def heapID :


