"""
Date: 2020. 06. 16.
Programmer: MH
Description: Code for Corona Map displaying Seoul information based on Geopandas library and GADM data
"""
import os

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
from functools import partial
from pyproj import transform, Proj
from shapely.ops import transform
from shapely.geometry import Point, shape


class CoronaMapSeoul:

    def __init__(self):
        self.shapefile = {"Seoul": r"D:\2. Project\Python\CoronaMap\201912기초구역DB_전체분\서울특별시\TL_KODIS_BAS_11.shp"}
        self.corona_csv_path = r".\seoul_confirmed.csv"
        self.geometries = {}
        self.colors = ["white", "gray", "red", "sandybrown", "gold", "olivedrab", "darkgreen", "royalblue", "plum",
                       "lightcoral", "coral", "darkorange", "orange", "ivory", "lightskyblue", "cornsilk"]
        self.cmap = ['viridis', 'plasma', 'inferno', 'magma', 'cividis', 'Greys', 'Purples', 'Blues', 'Greens',
                     'Oranges', 'Reds', 'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu', 'GnBu', 'PuBu', 'YlGnBu',
                     'PuBuGn', 'BuGn', 'YlGn', 'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink', 'spring',
                     'summer', 'autumn', 'winter', 'cool', 'Wistia', 'hot', 'afmhot', 'gist_heat', 'copper']
        self.scale = 1.1    # Zoom scale
        self.ko_corona_data = None
        self.target = None  # label for displayed data

    def displayCoMap(self, region, regionUnit, areaColor, numberFlag, percentageFlag, convertionFlag):
        """
        To display corona map
        :param region: string, the target place
        :param regionUnit: string, the unit of the sub-region; city, district
        :param areaColor: string, color map
        :param numberFlag: boolean, whether a number associated with each infected area should be displayed.
        :param percentageFlag: boolean, whether a percentage (%) associated with each infected area should be displayed.
        :param convertionFlag: boolean, whether a notational/color convention should be displayed on a corner of the map.
        :return:
        """
        self.region_geo_data = gpd.read_file(self.shapefile[region])   # To load geo data following "region"
        self.region_geo_data.crs = {'init': "epsg:5178"}    # To initialize coordinate system (UTMK)
        print(self.region_geo_data.crs)
        self._preprocess_geodata(region)
        self.ko_corona_data = pd.read_csv(self.corona_csv_path)
        self.merge_data()
        self.region_geo_data = self._change_reqion_name(self.region_geo_data)
        self.region_geo_data = self.region_geo_data.to_crs({'init': "epsg:4326"})   # To change coordinate format to Wgs84

        self.fig, self.ax = plt.subplots(1, 1, figsize=(16, 8))
        print(self.region_geo_data.head())
        for i, row in self.region_geo_data.iterrows():
            polygon = row['geometry']
            centroid = polygon.centroid
            text = row["region"]
            if numberFlag:
                text += " (" + str(row['confirmed'])+")"
            # if percentageFlag:
            #     text += " (" + str(int(row['released']/row['confirmed']*100))+"%)"
            self.ax.text(centroid.x, centroid.y, text, fontsize=17)    # To print region Name

        zp = ZoomPan()      # To add mouse wheel zoom
        zp.zoom_factory(self.ax, base_scale=self.scale)
        zp.pan_factory(self.ax)

        # To set display using input color
        if areaColor in self.colors:
            self.region_geo_data.plot(column=self.target, ax=self.ax, legend=convertionFlag, color=areaColor, edgecolor="k")
        elif areaColor in self.cmap:
            self.region_geo_data.plot(column=self.target, ax=self.ax, legend=convertionFlag, cmap=areaColor)
        else:
            self.region_geo_data.plot(column=self.target, ax=self.ax, legend=convertionFlag, color="white", edgecolor="k")

        cid = self.fig.canvas.mpl_connect("button_press_event", self.on_click_region)   # on click event
        plt.show() # To show image

    def on_click_region(self, event):
        """
        To define click event
        :param event:
        :return:
        """
        point = Point(event.xdata, event.ydata)
        for region in self.geometries:
            if point.within(shape(self.geometries[region])):
                print(region)
                self.fig, self.ax = plt.subplots(1, 1, figsize=(16, 8))
                self.region_geo_data = gpd.read_file(self.shapefile[region])   # To load geo data following "region"
                zp = ZoomPan()      # To add mouse wheel zoom
                zp.zoom_factory(self.ax, base_scale=self.scale)
                zp.pan_factory(self.ax)
                self.region_geo_data.plot(ax=self.ax, legend=True, color="white")

                cid = self.fig.canvas.mpl_connect("button_press_event", self.on_click_region)   # on click event
                plt.show() # To show image

    def _preprocess_geodata(self, region):
        """
        To choose target columns from loaded geo data
        :param region: string, input region
        :return:
        """
        self.region_geo_data.geometry = self.region_geo_data.buffer(0.001)
        self.region_geo_data = self.region_geo_data.dissolve(by="SIG_CD")
        self.region_geo_data = self.region_geo_data[["SIG_KOR_NM", "geometry"]]
        self.region_geo_data.columns = ["region", "geometry"]

    def _change_reqion_name(self, df):
        df.loc[df.region == "강남구", "region"] = "Gangnam-gu"
        df.loc[df.region == "강동구", "region"] = "Gangdong-gu"
        df.loc[df.region == "강북구", "region"] = "Gangbuk-gu"
        df.loc[df.region == "강서구", "region"] = "Gangseo-gu"
        df.loc[df.region == "관악구", "region"] = "Gwanak-gu"
        df.loc[df.region == "광진구", "region"] = "Gwangjin-gu"
        df.loc[df.region == "구로구", "region"] = "Guro-gu"
        df.loc[df.region == "금천구", "region"] = "Geumcheon-gu"
        df.loc[df.region == "노원구", "region"] = "Nowon-gu"
        df.loc[df.region == "도봉구", "region"] = "Dobong-gu"
        df.loc[df.region == "동대문구", "region"] = "Dongdaemun-gu"
        df.loc[df.region == "동작구", "region"] = "Dongjak-gu"
        df.loc[df.region == "마포구", "region"] = "Mapo-gu"
        df.loc[df.region == "서대문구", "region"] = "Seodaemun-gu"
        df.loc[df.region == "서초구", "region"] = "Seocho-gu"
        df.loc[df.region == "성동구", "region"] = "Seongdong-gu"
        df.loc[df.region == "성북구", "region"] = "Seongbuk-gu"
        df.loc[df.region == "송파구", "region"] = "Songpa-gu"
        df.loc[df.region == "양천구", "region"] = "Yangcheon-gu"
        df.loc[df.region == "영등포구", "region"] = "Yeongdeungpo-gu"
        df.loc[df.region == "용산구", "region"] = "Yongsan-gu"
        df.loc[df.region == "은평구", "region"] = "Eunpyeong-gu"
        df.loc[df.region == "종로구", "region"] = "Jongno-gu"
        df.loc[df.region == "중구", "region"] = "Jung-gu"
        df.loc[df.region == "중랑구", "region"] = "Jungnang-gu"
        return df

    def merge_data(self):
        """
        To merge geo data and corona data
        :return: None
        """
        self.ko_corona_data = self.ko_corona_data.loc[:, ["region", "confirmed"]]
        self.region_geo_data = self.region_geo_data.merge(self.ko_corona_data, on="region", how="outer").dropna()
        self.target = "confirmed"

class ZoomPan:
    """
    Class for controlling zoom and pan in Matplotlib display
    """
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

            if event.button == 'up':
                # deal with zoom in
                scale_factor = 1 / base_scale
            elif event.button == 'down':
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


if __name__ == '__main__':
    corona_map = CoronaMapSeoul()
    corona_map.displayCoMap("Seoul", "City", 'Reds', True, True, True)