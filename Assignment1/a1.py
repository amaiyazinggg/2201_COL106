class node: #defining the nodes of linked list
	def __init__(self):
		self.value = None 
		self.next = None

class Linked_List: #defining the linked list
	def __init__(self):
		self.head = None #initialising the head of the linked list
	def insert_first(self, x): #function that inserts element(x) at the head of the linked list
		if self.head == None: 
			self.head = x #x is set to be the head if the list is empty
		else:
			x.next = self.head
			self.head = x
	def delete_first(self): #function that deletes the first node of the list
		a = self.head.value
		self.head = self.head.next
		return a

class Stack: #defining the stack
	def __init__(self):
		self._mystack = Linked_List() #mystack attribute is set equal to a linked list
	def push(self, x): #push element to the top of the stack
		newnode = node()
		newnode.value = x
		self._mystack.insert_first(newnode)
	def pop(self): #removes the top element from the stack
		return self._mystack.delete_first()
	def peek(self): #retrieves the value of the top element of the stack
		return self._mystack.head.value

def findPositionandDistance(term):
	commands = Stack()
	distance = 0
	axes = ['X', 'Y', 'Z']
	coordinates = [0,0,0]
	multiplier = 1 #the value by which the values have to multiplied
	thisnumber = 0
	counter = 0

	commands.push(1)
	for i in range(len(term)): #iterates over all the elements of the string
		if term[i] in '-+':
			commands.push(term[i]) #pushes the operator to the stack
		elif term[i] in axes:
			operand = commands.pop() #pops the last element
			if operand == '+':
				coordinates[axes.index(term[i])] += multiplier*1 #if +, increment respective coordinate
				counter += multiplier*1
			elif operand == '-':
				coordinates[axes.index(term[i])] -= multiplier*1 #if -, decrement respective coordinate
				counter += multiplier*1
		elif term[i] in '0123456789':
			thisnumber = thisnumber*10 + int(term[i]) #to calculate the number before the bracket
		elif term[i] == '(':
			commands.push(thisnumber*multiplier) #pushes the multiplier onto the stack
			multiplier = commands.peek() #last pushed element is set to be the mulitplier
			thisnumber = 0
		elif term[i] == ')':
			commands.pop() #remove the last pushed element of the stack when closing bracket is reached
			multiplier = commands.peek()
	return [int(i) for i in coordinates]+ [int(counter)]