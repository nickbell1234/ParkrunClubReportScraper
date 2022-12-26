import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

def plotGraphs(csvFile):
    df = pd.read_csv(csvFile)
    df["Date"] = pd.to_datetime(df["Date"],format='%d/%m/%Y')
    df["TimeInMins"] = pd.to_timedelta(df["Time"]).astype('timedelta64[s]')/60

    print(df.head)
    print(df.dtypes)

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

    bins=range(14,52,1)
    plt.hist(df['TimeInMins'],bins=bins,edgecolor='black')
    plt.xticks(range(10,65,5))
    plt.xlabel('Time (mins)')
    plt.ylabel('Number of runners')
    plt.title('Histogram of 2022 finish times')
    plt.show()

    individual = df.query("Name == 'Nicholas BELL'")
    individual.plot.line(x='Date',y='TimeInMins',marker='x',linestyle='dashed')

    plt.yticks(range(14,32,2))  
    plt.xlabel('Date')
    plt.ylabel('Time (mins)')
    plt.title('Individual finish times')
    plt.show()

    return

plotGraphs('parkrunData2022_21485.csv')