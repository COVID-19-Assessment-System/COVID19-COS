"""
Program Title: Metrics to compute GSR and ISR
created: June 29, 2020 8:54PM
Author: DoYeong
"""


class GSRMetric:
    group_type = None
    ###########################################################################
    # # data about number of people
    # num_of_confirmed = None  # from Group Class
    # num_of_contacted = None  # from Group Class
    # num_of_deceased = None  # from Group Class
    # num_of_recovered = None  # from Group Class
    #
    # # data about test
    # num_of_cc_tested_covid19 = None  # from Group Class
    # positivity_count = None  # from Group Class
    #
    # # data about isolation people
    # num_of_isolated_confirmed = None  # from Group Class
    # num_of_isolated_contacted = None  # from Group Class
    #
    # # data about identified people
    # num_of_identified_cc = None  # from Group Class
    # hospital_capability = None  # from Group Class, only city or province
    ###########################################################################

    gsr_factor_value_dic_prototype = {
        'COVID19 Test Rate': {
            'num_of_confirmed': 0,
            'num_of_contacted': 0,
            'num_of_cc_tested_covid19': 0
        },
        'COVID19 Positive Rate': {
            'positivity_count': 0,
            'num_of_cc_tested_covid19': 0
        },
        'Fatality Rate': {
            'num_of_deceased': 0,
            'num_of_confirmed': 0
        },
        'Confirmed Isolation Rate': {
            'num_of_isolated_confirmed': 0,
            'num_of_confirmed': 0
        },
        'Contacted Isolation Rate': {
            'num_of_isolated_contacted': 0,
            'num_of_contacted': 0
        },
        'Identified Rate': {
            'num_of_identified_cc': 0,
            'num_of_contacted': 0,
            'num_of_confirmed': 0
        },
        'Hospital Capability': {
            'num_of_confirmed': 0,
            'num_of_contacted': 0,
            'hospital_capability': 0
        },
        'Recovery Rate': {
            'num_of_recovered': 0,
            'num_of_confirmed': 0
        },
        'ISR Effect': {
            'related_isr_list': []
        }
    }

    def preprocess_gsr_factor(self, factor_value_dic):
        """
        method to call specific methods and to compute factor
        :param factor_value_dic: dictionary, key: method name of this class, value: parameters
        :return: dictionary, key: method name(or factor name) value: factor values
        """
        factor_dic = {}
        for factor_name, value_dic in factor_value_dic.items():
            if factor_name == 'COVID19 Test Rate':
                try:
                    num_of_confirmed = value_dic['num_of_confirmed']
                    num_of_contacted = value_dic['num_of_contacted']
                    num_of_cc_tested_covid19 = value_dic['num_of_cc_tested_covid19']
                except Exception as ex:
                    print("Exception!:", ex)
                    return None

                factor_dic[factor_name] = \
                    self.compute_covid19_test_rate(num_of_confirmed=num_of_confirmed,
                                                   num_of_contacted=num_of_contacted,
                                                   num_of_cc_tested_covid19=num_of_cc_tested_covid19)

            elif factor_name == 'COVID19 Positive Rate':
                try:
                    positivity_count = value_dic['positivity_count']
                    num_of_cc_tested_covid19 = value_dic['num_of_cc_tested_covid19']
                except Exception as ex:
                    print("Exception!:", ex)
                    return None

                factor_dic[factor_name] = \
                    self.compute_positive_rate(positivity_count=positivity_count,
                                               num_of_cc_tested_covid19=num_of_cc_tested_covid19)

            elif factor_name == 'Fatality Rate':
                try:
                    num_of_deceased = value_dic['num_of_deceased']
                    num_of_confirmed = value_dic['num_of_confirmed']
                except Exception as ex:
                    print("Exception!:", ex)
                    return None

                factor_dic[factor_name] = \
                    self.compute_fatality_rate(num_of_deceased=num_of_deceased,
                                               num_of_confirmed=num_of_confirmed)

            elif factor_name == 'Confirmed Isolation Rate':
                try:
                    num_of_isolated_confirmed = value_dic['num_of_isolated_confirmed']
                    num_of_confirmed = value_dic['num_of_confirmed']
                except Exception as ex:
                    print("Exception!:", ex)
                    return None

                factor_dic[factor_name] = \
                    self.compute_confirmed_isolation_rate(num_of_isolated_confirmed=num_of_isolated_confirmed,
                                                          num_of_confirmed=num_of_confirmed)

            elif factor_name == 'Contacted Isolation Rate':
                try:
                    num_of_isolated_contacted = value_dic['num_of_isolated_contacted']
                    num_of_contacted = value_dic['num_of_contacted']
                except Exception as ex:
                    print("Exception!:", ex)
                    return None

                factor_dic[factor_name] = \
                    self.compute_contacted_isolation_rate(num_of_isolated_contacted=num_of_isolated_contacted,
                                                          num_of_contacted=num_of_contacted)

            elif factor_name == 'Identified Rate':
                try:
                    num_of_identified_cc = value_dic['num_of_identified_cc']
                    num_of_contacted = value_dic['num_of_contacted']
                    num_of_confirmed = value_dic['num_of_confirmed']
                except Exception as ex:
                    print("Exception!:", ex)
                    return None

                factor_dic[factor_name] = \
                    self.compute_indetified_rate(num_of_identified_cc=num_of_identified_cc,
                                                 num_of_contacted=num_of_contacted,
                                                 num_of_confirmed=num_of_confirmed)

            elif factor_name == 'Hospital Capability':
                try:
                    num_of_contacted = value_dic['num_of_contacted']
                    num_of_confirmed = value_dic['num_of_confirmed']
                    hospital_capability = value_dic['hospital_capability']
                except Exception as ex:
                    print("Exception!:", ex)
                    return None

                factor_dic[factor_name] = \
                    self.compute_hospital_capability(num_of_contacted=num_of_contacted,
                                                     num_of_confirmed=num_of_confirmed,
                                                     hospital_capability=hospital_capability)

            elif factor_name == 'Recovery Rate':
                try:
                    num_of_recovered = value_dic['num_of_recovered']
                    num_of_confirmed = value_dic['num_of_confirmed']
                except Exception as ex:
                    print("Exception!:", ex)
                    return None

                factor_dic[factor_name] = \
                    self.compute_recovery_rate(num_of_recovered=num_of_recovered,
                                               num_of_confirmed=num_of_confirmed)

            elif factor_name == 'ISR Effect':
                try:
                    related_isr_list = value_dic['related_isr_list']
                except Exception as ex:
                    print("Exception!:", ex)
                    return None

                factor_dic[factor_name] = self.compute_isr_effect(related_isr_list=related_isr_list)

        return factor_dic

    def compute_gsr_factor1(self):
        # 1. Number of COVID-19 Tests Performed --> X
        pass

    def compute_covid19_test_rate(self, num_of_confirmed, num_of_contacted, num_of_cc_tested_covid19):
        # 2. COVID-19 Test Rate --> Proportion
        # (COVID-19 Test Rate) = (Number of C&C People not tested)
        #                           / (Number of C&C People)
        f2 = (num_of_confirmed + num_of_contacted - num_of_cc_tested_covid19) \
             / (num_of_contacted + num_of_confirmed)
        return f2

    def compute_positive_rate(self, positivity_count, num_of_cc_tested_covid19):
        # 3. Number of Confirmed Cases, Positivity Tests --> Proportion
        # (Rate of Positivity from COVID-19 Test) = (Number of Positivity) / (Number of COVID-19 Test)
        f3 = positivity_count / num_of_cc_tested_covid19
        return f3

    def compute_gsr_factor4(self):
        # 4. Number of Contacted People --> X
        pass

    def compute_gsr_factor5(self):
        # 5. Number of Deceased People --> X
        pass

    def compute_fatality_rate(self, num_of_deceased, num_of_confirmed):
        # 6. Fatality Rate
        # (Fatality Rate) = (Number of Deceased People) / (Number of Confirmed Cases)
        f6 = num_of_deceased / num_of_confirmed
        return f6

    def compute_confirmed_isolation_rate(self, num_of_isolated_confirmed, num_of_confirmed):
        # 7. Quarantine/Isolation Rate of Confirmed People --> Inverse Proportion
        # (Quarantine/Isolation Rate of Confirmed People) =
        #                 1 - (Number of Confirmed People in Quarantine/Isolation state) / (Number of Confirmed People)
        f7 = 1 - (num_of_isolated_confirmed / num_of_confirmed)
        return f7

    def compute_contacted_isolation_rate(self, num_of_isolated_contacted, num_of_contacted):
        # 8. Quarantine/Isolation Rate of Contacted People --> Inverse Proportion
        # (Quarantine/Isolation Rate of Contacted People) =
        #                 1 - (Number of Contacted People in Quarantine/Isolation state) / (Number of Contacted People)
        f8 = 1 - (num_of_isolated_contacted / num_of_contacted)
        return f8

    def compute_indetified_rate(self, num_of_identified_cc, num_of_contacted, num_of_confirmed):
        # 9. Traceability Rate of Infection Paths --> Inverse Proportion
        # (Traceability Rate of Infection Paths) =
        #                               1 - (Number of C&C People whose routes are identified) / (Number of C&C People)
        f9 = 1 - (num_of_identified_cc / (num_of_contacted + num_of_confirmed))
        return f9

    def compute_hospital_capability(self, num_of_confirmed, num_of_contacted, hospital_capability):
        # 10. Hospital Capability for Treating COVID-19 Patients --> Proportion
        # (Hospital Capability for Treating COVID-19 Patients) =
        #                                              max(1, (Number of C&C People) / (Number of Capability Hospital))
        f10 = max(1, (num_of_confirmed + num_of_contacted) / hospital_capability)
        return f10

    def compute_recovery_rate(self, num_of_recovered, num_of_confirmed):
        # 11. Recovery Rate of COVID-19 Patients --> Inverse Proportion
        # (Recovery Rate of COVID-19 Patients) = (Number of recovered People from COVID-19) / (Number of C&C People)
        if num_of_confirmed > 1 and (0 <= num_of_recovered <= num_of_confirmed):
            f11 = num_of_recovered / num_of_confirmed
        return f11

    def compute_isr_effect(self, related_isr_list):
        # This factor is not in SRS.
        # The focus is the high level ISR people.
        return max(related_isr_list)

    def compute_gsr(self, weight_dic, factor_dic):
        if weight_dic.keys() != factor_dic.keys():  # s
            try:
                raise ValueError("The targets of Weight Dictionary and Types of GSR Factor is different!")
            except ValueError:
                return None

        gsr = sum(list([(factor_dic[k] * weight_dic[k]) for k in set(weight_dic) & set(factor_dic)]))

        if gsr > 1:  # gsr is out of range?
            try:
                raise ValueError("GSR Value is greater than 1!")
            except ValueError:
                return None
        elif gsr < 0:  # gsr is out of range?
            try:
                raise ValueError("GSR Value is negative number!")
            except ValueError:
                return None
        else:
            return gsr


