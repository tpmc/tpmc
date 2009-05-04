from math import log, floor

def binaryheap(entry, heap=[], index=0):
	if index == 0:
		del heap[:]
		heap += [-1]
	# ensure heap size, we need 2^(level+1)-1 entries
	level = int(floor(log(index+1)/log(2)))
	required = ((1<<level+1)-1)
	if len(heap) < required:
		append = required - len(heap)
		heap += [-1]*append
	# process the entry
	if type(entry) is tuple:
		if len(entry) == 1:
			heap[index]=entry[0]
		else:
			assert(len(entry) == 3)
			# write myself into heap
			heap[index]=entry[0]
			index+=1
			# call children
			binaryheap(entry[1], heap, 2*index-1)
			binaryheap(entry[2], heap, 2*index)
	else:
		heap[index]=entry
	return list(heap)
