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
url = '{}{}'.format(fixed,'bd_l_form')
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

mydata = mydata[mydata['indic_sbs']=='Enterprises - number']
mydata = mydata[mydata['nace_r2'].str.contains('Industry, construction and market services')]
mydata = mydata[mydata['time']=='2021']
mydata = mydata[(mydata['leg_form']=='Total')|(mydata['leg_form']=='Partnership, co-operatives, associations, etc.')]
mydata = mydata[['geo','leg_form',0]]
mydata.rename(columns={'geo':'ADMIN'},inplace=True)
mydata.rename(columns={0:'Empresas'},inplace=True)
mydata = mydata.pivot(index='ADMIN',columns='leg_form',values='Empresas').reset_index()
mydata['Porcentaje'] = 100*mydata['Partnership, co-operatives, associations, etc.']/mydata['Total']
mydata = mydata[['ADMIN','Porcentaje']]
print(mydata)

world = geopandas.read_file('/content/EXPERTO/ne_110m_admin_0_countries.zip')[['ADMIN','geometry']]
polygon = Polygon([(-25,35),(40,35),(40,75),(-25,75)])
europe = geopandas.clip(world,polygon)

mydata = mydata.merge(europe,on='ADMIN',how='right')
mydata = geopandas.GeoDataFrame(mydata,geometry='geometry')
fig,ax = plt.subplots(1,figsize=(10,10))
mydata.plot(column='Porcentaje',alpha=0.8,cmap='viridis',ax=ax,legend=True)
ax.set_title('Porcentaje de cooperativas y asociaciones (fuente: Eurostat)')
ax.axis('off')
    
