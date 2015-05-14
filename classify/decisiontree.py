# coding=UTF-8

# Unsupervised Classification by Decision Tree with Car+Evaluation data
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
        # buying, maint, doors, persons, lug_boot, safety
        self.buying = car_data[0]
        self.maint = car_data[1]
        self.doors = car_data[2]
        self.persons = car_data[3]
        self.lug_boot = car_data[4]
        self.safety = car_data[5]

    # TODO

def annotate_car_data(car_data) :
    car = Car(car_data)
    return car

car_data_list = read_csv_data('.\\car\\car.data')

for car_data in car_data_list :
    car = annotate_car_data(car_data)
    print car.safety