class ISRMetric:
    ###########################################################################
    # large_group_gsr = None
    # age = None
    # disease_score = None
    # gsr_visited_list = None
    # gsr_commute_list = None
    ###########################################################################

    isr_factor_value_dic_prototype = {
        'Large Group GSR': {
            'large_group_gsr': 0
        },
        'Age Score': {
            'age': 0
        },
        'Disease Score': {
            'disease_score': 0
        },
        'GSR Visited': {
            'gsr_visited_list': []
            # or
            # 'max_gsr_visited': 0
        },
        'GSR on Commute': {
            'GSR Values on commute': []
            # or
            # 'avg_gsr_on_commute': 0
        }
    }

    def preprocess_isr_factor(self, factor_value_dic):
        """
        method to call specific methods and to compute factor
        :param factor_value_dic: dictionary, key: method name of this class, value: parameters
        :return: dictionary, key: method name(or factor name) value: factor values
        """
        factor_dic = {}
        for factor_name, value_dic in factor_value_dic.items():
            if factor_name == 'Large Group GSR':
                try:
                    large_group_gsr = value_dic['large_group_gsr']
                except Exception as ex:
                    print("Exception!:", ex)
                    return None

                factor_dic[factor_name] = \
                    self.compute_large_group_gsr(large_group_gsr=large_group_gsr)

            elif factor_name == 'Age Score':
                try:
                    age = value_dic['age']
                except Exception as ex:
                    print("Exception!:", ex)
                    return None

                factor_dic[factor_name] = \
                    self.compute_age_score(age=age)

            elif factor_name == 'Disease Score':
                try:
                    disease_score = value_dic['disease_score']
                except Exception as ex:
                    print("Exception!:", ex)
                    return None

                factor_dic[factor_name] = \
                    self.compute_disease_score(disease_score=disease_score)

            elif factor_name == 'GSR Visited':
                try:
                    gsr_visited_list = value_dic['gsr_visited_list']
                except Exception as ex:
                    print("Exception!:", ex)
                    return None

                factor_dic[factor_name] = \
                    self.compute_gsr_visitied(gsr_visited_list=gsr_visited_list)

            elif factor_name == 'GSR on Commute':
                try:
                    gsr_commute_list = value_dic['gsr_commute_list']
                except Exception as ex:
                    print("Exception!:", ex)
                    return None

                factor_dic[factor_name] = \
                    self.compute_gsr_on_commute(gsr_commute_list=gsr_commute_list)

        return factor_dic

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
