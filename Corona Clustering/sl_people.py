from datetime import datetime, timedelta
from dateutil.parser import parse
import random
import pandas as pd
import numpy as np
import sklearn
from sklearn import cluster
from sklearn.metrics import silhouette_score
from sklearn import preprocessing
import matplotlib.pyplot as plt
from matplotlib import cm


class SlClusteringPeople:
    df_corona = None  # initial loaded data
    added_column_list = []  # Columns added by calculation within class
    cluster_result_dic = {}

    weight_list = [1, 1]  # only comparison

    sse_list = []  # list for displaying SSE of each cluster
    sil_score_list = []  # list for Silhouette score of clustering result
    centroids_coord_list = []  # list for storing coordinates of centroids

    def __init__(self, file_path):
        self.load_data(file_path)
        self.compute_severity()

    def compute_severity(self):
        """
        method to preprocess the data for distance function
        :return: None
        """
        col_num = len(self.df_corona)  # the number of rows from loaded data
        today = datetime.now().date()  # date of today, YEAR-MONTH-DAY

        # selecting specific column to compute 'severity'
        incur_date_col = self.df_corona['Incurred Date']
        status = self.df_corona['Covid Status']

        severity_list = []  # list for storing severity result

        for i in range(col_num):
            severity = 0  # default is healthy, 0.
            if status[i] == 'Contacted':  # contacted person?
                # formula for contacted person:
                #   x = 1 - ((today's date) - (infected date)) * 0.05)
                elapsed_days = (today - parse(incur_date_col[i]).date()).days
                severity = (1 - (elapsed_days * 0.05)) * 0.5

            elif status[i] == 'Confirmed':  # confirmed person?
                # formula for confirmed person:
                #   x = (1 - ((today's date) - (infected date)) * 0.05)) / 2
                elapsed_days = (today - parse(incur_date_col[i]).date()).days
                severity = 1 - (elapsed_days * 0.05)

            severity_list.append(severity)  # add the value to the list
        self.df_corona["Severity"] = severity_list
        self.added_column_list.append("Severity")
        self.added_column_list.append("Age")

    def display_clustering_result(self,
                                  num_cluster,
                                  cluster_idx_list,
                                  cluster_predicted_list):
        """
        function to display clustering result on console as tabular type
        :param num_cluster: int, the number of cluster
        :param cluster_idx_list: list, cluster index list, ie. [2, 3, 4, 5, 6]
        :param cluster_predicted_list: list, result of clustering
        :return: None
        """

        severity_list = self.df_corona["Severity"].values.tolist()
        age_list = self.df_corona["Age"].values.tolist()

        if type(cluster_predicted_list) != list:
            cluster_predicted_list = cluster_predicted_list.tolist()
        people_num_of_a_cluster_list = []
        avg_age_of_a_cluster_list = []
        avg_severity_of_a_cluster_list = []

        print(f"Number of Clusters: {len(cluster_idx_list)}")

        for cluster_idx in cluster_idx_list:  # 1 cluster
            num_people = cluster_predicted_list.count(cluster_idx)
            id_target_data_tuple_list = []
            target_severity_list = []
            target_age_list = []

            for person_idx in range(len(cluster_predicted_list)):
                if cluster_idx == cluster_predicted_list[person_idx]:
                    target_severity_list.append(severity_list[person_idx])
                    target_age_list.append(age_list[person_idx])
                    id_target_data_tuple_list.append((
                        person_idx + 1,  # [0] of tuple is id
                        age_list[person_idx],  # [1] of tuple is age
                        round(severity_list[person_idx], 2)))  # [2] of tuple is severity

            people_num_of_a_cluster_list.append(num_people)

            print(f"\tCluster {cluster_idx}:")
            print(f"\t\tNumber of People: {num_people}")
            # print(f"\t\t\t{'ID':<4}{'Age':<4}{'Severity Value'}")
            # for person_in_cluster in id_target_data_tuple_list:
            #     print(f"\t\t\t{person_in_cluster[0]:<4}"
            #           f"{person_in_cluster[1]:<4}"
            #           f"{person_in_cluster[2]}")
            print(f"\t\tMinimum of Age values: {min(target_age_list)}")
            print(f"\t\tMaximum of Age values: {max(target_age_list)}")
            print(f"\t\tAverage of Age values: "
                  f"{round(sum(target_age_list) / len(id_target_data_tuple_list), 2)}")
            print(f"\t\tMinimum of Severity values: {min(target_severity_list)}")
            print(f"\t\tMaximum of Severity values: {max(target_severity_list)}")
            print(f"\t\tAverage of Severity values: "
                  f"{round(sum(target_severity_list) / len(id_target_data_tuple_list), 2)}")
            print(f"\t\tThe Coordinates of Centroid:")
            coords = self.centroids_coord_list[num_cluster - 2][cluster_idx]
            print(f"\t\t\tX1 (Severity): {round(coords[0], 2)}")
            print(f"\t\t\tX2 (Age): {round(coords[1], 2)}")
            try:
                avg_age_of_a_cluster_list.append(
                    round(sum(target_age_list) / len(id_target_data_tuple_list), 2))
            except ZeroDivisionError:
                avg_age_of_a_cluster_list.append(0)

            try:
                avg_severity_of_a_cluster_list.append(
                    round(sum(target_severity_list) / len(id_target_data_tuple_list), 2))
            except ZeroDivisionError:
                avg_severity_of_a_cluster_list.append(0)

            print()  # float 1 line
        self.display_summary_table(people_num_of_a_cluster_list,
                                   avg_age_of_a_cluster_list,
                                   avg_severity_of_a_cluster_list)
        print()  # float 1 line

    def display_load_data(self):
        """
        function to display data
        :return: None
        """
        print(f"Total number of People: {len(self.df_corona)}")
        print(f"{'ID':<4}"
              f"{'Age':<4}"
              f"{'Covid Status':<13}"
              f"{'Severity':<9}"
              f"{'Address':<10}")
        for i in range(len(self.df_corona)):
            print(f"{self.df_corona['ID'][i]:<4}"
                  f"{self.df_corona['Age'][i]:<4}"
                  f"{self.df_corona['Covid Status'][i]:<13}"
                  f"{round(self.df_corona['Severity'][i], 3):<9}"
                  f"{self.df_corona['Address'][i].split()[0]:<10}"
                  )
        print()  # float 1 line
        grouped_status = self.df_corona['Severity'].groupby(self.df_corona['Covid Status'])

        print(f"Number of healthy people: {grouped_status.count()['Healthy']}")
        print(f"Number of contacted people: {grouped_status.count()['Contacted']}")
        print(f"Number of confirmed people: {grouped_status.count()['Confirmed']}")

        print(f"Average Severity of contacted people: "
              f"{round(grouped_status.mean()['Contacted'], 2)}")
        print(f"Average Severity of confirmed people: "
              f"{round(grouped_status.mean()['Confirmed'], 2)}")
        print()  # float 1 line

    def display_summary_table(self,
                              people_of_cluster_list,
                              avg_age_of_cluster_list,
                              avg_severity_of_cluster_list):
        len_id = 17
        len_p_num = 11
        len_age = 13
        len_sev = 15
        len_sum = len_id + len_p_num + len_age + len_sev

        # top row
        print(f"\t{'-' * (len_sum + 11)}")
        print(f"\t{'Cluster ID':>{len_id}} "
              f"| {'# of People':>{len_p_num}} "
              f"| {'Avg. of Ages':>{len_age}} "
              f"| {'Avg. of Severity':>{len_sev}} ")

        # contents of table
        cluster_id = 0
        for people_num, avg_age, avg_sev in zip(people_of_cluster_list,
                                                avg_age_of_cluster_list,
                                                avg_severity_of_cluster_list):
            print(f"\t{cluster_id:>{len_id}} "
                  f"| {people_num:>{len_p_num}} "
                  f"| {avg_age:>{len_age}} "
                  f"|{avg_sev:>{len_sev}}")
            cluster_id += 1

        print(f"\t{'-' * (len_id + 1)}"
              f"|{'-' * (len_p_num + 2)}"
              f"|{'-' * (len_age + 2)}"
              f"|{'-' * (len_sev + 2)}-")

        # bottom row
        print(f"\t{'Total':^{len_id}} | {sum(people_of_cluster_list):>{len_p_num}} |")
        print(f"\t{'SSE':^{len_id}} | {round(self.sse_list[len(people_of_cluster_list) - 2], 2):>{len_p_num}} |")
        print(f"\t{'Silhouette Score':>{len_id}} "
              f"| {round(self.sil_score_list[len(people_of_cluster_list) - 2], 2):>{len_p_num}} |")
        print(f"\t{'-' * (len_sum + 11)}")

    def draw_elbow_method(self, sse_list):
        """
        method to draw elbow graph using SSE(Sum of Squares Error)
        :param sse_list: list of SSE
        :return: None
        """
        plt.plot(range(2, 10), sse_list, marker='o')
        plt.xlabel("The Number of Cluster")
        plt.ylabel("SSE")
        plt.show()

    def draw_silhouette(self):
        """
        method to draw graph using silhouette scores
        :return: None
        """
        pass

    def draw_graph(self):
        """
        method to draw clustering result
        :return: None
        """
        pass

    def load_data(self, file_path):
        """
        method to load .csv file
        :param file_path: string, the path of file
        :return:
        """
        self.df_corona = pd.read_csv(file_path)

    def plot_data(self, num_cluster):
        """
        To plot result
        :return:
        """
        groups = self.df_corona.groupby("Cluster ID")
        fig, ax = plt.subplots()
        for name, group in groups:
            ax.plot(group.Severity, group.Age, marker='o', linestyle="", label=name)
        ax.legend(fontsize=12)
        plt.title("Result of Clustering (K="+str(num_cluster)+", Weight="+str(self.weight_list)+")")
        plt.xlabel("Severity")
        plt.ylabel("Age")
        # plt.show()
        fig.savefig("./Cluster_Result_Plotting_sl/cluster_result_"+str(num_cluster)+"_"+str(self.weight_list)+".png", dpi=300)
        plt.close()

    def sl_cluster_kmeans(self, target_col_name_list, num_cluster):
        # load the k-means model
        km = cluster.KMeans(
            n_clusters=num_cluster,  # the number of cluster
            init='k-means++',  # how to initial cluster centers
            max_iter=300,  # maximum number of iterations
            algorithm='auto'  # three choices: auto, full, and elkan.
        )

        # cluster
        if len(target_col_name_list) == 1:
            target_data = self.df_corona[target_col_name_list].values.tolist()
            target_data = np.array(target_data)
            cluster_predicted_list = km.fit_predict(
                target_data.reshape(-1, 1))  # changing the shape of data
            self.sil_score_list.append(
                silhouette_score(target_data.reshape(-1, 1),
                                 cluster_predicted_list))

        else:  # at least 2 columns
            target_data = self.df_corona.loc[:, target_col_name_list]  # To select required data
            if "Age" in target_col_name_list:  # scaling only "Age" column
                age = target_data.loc[:, "Age"].values.reshape(-1, 1)
                scaler = preprocessing.MinMaxScaler()
                # data = scaler.fit_transform(data)   # To scale data from 0 to 1
                target_data.loc[:, "Age"] = scaler.fit_transform(age)

            min_max_scaler = preprocessing.MinMaxScaler()
            target_data = min_max_scaler.fit_transform(target_data)

            cluster_predicted_list = km.fit_predict(target_data)
            self.sil_score_list.append(
                silhouette_score(target_data,
                                 cluster_predicted_list))

        # add the column
        self.df_corona['Cluster ID'] = cluster_predicted_list

        # storing the coordinates of centroids
        self.centroids_coord_list.append(km.cluster_centers_)

        # storing the prediction result
        self.cluster_result_dic[num_cluster] = cluster_predicted_list

        # storing SSE(Sum of Squared Errors)
        self.sse_list.append(km.inertia_)

        return cluster_predicted_list

    def save_as_csv(self, num_cluster):
        """
        function to save data as .csv file
        :param num_cluster: int, the number of cluster.
        :return: None
        """
        temp_df = self.df_corona.__deepcopy__()

        file_name = f"clustered_corona_data_k={num_cluster}_" \
                    f"{'Severity_Age'}_{''.join(str(self.weight_list))}.csv"
        temp_df.to_csv(file_name, index=False, encoding='utf-8-sig')


if __name__ == '__main__':
    # CODE FOR CLUSTERING
    file_path = './corona_data.csv'

    cp = SlClusteringPeople(file_path)
    cp.display_load_data()

    sse_list = []  # list for storing SSE(Sum of squares errors)

    # cluster with 'Severity' and 'Age' columns
    col_name_list = ['Severity', 'Age']
    k_list = [k for k in range(2, 10)]  # cluster list


    for num_cluster in k_list:
        print(num_cluster)
        cluster_id_list = [id for id in range(num_cluster)]
        predicted_list = cp.sl_cluster_kmeans(col_name_list, num_cluster)
        print(predicted_list)
        cp.display_clustering_result(num_cluster,
                                     cluster_id_list,
                                     predicted_list)
        if num_cluster == 5:
            cp.save_as_csv(num_cluster)
        # cp.plot_data(num_cluster)
