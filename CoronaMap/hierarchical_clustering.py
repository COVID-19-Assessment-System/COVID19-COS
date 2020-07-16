"""
Date: 2020. 07.06.
Programmer: MH
Description: Code for Hierarchical Clustering
"""
from datetime import datetime
from dateutil.parser import parse
from matplotlib import pyplot as plt

import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import dendrogram
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import pairwise_distances, silhouette_score


class COVID19Cluster:
    def __init__(self, k, metric="euclidean", linkage="average"):
        self.weight = []
        self.features = []
        self.k = k

        # To select distance metric
        if metric in ["euclidean", "l1", "l2", "cosine"]:
            pass
        elif metric == "weight_euclidean":
            metric = self.compute_distance

        self.aggl_clustering = AgglomerativeClustering(n_clusters=k, affinity=metric, linkage=linkage)

    def set_weights(self, weights):
        """
        To set weights for each feature applied when computing distances
        :param weights: list, a list of weights
        :return:
        """
        if len(self.features) == len(weights):  # if size of weight is same to size of features
            self.weight = weights
        else:  # if size of weight is not same to size of features
            # To set weight equally
            self.weight = [1.0/len(self.features) for _ in range(len(self.features))]

    def set_features(self, features):
        """
        To set target features
        :param features: list, a list of feature names
        :return:
        """
        self.features = features

    def load_data(self, file_loc):
        """
        To load data from local file location
        :param file_loc: str, location of csv file
        :return: None
        """
        self.df_corona = pd.read_csv(file_loc)

    def compute_severity(self, criterion_date=datetime.now().date()):
        """
        To compute severity following formula
        if COVID Status: Confirm ==> (1-((Today's Date)-(Infected Date))*0.05)
        if COVID Status: Contracted ==> (1-((Today's Date)-(Infected Date))*0.05)/2
        :param criterion_date: date, date for criterion
        :return:
        """
        list_severity=[]
        for _, row in self.df_corona.iterrows():
            severity = 0    # If the status is "Healthy"
            status = row.loc["Covid Status"]
            elapsed_days = (criterion_date - parse(row.loc["Incurred Date"]).date()).days
            if "Contacted" == status:   # If the status is "contacted"
                severity = round((1 - (elapsed_days * 0.05)) * 0.5, 3)
            elif "Confirmed" == status:   # If the status is "Confirmed"
                severity = round(1 - (elapsed_days * 0.05), 3)
            list_severity.append(severity)
        self.df_corona["Severity"] = list_severity

    def draw_dendrogram(self, data):
        """
        To draw dendrogram using the data
        :return:
        """
        dn = dendrogram(data)
        fig = plt.figure(figsize=(25, 10))
        plt.show()

    def cluster_data(self):
        """
        To make clusters using input data
        :return:
        """
        # To scale values
        data = self.df_corona.loc[:, self.features]  # To select required data
        if "Age" in self.features:
            age = data.loc[:, "Age"].values.reshape(-1, 1)
            scaler = MinMaxScaler()
            # data = scaler.fit_transform(data)   # To scale data from 0 to 1
            data.loc[:, "Age"] = scaler.fit_transform(age)
        result = self.aggl_clustering.fit_predict(data)  # To cluster instances
        return result

    def combine_result(self, clusters):
        """
        To combine data with clusters
        :param clusters: ndarray, the result of clustering
        :return:
        """
        self.df_corona["Cluster ID"] = clusters
        self.df_corona =self.df_corona.iloc[:, 2:]
        self.df_corona.to_csv("./clustering_result_csv/clustered_corona_data_k="+str(self.k)+"_"+
                              "_".join(self.features)+"_"+str(self.weight)+".csv")

    def compute_distance(self, X):
        return pairwise_distances(X, metric=self.compute_distance_euc)

    def compute_distance_euc(self, p1, p2):
        """
        To compute the distance between P1 and P2
        :param p1: array, coordinate of p1
        :param p2: array, coordinate of p2
        :return: float, euclide distance between p1 and p2
        """
        distance = 0.0
        for i in range(len(p1)):
            distance += self.weight[i]*(p1[i]-p2[i])**2
        # distance = (self.weight[0] * (p1[0] - p2[0]) ** 2 + self.weight[1] * (p1[1] - p2[1]) ** 2) ** 0.5
        return distance**0.5

    def plot_data(self):
        """
        To plot result
        :return:
        """
        groups = self.df_corona.groupby("Cluster ID")
        fig, ax = plt.subplots(1, 1, figsize=(10, 10))
        for name, group in groups:
            ax.plot(group.Severity, group.Age, marker='o', linestyle="", label=name)
        ax.legend(fontsize=12)
        plt.title("Result of Clustering (Features: "+", ".join(self.features)+", The Number of Clusters: "+str(self.k)+", Weight="+str(self.weight)+")")
        plt.xlabel("Severity")
        plt.ylabel("Age")
        # plt.show()
        fig.savefig("./clustering_result/cluster_result_"+",".join(self.features)+"_"+str(self.k)+"_"+str(self.weight)+".png", dpi=300)
        plt.close()

    def compute_performance(self, X, labels, metric="euclidean"):
        """
        To compute performance
        :param X: ndarray, features
        :param labels: ndarray, clusters
        :param metric: string, metric for computing distance
        :return: dict, dictionary of computed performance
        """
        silhouette = silhouette_score(X, labels, metric=metric)
        result = {"Silhouette Score": silhouette}
        groups = self.df_corona.groupby("Cluster ID")
        cluster_result = {}
        for name, group in groups:
            cluster_result[name] = {"Number of People": len(group.Severity),
                                    "Average Age 	 ": round(np.mean(group.Age), 2),
                                    "Minimum Age 	 ": min(group.Age), "Maximum Age 	 ": max(group.Age),
                                    "Average Severity": round(np.mean(group.Severity), 2),
                                    "Minimum Severity": min(group.Severity), "Maximum Severity": max(group.Severity)}
            # Number of People, Avg. age , Avg. Sev,
        result["Cluster Result"] = cluster_result

        return result


if __name__ == '__main__':
    j = 2
    i = [0.5, 0.5]
    for features in [["Severity"],["Severity", "Age"]]:
        for j in [2, 3, 4, 5, 6, 7, 8, 9]:
            cluster = COVID19Cluster(j, metric="weight_euclidean")
            for i in [[0.0, 1.0], [0.1, 0.9], [0.2, 0.8], [0.3, 0.7], [0.4, 0.6], [0.5, 0.5],
                      [0.6, 0.4], [0.7, 0.3], [0.8, 0.2], [0.9, 0.1], [1.0, 0.0]]:
                if len(features) == 1 and i[0] != 1.0:
                    continue
                print("Current Conditions >> Features: ", " ".join(features), ", Number of Cluster: ", j, ",  Weight: ", i)
                cluster.load_data("./Corona_data_set/clustered_corona_data_k=5_Severity_Age.csv")
                cluster.set_features(features)
                cluster.set_weights(i)
                result = cluster.cluster_data()
                cluster.combine_result(result)
                cluster.plot_data()
                performance = cluster.compute_performance(X=cluster.df_corona.loc[:, cluster.features], labels=cluster.df_corona.iloc[:, -1])
                print("    Silhouette Score:", round(performance["Silhouette Score"], 2))
                print("    Result of Clusters")
                result_cluster = performance["Cluster Result"]
                for key in result_cluster:
                    print("      Cluster ID:", key)
                    for k in result_cluster[key]:
                        print("        ", k+": ", result_cluster[key][k])

                print("----------"*4)
                print("\n")
            print("==========" * 4)
            print("\n\n\n")
        print("**********" * 4)