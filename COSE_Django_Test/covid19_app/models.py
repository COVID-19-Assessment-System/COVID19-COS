"""
Program Title: DB query statement
created: June 27, 2020 9:39AM
Author: DoYeong
"""
from django.db import models
from datetime import datetime


class Alert(models.Model):
    # [column name] = model.[column type].(conditions of column)

    class Meta:
        managed = True
        db_table = 'alert'

    def create_alert(self):
        pass

    def retrieve_alert(self):
        pass

    def update_alert(self):
        pass

    def delete_alert(self):
        pass


class AlertOption(models.Model):
    # [column name] = model.[column type].(conditions of column)

    class Meta:
        managed = True
        db_table = 'alert_option'

    def create_alert_option(self):
        pass

    def retrieve_alert_option(self):
        pass

    def update_alert_option(self):
        pass

    def delete_alert_option(self):
        pass


class Building(models.Model):
    # [column name] = model.[column type].(conditions of column)
    building_type = models.CharField(max_length=255, blank=True, null=True)
    building_name = models.CharField(max_length=255, blank=True, null=True)
    group = models.ForeignKey('Group', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'building'

    def create_building(self,
                        address,
                        area,
                        num_person,
                        severity_average,
                        building_type,
                        building_name):
        g = Group()
        g.create_group(address=address,
                       area=area,
                       num_person=num_person,
                       severity_average=severity_average)
        self.group = g

        self.building_type = building_type
        self.building_name = building_name

        try:
            self.save()  # execute query
            return True
        except Exception as ex:
            print("Exception!:", ex)
            return False

    def retrieve_building(self,
                          address=None,
                          area=None,
                          num_person=None,
                          severity_average=None,
                          building_type=None,
                          building_name=None):
        queryset = Building.objects.select_related('group')

        try:
            if address is not None:
                queryset = queryset.filter(group__address=address)
            if area is not None:
                queryset = queryset.filter(group__area=area)
            if num_person is not None:
                queryset = queryset.filter(group__num_person=num_person)
            if severity_average is not None:
                queryset = queryset.filter(group__severity_average=severity_average)

            if building_type is not None:
                queryset = queryset.filter(building_type=building_type)
            if building_name is not None:
                queryset = queryset.filter(building_name=building_name)
        except Exception as ex:
            print("Exception!:", ex)
            return ()

        result = []
        for i in queryset:
            dic = {'id': i.id,
                   'building_type': i.building_type,
                   'building_name': i.building_name,
                   'group_id': i.group_id,
                   'address': i.group.address,
                   'area': i.group.area,
                   'num_person': i.group.num_person,
                   'severity_average': i.group.severity_average}
            result.append(dic)

        return tuple(result)

    def update_building(self,
                        address=None,
                        area=None,
                        num_person=None,
                        severity_average=None,
                        building_type=None,
                        building_name=None):
        if (address is not None) \
                or (area is not None) \
                or (num_person is not None) \
                or (severity_average is not None):
            self.user.update_user(address=address,
                                  area=area,
                                  num_person=num_person,
                                  severity_average=severity_average)

        if building_type is not None:
            self.building_type = building_type
        if building_name is not None:
            self.building_name = building_name

        try:
            self.save()  # execute query
            return True
        except Exception as ex:
            print("Exception!:", ex)
            return False

    def delete_building(self):
        try:
            self.delete()
            self.group.delete_group()
            return True
        except Exception as ex:
            print("Exception!:", ex)
            return False


class Country(models.Model):
    # [column name] = model.[column type].(conditions of column)
    continent = models.CharField(max_length=255, blank=True, null=True)
    region = models.ForeignKey('Region', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'country'

    def create_country(self,
                       address,
                       area,
                       num_person,
                       severity_average,
                       region_name,
                       continent):
        r = Region()
        r.create_region(address=address,
                        area=area,
                        num_person=num_person,
                        severity_average=severity_average,
                        region_name=region_name)

        self.region = r

        self.continent = continent

        try:
            self.save()  # execute query
            return True
        except Exception as ex:
            print("Exception!:", ex)
            return False

    def retrieve_country(self,
                         address=None,
                         area=None,
                         num_person=None,
                         severity_average=None,
                         region_name=None,
                         continent=None):
        queryset = Country.objects.select_related('region')

        try:
            if address is not None:
                queryset = queryset.filter(region__group__address=address)
            if area is not None:
                queryset = queryset.filter(region__group__area=area)
            if num_person is not None:
                queryset = queryset.filter(region__group__num_person=num_person)
            if severity_average is not None:
                queryset = queryset.filter(region__group__severity_average=severity_average)
            if region_name is not None:
                queryset = queryset.filter(region__region_name=region_name)

            if continent is not None:
                queryset = queryset.filter(continent=continent)
        except Exception as ex:
            print("Exception!:", ex)
            return ()
        # TODO: 구현안됨

    def update_country(self,
                       address=None,
                       area=None,
                       num_person=None,
                       severity_average=None,
                       region_name=None,
                       continent=None):
        if (address is not None) \
                or (area is not None) \
                or (num_person is not None) \
                or (severity_average is not None) \
                or (region_name is not None):
            self.region.update_region(address=address,
                                      area=area,
                                      num_person=num_person,
                                      severity_average=severity_average,
                                      region_name=region_name)

        if continent is not None:
            self.continent = continent

        try:
            self.save()  # execute query
            return True
        except Exception as ex:
            print("Exception!:", ex)
            return False

    def delete_country(self):
        try:
            self.delete()
            self.region.delete_region()
            return True
        except Exception as ex:
            print("Exception!:", ex)
            return False


class Facility(models.Model):
    # [column name] = model.[column type].(conditions of column)
    facility_type = models.CharField(max_length=255, blank=True, null=True)
    facility_name = models.CharField(max_length=255, blank=True, null=True)
    group = models.ForeignKey('Group', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'facility'

    def create_facility(self,
                        address,
                        area,
                        num_person,
                        severity_average,
                        facility_type,
                        facility_name):
        g = Group()
        g.create_group(address=address,
                       area=area,
                       num_person=num_person,
                       severity_average=severity_average)
        self.group = g
        self.facility_type = facility_type
        self.facility_name = facility_name

        try:
            self.save()  # execute query
            return True
        except Exception as ex:
            print("Exception!:", ex)
            return False

    def retrieve_facility(self,
                          address=None,
                          area=None,
                          num_person=None,
                          severity_average=None,
                          facility_type=None,
                          facility_name=None):
        queryset = Facility.objects.select_related('group')

        try:
            if address is not None:
                queryset = queryset.filter(group__address=address)
            if area is not None:
                queryset = queryset.filter(group__area=area)
            if num_person is not None:
                queryset = queryset.filter(group__num_person=num_person)
            if severity_average is not None:
                queryset = queryset.filter(group__severity_average=severity_average)

            if facility_type is not None:
                queryset = queryset.filter(facility_type=facility_type)
            if facility_name is not None:
                queryset = queryset.filter(facility_name=facility_name)
        except Exception as ex:
            print("Exception!:", ex)
            return ()

        result = []
        for i in queryset:
            dic = {'id': i.id,
                   'facility_type': i.facility_type,
                   'facility_name': i.facility_name,
                   'group_id': i.group_id,
                   'address': i.group.address,
                   'area': i.group.area,
                   'num_person': i.group.num_person,
                   'severity_average': i.group.severity_average}
            result.append(dic)

        return tuple(result)

    def update_facility(self,
                        address=None,
                        area=None,
                        num_person=None,
                        severity_average=None,
                        facility_type=None,
                        facility_name=None):
        if (address is not None) \
                or (area is not None) \
                or (num_person is not None) \
                or (severity_average is not None):
            self.user.update_user(address=address,
                                  area=area,
                                  num_person=num_person,
                                  severity_average=severity_average)

        if facility_type is not None:
            self.facility_type = facility_type
        if facility_name is not None:
            self.facility_name = facility_name

        try:
            self.save()  # execute query
            return True
        except Exception as ex:
            print("Exception!:", ex)
            return False

    def delete_facility(self):
        try:
            self.delete()
            self.group.delete_group()
            return True
        except Exception as ex:
            print("Exception!:", ex)
            return False


class Group(models.Model):
    # [column name] = model.[column type].(conditions of column)
    address = models.CharField(max_length=255, blank=True, null=True)
    area = models.FloatField(blank=True, null=True)
    num_person = models.CharField(max_length=255, blank=True, null=True)
    severity_average = models.FloatField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'group'

    def create_group(self,
                     address,
                     area,
                     num_person,
                     severity_average):
        self.address = address
        self.area = area
        self.num_person = num_person
        self.severity_average = severity_average

        try:
            self.save()  # execute query
            return True
        except Exception as ex:
            print("Exception!:", ex)
            return False

    def retrieve_group(self,
                       address=None,
                       area=None,
                       num_person=None,
                       severity_average=None):
        queryset = Group.objects

        try:
            if address is not None:
                queryset = queryset.filter(address=address)
            if area is not None:
                queryset = queryset.filter(area=area)
            if num_person is not None:
                queryset = queryset.filter(num_person=num_person)
            if severity_average is not None:
                queryset = queryset.filter(severity_average=severity_average)

            return tuple(queryset.values())

        except Exception as ex:
            print("Exception!:", ex)
            return ()

    def update_group(self,
                     address=None,
                     area=None,
                     num_person=None,
                     severity_average=None):

        if address is not None:
            self.address = address
        if area is not None:
            self.area = area
        if num_person is not None:
            self.num_person = num_person
        if severity_average is not None:
            self.severity_average = severity_average

        try:
            self.save()  # execute query
            return True
        except Exception as ex:
            print("Exception!:", ex)
            return False

    def delete_group(self):
        try:
            self.delete()
            return True
        except Exception as ex:
            print("Exception!:", ex)
            return False


class GroupSafetyRisk(models.Model):
    # [column name] = model.[column type].(conditions of column)
    gsr = models.FloatField(blank=True, null=True)
    group = models.ForeignKey(Group, models.DO_NOTHING, blank=True, null=True)
    gsr_option = models.ForeignKey('GsrOption', blank=True, null=True, on_delete=models.DO_NOTHING)
    safety_risk = models.ForeignKey('SafetyRisk', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'group_safety_risk'

    def create_group_safety_risk(self, gsr, group_object, gsr_option_object, methods_object):
        sr = SafetyRisk()
        sr.create_safety_risk(datetime.now(), methods_object)
        self.safety_risk = sr

        self.gsr = gsr
        self.group = group_object
        self.gsr_option = gsr_option_object

        try:
            self.save()  # execute query
            return True
        except Exception as ex:
            print("Exception!:", ex)
            return False

    def retrieve_group_safety_risk(self, gsr=None, group_object=None, gsr_option_object=None, methods_object=None):
        queryset = GroupSafetyRisk.objects

        try:
            # checking the value of super class
            if methods_object is not None:
                queryset = queryset.filter(safety_risk__methods=methods_object)

            # checking the value of this(sub) class
            if gsr is not None:
                queryset = queryset.filter(gsr=gsr)
            if group_object is not None:
                queryset = queryset.filter(group_object=group_object)
            if gsr_option_object is not None:
                queryset = queryset.filter(gsr_option=gsr_option_object)
        except Exception as ex:
            print("Exception!:", ex)
            return ()

        return tuple(queryset.values())

    def update_group_safety_risk(self, gsr=None, group_object=None, gsr_option_object=None, methods_object=None):
        # updating values of super class
        if methods_object is not None:
            self.safety_risk.update_safety_risk(methods_object=methods_object)

        # updating values of sub class
        if gsr is not None:
            self.gsr = gsr
        if group_object is not None:
            self.group = group_object
        if gsr_option_object is not None:
            self.gsr_option = gsr_option_object

        try:
            self.save()  # execute query
            return True

        except Exception as ex:
            print("Exception!:", ex)
            return False

    def delete_group_safety_risk(self):
        try:
            self.delete()
            self.safety_risk.delete_safety_risk()
            return True
        except Exception as ex:
            print("Exception!:", ex)
            return False


class GsrOption(models.Model):
    # [column name] = model.[column type].(conditions of column)
    weight_list = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'gsr_option'

    def create_gsr_option(self, weight_list):
        self.weight_list = weight_list

        try:
            self.save()  # execute query
            return True
        except Exception as ex:
            print("Exception!:", ex)
            return False

    def retrieve_gsr_option(self, weight_list):
        queryset = GsrOption.objects

        try:
            # TODO: How to handle the 'list'?
            # checking the value of this(sub) class
            if metric_name is not None:
                queryset = queryset.filter(weight_list=weight_list)
        except Exception as ex:
            print("Exception!:", ex)
            return ()

        return tuple(queryset.values())  # returning the queryset as tuple

    def update_gsr_option(self, weight_list):
        self.weight_list = weight_list

        try:
            self.save()  # execute query
            return True
        except Exception as ex:
            print("Exception!:", ex)
            return False

    def delete_gsr_option(self):

        try:
            self.delete()  # execute query
            return True
        except Exception as ex:
            print("Exception!:", ex)
            return False


class IndividualSafetyRisk(models.Model):
    # [column name] = model.[column type].(conditions of column)
    isr = models.FloatField(blank=True, null=True)
    member = models.ForeignKey('Member', models.DO_NOTHING, blank=True, null=True)
    isr_option = models.OneToOneField('IsrOption', blank=True, null=True, on_delete=models.DO_NOTHING)
    safety_risk = models.ForeignKey('SafetyRisk', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'individual_safety_risk'

    def create_individual_safety_risk(self, isr, member_object, isr_option_object, methods_object):
        sr = SafetyRisk()
        sr.create_safety_risk(datetime.now(), methods_object)
        self.safety_risk = sr

        self.isr = isr
        self.member = member_object
        self.isr_option = isr_option_object

        try:
            self.save()  # execute query
            return True
        except Exception as ex:
            print("Exception!:", ex)
            return False

    def retrieve_individual_safety_risk(self, isr=None, member_object=None, isr_option_object=None,
                                        methods_object=None):
        queryset = IndividualSafetyRisk.objects

        try:
            # checking the value of super class
            if methods_object is not None:
                queryset = queryset.filter(safety_risk__methods=methods_object)

            # checking the value of this(sub) class
            if isr is not None:
                queryset = queryset.filter(isr=isr)
            if member_object is not None:
                queryset = queryset.filter(member_object=member_object)
            if isr_option_object is not None:
                queryset = queryset.filter(isr_option=isr_option_object)
        except Exception as ex:
            print("Exception!:", ex)
            return ()

        return tuple(queryset.values())

    def update_individual_safety_risk(self, isr=None, member_object=None, isr_option_object=None,
                                      methods_object=None):
        # updating values of super class
        if methods_object is not None:
            self.safety_risk.update_safety_risk(methods_object=methods_object)

        # updating values of sub class
        if isr is not None:
            self.isr = isr
        if member_object is not None:
            self.member = member_object
        if isr_option_object is not None:
            self.isr_option = isr_option_object

        try:
            self.save()  # execute query
            return True

        except Exception as ex:
            print("Exception!:", ex)
            return False

    def delete_individual_safety_risk(self):
        try:
            self.delete()
            self.safety_risk.delete_safety_risk()
            return True
        except Exception as ex:
            print("Exception!:", ex)
            return False


class IsrOption(models.Model):
    weight_list = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'isr_option'

    def create_isr_option(self):
        pass

    def retrieve_isr_option(self):
        pass

    def update_isr_option(self):
        pass

    def delete_isr_option(self):
        pass


class Member(models.Model):
    # [column name] = model.[column type].(conditions of column)
    address = models.CharField(max_length=255, blank=True, null=True)
    living_distance = models.FloatField(blank=True, null=True)
    preferred_group = models.CharField(max_length=255, blank=True, null=True)
    fcm_id = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'member'

    def create_member(self, age, name, email, password, address, living_distance, preferred_group, fcm_id):
        """
        method to create 1 member data
        :param age: int, parameter for user, age of member
        :param name: string, parameter for user, name of member
        :param email: string, parameter for user, email address as login ID
        :param password: string, parameter for user, password
        :param address: string, residence address of member
        :param living_distance: float, living distance of member
        :param preferred_group: string, related and preferred group of member
        :param fcm_id: string, member device id
        :return: bool, the result of adding data in the table. If the data is input well, True is returned.
        """
        u = User()  # super class call
        u.create_user(age=age,  # create super class
                      name=name,
                      email=email,
                      password=password)
        self.user = u

        # column value assignment
        self.address = address
        self.living_distance = living_distance
        self.preferred_group = preferred_group
        self.fcm_id = fcm_id
        try:
            self.save()  # execute query
            return True
        except Exception as ex:
            print("Exception!:", ex)
            return False

    def retrieve_member(self, age=None, name=None, email=None, password=None, address=None, living_distance=None,
                        preferred_group=None, fcm_id=None):
        """
        method to retrieve member data
        :param age: int, parameter for user, age of member
        :param name: string, parameter for user, name of member
        :param email: string, parameter for user, email address as login ID
        :param password: string, parameter for user, password for login
        :param address: string, residence address of member
        :param living_distance: float, living distance of member
        :param preferred_group: string, related and preferred group of member
        :param fcm_id: string, member device id
        :return: tuple, the result of query, shape is as below:
                    0 element or Error, Exception : ()
                    1 element: ({}, )
                    n elements: ({}, {}, {}, ... , {})
        """
        queryset = Member.objects.select_related('user')  # inner join

        try:
            # checking the value of super class
            if age is not None:
                queryset = queryset.filter(user__age=age)
            if name is not None:
                queryset = queryset.filter(user__name=name)
            if email is not None:
                queryset = queryset.filter(user__email=email)
            if password is not None:
                queryset = queryset.filter(user__password=password)

            # checking the value of this(sub) class
            if address is not None:
                queryset = queryset.filter(address=address)
            if living_distance is not None:
                queryset = queryset.filter(living_distance=living_distance)
            if preferred_group is not None:
                queryset = queryset.filter(preferred_group=preferred_group)
            if fcm_id is not None:
                queryset = queryset.filter(fcm_id=fcm_id)
        except Exception as ex:
            print("Exception!:", ex)
            return ()

        result = []  # list for store
        for i in queryset:  # Combining 2 types query sets(superclass, subclass)
            dic = {
                # columns of sub class
                'id': i.id,
                'address': i.address,
                'living_distance': i.living_distance,
                'preferred_group': i.preferred_group,
                'fcm_id': i.fcm_id,

                # columns of super class
                'user_id': i.user_id,
                'age': i.user.age,
                'name': i.user.name,
                'email': i.user.email}
            result.append(dic)  # appending the dictionary at the result list

        return tuple(result)  # returning the dictionary list as tuple

    def update_member(self, age=None, name=None, email=None, password=None, address=None, living_distance=None,
                      preferred_group=None, fcm_id=None):
        """
        method to update 1 member data
        :param age: int, parameter for user, age of member
        :param name: string, parameter for user, name of member
        :param email: string, parameter for user, email address as login ID
        :param password: string, parameter for user, password
        :param address: string, residence address of member
        :param living_distance: float, living distance of member
        :param preferred_group: string, related and preferred group of member
        :param fcm_id: string, member device id
        :return: bool, the result of updating data in the table. If the data is input well, True is returned.
        """

        # updating values of super class
        if (age is not None) \
                or (name is not None) \
                or (email is not None) \
                or (password is not None):
            self.user.update_user(age=age,
                                  name=name,
                                  email=email,
                                  password=password)

        # updating values of sub class
        if address is not None:
            self.address = address
        if living_distance is not None:
            self.living_distance = living_distance
        if preferred_group is not None:
            self.preferred_group = preferred_group
        if fcm_id is not None:
            self.fcm_id = fcm_id

        try:
            self.save()  # execute query
            return True

        except Exception as ex:
            print("Exception!:", ex)
            return False

    def delete_member(self):
        try:
            self.delete()
            self.user.delete_user()
            return True
        except Exception as ex:
            print("Exception!:", ex)
            return False


class Person(models.Model):
    # [column name] = model.[column type].(conditions of column)

    class Meta:
        managed = True
        db_table = 'person'

    def create_person(self):
        """
        method to create 1 person dat a
        :return: bool, the result of adding data in the table. If the data is input well, True is returned.
        """
        try:
            self.save()  # execute query
            return True
        except Exception as ex:
            print("Exception!:", ex)
            return False

    def retrieve_person(self):
        """
        method to retrieve all person data
        :return: tuple, the result of query, shape is as below:
                    0 element: ()
                    1 element: ({}, )
                    n elements: ({}, {}, {}, ... , {})
        """
        queryset = Person.objects
        try:
            return tuple(queryset.values())
        except Exception as ex:
            print("Exception!:", ex)
            return ()

    def delete_person(self):
        """
        method to delete 1 person data
        :return: bool, the result of deleting data in the table. If the data is deleted well, True is returned.
        """
        try:
            self.delete()  # execute query
            return True
        except Exception as ex:
            print("Exception!:", ex)
            return False


class Region(models.Model):
    # [column name] = model.[column type].(conditions of column)
    region_name = models.CharField(max_length=255, blank=True, null=True)
    group = models.ForeignKey(Group, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'region'

    def create_region(self,
                      address,
                      area,
                      num_person,
                      severity_average,
                      region_name):
        g = Group()
        g.create_group(address=address,
                       area=area,
                       num_person=num_person,
                       severity_average=severity_average)
        self.group = g

        self.region_name = region_name

        try:
            self.save()  # execute query
            return True
        except Exception as ex:
            print("Exception!:", ex)
            return False

    def update_region(self,
                      address=None,
                      area=None,
                      num_person=None,
                      severity_average=None,
                      region_name=None):
        if (address is not None) \
                or (area is not None) \
                or (num_person is not None) \
                or (severity_average is not None):
            self.group.update_group(address=address,
                                    area=area,
                                    num_person=num_person,
                                    severity_average=severity_average)

        if region_name is not None:
            self.region_name = region_name

        try:
            self.save()  # execute query
            return True
        except Exception as ex:
            print("Exception!:", ex)
            return False

    def delete_region(self):
        try:
            self.delete()
            self.group.delete_group()
            return True
        except Exception as ex:
            print("Exception!:", ex)
            return False


class SafetyRisk(models.Model):
    # [column name] = model.[column type].(conditions of column)
    enrolled_datetime = models.DateTimeField(blank=True, null=True)
    methods = models.ManyToManyField('SafetyRiskAnalyticMethod', through='SrMethod')

    class Meta:
        managed = True
        db_table = 'safety_risk'

    def create_safety_risk(self, enrolled_datetime, methods_object):
        """
        method to create 1 safety risk data
        :param enrolled_datetime: datetime, date and time when safety risk is enrolled
        :param methods_object: SafetyRiskAnalyticMethod, SafetyRiskAnalyticMethod object
        :return: bool, the result of adding data in the table. If the data is input well, True is returned.
        """
        self.enrolled_datetime = enrolled_datetime

        try:
            self.save()  # execute query
            self.methods.add(methods_object)  # add the value to the join table
            return True
        except Exception as ex:
            print("Exception!:", ex)
            return False

    def retrieve_safety_risk(self, enrolled_datetime=None, methods_object=None):
        """
        method to retrieve specific safety risk data
        :param enrolled_datetime: datetime, date and time when safety risk is enrolled
        :param methods_object: SafetyRiskAnalyticMethod, SafetyRiskAnalyticMethod object
        :return: tuple, the result of query, shape is as below:
                    0 element: ()
                    1 element: ({}, )
                    n elements: ({}, {}, {}, ... , {})
        """
        queryset = SafetyRisk.objects

        try:
            if enrolled_datetime is not None:
                queryset = queryset.filter(datetime=datetime)
            if methods_object is not None:
                queryset = queryset.filter(methods=methods_object)

            return tuple(queryset.values())

        except Exception as ex:
            print("Exception!:", ex)
            return ()

    def update_safety_risk(self, enrolled_datetime=None, methods_object=None):
        """
        method to update 1 safety risk data
        :param enrolled_datetime: datetime, date and time when safety risk is enrolled
        :param methods_object: SafetyRiskAnalyticMethod, SafetyRiskAnalyticMethod object
        :return: bool, the result of updating data in the table. If the data is updated well, True is returned.
        """
        if datetime is not None:
            self.enrolled_datetime = enrolled_datetime

        # TODO: This part do not work now!
        if methods_object is not None:
            self.methods.update(safety_risk_analytic_method=methods_object)

        try:
            self.save()  # execute query
            return True
        except Exception as ex:
            print("Exception!:", ex)
            return False

    def delete_safety_risk(self):
        """
        method to delete 1 safety risk data
        :return: bool, the result of deleting data in the table. If the data is deleted well, True is returned.
        """
        try:
            self.delete()
            return True
        except Exception as ex:
            print("Exception!:", ex)
            return False


class SafetyRiskAnalyticMethod(models.Model):
    # [column name] = model.[column type].(conditions of column)
    enrolled_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'safety_risk_analytic_method'

    def create_safety_risk_analytic_method(self):
        """
        method to create 1 safety risk analytic method data
        :return: bool, the result of adding data in the table. If the data is input well, True is returned.
        """
        self.enrolled_date = datetime.now()

        try:
            self.save()  # execute query
            return True
        except Exception as ex:
            print("Exception!:", ex)
            return False

    def retrieve_safety_risk_analytic_method(self):
        """
        method to retrieve all safety risk analytic method data
        :return: tuple, the result of query, shape is as below:
                    0 element: ()
                    1 element: ({}, )
                    n elements: ({}, {}, {}, ... , {})
        """
        queryset = SafetyRiskAnalyticMethod.objects

        try:
            return tuple(queryset.values())
        except Exception as ex:
            print("Exception!:", ex)
            return ()

    def update_safety_risk_analytic_method(self, enrolled_date):
        """
        method to update 1 safety risk analytic method data
        :param enrolled_date: datetime, the enrolled datetime of the method
        :return: bool, the result of updating data in the table. If the data is updated well, True is returned.
        """
        self.enrolled_date = enrolled_date

        try:
            self.save()  # execute query
            return True
        except Exception as ex:
            print("Exception!:", ex)
            return False

    def delete_safety_risk_analytic_method(self):
        """
        method to delete 1 safety risk analytic method data
        :return: bool, the result of deleting data in the table. If the data is deleted well, True is returned.
        """
        try:
            self.delete()  # execute query
            return True
        except Exception as ex:
            print("Exception!:", ex)
            return False


class SrMethod(models.Model):
    # [column name] = model.[column type].(conditions of column)
    sr_analytic_method = models.ForeignKey(SafetyRiskAnalyticMethod, models.DO_NOTHING, blank=True, null=True)
    sr = models.ForeignKey(SafetyRisk, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'sr_method'

# TODO: divide and convert 'StatisticalMethod' to 'GsrMetric' and 'IsrMetric'
class StatisticalMethod(models.Model):
    # [column name] = model.[column type].(conditions of column)
    metric_name = models.CharField(max_length=255, blank=True, null=True)
    safety_risk_analytic_method = models.ForeignKey(SafetyRiskAnalyticMethod, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'statistical_method'

    def create_statistical_method(self, metric_name):
        sram = SafetyRiskAnalyticMethod()  # super class call
        sram.create_safety_risk_analytic_method()  # create super class
        self.safety_risk_analytic_method = sram

        # column value assignment
        self.metric_name = metric_name

        try:
            self.save()  # execute query
            return True
        except Exception as ex:
            print("Exception!:", ex)
            return False

    def retrieve_statistical_method(self, metric_name=None):
        queryset = SafetyRiskAnalyticMethod.objects

        try:
            # checking the value of this(sub) class
            if metric_name is not None:
                queryset = queryset.filter(metric_name=metric_name)
        except Exception as ex:
            print("Exception!:", ex)
            return ()

        return tuple(queryset.values())  # returning the queryset as tuple

    def update_statistical_method(self, metric_name=None):
        self.metric_name = metric_name

        try:
            self.save()  # execute query
            return True
        except Exception as ex:
            print("Exception!:", ex)
            return False

    def delete_statistical_method(self):
        try:
            self.delete()  # execute query
            # delete super class
            self.safety_risk_analytic_method.delete_safety_risk_analytic_method()
            return True
        except Exception as ex:
            print("Exception!:", ex)
            return False


class User(models.Model):
    # [column name] = model.[column type].(conditions of column)
    age = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, unique=True, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    person = models.ForeignKey(Person, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'user'

    def create_user(self, age, name, email, password):
        """
        method to create 1 user data
        :param age: int, age of user
        :param name: string, name of user
        :param email: string, email address as login ID
        :param password: string, password
        :return: bool, the result of adding data in the table. If the data is input well, True is returned.
        """
        p = Person()  # super class call
        p.create_person()  # create super class
        self.person = p

        # column value assignment
        self.age = age
        self.name = name
        self.email = email
        self.password = password

        try:
            self.save()  # execute query
            return True
        except Exception as ex:
            print("Exception!:", ex)
            return False

    def retrieve_user(self, age=None, name=None, email=None, password=None):
        """
        method to retrieve specific user data
        :param age: int, age of user
        :param name: string, name of user
        :param email: string, email address as login ID
        :param password: string, password
        :return: tuple, the result of query, shape is as below:
                    0 element: ()
                    1 element: ({}, )
                    n elements: ({}, {}, {}, ... , {})

        """
        queryset = User.objects

        try:
            if age is not None:
                queryset = queryset.filter(age=age)
            if name is not None:
                queryset = queryset.filter(name=name)
            if email is not None:
                queryset = queryset.filter(email=email)
            if password is not None:
                queryset = queryset.filter(password=password)

            return tuple(queryset.values())
        except Exception as ex:
            print("Exception!:", ex)
            return ()  # returning an empty tuple if none of the above apply

    def update_user(self, age=None, name=None, email=None, password=None):
        """
        method to retrieve specific user data
        :param age: int, age of user
        :param name: string, name of user
        :param email: string, email address as login ID
        :param password: string, password
        :return: bool, the result of updating data in the table. If the data is updated well, True is returned.
        """
        if age is not None:
            self.age = age
        if name is not None:
            self.name = name
        if email is not None:
            self.email = email
        if password is not None:
            self.password = password

        try:
            self.save()  # execute query
            return True
        except Exception as ex:
            print("Exception!:", ex)
            return False

    def delete_user(self):
        """
        method to delete 1 user data
        :return: bool, the result of deleting data in the table. If the data is deleted well, True is returned.
        """
        try:
            self.delete()  # execute query
            self.person.delete_person()  # delete super class
            return True
        except Exception as ex:
            print("Exception!:", ex)
            return False
