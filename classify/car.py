# coding=UTF-8

##
# @brief Car Evaluation Database Handler
# @author webofthink@snu.ac.kr
#

##
# read data from csv file
# @param csv_file CSV file to be loaded
# @return table data
#
def read_csv_data(csv_file):
    import csv
    reader = csv.reader(open(csv_file, 'r'), delimiter=',')
    data = [row for row in reader]
    return data

class Car() :

    def __init__(self, car_data):
        # validate list size
        if len(car_data) == 7 :
            # buying, maint, doors, persons, lug_boot, safety
            self.buying = car_data[0]
            self.maint = car_data[1]
            self.doors = car_data[2]
            self.persons = car_data[3]
            self.lug_boot = car_data[4]
            self.safety = car_data[5]
            self.untitled = car_data[6]
        else :
            print "invalid list input: " + str(car_data)



    def __str__(self):
        info = 'buying price: ' + self.buying + ', price of maintenance: ' + self.maint + \
            '\nnumber of doors: ' + self.doors + ', capacity in terms of persons to carry: ' + \
            self.persons + ', the size of luggage boot: ' + self.lug_boot + \
            ', estimated safety of the car: ' + self.safety
        return info

    def __repr__(self):
        return self.__str__()

    def price(self):
        info = 'buying price: ' + self.buying + ', price of maintenance: ' + self.maint
        return info

    def tech(self):
        info = '\nnumber of doors: ' + self.doors + ', capacity in terms of persons to carry: ' + \
            self.persons + ', the size of luggage boot: ' + self.lug_boot + \
            ', estimated safety of the car: ' + self.safety
        return info
