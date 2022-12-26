import pandas as pd

def analyseParkrunReport(csvFile):
    df = pd.read_csv(csvFile)
    df["Date"] = pd.to_datetime(df["Date"],format='%d/%m/%Y')
    df["TimeInSec"] = pd.to_timedelta(df["Time"])
    #print(df.head)
    #print(df.dtypes)

    df.sort_values(by='Date',ascending = True,inplace=True)

    dfTime = df.sort_values(by='Time',ascending = True)
    print('Top 10 quickest times:\n',dfTime.head(10),'\n')

    print('Top 10 performers:\n',dfTime.drop_duplicates(subset = "Name").head(10),'\n')
    print('─' * 25)

    firstPosition = df.query('Position == 1')
    print('First position:\n',firstPosition,'\n')

    firstGenderPosition = df.query('GenderPosition == 1')
    print('First gender position:\n',firstGenderPosition,'\n')
    print('─' * 25)

    # TODO: Minimum no. of events 
    lowestAveragePosition = df.groupby(['Name'])['Position'].mean().nsmallest(10)
    print('Lowest average position:\n',lowestAveragePosition,'\n')

    # TODO: Minimum no. of events 
    lowestAverageTime = df.groupby(['Name'])['TimeInSec'].mean(numeric_only=False).nsmallest(10)
    print('Lowest average time:\n',lowestAverageTime,'\n')
    
    print('─' * 25)

    mostParkruns=df.groupby('Name')['Parkrun'].count().nlargest(10)
    print("Most parkruns:\n",mostParkruns,'\n')

    mostLocations=df.groupby(['Name'])['Parkrun'].nunique().sort_values(ascending=False)
    print("Most unique locations:\n",mostLocations.head(10),'\n')
    
    mostSingleEvent=df.groupby(['Name','Parkrun'])['Name'].count().nlargest(10)
    print("Most events at a single parkrun location:\n",mostSingleEvent,'\n')
    print('─' * 25)

    mostPopularLocations=df.groupby(['Parkrun'])['Parkrun'].count().nlargest(10)
    print("Most popular parkrun locations:\n",mostPopularLocations,'\n')

    mostAtPeel = df.query("Parkrun == 'Peel parkrun'").groupby(['Name'])['Name'].count().nlargest(10)
    print("Most runs at Peel parkrun:\n",mostAtPeel,'\n')

    uniqueLocations=df.groupby(['Parkrun'])['Parkrun'].count()
    print("Total unique parkrun locations: ",uniqueLocations.count())

    print("Unique parkrun locations (only 1 visitor):\n",uniqueLocations.where(lambda x:x==1).dropna(),'\n')
    print('─' * 25)

    mostPopularDay=df.groupby(['Date'])['Parkrun'].count().nlargest(5)
    print("Most popular parkrun days:\n",mostPopularDay,'\n')

    return

analyseParkrunReport('parkrunData2022_21485.csv')