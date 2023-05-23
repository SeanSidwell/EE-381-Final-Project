import math
import numpy as np
import matplotlib.pyplot as plt
import csv

# load text file  (list year, sale price) (homes)
fname = 'Sales_01_20.csv'  # comma separated values
data1 = np.loadtxt(fname, delimiter=',', skiprows=1)  # skip first row

years = []
prices = []

with open(fname) as f:
    reader = csv.reader(f)
    count = 0
    for row in reader:
        if count == 0:
            print(row[0], row[1])
        else:
            years.append(float(row[0]))
            prices.append(float(row[1]))
        count = count + 1

print(years)
print(prices)

a = np.array(years)
b = np.array(prices)
table = np.column_stack((a, b))

sortedTable = table[table[:, 0].argsort()]
# sortedTable = np.sort(table, 0)
# twiceSortedTable = np.sort(sortedTable, 1)
# sortedTable = np.sort(table, axis=1, kind='stable')
# axis 0 --> year
# axis 1 --> price

# fixedTable = np.float32(sortedTable)
listOfYears = np.split(sortedTable, np.cumsum(np.unique(sortedTable[:, 0], return_counts=True)[1])[:-1])

# list of years creates a list of arrays
# 00=2001
# 01=2002
# ...

# i is an ndarray of a year
# j is a tuple of indiviual table entry ex: 2001, 50000


# sum of prices for each year in order
sums = []
numSalesEachYear = []
for i in listOfYears:
    s = 0
    count = 0
    for j in i:
        s = s + j[1]
        count += 1
    sums.append(s)
    numSalesEachYear.append(count)

means = []

for i in range(len(sums)):
    means.append(sums[i] / numSalesEachYear[i])

# find standard deviation = sqrt( sum((xi-mean)^2)/n )

toBeSummed = []
varianceByYear = []
standardDeviationByYear = []
probabilityByYear = []

for i in listOfYears:
    yearCount = 0
    numBetween200And300k = 0
    for j in i:
        # step 1: find xi-mean
        xiMinusXbar = j[1] - means[yearCount]
        toBeSummed.append(pow(xiMinusXbar, 2))
        # counter for probability
        if (j[1] >= 200000) and (j[1] <= 300000):
            numBetween200And300k += 1
    numerator = np.sum(toBeSummed)
    variance = numerator / (numSalesEachYear[yearCount] - 1)
    varianceByYear.append(variance)
    standardDeviation = math.sqrt(variance)
    standardDeviationByYear.append(standardDeviation)
    probability = numBetween200And300k / numSalesEachYear[yearCount]
    probabilityByYear.append(probability)
    toBeSummed.clear()
    yearCount += 1

# if sale price is between 200k and 300k
# count it
# counted houses / total houses
# do that for each year to get probability


years = [2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018,
         2019, 2020]

# stackedYearsAverages is axis0 year axis1 values
stackedYearsAverages = np.column_stack((years, means))
stackedYearsStdDevs = np.column_stack((years, standardDeviationByYear))
stackedYearsProbabilities = np.column_stack((years, probabilityByYear))

positions = range(len(means))

plt.bar(positions, means)

plt.xticks(positions, years)

plt.title('Mean House Price by Year')
plt.xlabel('Year')
plt.ylabel('Mean House Price')

plt.show()

positions = range(len(standardDeviationByYear))
plt.bar(positions, standardDeviationByYear)
plt.xticks(positions, years)
plt.title('Standard Deviation of House Price by Year')
plt.xlabel('Year')
plt.ylabel('STD in Millions')
plt.show()


positions = range(len(probabilityByYear))
plt.bar(positions, probabilityByYear)
plt.xticks(positions, years)
plt.title('Probability of House Price between 20k-30k Dollars by Year')
plt.xlabel('Year')
plt.ylabel('Probability')
plt.show()

#
# # print (data1)
# fig, ax = plt.subplots(1, 2)  # Create a figure containing a single axes
# ax[0].hist(stackedYearsAverages, ec='black')
# ax[0].set_title("Equal width bins")
#
# ax[1].hist(data3, ec='black', bins='auto')
# ax[1].set_title("Unequal width")
#
# ax[0].set_xlabel('Bond strength')
# ax[1].set_xlabel('Bond strength')
# ax[0].set_ylabel('chikn')
# plt.show()
