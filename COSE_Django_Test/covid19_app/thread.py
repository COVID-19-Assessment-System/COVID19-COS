import time
import random
import threading
from threading import Timer, Thread
from covid19_app.statistical_method import *

toggle = False


class ReceiveAnnouncement(Thread):
    num_announcement = 0
    announcement = None

    def __init__(self):
        Thread.__init__(self)
        self.name = "Announcement Receiver"

    def run(self):
        global toggle

        while True:
            time.sleep(random.randint(1, 6))  # wait some seconds to received announcement

            # receiving announcement randomly (True or False)
            announcement = bool(random.getrandbits(1))

            if announcement:  # new announcement is received?
                print("COVID19 announcement is received!")

                # checking the announcement valid or not
                toggle = self.validate_announcement(announcement)

    def validate_announcement(self, announcement):
        if bool(random.getrandbits(1)):  # 50% chance to validate
            self.num_announcement += 1
            print("Received announcement is validate!")
            return True
        else:  # 50% chance to invalidate
            print("Received announcement is not validate!")
            return False


class PullAnnouncement(Thread):
    num_announcement = 0
    announcement = None

    def __init__(self, timer):
        Thread.__init__(self)
        self.timer = timer
        self.name = "Announcement Puller"

    def run(self):
        global toggle

        while True:
            time.sleep(self.timer)  # wait some seconds to received announcement

            # receiving announcement randomly (True or False)
            announcement = bool(random.getrandbits(1))

            if announcement:  # new announcement is received?
                print("COVID19 announcement is pulled!")

                # checking the announcement valid or not
                toggle = self.validate_announcement(announcement)


    def validate_announcement(self, announcement):
        if bool(random.getrandbits(1)):  # 50% chance to validate
            self.num_announcement += 1
            print("Pulled announcement is validate!")
            return True
        else:  # 50% chance to invalidate
            print("Pulled announcement is not validate!")
            return False


class HandleSR(Thread):
    isr_weight_dic = {}
    isr_factor_value_dic = {}
    gsr_weight_dic = {}
    gsr_factor_value_dic = {}

    def __init__(self):
        Thread.__init__(self)
        self.name = "SR Handler"

    def run(self):
        global toggle
        while True:
            if toggle:
                self.load_gsr_factor(gsr_weight_dic, gsr_factor_value_dic)
                self.load_isr_factor(isr_weight_dic, isr_factor_value_dic)

                self.create_gsr_thread()
                self.create_isr_thread()
                toggle = False
            else:
                continue

    def create_gsr_thread(self):

        c_gsr = ComputeGSR(self.gsr_weight_dic, self.gsr_factor_value_dic)
        # c_gsr.set_weight(weight_dic)
        # c_gsr.set_factor_value_dic(factor_value_dic)
        c_gsr.start()

    def load_isr_factor(self, weight_dic, factor_value_dic):
        # loading latest data from DB in this method
        self.isr_weight_dic = weight_dic
        self.isr_factor_value_dic = factor_value_dic

    def create_isr_thread(self):
        c_isr = ComputeISR(self.isr_weight_dic, self.isr_factor_value_dic)
        # c_isr.set_weight()
        # c_isr.set_factor_value_dic()
        c_isr.start()

    def load_gsr_factor(self, weight_dic, factor_value_dic):
        # loading latest data from DB in this method
        self.gsr_weight_dic = weight_dic
        self.gsr_factor_value_dic = factor_value_dic


class ComputeISR(Thread):
    factor_value_dic = {}
    weight_dic = {}
    isr_list = []

    def __init__(self, weight_dic, factor_value_dic):
        Thread.__init__(self)
        self.weight_dic = weight_dic
        self.factor_value_dic = factor_value_dic
        self.name = "ISR Computer"
        self.isr_metric = ISRMetric()

    def run(self):
        self.compute_isr()

    def compute_isr(self):
        time.sleep(random.randint(1, 10))  # timer for computing ISR value
        factor_dic = self.isr_metric.preprocess_isr_factor(self.factor_value_dic)
        self.isr_list.append(self.isr_metric.compute_isr(self.weight_dic, factor_dic))

        print("\nISR value is computed!")
        print("ISR List:", self.isr_list)

    # def set_weight(self, weight_dic):
    #     self.weight_dic = weight_dic
    #
    # def set_factor_value_dic(self, factor_value_dic):
    #     # load latest data from DB in this method
    #     self.factor_value_dic = factor_value_dic

    def get_isr_list(self):
        return self.isr_list


