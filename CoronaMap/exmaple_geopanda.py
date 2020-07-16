"""
Date: 2020. 06. 16.
Programmer: MH
Description: Code for Corona Map based on Geopandas library and GADM data
"""
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta

# countries = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
# cities = gpd.read_file(gpd.datasets.get_path('naturalearth_cities'))
# print(countries.tail(5))
# ax = countries.plot(column="continent", legend=True, categorical=True)
# ax.set_axis_off()
# ax.plot()
# plt.show()
#
#
from shapely.geometry import Point, shape

geometries = {}
class ZoomPan:
    def __init__(self):
        self.press = None
        self.cur_xlim = None
        self.cur_ylim = None
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.xpress = None
        self.ypress = None


    def zoom_factory(self, ax, base_scale = 2.):
        def zoom(event):
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()

            xdata = event.xdata # get event x location
            ydata = event.ydata # get event y location

            if event.button == 'down':
                # deal with zoom in
                scale_factor = 1 / base_scale
            elif event.button == 'up':
                # deal with zoom out
                scale_factor = base_scale
            else:
                # deal with something that should never happen
                scale_factor = 1

            new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
            new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

            relx = (cur_xlim[1] - xdata)/(cur_xlim[1] - cur_xlim[0])
            rely = (cur_ylim[1] - ydata)/(cur_ylim[1] - cur_ylim[0])

            ax.set_xlim([xdata - new_width * (1-relx), xdata + new_width * (relx)])
            ax.set_ylim([ydata - new_height * (1-rely), ydata + new_height * (rely)])
            ax.figure.canvas.draw()

        fig = ax.get_figure() # get the figure of interest
        fig.canvas.mpl_connect('scroll_event', zoom)

        return zoom

    def pan_factory(self, ax):
        def onPress(event):
            if event.inaxes != ax: return
            self.cur_xlim = ax.get_xlim()
            self.cur_ylim = ax.get_ylim()
            self.press = self.x0, self.y0, event.xdata, event.ydata
            self.x0, self.y0, self.xpress, self.ypress = self.press

        def onRelease(event):
            self.press = None
            ax.figure.canvas.draw()

        def onMotion(event):
            if self.press is None: return
            if event.inaxes != ax: return
            dx = event.xdata - self.xpress
            dy = event.ydata - self.ypress
            self.cur_xlim -= dx
            self.cur_ylim -= dy
            ax.set_xlim(self.cur_xlim)
            ax.set_ylim(self.cur_ylim)

            ax.figure.canvas.draw()

        fig = ax.get_figure() # get the figure of interest

        # attach the call back
        fig.canvas.mpl_connect('button_press_event', onPress)
        fig.canvas.mpl_connect('button_release_event', onRelease)
        fig.canvas.mpl_connect('motion_notify_event', onMotion)

        #return the function
        return onMotion


def set_resion_label(x, y, val, ax):
        ax.text(x, y, val, fontsize=13)

def on_click_resion_1(event):
    print(event.x, event.y, event.xdata, event.ydata)
    point = Point(event.xdata, event.ydata)
    for region in geometries:
        print(region, shape(geometries[region]).within(point), point.within(shape(geometries[region])))
        if point.within(shape(geometries[region])):
            print(region)

shapefile = r".\gadm36_KOR_shp\gadm36_KOR_1.shp"
gdf = gpd.read_file(shapefile)[["NAME_1", "geometry"]]
gdf.columns = ["region", "geometry"]

for i, row in gdf.iterrows():
    geometries[row['region']] = row['geometry']

print(gdf.head())
print(type(gdf.loc[0, 'geometry']))

corona_csv_path = r".\kr_regional_daily.csv"
ko_corona_data = pd.read_csv(corona_csv_path)
target_date = datetime.now().strftime("%Y%m%d")
selected_data = ko_corona_data[ko_corona_data['date'] == int(target_date)]
if selected_data.empty:
    target_date = (datetime.now()-timedelta(days=1)).strftime("%Y%m%d")
    selected_data = ko_corona_data[ko_corona_data['date'] == int(target_date)]
selected_data = selected_data.loc[:, ["region", "confirmed"]]
gdf = gdf.merge(selected_data, on="region", how="outer").dropna()
f, ax = plt.subplots(1, 1, figsize=(16, 8))
for i, row in gdf.iterrows():
    polygon = row['geometry']
    centroid = polygon.centroid
    set_resion_label(centroid.x, centroid.y, row['region'], ax)
gdf.plot(column="confirmed", ax=ax, legend=True, cmap='Reds')
scale = 1.1
zp = ZoomPan()
figZoom = zp.zoom_factory(ax, base_scale=scale)
figPan = zp.pan_factory(ax)

gdf.plot()
cid = f.canvas.mpl_connect("button_press_event", on_click_resion_1)
plt.show()


