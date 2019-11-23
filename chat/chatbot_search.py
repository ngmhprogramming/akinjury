import pandas as pd

df = pd.read_csv("injurylist.csv")
#df = base_df.iloc[:,:-1]

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