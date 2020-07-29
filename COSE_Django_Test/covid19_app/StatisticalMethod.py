"""
Program Title: Metrics to compute GSR and ISR
created: June 29, 2020 8:54PM
Author: DoYeong
"""


class GSRMetric:
    def compute_gsr(self, group_type,  # group type
                    confirmed_count, contacted_count, decease_count, recovered_count,  # about number of people
                    covid19_test_cc_count, positivity_count,  # about test
                    isolated_confirmed_count, isolated_contacted_count,  # about isolation people
                    identified_cc_count,  # about identified people
                    hospital_capability):  # about hospital capability
        # TODO: methodnize the all factors as pre-precessing
        # 1. Number of COVID-19 Tests Performed --> X

        # 2. COVID-19 Test Rate --> Proportion
        # (COVID-19 Test Rate) = (Number of C&C People not tested - Number of recovered People from COVID-19)
        #                           / (Number of C&C People)
        f2 = (confirmed_count + contacted_count - recovered_count - covid19_test_cc_count) \
             / (contacted_count + confirmed_count)

        # 3. Number of Confirmed Cases, Positivity Tests --> Proportion
        # (Rate of Positivity from COVID-19 Test) = (Number of Positivity) / (Number of COVID-19 Test)
        f3 = positivity_count / covid19_test_cc_count

        # 4. Number of Contacted People --> X

        # 5. Number of Deceased People --> X

        # 6. Fatality Rate
        # (Fatality Rate) = (Number of Deceased People) / (Number of Confirmed Cases)
        f6 = decease_count / confirmed_count

        # 7. Quarantine/Isolation Rate of Confirmed People --> Inverse Proportion
        # (Quarantine/Isolation Rate of Confirmed People) =
        #                 1 - (Number of Confirmed People in Quarantine/Isolation state) / (Number of Confirmed People)
        f7 = 1 - (isolated_confirmed_count / confirmed_count)

        # 8. Quarantine/Isolation Rate of Contacted People --> Inverse Proportion
        # (Quarantine/Isolation Rate of Contacted People) =
        #                 1 - (Number of Contacted People in Quarantine/Isolation state) / (Number of Contacted People)
        f8 = 1 - (isolated_contacted_count / contacted_count)

        # 9. Traceability Rate of Infection Paths --> Inverse Proportion
        # (Traceability Rate of Infection Paths) =
        #                               1 - (Number of C&C People whose routes are identified) / (Number of C&C People)
        f9 = 1 - (identified_cc_count / (contacted_count + confirmed_count))

        # only for city or district?
        # 10. Hospital Capability for Treating COVID-19 Patients --> Proportion
        # (Hospital Capability for Treating COVID-19 Patients) =
        #                                              max(1, (Number of C&C People) / (Number of Capability Hospital))
        if group_type == 'city':
            f10 = max(1, (confirmed_count + contacted_count) / hospital_capability)

        # 11. Recovery Rate of COVID-19 Patients --> Inverse Proportion
        # (Recovery Rate of COVID-19 Patients) = (Number of recovered People from COVID-19) / (Number of C&C People)
        f11 = recovered_count / (confirmed_count + contacted_count)

        if group_type == 'city':
            return [f2, f3, f6, f7, f8, f9, f10, f11]


class ISRMetric:
    def compute_isr(self, large_group_gsr, age, disease_score, gsr_visited_list, gsr_commute_list):
        # TODO: methodnize the all factors as pre-precessing
        # 1. GSR Value of the City/Region where the individual lives --> Proportion
        f1 = large_group_gsr
        # or f1 = large_group_gsr / (Number of GSR Factor)

        # 2. Age of the Individual --> Proportion
        # Basis of Calculation: 4page of COSE SRS
        # Age   | Factor Value
        #  0~17 | ?
        # 18~29 | ~0.066~
        # 30~39 | ~0.136~
        # 40~49 | ~0.274~
        # 50~59 | ~0.451~
        # 60~69 | ~0.612~
        # 70~79 | ~0.751~
        # 80+   | ~0.79~
        f2 = age_to_value(age)

        # 3. Underlying Diseases such as Heart Disease, Lung Disease, and Diabetes --> Proportion
        f3 = disease_score

        # 4. History of Places visited --> Proportion
        # The most highest GSR values is critical to person
        f4 = max(gsr_visited_list)

        # 5. Commute Routes --> Proportion
        # GSR Values of Small Groups
        # (Average of GSR during commute) = (Sum of GSR values on commute) / (Number of GSR values)
        f5 = sum(gsr_commute_list) / len(gsr_commute_list)
        # or f5 = (sum(gsr_commute_list) / (Number of GSR Factor)) / len(gsr_commute_list)

        return [f1, f2, f3, f4, f5]

    def age_to_value(self, age):
        pass
