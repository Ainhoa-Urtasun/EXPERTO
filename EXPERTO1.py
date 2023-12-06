import requests
import json
import pandas
import geopandas
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import pyproj
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
mydata = mydata[(mydata['na_item'].str.contains('Real'))&(mydata['na_item'].str.contains('person')]
print(mydata)
mydata.rename(columns={'geo':'ADMIN'},inplace=True)
#table = mydata[['ADMIN','Porcentaje']]

