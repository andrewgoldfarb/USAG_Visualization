import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re

data_files = ['./cotton_harvested_planted.csv', './soybeans_harvested_planted.csv', 
		'./wheat_harvested_planted.csv', './corn_grain_harvested_planted.csv']
data_columns = []
new_columns = []
planted_df = []
# planted_delta = []
year = []
regex = '^\w*\s\-\s\w*\s\w*\s\s\-\s\s\<b\>\w*\<\/b\>'

comms = {
	"cot_h":"cotton_harvested",
	"cot_p":"cotton_planted",
	"whe_h":"wheat_harvested",
	"whe_p":"wheat_planted",
	"soy_h":"soybeans_harvested",
	"soy_p":"soybeans_planted",
	"cor_h":"corn_harvested",
	"cor_p":"corn_planted",
}
# #read in dta files in get all column names
# for csv in range(len(data_files)):
# 	df = pd.read_csv(data_files[csv])
# 	data_columns.append(df.columns)
# 	for idx in range(len(data_columns)):
# 		new_column = re.search(regex,data_columns[idx])
# 		if new_column:
# 			df.drop()

# # Get all column names that match the regex for the commodity that was harvested or planted
# print(data_columns)
# for idx in range(len(data_columns)):
# 	for name in range(len(data_columns[0])):
# 		new_column = re.search(regex,data_columns[idx][name])

# 		if new_column:
# 			new_columns.append(new_column.string.lower())

# #create column renames
# for idx in range(len(new_columns)):
# 	if 'harvested' in new_columns[idx]:
# 		comm = re.search('\w*',new_columns[idx])
# 		new_columns[idx] = comm.group(0)+'_harvested'
# 	else:
# 		comm = re.search('\w*',new_columns[idx])
# 		new_columns[idx] = comm.group(0)+'_planted'
# # print(new_columns)

'''
Read all the commodity data csv files then drop unnecessary columns and rename remaining columns
to be more user friendly.
'''
df = pd.read_csv('./cotton_harvested_planted.csv')
df.drop(columns=['Week Ending', 'Geo Level', 'State', 'State ANSI',
       'Ag District', 'Ag District Code', 'County', 'County ANSI', 'Zip Code',
       'Region', 'watershed_code', 'Watershed', 'Domain', 'Domain Category', 
	   'Period', 'Program', 'COTTON - ACRES PLANTED  -  <b>CV (%)</b>', 
	   'COTTON - ACRES HARVESTED  -  <b>CV (%)</b>'],axis=1, inplace=True)
df.rename({"COTTON - ACRES HARVESTED  -  <b>VALUE</b>" : "cotton_harvested", 
		"COTTON - ACRES PLANTED  -  <b>VALUE</b>": "cotton_planted"}, axis=1, inplace=True)

df_wheat = pd.read_csv('./wheat_harvested_planted.csv')
df_wheat.drop(columns=['Week Ending', 'Geo Level', 'State', 'State ANSI',
       'Ag District', 'Ag District Code', 'County', 'County ANSI', 'Zip Code',
       'Region', 'watershed_code', 'Watershed', 'Domain', 'Domain Category', 
	   'Period', 'Program', 'WHEAT - ACRES PLANTED  -  <b>CV (%)</b>', 
	   'WHEAT - ACRES HARVESTED  -  <b>CV (%)</b>'],axis=1, inplace=True)
df_wheat.rename({"WHEAT - ACRES HARVESTED  -  <b>VALUE</b>" : "wheat_harvested", 
		"WHEAT - ACRES PLANTED  -  <b>VALUE</b>": "wheat_planted"}, axis=1, inplace=True)

df_soy = pd.read_csv('./soybeans_harvested_planted.csv')
df_soy.drop(columns=['Week Ending', 'Geo Level', 'State', 'State ANSI',
       'Ag District', 'Ag District Code', 'County', 'County ANSI', 'Zip Code',
       'Region', 'watershed_code', 'Watershed', 'Domain', 'Domain Category', 
	   'Period', 'Program', 'SOYBEANS - ACRES PLANTED  -  <b>CV (%)</b>', 
	   'SOYBEANS - ACRES HARVESTED  -  <b>CV (%)</b>'],axis=1, inplace=True)
df_soy.rename({"SOYBEANS - ACRES HARVESTED  -  <b>VALUE</b>" : "soybeans_harvested", 
		"SOYBEANS - ACRES PLANTED  -  <b>VALUE</b>": "soybeans_planted"}, axis=1, inplace=True)

df_corn = pd.read_csv('./corn_grain_harvested_planted.csv')
df_corn.drop(columns=['Week Ending', 'Geo Level', 'State', 'State ANSI',
       'Ag District', 'Ag District Code', 'County', 'County ANSI', 'Zip Code',
       'Region', 'watershed_code', 'Watershed', 'Domain', 'Domain Category', 
	   'Period', 'Program', 'CORN - ACRES PLANTED  -  <b>CV (%)</b>', 
	   'CORN, GRAIN - ACRES HARVESTED  -  <b>CV (%)</b>'],axis=1, inplace=True)
df_corn.rename({"CORN, GRAIN - ACRES HARVESTED  -  <b>VALUE</b>" : "corn_harvested", 
		"CORN - ACRES PLANTED  -  <b>VALUE</b>": "corn_planted"}, axis=1, inplace=True)


'''
Concatenate all 4 main dataframes using an outer join into a single data frame. Perform data transformations
required to have adequate plotting.
'''
frames=[df,df_soy,df_wheat,df_corn]
full_df = pd.concat(frames,join='outer')
melt_df = pd.melt(full_df, id_vars=['Year','Commodity'],value_vars=['cotton_harvested','cotton_planted',
															'wheat_harvested','wheat_planted',
															'soybeans_harvested','soybeans_planted',
															'corn_harvested','corn_planted'])
melt_df.replace('\,','',regex=True,inplace=True)
melt_df = melt_df.dropna()
melt_df = melt_df.astype({'variable': 'str'})
melt_df = melt_df.astype({'value': 'float'})
for val in comms.values():
	planted_delta = []
	# plt.plot(melt_df.loc[(melt_df.variable == val),['Year']], melt_df.loc[(melt_df.variable == val),['value']],label=val)
	if 'planted' in val:
		# print(val)
		planted_df = melt_df.loc[(melt_df.variable == val),['value','Year']]
		# print(planted_df)
		year = planted_df['Year'].tolist()
		planted_df = planted_df['value'].tolist()
		# year = planted_df['Year']
		# print(type(planted_df['value']))
		for idx,val in enumerate(planted_df):
			# print(idx)
			if idx !=0:
				delta = val - planted_df[idx-1]
				planted_delta.append(delta)
		print(len(year))
		print(len(planted_delta))
		plt.scatter(year[1:],planted_delta)
		plt.xticks(rotation=90)
		plt.show()

# plt.legend()
# plt.show()

if __name__ == '__main__':
	print('Running Clean')