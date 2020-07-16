"""
Date: 2020. 07. 03.
Programmer: MH
Description: code for drawing Corona map using clustered data
"""
import copy
import numpy as np
import time

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import PathPatch
from matplotlib.textpath import TextPath
from enum import Enum

# Code for displaying Korean text
plt.rcParams["font.family"] = 'Malgun Gothic'
plt.rcParams["font.size"] = 20


class RegionUnit(Enum):
    SI = 1
    GUN_GU = 2
    EMD = 3


class CoronaMap:
    def __init__(self):
        self.loc_shp_file = {RegionUnit.SI: r"./CTPRVN_202005/CTPRVN.shp", RegionUnit.GUN_GU: r"./SIG_202005/SIG.shp",
                             RegionUnit.EMD: r"./EMD_202005/EMD.shp"}
        self.scale = 1.3    # Zoom scale
        self.colors = ["red", "sandybrown", "gold", "olivedrab", "darkgreen", "royalblue", "plum",
                       "lightcoral", "coral", "darkorange", "orange", "lightskyblue", "cornsilk"]
        self.selected_colors = []
        self.circle_legend_elements = []
        self.size_legend_elements = []
        self.features = []
        self.region_unit =RegionUnit.EMD
        self.code_key = "EMD_CD"
        self.radius = 0.05
        self.text_size =0.03

        self.dic_region_geo_data ={RegionUnit.SI: None, RegionUnit.GUN_GU:None, RegionUnit.EMD:None}

        self.press = None
        self.cur_xlim = None
        self.cur_ylim = None
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.xpress = None
        self.ypress = None

    def set_region_unit(self, region_unit=RegionUnit.EMD):
        self.region_unit = region_unit
        if self.region_unit == RegionUnit.SI:
            self.code_key = "CTPRVN_CD"
            self.radius = 0.12
            self.text_size = 0.1
            self.y_weight = 0.1
        elif self.region_unit == RegionUnit.GUN_GU:
            self.code_key = "SIG_CD"
            self.radius = 0.05
            self.text_size =0.03
            self.y_weight = 0.05
        else:
            self.code_key = "EMD_CD"
            self.radius = 0.02
            self.text_size =0.03
            self.y_weight = 0.03

    def prepare(self):
        self.set_region_unit(RegionUnit.SI)
        self.load_map_data()
        self.load_data("./clustering_result_csv/clustered_corona_data_k=" + str(self.num_clusters) + "_" + "_".join(
            self.features) + "_[0.4, 0.6]" + ".csv")
        self.prepare_data()

    def load_data(self, loc):
        """
        To load clustered data from csv file
        :param loc: str, file location
        :return: None
        """
        self.data = pd.read_csv(loc)    # To load csv file to dataframe
        self.data = copy.deepcopy(self.divide_address(self.data))

        if self.region_unit == RegionUnit.EMD:      # Region Unit is 읍면동
            address_data = pd.read_csv("./address_emd.csv")     # To load csv file having 법정동 Code
        elif self.region_unit == RegionUnit.GUN_GU: # Region Unit is 시, 군, 구
            address = []
            for index, row in self.data.iterrows():
                address.append(row['Address1']+" "+row["Address2"])
            self.data['Address'] = address
            address_data = pd.read_csv("./address_gg.csv")     # To load csv file having 법정동 Code

        else:       # Region Unit is 특별시, 도
            address = []
            for index, row in self.data.iterrows():
                address.append(row['Address1'])
            self.data['Address'] = address
            address_data = pd.read_csv("./address_si.csv")     # To load csv file having 법정동 Code

        self.data = self.data.merge(address_data, on="Address", how="inner")
        self.add_centroid()
        self.data = self.data.astype({self.code_key: object})

        self.size_legend_elements.append(Line2D([0], [0], marker='o', color="white", label="< 10",
                                                  markerfacecolor="gray", markersize=18))
        self.size_legend_elements.append(Line2D([0], [0], marker='o', color="white", label="< 30",
                                                markerfacecolor="gray", markersize=25))
        self.size_legend_elements.append(Line2D([0], [0], marker='o', color="white", label="< 60",
                                                markerfacecolor="gray", markersize=30))
        self.size_legend_elements.append(Line2D([0], [0], marker='o', color="white", label="< 100",
                                                markerfacecolor="gray", markersize=35))

    def divide_address(self, data):
        """
        To divide address
        :param data: dataframe, address data
        :return:
        """
        address = data.loc[:, "Address"]
        address_detail = {"Address1": [], "Address2": [], "Address3": []}
        for i, value in address.items():
            a = value.split(" ")
            address_detail["Address1"].append(a[0])
            address_detail["Address2"].append(a[1])
            address_detail["Address3"].append(a[2])
        data["Address1"] = address_detail["Address1"]
        data["Address2"] = address_detail["Address2"]
        data["Address3"] = address_detail["Address3"]
        data = data.iloc[:, 1:]
        return data

    def set_features(self, features):
        self.features = features

    def load_map_data(self):
        """
        To load map data from *.shp file and change coordinate format
        :return:
        """
        self.region_geo_data = gpd.read_file(self.loc_shp_file[self.region_unit], encoding='euckr')     # To load shp file to geopandas format
        self.region_geo_data.crs = {'init': "epsg:5178"}    # To initialize coordinate system (UTMK)
        self.region_geo_data = self.region_geo_data.to_crs({'init': "epsg:4326"})   # To change coordinate format to Wgs84
        self.dic_region_geo_data[self.region_unit] = copy.deepcopy(self.region_geo_data)

    def set_num_clusters(self, clusters):
        """
        To set number of cluster
        :param clusters: int, the number of clusters
        :return:
        """
        self.num_clusters = clusters
        self.selected_colors = ["red", "darkgreen", "gold", "olivedrab", "lightskyblue"]
        for i in range(self.num_clusters):
            # selected_color = random.choice(self.colors)
            # self.colors.remove(selected_color)
            # self.selected_colors.append(selected_color)
            selected_color = self.selected_colors[i]
            self.circle_legend_elements.append(Line2D([0], [0], marker='o', color="white", label=str(i+1),
                                                      markerfacecolor=selected_color, markersize=15))
        # self.selected_colors = random.choices(self.colors, k=self.num_clusters)

    def prepare_data(self):
        self.region_geo_data = self.dic_region_geo_data[self.region_unit].merge(self.data, on=self.code_key, how="outer")

    def add_centroid(self):
        """
        To compute centroids of input polygon
        :return:
        """
        data = {self.code_key: [], "centroid": [], }
        for i, row in self.dic_region_geo_data[self.region_unit].iterrows():
            polygon = row['geometry']
            data[self.code_key].append(row[self.code_key])
            data["centroid"].append(polygon.centroid)
        df_centroid = pd.DataFrame.from_dict(data)

        centroids = []
        for i, row in self.data.iterrows():
            result = df_centroid[df_centroid[self.code_key] == str(row[self.code_key])]
            centroid = result['centroid']
            centroids.append(centroid)
        self.data['centroid'] = centroids

    def make_autopct(self, values):
        def make_custom_autopct(pct):
            total = sum(values)
            val = int(round(pct*total/100.0))
            return '{p:2.1f}% ({v:d})'.format(p=pct, v=val)
        return make_custom_autopct

    def _plot(self, numberFlag=None, percentageFlag=None, convertionFlag=None):
        groups = self.region_geo_data.groupby("Address")
        for name, group in groups:
            try:
                centroid = group.loc[:, 'centroid'].values[0].values[0]
            except:
                continue
            s = group.loc[:, "Cluster ID"].value_counts()
            labels = list(s.index.astype(int))
            sizes = s.values
            # print(labels, sizes)
            colors = [self.selected_colors[i] for i in labels]
            x, y = centroid.x, centroid.y
            if "경기도" == name:
                y -= 0.1
                x += 0.1
            if "인천광역시" == name:
                y += 0.1

            num_people = sum(sizes.tolist())
            radius = self.radius
            if num_people < 10:
                radius = self.radius * 0.7
            elif num_people < 30:
                radius = self.radius * 1.0
            elif num_people < 60:
                radius = self.radius * 1.3
            elif num_people < 100:
                radius = self.radius * 1.6

            pie = self.ax.pie(sizes, colors=colors, labels=None, startangle=90, radius=radius, center=(x, y),
                              autopct=self.make_autopct(sizes.tolist()), wedgeprops={"clip_on": True},
                              textprops={"fontsize": 13, "clip_on": True})
            # pie[0][len(sizes)-1].set_alpha(0.7)
            # except Exception as e:
            #     print(">> ", group.loc[:, "Address"], group.loc[:, "EMD_CD"], e)
            #     pass
            text = group.loc[:, "Address"].values[0]

            if numberFlag:
                text += " (" + str(num_people) + ")"

            if percentageFlag:
                avg_severity = np.mean(group.loc[:, "Severity"].values)
                text += " (" + str(int(avg_severity * 100)) + "%)"
            tp = TextPath((x, y+self.y_weight), text, size=self.text_size)  # To add Text
            plt.gca().add_patch(PathPatch(tp, color="black"))

        if convertionFlag:
            legend1 = plt.legend(handles=self.circle_legend_elements, loc='lower right')
            # legend2 = plt.legend(handles=self.size_legend_elements, loc='upper right')
            plt.gca().add_artist(legend1)
            # plt.gca().add_artist(legend2)
        self.region_geo_data.loc[:, self.code_key] = self.region_geo_data.loc[:, self.code_key].astype(int)
        self.region_geo_data.plot(ax=self.ax, column=self.code_key, cmap="summer", categorical=True)

    def plot_corona_map(self, numberFlag=None, percentageFlag=None, convertionFlag=None):
        """
        To display corona map
        :param region: string, the target place
        :param regionUnit: string, the unit of the sub-region; city, district
        :param numberFlag: boolean, whether a number associated with each infected area should be displayed.
        :param percentageFlag: boolean, whether a percentage (%) associated with each infected area should be displayed.
        :param convertionFlag: boolean, whether a notational/color convention should be displayed on a corner of the map.
        :return: None
        """
        self.fig, self.ax = plt.subplots(1, 1, figsize=(24, 40), frameon=False)
        self.set_region_unit(RegionUnit.SI)

        self._plot(numberFlag, percentageFlag, convertionFlag)

        self.zoom_factory(self.ax, base_scale=self.scale, numberFlag=numberFlag, percentageFlag=percentageFlag,
                          convertionFlag=convertionFlag)
        self.pan_factory(self.ax)
        axes = plt.gca()
        axes.set_xlim([124, 132])
        axes.set_ylim([34, 43])
        plt.rcParams['figure.figsize'] = (120, 80)
        # self.fig.tight_layout()
        self.ax.autoscale(enable=True)

        plt.show()
        self.fig.savefig("./map_result/coronamap_k="+str(num_clusters)+"_"+"_".join(self.features)+str(time.time())+".png")

    def zoom_factory(self, ax, base_scale=2., numberFlag=None, percentageFlag=None, convertionFlag=None):
        self.zoom_count = 0
        def zoom(event):
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()

            xdata = event.xdata # get event x location
            ydata = event.ydata # get event y location

            if event.button == 'up':
                # deal with zoom in
                scale_factor = 1 / base_scale
                self.zoom_count += 1
            elif event.button == 'down':
                # deal with zoom out
                scale_factor = base_scale
                self.zoom_count -=1
            else:
                # deal with something that should never happen
                scale_factor = 1

            new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
            new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

            relx = (cur_xlim[1] - xdata)/(cur_xlim[1] - cur_xlim[0])
            rely = (cur_ylim[1] - ydata)/(cur_ylim[1] - cur_ylim[0])

            ax.set_xlim([xdata - new_width * (1-relx), xdata + new_width * (relx)])
            ax.set_ylim([ydata - new_height * (1-rely), ydata + new_height * (rely)])
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()
            if event.button == "up" and self.zoom_count == 5:
                print("Si->Gun Gu")
                self.set_region_unit(RegionUnit.GUN_GU)
                self.load_map_data()
                self.load_data(
                    "./clustering_result_csv/clustered_corona_data_k=" + str(self.num_clusters) + "_" + "_".join(
                        self.features) + "_[0.4, 0.6]" + ".csv")
                self.prepare_data()
                ax.clear()
                self._plot(numberFlag, percentageFlag, convertionFlag)
                # ax.text(125, 40, "Si->Gun Gu", color="blue",  fontsize=10)
            if event.button == "down" and self.zoom_count == 4:
                print("Gun Gu->Si")
                self.set_region_unit(RegionUnit.SI)
                self.load_map_data()
                self.load_data(
                    "./clustering_result_csv/clustered_corona_data_k=" + str(self.num_clusters) + "_" + "_".join(
                        self.features) + "_[0.4, 0.6]" + ".csv")
                self.prepare_data()
                ax.clear()
                self._plot(numberFlag, percentageFlag, convertionFlag)
            if event.button == "up" and self.zoom_count == 9:
                print("Gun Gu -> EMD")
                self.set_region_unit(RegionUnit.EMD)
                self.load_map_data()
                self.load_data(
                    "./clustering_result_csv/clustered_corona_data_k=" + str(self.num_clusters) + "_" + "_".join(
                        self.features) + "_[0.4, 0.6]" + ".csv")
                self.prepare_data()
                ax.clear()
                self._plot(numberFlag, percentageFlag, convertionFlag)
            elif event.button == "down" and self.zoom_count == 8:
                print("EMD -> Gun Gu")
                self.set_region_unit(RegionUnit.GUN_GU)
                self.load_map_data()
                self.load_data(
                    "./clustering_result_csv/clustered_corona_data_k=" + str(self.num_clusters) + "_" + "_".join(
                        self.features) + "_[0.4, 0.6]" + ".csv")
                self.prepare_data()
                ax.clear()
                self._plot(numberFlag, percentageFlag, convertionFlag)
            ax.set_xlim(cur_xlim)
            ax.set_ylim(cur_ylim)
            ax.figure.canvas.draw()

        fig = ax.get_figure()    # get the figure of interest
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
    pd.set_option('display.max_rows', 100)
    pd.set_option('display.max_columns', 100)
    # num_clusters = int(input("Enter the number of clusters: "))
    num_clusters = 5
    # features = input("Enter the features applied at clustering (ex' Severity, Age): ")
    features = "Severity, Age"
    features = features.split(", ")

    corona_map = CoronaMap()
    corona_map.set_region_unit(RegionUnit.SI)
    corona_map.set_num_clusters(num_clusters)
    corona_map.set_features(features)
    corona_map.prepare()
    # corona_map.load_map_data()
    # corona_map.load_data("./clustering_result_csv/clustered_corona_data_k="+str(num_clusters)+"_"+"_".join(features)+"_[0.4, 0.6]"+".csv")
    # corona_map.prepare_data()
    corona_map.plot_corona_map(percentageFlag=True, numberFlag=True, convertionFlag=True)
    print("======"*10)
    #
    # corona_map = CoronaMap()
    # corona_map.set_region_unit(RegionUnit.GUN_GU)
    # corona_map.load_map_data()
    # corona_map.set_features(features)
    # corona_map.load_data("./clustering_result_csv/clustered_corona_data_k="+str(num_clusters)+"_"+"_".join(features)+"_[0.4, 0.6]"+".csv")
    # corona_map.prepare_data()
    # corona_map.set_num_clusters(num_clusters)
    # corona_map.plot_corona_map(percentageFlag=True, numberFlag=True, convertionFlag=True)
    # print("======"*10)
    #
    # corona_map = CoronaMap()
    # corona_map.set_region_unit(RegionUnit.EMD)
    # corona_map.load_map_data()
    # corona_map.set_features(features)
    # corona_map.load_data("./clustering_result_csv/clustered_corona_data_k="+str(num_clusters)+"_"+"_".join(features)+"_[0.4, 0.6]"+".csv")
    # corona_map.prepare_data()
    # corona_map.set_num_clusters(num_clusters)
    # corona_map.plot_corona_map(percentageFlag=True, numberFlag=True, convertionFlag=True)


