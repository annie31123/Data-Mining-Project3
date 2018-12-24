import csv
import sys
from itertools import chain, combinations
from collections import OrderedDict




if __name__ == '__main__':
    data_process = list()  # transcation
    with open('mushrooms.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                
        for idx, row in enumerate(spamreader):   # get transcation list and process the origin data 
            if idx != 0:
                data_process.append(row[0])
    
    for idx, data in enumerate(data_process):
        for idx2, data2 in enumerate(data_process):
            if idx != idx2:
                if data == data2:
                    print(idx, idx2)