temperatures = []

"""
temperatures = temperatures + [40,60,80]

for i in range(100,195,5): #Note last value is not included
    temperatures = temperatures + [i]

for i in range(180,105,-5): #Note last value is not included
    temperatures = temperatures + [i]

print len(temperatures)
"""

for i in range(100,185,5): #Note last value is not included
    temperatures = temperatures + [i]

temperatures = temperatures + [190]

for i in range(180,95,-5): #Note last value is not included
    temperatures = temperatures + [i]

initial_db = 189+38

masses = []
#masses.append(['H2',4.387,8])
masses.append(['OH',12.418,6])
masses.append(['NH3',12.427,6])
masses.append(['H2O',12.777,8])
masses.append(['N2',15.89,8])
masses.append(['O2',16.972,8])
#masses.append(['N2O',19.874,10])

