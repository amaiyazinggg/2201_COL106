class y_array:
	def __init__(self, y_sorted_array):
		self.struct = y_sorted_array
	
	def binary_search(self, start, end, x, output_index):
		if len(self.struct) == 0:
			return None
			
		mid = (start + end)//2
		t = self.struct[mid]
		if start < end:
			if t >= x:
				return self.binary_search(start, mid - 1, x, output_index)
			else:
				return self.binary_search(mid+1, end, x, mid)
		elif start == end:
			if t >= x:
				return output_index
			else:
				return mid
		else:
			return output_index

	def y_search(self, y_range):
		l = self.binary_search(0, len(self.struct)-1, y_range[0] , None)
		out = []
		if l == None:
			l = -1
		l+=1
		while l < len(self.struct):
			if self.struct[l] <= y_range[1]:
				out.append(self.struct[l])
			else:
				break
			l+=1
		return out
		
class x_node:
	def __init__(self, x):
		self.value = x
		self.ytree = None
		self.left = None
		self.right = None
		

class PointDatabase:
	def __init__(self, pointlist):
		self.root = None
		self.y_from_x = None
		self.x_from_y = None
		self.build(pointlist)
		
		
	def build_help(self, y_from_x, x_from_y, x_sorted_array, y_sorted_array):
		if len(x_sorted_array) == 0:
			return None
		elif len(x_sorted_array) == 1:
			leaf = x_node(x_sorted_array[0])
			leaf.ytree = y_array([y_sorted_array[0]])
			return leaf
			
		t = len(x_sorted_array)//2
		median = x_sorted_array[t]
		v = x_node(median)
		
		v.ytree = y_array(y_sorted_array)
		
		y_left, y_right = [], []
		
		for y in y_sorted_array:
			a = x_from_y[y]
			if a < median:
				y_left.append(y)
			elif a > median:
				y_right.append(y)
				
		v.left = self.build_help(y_from_x, x_from_y, x_sorted_array[:t], y_left)
		v.right = self.build_help(y_from_x, x_from_y, x_sorted_array[t+1:], y_right)
		return v
		
	def build(self, array):
		x_array = [i[0] for i in array]
		y_from_x = {}
		for i in array:
			y_from_x[i[0]] = i[1]
			
		y_array = [i[1] for i in array]
		x_from_y = {}
		for i in array:
			x_from_y[i[1]] = i[0]
        
		x_array.sort()
		y_array.sort()
		
		self.y_from_x = y_from_x
		self.x_from_y = x_from_y
		self.root = self.build_help(y_from_x, x_from_y, x_array, y_array)
		
		
	def inorder_traversal(self, p):
		if p is not None:
			self.inorder_traversal(p.left)
			print(p.value, end = " ")
			p.ytree.inorder_traversal(p.ytree.root)
			print()
			self.inorder_traversal(p.right)
		return
		
	def search_help(self, x_range, y_range):
		separator = self.root
		
		if separator is None:
			return []
		
		while True:
			#if separator.left is None and separator.right is None:
			#	break
			if separator.value < x_range[0]:
				if separator.right is not None:
					separator = separator.right 
				else:
					separator = None
					break
			elif separator.value > x_range[1]:
				if separator.left is not None:
					separator = separator.left
				else:
					separator = None
					break
			else:
				break
				
		if separator is None:
			return []
		elif separator.left == None and separator.right == None:
			t = self.y_from_x[separator.value]
			if t >= y_range[0] and t <= y_range[1]:
				return [t]
		else:
			v = separator.left
			left = []
			while True:
				if v is None:
					break
				elif v.value >= x_range[0]:
					t = self.y_from_x[v.value]
					if t >= y_range[0] and t <= y_range[1]:
						left.append(t)
					if v.right is not None:
						left += v.right.ytree.y_search(y_range)
					v = v.left
				else:
					v = v.right
			
			v = separator.right
			right = []
			while True:
				if v is None:
					break
				elif v.value <= x_range[1]:
					t = self.y_from_x[v.value]
					if t >= y_range[0] and t <= y_range[1]:
						right.append(t)
					if v.left is not None:
						right += v.left.ytree.y_search(y_range)
					v = v.right
				else:
					v = v.left
					
			t = self.y_from_x[separator.value]
			if t >= y_range[0] and t <= y_range[1]:
				return [t] + left + right
			return left + right 
				
	def searchNearby(self, q, d):
		x_range = [q[0] - d, q[0] + d]
		y_range = [q[1] - d, q[1] + d]
		
		y_list = self.search_help(x_range, y_range)
		
		result = []
		if y_list is None:
			return []
		else:
			for y in y_list:
				result.append((self.x_from_y[y], y))
		return result
		
test = PointDatabase([(2,2), (3,5)])
print(test.searchNearby((2,2),2))