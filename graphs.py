import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

def plotGraphs(csvFile):
    df = pd.read_csv(csvFile)
    df["Date"] = pd.to_datetime(df["Date"],format='%d/%m/%Y')
    df["TimeInSec"] = pd.to_timedelta(df["Time"])
    #print(df.head)
    #print(df.dtypes)

    df.sort_values(by='Date',ascending = True,inplace=True)
    mostParkruns=df.groupby('Name')['Parkrun'].count().nlargest(10)
    print("Most parkruns:\n",mostParkruns,'\n')

    matplotlib.style.use('fivethirtyeight') 

    mostParkruns.plot.bar(x='Name', y='Parkruns', rot=0)
    plt.xlabel('Name')
    plt.ylabel('Parkruns')
    plt.title('Most parkruns by a runner in 2022')
    plt.show()

    mostPopularLocations=df.groupby(['Parkrun'])['Parkrun'].count().nlargest(10)
    print("Most popular parkrun locations:\n",mostPopularLocations,'\n')

    mostPopularLocations.plot.bar(x='Parkrun', y='Number of finishers', rot=0)
    plt.xlabel('Event')
    plt.ylabel('Number of MRR finishers')
    plt.title('Most popular parkrun locations in 2022')
    plt.show()


    return

plotGraphs('parkrunData2022_21485.csv')