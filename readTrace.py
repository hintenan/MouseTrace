import csv
import numpy as np

get = np.loadtxt(open("./output.csv","rb"), delimiter=",", skiprows=0)
distance = get[:, 0]
print(np.diff(distance))
