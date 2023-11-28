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
url = '{}{}'.format(fixed,'bd_size')
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
mydata = mydata[mydata['age']=='Total']
mydata = mydata[mydata['sizeclas']=='Total']
mydata = mydata[mydata['indic_sbs']=='Enterprises - number']
mydata = mydata[mydata['nace_r2'].str.contains('Industry, construction and market services')]
mydata = mydata[['geo','time',0]]
print(mydata)
mydata.rename(columns={'geo':'ADMIN'},inplace=True)
mydata.rename(columns={'time':'Año'},inplace=True)
mydata.rename(columns={0:'Número de empresas'},inplace=True)
datos = mydata.copy()
mydata = mydata.loc[mydata['Año']==2021,['ADMIN','Número de empresas']]

world = geopandas.read_file('/content/EXPERTO/ne_110m_admin_0_countries.zip')[['ADMIN','geometry']]
polygon = Polygon([(-25,35),(40,35),(40,75),(-25,75)])
europe = geopandas.clip(world,polygon)

mydata = mydata.merge(europe,on='ADMIN',how='right')
mydata = geopandas.GeoDataFrame(mydata,geometry='geometry')
fig,ax = plt.subplots(1,figsize=(10,10))
mydata.plot(column='Número de empresas',alpha=0.8,cmap='viridis',ax=ax,legend=True)
ax.set_title('Número de empresas por forma legal (fuente: Eurostat)')
ax.axis('off')
    
