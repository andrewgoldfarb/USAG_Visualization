import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('./export_comm2.csv')
values = []
corn, wheat, soybeans, cotton = [], [], [], []
years = []

drop_list = [year for idx,year in enumerate(df.columns[1:]) if idx%2 == 0]

df = df.drop(columns=drop_list).drop(0,axis=0)
for idx,year in enumerate(df.columns[1:]):
	df.rename({year:drop_list[idx]},axis=1,inplace=True)


melt_df = pd.melt(df, id_vars=['Product'],value_vars=df.columns[1:])

for idx,comm in enumerate(melt_df.Product):
	#needs to send to series
	if comm == 'Corn':
		corn.append(float(melt_df['value'][idx]))
		years.append(melt_df['variable'][idx])
	elif comm == 'Wheat':
		wheat.append(float(melt_df['value'][idx]))
	elif comm == 'Soybeans':
		soybeans.append(float(melt_df['value'][idx]))
	else:
		cotton.append(float(melt_df['value'][idx]))
	
values.append(pd.Series(corn))
values.append(pd.Series(wheat))
values.append(pd.Series(soybeans))
values.append(pd.Series(cotton))
'''
plt.plot(years,values[0], label="Corn Exports")
plt.plot(years,values[1], label="Wheat Exports")
plt.plot(years,values[2], label="Soybeans Exports")
plt.plot(years,values[3], label="Cotton Exports")
plt.xticks(rotation=90)
plt.legend()
plt.show()
'''

# Calculate differences year/year 
delta=[val-values[0][idx-1] for idx, val in enumerate(values[0]) if idx != 0]
plt.scatter(years[1:],delta)
plt.xticks(rotation=90)
plt.show()
print(delta)
