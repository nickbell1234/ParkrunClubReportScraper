import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
from geopandas import GeoDataFrame

df_all_locations = pd.read_csv('parkrunUK.csv')
df_club_locations = pd.read_csv('parkrunData2022_21485.csv')
#df_club_locations = df_club_locations.query("Name == 'Nicholas BELL'")

df = df_club_locations.join(df_all_locations.set_index('Event'),on='Parkrun')

df_count= df.groupby(['Parkrun','Latitude','Longitude']).count().reset_index()
df_count.drop(['Position','GenderPosition','Name','Time','Country','State','County','Website'], axis=1, inplace=True)

geometry = [Point(xy) for xy in zip(df_count['Longitude'], df_count['Latitude'])]
gdf = GeoDataFrame(df_count, geometry=geometry)   
uk = gpd.read_file('Shapes\GBR_adm1.shp')
ax = gdf.plot(ax=uk.plot(figsize=(12, 12)), marker='o', color='red', markersize=df_count['Date'])
for x, y, label in zip(gdf.geometry.x, gdf.geometry.y, gdf.Parkrun):
    ax.annotate(label, xy=(x, y), xytext=(2, 2), textcoords="offset points")

plt.show()