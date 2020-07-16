"""
Date: 2020. 06. 16.
Programmer: MH
Description: Code for Corona Map based on Geopandas library and GADM data
"""
import os

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta

import requests
from matplotlib.lines import Line2D
from matplotlib.patches import PathPatch
from matplotlib.textpath import TextPath
from shapely.geometry import Point, shape

from corona_map_seoul import CoronaMapSeoul


class CoronaMap:

    def __init__(self):
        self.shapefile = {"South Korea": r".\gadm36_KOR_shp\gadm36_KOR_1.shp",
                          "South Korea 2": r".\gadm36_KOR_shp\gadm36_KOR_2.shp",
                          "Seoul": r"D:\2. Project\Python\CoronaMap\201912기초구역DB_전체분\서울특별시\TL_KODIS_BAS_11.shp"}
        self.corona_csv_path = r".\kr_regional_daily.csv"
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

        self.circle_legend_elements = [Line2D([0], [0], marker='o', color='b', label='<100', markerfacecolor='b',
                                              markersize=4),
                                       Line2D([0], [0], marker='o', color='b', label='<500', markerfacecolor='b',
                                              markersize=7),
                                       Line2D([0], [0], marker='o', color='b', label='<1000', markerfacecolor='b',
                                              markersize=10),
                                       Line2D([0], [0], marker='o', color='b', label='<5000', markerfacecolor='b',
                                              markersize=20),
                                       Line2D([0], [0], marker='o', color='b', label='>=5000', markerfacecolor='b',
                                              markersize=30),
                                       ]

    def _compute_radius(self, populataion):
        if populataion < 100:
            return 0.04
        elif populataion < 500:
            return 0.07
        elif populataion < 1000:
            return 0.1
        elif populataion < 5000:
            return 0.2
        else:
            return 0.3


    def displayCoMap(self, region, regionUnit, areaColor, numberFlag,percentageFlag, convertionFlag, circleFlag):
        """
        To display corona map
        :param region: string, the target place
        :param regionUnit: string, the unit of the sub-region; city, district
        :param areaColor: string, color map
        :param numberFlag: boolean, whether a number associated with each infected area should be displayed.
        :param percentageFlag: boolean, whether a percentage (%) associated with each infected area should be displayed.
        :param convertionFlag: boolean, whether a notational/color convention should be displayed on a corner of the map.
        :param circleFlag: boolean, whether drawing the rate of danger as circle
        :return:
        """
        self.region_geo_data = gpd.read_file(self.shapefile[region])   # To load geo data following "region"
        if region == "South Korea" and regionUnit=="District":
            self.region_geo_data = gpd.read_file(self.shapefile["South Korea 2"])   # To load geo data following "region"
        self._preprocess_geodata(region)
        if region == "South Korea":
            self.load_corona_data(regionUnit)
        if self.ko_corona_data is not None:
            self.merge_data()

        self.fig, self.ax = plt.subplots(1, 1, figsize=(15, 8))
        print(self.region_geo_data.head())
        count = 0
        for i, row in self.region_geo_data.iterrows():
            polygon = row['geometry']
            centroid = polygon.centroid
            region = row["region"]
            text = region
            if numberFlag:      # To write number data
                text += " (" + str(row['confirmed'])+")"
            if percentageFlag:  # To write percentage data
                text += " (" + str(int(row['released']/row['confirmed']*100))+"%)"
            if circleFlag:      # To draw circle
                radius = self._compute_radius(row['confirmed'])
                circle = plt.Circle((centroid.x, centroid.y), radius, color='b', alpha=0.7)
                self.ax.add_artist(circle)
                self.ax.legend(handles=self.circle_legend_elements, loc='lower right')
            x = centroid.x
            y = centroid.y
            # To text
            if "Incheon" == region:
                y += 0.1
                x -= 0.05
            if "Gyeonggi-do" == region:
                y -= 0.1
            if "Chungcheongnam-do" == region:
                x -= 0.4
                y -= 0.08
            if "Busan" == region:
                y -= 0.05
                x += 0.05
            # if count % 2 == 0:
            #     y = centroid.y+0.5
            # else:
            #     y = centroid.y-0.5
            # count+= 1
            tp = TextPath((x, y), text, size=0.12)
            plt.gca().add_patch(PathPatch(tp, color="black"))
            # self.ax.text(centroid.x, centroid.y, text, fontsize=17)    # To print region Name

        zp = ZoomPan()      # To add mouse wheel zoom
        zp.zoom_factory(self.ax, base_scale=self.scale)
        zp.pan_factory(self.ax)
        self.region_geo_data.plot(ax=self.ax, cmap=areaColor)

        # # To set display using input color
        # if areaColor in self.colors:
        #     self.region_geo_data.plot(column=self.target, ax=self.ax, legend=convertionFlag, color=areaColor, edgecolor="k")
        # elif areaColor in self.cmap:
        #     self.region_geo_data.plot(column=self.target, ax=self.ax, legend=convertionFlag, cmap=areaColor)
        # else:
        #     self.region_geo_data.plot(column=self.target, ax=self.ax, legend=convertionFlag, color="white", edgecolor="k")


        self.fig.canvas.mpl_connect("button_press_event", self.on_click_region)   # on click event
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
                if region == "Seoul":
                    corona_map_seoul = CoronaMapSeoul()
                    corona_map_seoul.displayCoMap("Seoul", "City", "Reds", True, True, True)

    def _preprocess_geodata(self, region):
        """
        To choose target columns from loaded geo data
        :param region: string, input region
        :return:
        """
        if region == "South Korea":  # if the target is South Korea
            self.region_geo_data = self.region_geo_data[["NAME_1", "geometry"]]
            print(self.region_geo_data.head(100))
            self.region_geo_data.columns = ["region", "geometry"]
            for i, row in self.region_geo_data.iterrows():
                self.geometries[row['region']] = row['geometry']
        elif region == "Seoul":
            self.region_geo_data.geometry = self.region_geo_data.buffer(0.001)
            self.region_geo_data = self.region_geo_data.dissolve(by="SIG_CD")
            self.region_geo_data = self.region_geo_data[["SIG_KOR_NM", "geometry"]]
            self.region_geo_data.columns = ["region", "geometry"]

    def load_corona_data(self, regionUnit):
        """
        To load corona data from csv file
        :return:
        """
        if regionUnit == "City":
            csv_url = "https://raw.githubusercontent.com/jooeungen/coronaboard_kr/master/kr_regional_daily.csv"
            req = requests.get(csv_url)
            url_content = req.content  # To download Korea COVID-19 Data
            try:
                csv_file = open(self.corona_csv_path, 'wb')
            except:
                os.remove(self.corona_csv_path)
                csv_file = open(self.corona_csv_path, 'wb')
            csv_file.write(url_content)
            csv_file.close()

            ko_whole_corona_data = pd.read_csv(self.corona_csv_path)
            ko_whole_corona_data = self._change_reqion_name(ko_whole_corona_data)
            print(ko_whole_corona_data.head())
            target_date = datetime.now().strftime("%Y%m%d")     # To set target date to today
            self.ko_corona_data = ko_whole_corona_data[ko_whole_corona_data['date'] == int(target_date)]    # To get today's data
            if self.ko_corona_data.empty: # if there is no today's data
                target_date = (datetime.now()-timedelta(days=1)).strftime("%Y%m%d") # To set  target date to yesterday
                self.ko_corona_data = ko_whole_corona_data[ko_whole_corona_data['date'] == int(target_date)]  # To load data
        elif regionUnit == "District":
            pass

    def _change_reqion_name(self, df):
        """
        To change city name from Korean to English
        :param df:
        :return:
        """
        df.loc[df.region == "서울", "region"] = "Seoul"
        df.loc[df.region == "부산", "region"] = "Busan"
        df.loc[df.region == "대구", "region"] = "Daegu"
        df.loc[df.region == "인천", "region"] = "Incheon"
        df.loc[df.region == "광주", "region"] = "Gwangju"
        df.loc[df.region == "대전", "region"] = "Daejeon"
        df.loc[df.region == "울산", "region"] = "Ulsan"
        df.loc[df.region == "세종", "region"] = "Sejong"
        df.loc[df.region == "경기", "region"] = "Gyeonggi-do"
        df.loc[df.region == "강원", "region"] = "Gangwon-do"
        df.loc[df.region == "충북", "region"] = "Chungcheongbuk-do"
        df.loc[df.region == "충남", "region"] = "Chungcheongnam-do"
        df.loc[df.region == "전북", "region"] = "Jeollabuk-do"
        df.loc[df.region == "전남", "region"] = "Jeollanam-do"
        df.loc[df.region == "경북", "region"] = "Gyeongsangbuk-do"
        df.loc[df.region == "경남", "region"] = "Gyeongsangnam-do"
        df.loc[df.region == "제주", "region"] = "Jeju"
        df.loc[df.region == "검역", "region"] = "Quarantine"
        return df

    def merge_data(self):
        """
        To merge geo data and corona data
        :return: None
        """
        self.ko_corona_data = self.ko_corona_data.loc[:, ["region", "confirmed", "death", "released"]]
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
    corona_map = CoronaMap()
    # corona_map.displayCoMap("South Korea", "District", 'Reds', False, False, False, True)
    corona_map.displayCoMap("South Korea", "City", 'Reds', False, False, False, True)
    corona_map.displayCoMap("South Korea", "City", 'Reds', False, False, True, False)
    corona_map.displayCoMap("South Korea", "City", 'Reds', False, True, False, False)
    corona_map.displayCoMap("South Korea", "City", 'Reds', True, False, False, False)
