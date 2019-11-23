import pandas as pd


class diagnoser():
	def __init__(self):
		self.df = pd.read_csv("injurylist.csv")
		self.counter = 0
		self.max = self.df.shape[1] - 1
		self.colnames = list(self.df.columns)

	def conclude_injury(self):
		#print("Injury found!")
		return list(self.df['Injury name'])

	def ask_qn(self):
		options = list(self.df.loc[:,self.colnames[self.counter]].unique())

		if len(options) > 1: 
			return [self.colnames[self.counter]], options, list(self.df['Injury name']) # returns question, list of allowed responses, and the possible injuries
			
		else:
			if self.counter < self.max:
				self.counter += 1
				return self.ask_qn()
			else:
				return False
				

	def ans_qn(self,value):
		item = self.colnames[self.counter]
		if 'location' not in item:
			self.df = self.df.loc[self.df[item] == value,:]
		else:
			if value != "No specific location":
				self.df = self.df.loc[ (self.df[item] == value) | (self.df[item] == 'Other area'),:]
			else:
				self.df = self.df.loc[self.df[item] == value,:]

		self.counter += 1
		if len(self.df) == 1:
			#return self.conclude_injury()
			return False
		else:
			return True

		# @mun heen is u see any of the 2 functions return False --> means that injuries has concluded, u need to call conclude_injuries to find out the injuries


"""
#df = base_df.iloc[:,:-1]
df = pd.read_csv("injurylist.csv")

for item in df.iloc[:,:-1]:
	options = list(df.loc[:,item].unique())
	
	if len(options) > 1: 
		print("Question:",item)
		print("Options:",options)
		uinput = input("Input pls: ")
		while uinput not in options:
			uinput = input("Input pls: ")

		if "location" not in item:
			df = df.loc[df[item] == uinput,:]
		else:
			if uinput != "No specific location":
				df = df.loc[ (df[item] == uinput) | (df[item] == 'Other area'),:]
			else:
				df = df.loc[df[item] == uinput,:]

		print("Possible injuries",list(df['Injury name']))

	if len(df) == 1:
		print("Injury found! ->",df.iloc[0,df.shape[1]-1])
		break

if len(df) != 1:
	print("Injury found! The following injuries are possible")
	print(list(df['Injury name']))
"""

