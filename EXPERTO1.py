import requests
import json
import pandas
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

fixed = 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/'
url = '{}{}'.format(fixed,'namq_10_lp_ulc')
metadata = requests.get(url).json()
print(metadata['label'])
data = pandas.Series(metadata['value']).rename(index=int).sort_index()
n = 1 # Initialize the result to 1
for num in metadata['size']:
  n *= num
data = data.reindex(range(0,n),fill_value=0)
structure = [pandas.DataFrame({key:val for key,val in metadata['dimension'][dim]['category'].items()}).sort_values('index')['label'].values for dim in metadata['id']]
data.index = pandas.MultiIndex.from_product(structure,names=metadata['id'])
mydata = data.reset_index()

mydata = mydata[mydata.geo=='Spain']
mydata = mydata[mydata.unit=='Index, 2015=100']
mydata = mydata[mydata['s_adj'].str.contains('Unadjusted')]
mydata = mydata[mydata['na_item'].str.contains('work')]
mydata = mydata[mydata.time.str.contains('20')]
mydata = mydata.pivot(index='time',columns='na_item',values=0).reset_index()

plt.figure(figsize=(20,6))  # Adjust the figure size if needed
plt.plot(mydata.time,mydata['Nominal unit labour cost based on hours worked'], label='Variable 1', marker='o')  # Plotting variable 1
plt.plot(mydata.time,mydata['Real labour productivity per hour worked'], label='Variable 2', marker='x')  # Plotting variable 2
plt.xlabel('Time')
plt.ylabel('Value')
plt.title('Variables Across Time')
plt.legend()

