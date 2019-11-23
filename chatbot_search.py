import pandas as pd


class diagnoser():
	def __init__(self):
		self.df = pd.read_csv("injurylist.csv")
		self.counter = 0
		self.max = self.df.shape[1] - 1
		self.colnames = list(self.df.columns)

	def conclude_injury(self):
		return list(self.df['Injury name'])

	def ask_qn(self):
		options = list(self.df.loc[:,self.colnames[self.counter]].unique())
		if len(options) > 1: 
			return [self.colnames[self.counter]], options, list(self.df['Injury name'])
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
			return False
		else:
			return True

if __name__ == "__main__":
	yay = diagnoser()
	while yay.ask_qn() != False:
		[qn, options, possibleinjury] = yay.ask_qn()
		print(qn)
		print(options)
		print(possibleinjury)
		myinput = input("ans ")
		yay.ans_qn(myinput)

	print(yay.conclude_injury())