class ComputeGSR(Thread):
    factor_value_dic = {}
    weight_dic = {}
    gsr_list = []

    def __init__(self, weight_dic, factor_value_dic):
        Thread.__init__(self)
        self.weight_dic = weight_dic
        self.factor_value_dic = factor_value_dic
        self.name = "GSR Computer"
        self.gsr_metric = GSRMetric()

    def run(self):
        self.compute_gsr()

    def compute_gsr(self):
        time.sleep(random.randint(1, 10))  # timer for computing GSR value
        factor_dic = self.gsr_metric.preprocess_gsr_factor(self.factor_value_dic)
        self.gsr_list.append(self.gsr_metric.compute_gsr(self.weight_dic, factor_dic))
        print("\nGSR value is computed!")
        print("GSR List:", self.gsr_list)

    # def set_weight(self, weight_dic):
    #     self.weight_dic = weight_dic
    #
    # def set_factor_value_dic(self, factor_value_dic):
    #     # load latest data from DB in this method
    #     self.factor_value_dic = factor_value_dic

    def get_gsr_list(self):
        return self.gsr_list


if __name__ == '__main__':
    # data about number of people
    num_of_confirmed = 100
    num_of_contacted = 80
    num_of_deceased = 10
    num_of_recovered = 30

    # data about test
    num_of_cc_tested_covid19 = 180
    positivity_count = 90

    # data about isolation people
    num_of_isolated_confirmed = 90
    num_of_isolated_contacted = 70

    # data about identified people
    num_of_identified_cc = 150
    hospital_capability = 1000

    gsr_factor_value_dic = {
        'COVID19 Test Rate': {
            'num_of_confirmed': num_of_confirmed,
            'num_of_contacted': num_of_contacted,
            'num_of_cc_tested_covid19': num_of_cc_tested_covid19
        },
        'COVID19 Positive Rate': {
            'positivity_count': positivity_count,
            'num_of_cc_tested_covid19': num_of_cc_tested_covid19
        },
        'Fatality Rate': {
            'num_of_deceased': num_of_deceased,
            'num_of_confirmed': num_of_confirmed
        },
        'Confirmed Isolation Rate': {
            'num_of_isolated_confirmed': num_of_isolated_confirmed,
            'num_of_confirmed': num_of_confirmed
        },
        'Contacted Isolation Rate': {
            'num_of_isolated_contacted': num_of_isolated_contacted,
            'num_of_contacted': num_of_contacted
        },
        'Identified Rate': {
            'num_of_identified_cc': num_of_identified_cc,
            'num_of_contacted': num_of_contacted,
            'num_of_confirmed': num_of_confirmed
        },
        'Hospital Capability': {
            'num_of_confirmed': num_of_confirmed,
            'num_of_contacted': num_of_contacted,
            'hospital_capability': hospital_capability
        },
        'Recovery Rate': {
            'num_of_recovered': num_of_recovered,
            'num_of_confirmed': num_of_confirmed
        },
        'ISR Effect': {
            'related_isr_list': [0.1, 0.2]
        }
    }
    gsr_weight_dic = {
        'COVID19 Test Rate': 1 / 9,
        'COVID19 Positive Rate': 1 / 9,
        'Fatality Rate': 1 / 9,
        'Confirmed Isolation Rate': 1 / 9,
        'Contacted Isolation Rate': 1 / 9,
        'Identified Rate': 1 / 9,
        'Hospital Capability': 1 / 9,
        'Recovery Rate': 1 / 9,
        'ISR Effect': 1 / 9
    }

    isr_factor_value_dic = {
        'Large Group GSR': {
            'large_group_gsr': 0.8
        },
        'Age Score': {
            'age': 27
        },
        'Disease Score': {
            'disease_score': 0.8
        },
        'GSR Visited': {
            'gsr_visited_list': [0.2, 0.3, 0.7]
            # or
            # 'max_gsr_visited': 0
        },
        'GSR on Commute': {
            'gsr_commute_list': [0.1, 0.2, 0.3]
            # or
            # 'avg_gsr_on_commute': 0
        }
    }
    isr_weight_dic = {
        'Large Group GSR': 0.2,
        'Age Score': 0.2,
        'Disease Score': 0.2,
        'GSR Visited': 0.2,
        'GSR on Commute': 0.2
    }

    sr_handler = HandleSR()
    sr_handler.start()

    ra = ReceiveAnnouncement()
    ra.start()

    pa = PullAnnouncement(5)
    pa.start()

    while True:
        time.sleep(1)  # wait 1 second
        print("1 Second(main)...")

        print("The Number of Active threads", threading.activeCount())
        for i in threading.enumerate():
            print('-', i.getName())
        print("")

