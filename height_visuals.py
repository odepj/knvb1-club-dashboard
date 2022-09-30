import pandas as pd
from matplotlib import pyplot as plt

#Read in file
han_data = pd.read_csv('HAN_csv_example.csv')

#Sorting data on ID
han_data.sort_values(by=['id'], inplace=True)

#Scatter plot for height sitting and standing
plt.scatter(han_data.team_naam, han_data['Staande.lengte'], alpha=0.1, color='r')
plt.scatter(han_data.team_naam, han_data['Zittende.lengte'], alpha=0.1, color='g')

plt.title('Lengtes per leeftijdsgroep')
plt.xlabel('Leeftijdsgroep')
plt.ylabel('Lengte in centimeters')

plt.show()