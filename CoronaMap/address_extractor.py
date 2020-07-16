"""
Date: 2020. 07. 02.
Programmer: MH
Description: Code for extracting Korea address from *.shp data
"""

import geopandas as gpd
import pandas as pd
#
# data = gpd.read_file(r".\gadm36_KOR_shp\gadm36_KOR_2.shp")
# data = gpd.read_file(r".\EMD_202005\EMD.shp")
# print(data.info())
# print(data.loc[:,["EMD_CD", "EMD_ENG_NM"]])


f = open(r"./address.txt")
is_header = True
data ={"EMD_CD":[], "address":[]}
while True:
    line = f.readline()
    if not line: break
    if is_header:
        is_header = False
        continue
    result = line.split("	")
    # print(result[1]=="서울특별시")
    if result[2] != "존재\n":
        continue
    if len(result[1].split(" ")) == 1:
        print(result[1])
        data["EMD_CD"].append(result[0][0:8])
        data["address"].append(result[1])

f.close()

pd_data = pd.DataFrame.from_dict(data)
pd_data.to_csv("./address_si.csv")