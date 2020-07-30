"""
Program Title: Metrics to compute GSR and ISR
created: June 29, 2020 8:54PM
Author: DoYeong
"""


class GSRMetric:
    group_type = None
    #########################################
    # # data about number of people
    # confirmed_count = None  # from Group Class
    # contacted_count = None  # from Group Class
    # decease_count = None  # from Group Class
    # recovered_count = None  # from Group Class
    #
    # # data about test
    # covid19_test_cc_count = None  # from Group Class
    # positivity_count = None  # from Group Class
    #
    # # data about isolation people
    # isolated_confirmed_count = None  # from Group Class
    # isolated_contacted_count = None  # from Group Class
    #
    # # data about identified people
    # identified_cc_count = None  # from Group Class
    # hospital_capability = None  # from Group Class, only city or province
    #########################################

    def compute_gsr_factor1(self):
        # 1. Number of COVID-19 Tests Performed --> X
        pass

    def compute_covid19_test_rate(self, confirmed_count, contacted_count, recovered_count, covid19_test_cc_count):
        # 2. COVID-19 Test Rate --> Proportion
        # (COVID-19 Test Rate) = (Number of C&C People not tested - Number of recovered People from COVID-19)
        #                           / (Number of C&C People)
        f2 = (confirmed_count + contacted_count - recovered_count - covid19_test_cc_count) \
             / (contacted_count + confirmed_count)
        return f2

    def compute_positive_rate(self, positivity_count, covid19_test_cc_count):
        # 3. Number of Confirmed Cases, Positivity Tests --> Proportion
        # (Rate of Positivity from COVID-19 Test) = (Number of Positivity) / (Number of COVID-19 Test)
        f3 = positivity_count / covid19_test_cc_count
        return f3

    def compute_gsr_factor4(self):
        # 4. Number of Contacted People --> X
        pass

    def compute_gsr_factor5(self):
        # 5. Number of Deceased People --> X
        pass

    def compute_fatality_rate(self, decease_count, confirmed_count):
        # 6. Fatality Rate
        # (Fatality Rate) = (Number of Deceased People) / (Number of Confirmed Cases)
        f6 = decease_count / confirmed_count
        return f6

    def compute_confirmed_isolation_rate(self, isolated_confirmed_count, confirmed_count):
        # 7. Quarantine/Isolation Rate of Confirmed People --> Inverse Proportion
        # (Quarantine/Isolation Rate of Confirmed People) =
        #                 1 - (Number of Confirmed People in Quarantine/Isolation state) / (Number of Confirmed People)
        f7 = 1 - (isolated_confirmed_count / confirmed_count)
        return f7

    def compute_contacted_isolation_rate(self, isolated_contacted_count, contacted_count):
        # 8. Quarantine/Isolation Rate of Contacted People --> Inverse Proportion
        # (Quarantine/Isolation Rate of Contacted People) =
        #                 1 - (Number of Contacted People in Quarantine/Isolation state) / (Number of Contacted People)
        f8 = 1 - (isolated_contacted_count / contacted_count)
        return f8

    def compute_indetified_rate(self, identified_cc_count, contacted_count, confirmed_count):
        # 9. Traceability Rate of Infection Paths --> Inverse Proportion
        # (Traceability Rate of Infection Paths) =
        #                               1 - (Number of C&C People whose routes are identified) / (Number of C&C People)
        f9 = 1 - (identified_cc_count / (contacted_count + confirmed_count))
        return f9

    def compute_hospital_capability(self, confirmed_count, contacted_count, hospital_capability):
        # 10. Hospital Capability for Treating COVID-19 Patients --> Proportion
        # (Hospital Capability for Treating COVID-19 Patients) =
        #                                              max(1, (Number of C&C People) / (Number of Capability Hospital))
        f10 = max(1, (confirmed_count + contacted_count) / hospital_capability)
        return f10

    def compute_recovery_rate(self, recovered_count, confirmed_count, contacted_count):
        # 11. Recovery Rate of COVID-19 Patients --> Inverse Proportion
        # (Recovery Rate of COVID-19 Patients) = (Number of recovered People from COVID-19) / (Number of C&C People)
        f11 = recovered_count / (confirmed_count + contacted_count)
        return f11

    def compute_isr_effect(self, related_isr_list):
        # This factor is not in SRS.
        # The focus is the high level ISR people.
        return max(related_isr_list)

    def compute_gsr(self, weight_dic, factor_dic):
        if weight_dic.keys() != factor_dic.keys():
            try:
                raise ValueError("The targets of Weight Dictionary and Types of GSR Factor is different!")
            except ValueError:
                return None

        return sum(list([(a[k] * b[k]) for k in set(b) & set(a)]))

class ISRMetric:
    # large_group_gsr = None
    # age = None
    # disease_score = None
    # gsr_visited_list = None
    # gsr_commute_list = None

    def compute_large_group_gsr(self, large_group_gsr):
        # 1. GSR Value of the City/Region where the individual lives --> Proportion
        f1 = large_group_gsr
        # or f1 = large_group_gsr / (Number of GSR Factor)

        return f1

    def compute_age_score(self, age):
        # 2. Age of the Individual --> Proportion
        # Basis of Calculation: p.4 of COSE SRS
        # Age   | Factor Value
        #  0~17 | ?
        # 18~29 | ~0.066~
        # 30~39 | ~0.136~
        # 40~49 | ~0.274~
        # 50~59 | ~0.451~
        # 60~69 | ~0.612~
        # 70~79 | ~0.751~
        # 80+   | ~0.79~

        if age < 18:
            return 0.033
        elif age < 29:
            return 0.066
        elif age < 39:
            return 0.136
        elif age < 49:
            return 0.274
        elif age < 59:
            return 0.451
        elif age < 69:
            return 0.612
        elif age < 79:
            return 0.751
        else:
            return 0.79

    def compute_disease_score(self, disease_score):
        # 3. Underlying Diseases such as Heart Disease, Lung Disease, and Diabetes --> Proportion
        f3 = disease_score
        return f3

    def compute_gsr_visitied(self, gsr_visited_list):
        # 4. History of Places visited --> Proportion
        # The most highest GSR values is critical to person
        f4 = max(gsr_visited_list)
        return f4

    def compute_gsr_on_commute(self, gsr_commute_list):
        # 5. Commute Routes --> Proportion
        # GSR Values of Small Groups
        # (Average of GSR during commute) = (Sum of GSR values on commute) / (Number of GSR values)
        f5 = sum(gsr_commute_list) / len(gsr_commute_list)
        # or f5 = (sum(gsr_commute_list) / (Number of GSR Factor)) / len(gsr_commute_list)
        return f5

    def compute_isr(self, weight_dic, factor_dic):
        if weight_dic.keys() != factor_dic.keys():
            try:
                raise ValueError("The targets of Weight Dictionary and Types of ISR Factor is different!")
            except ValueError:
                return None

        return sum([(a[k] * b[k]) for k in set(b) & set(a)])
