"""
import csv

# Split a dataset based on an attribute and an attribute value
def test_split(index, value, dataset, location_tag = False):
	left, right = list(), list()
	for row in dataset:
		if location_tag == False:
			if row[index] == value:
				left.append(row)
			else:
				right.append(row)
		else:

			if value == "No specific location":
				if row[index] == value:
					left.append(row)
				else:
					right.append(row)
			else:
				if row[index] == value or row[index] == "Other area":
					left.append(row)
				if row[index] != value or row[index] == "Other area":
					right.append(row)

	return left, right

# Calculate the Gini index for a split dataset
def gini_index(groups):
	gini = abs(len(groups[0]) - len(groups[1]))
	return gini

# Select the best split point for a dataset
def get_split(dataset,first_row):
	#class_values = list(set(row[-1] for row in dataset))
	b_index, b_value, b_score, b_groups = 999, 999, 999, None
	containerset = set()
	injuryset = set()

	for index in range(len(dataset[0])-1):
		#print(index)
		for row in dataset:
			#print(first_row)
			#print(row)
			#print(index,"length of first row",len(first_row))
			groups = test_split(index, row[index], dataset, 'location' in first_row[index] ) ##check if it is asking for location
			gini = gini_index(groups)
			#print('X%d < %.3f Gini=%.3f' % ((index+1), row[index], gini))
			if gini < b_score:
				b_index, b_value, b_score, b_groups = index, row[index], gini, groups

	newb_groups = ([],[])
	
	myquestion = first_row[b_index]

	#if "location" not in myquestion:

	for index in range(len(b_groups)):
		for row in b_groups[index]:
			newb_groups[index].append(row[:b_index] + row[b_index+1:])
			containerset.add(row[b_index])
			injuryset.add(row[-1])

	
	newfirstrow = first_row[:b_index] + first_row[b_index+1:]

	
	else:
		#if b_value != "Other area" and b_value != "No specific location":
			#myquestion = myquestion + ", is it at " + b_value
			#containerset = {"Yes",""}

		for index in range(len(b_groups)):
			for row in b_groups[index]:
				newb_groups[index].append(row[:b_index] + row[b_index:])
				containerset.add(row[b_index])
				injuryset.add(row[-1])

		
		newfirstrow = first_row[:b_index] + first_row[b_index:]
	
	#print(b_groups)

	return [{'index':b_index, 'value':b_value, 'groups':newb_groups, "myquestion":myquestion,"options":containerset, "injuryset":injuryset} , newfirstrow]

def terminal_node(mylist):
	if len(mylist) > 2:
		small_value = mylist[0]
		myquestion = "Is your injury " + str(small_value) + "?"
		mydict = {"myquestion":myquestion, 'value':"Yes",'options':{"Yes",""},"injuryset":mylist}
		mydict['left'] = small_value
		mydict['right'] = terminal_node(mylist[1:])
	elif len(mylist) == 2:
		small_value = mylist[0]
		myquestion = "Is your injury " + str(small_value) + "?"
		mydict = {"myquestion":myquestion, 'value':"Yes",'options':{"Yes",""},"injuryset":mylist}
		mydict['left'] = small_value
		mydict['right'] = mylist[1]
	else:
		mydict = mylist[0]

	return mydict

# Create a terminal node value
def to_terminal(group):
	outcomes = [row[-1] for row in group]
	return terminal_node(list(set(outcomes)))
 
# Create child splits for a node or make terminal
def split(node, max_depth, min_size, depth,first_row):
	left, right = node['groups']
	del(node['groups'])
	# check for a no split
	if not left or not right:
		node['left'] = node['right'] = to_terminal(left + right)
		return
	# check for max depth
	if depth >= max_depth:
		node['left'], node['right'] = to_terminal(left), to_terminal(right)
		return
	# process left child
	if len(left) <= min_size:
		node['left'] = to_terminal(left)
	else:
		
		[node['left'],first_row1] = get_split(left, first_row)
		
		
		split(node['left'], max_depth, min_size, depth+1,first_row1)
	# process right child
	if len(right) <= min_size:
		node['right'] = to_terminal(right)
	else:
		[node['right'],first_row2] = get_split(right,first_row)
		
		split(node['right'], max_depth, min_size, depth+1,first_row2)
 
# Build a decision tree
def build_tree(train, max_depth, min_size,first_row):
	[root,first_row] = get_split(train,first_row)
	split(root, max_depth, min_size, 1,first_row)
	return root
 
# Print a decision tree
def print_tree(node,first_row, depth=0):
	if isinstance(node, dict):
		print('%s[X	%s is %s]' % ((depth*'|', (node['myquestion']), str(node['value']))))
		print_tree(node['left'],first_row,depth+1)
		print_tree(node['right'],first_row, depth+1)
	else:
		print('%s[%s]' % ((depth*' ', node)))


# {'index':b_index, 'value':b_value, 'groups':b_groups, "myquestion":myquestion,"options":containerset}

def predict(node):
	print(node['myquestion'])
	print("Here are the options:", node['options'])
	print("List of possible injuries", node['injuryset'])
	uinput = input("Ans: ")

	#while uinput not in node['options']:
		#uinput = input("Ans: ")

	if uinput == node['value']:
		if isinstance(node['left'], dict):
			return predict(node['left'])
		else:
			return node['left']
	else:
		if isinstance(node['right'], dict):
			return predict(node['right'])
		else:
			return node['right']

with open('injurylist.csv') as csv_file:
	csv_reader = list(csv.reader(csv_file, delimiter=','))
	#print(csv_reader[1:])


#first_row = ["location of injury", "is there bleeding", "were you bitten","Injury"]

#csv_reader = [
#	["location of injury", "is there bleeding", "were you bitten","Injury"],
#	["Nose","Yes","","Nosebleed"],
#	["Other area","Yes","Yes","Dog bite"],
#	["No specific location","Yes","","Shock"],
#]

first_row = csv_reader[0]
tree = build_tree(csv_reader[1:], 100, 1,first_row)
#print_tree(tree,first_row)
print(predict(tree))
"""











