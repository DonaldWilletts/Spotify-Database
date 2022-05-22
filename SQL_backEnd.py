'''
This is going to be the backend of our project. 
This is were we will load the database into python and run SQL commands on it
Graphs will be created here and sent back to GUI 
'''
import sqlite3 as lite
import matplotlib.pyplot as plt

#Can change plot's default style
plt.style.use('ggplot')

#Setting some default font sizes
plt.rc('xtick', labelsize=12)    # fontsize of the tick labels
plt.rc('ytick', labelsize=12)    # fontsize of the tick labels
plt.rc('axes', labelsize=12)    # fontsize of the x and y labels

class test():
    #Build and return a png displaying decade graph statistics
    def createDecadeGraphics(Var):
        #Flag denoting if the 'All-time' option was selected
        allTimeFlag = False #False -> specific decade is chosen, True -> All-time option was chosen

        begin = Var.get()

        #Check for default begin or 'All-time' value
        if (begin == ''):
            begin = '1920'
        elif (begin == 'All-time'):
            begin = '1920'
            end = '2021'
            allTimeFlag = True

        #A decade was given - set the end year based on the begin value
        if (allTimeFlag == False):
            end = begin[:3] + '9'

        #Setup plot grid
        fig = plt.figure(figsize=(14.25,9.5))#constrained_layout=True, figsize=(9,6)
        gs = fig.add_gridspec(nrows=2, ncols=3)
        topFig = fig.add_subplot(gs[0, :])    #Top half for displaying characteristic line plot
        botRight = fig.add_subplot(gs[1, 2])  #Bottom right block for pie chart
        botMid = fig.add_subplot(gs[1, 1])    #Bottom middle block for bar chart
        botLeft = fig.add_subplot(gs[1, 0])   #Bottom left block for other statistics

        #Calling functions to populate the empty plot grid made above with actual graphics
        test.createCharacteristicLinePlot(topFig, begin, end, allTimeFlag)
        test.createCharacteristicPiePlot(botRight, begin, end)
        test.createKeyBarPlot(botMid, begin, end)
        test.createTextPlot(botLeft, begin, end, allTimeFlag)

        #Save final plot as a png for displaying on frontend
        fig.tight_layout()
        fig.savefig('plot.png', dpi=100)
        fig.clf()

        return ('plot.png')

    #Build line graph for characteristics as they change over a decade
    def createCharacteristicLinePlot(plot, begin, end, allTimeFlag):
        #Labels to identify each line on the graph
        characteristicLabels = ['Acousticness', 'Danceability', 'Energy', 'Instrumentalness', 'Liveness', 'Speechiness', 'Valence']

        #Populate the tick labels for the x-axis
        characteristicXTicks = [] #Store years in the decade to label the x-axis with
        if (allTimeFlag):
            for i in range(int(begin), int(end), 10): #If allTime, use 10 year increments for ticks
                characteristicXTicks.append(i)
        else:
            for i in range(int(begin), int(begin) + 10): #Else use 1 year increments for ticks
                characteristicXTicks.append(i)

        #Create array of data for each of the characteristic lines to be plotted
        characteristicLines = []
        for characteristic in characteristicLabels:
            coords = test.characteristicLinePlotData(characteristic, begin, end)
            line, = plot.plot(coords[0], coords[1])
            characteristicLines.append(line)

        #Plot the lines on the graph
        plot.legend(characteristicLines, characteristicLabels, prop={'size' : 12})
        plot.set_xticks(characteristicXTicks)
        plot.grid('on')
        #Set the graph title - different depending on the allTimeFlag
        if (allTimeFlag):
            plot.set_title(f'Changes in Song Characteristics from 1920 to 2021', bbox ={'facecolor':'tab:blue', 'alpha':0.6, 'pad':0.6, 'boxstyle':'square'})
        else:
            plot.set_title(f'Changes in Song Characteristics During the {begin}s', bbox ={'facecolor':'tab:blue', 'alpha':0.6, 'pad':0.6, 'boxstyle':'square'})

        return

    #Calculate the plotting points for a characteristic line
    def characteristicLinePlotData(characteristic, begin, end):
        #Connect to the database
        db = lite.connect('SpotifyDB.db')
        cur = db.cursor()

        #Query to gather the X & Y datapoints for a line from the database
        characteristicChangeQuery = (f"""SELECT songs.year, ROUND(AVG({characteristic} * popularity), 4) FROM characteristics JOIN songs ON 
                    songs.characteristic_id = characteristics.characteristic_id WHERE songs.year >= {begin} AND songs.year <= {end} 
                    GROUP BY songs.year""")

        #Arrays to store X & Y datapoints
        xCoord = []
        yCoord = []

        #Execute and extract data from query
        for row in cur.execute(characteristicChangeQuery):
            xCoord.append(row[0]) #x-coord from row tuple (year)
            yCoord.append(row[1]) #y-coord from row tuple (characteristic popularity)

        #Close database connection
        db.close()

        return [xCoord, yCoord]
        
    #Build pie chart for song characteristics weighted by popularity    
    def createCharacteristicPiePlot(plot, begin, end):
        #Connect to the database
        db = lite.connect('SpotifyDB.db')
        cur = db.cursor()

        #Create characteristic pie chart
        characteristicValues = [] #Store query output for manipulation
        characteristicPercentages = [] #Input for pie chart values

        #Input for pie chart labels
        characteristicLabels = ['Acousticness', 'Danceability', 'Energy', 'Instrumentalness', 'Liveness', 'Speechiness', 'Valence']

        #Query to get relative characteristic popularity from database
        characteristicQuery = (f"""SELECT AVG(acousticness * popularity), AVG(danceability * popularity), AVG(energy * popularity), 
            AVG(instrumentalness * popularity), AVG(liveness * popularity), AVG(speechiness * popularity), AVG(valence * popularity) 
            FROM characteristics JOIN songs ON songs.characteristic_id = characteristics.characteristic_id WHERE songs.year >= {begin} 
            AND songs.year <= {end}""")

        #Run SQLite query and store results
        for row in cur.execute(characteristicQuery):
            characteristicValues.append(row[0])
            characteristicValues.append(row[1])
            characteristicValues.append(row[2])
            characteristicValues.append(row[3])
            characteristicValues.append(row[4])
            characteristicValues.append(row[5])
            characteristicValues.append(row[6])
            
        #Sum of all characteristic values for weighing them out of 100 for pie chart    
        characteristicTotal = sum(characteristicValues)

        #Calculate and store weighted characteristic values for pie chart
        for num in characteristicValues:
            characteristicPercentages.append(round(((num / characteristicTotal) * 100), 0))

        #Create the pie chart
        plot.pie(characteristicPercentages, labels=characteristicLabels, shadow=True, startangle=90,
                        autopct='%1.0f%%', pctdistance=0.8, labeldistance=1.1)
        plot.axis('equal')
        plot.set_title('Characteristics by Popularity', bbox ={'facecolor':'orange', 'alpha':0.6, 'pad':0.4, 'boxstyle':'square'}) #plot.set_title('Characteristics by Popularity', **tfont) <- for set font

        #Close database connection
        db.close()

        return

    #Build bar plot for song key popularity
    def createKeyBarPlot(plot, begin, end):
        #Connect to the database
        db = lite.connect('SpotifyDB.db')
        cur = db.cursor()

        #Query for key popularity
        keyQuery = (f"""SELECT COUNT(key) AS keys FROM characteristics JOIN songs ON 
                    songs.characteristic_id = characteristics.characteristic_id WHERE songs.year >= {begin} 
                    AND songs.year <= {end} GROUP BY key""")

        keyLabels = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

        #Execute and extract data from query
        keyValues = []
        for row in cur.execute(keyQuery):
            keyValues.append(row[0])

        #Create the bar chart
        plot.bar(keyLabels, keyValues)
        plot.set_title("Songs by Key")
        plot.set_xlabel('Key')
        plot.set_ylabel('# of Songs')

        #Close database connection
        db.close()

        return

    
    #Build text plot containing additional statistics about decade
    def createTextPlot(plot, begin, end, allTimeFlag):
        #Hide gridlines
        plot.grid(False)

        #Hide axes ticks
        plot.set_xticks([])
        plot.set_yticks([])

        #Get data to display
        avgDuration = test.getAvgSongDuration(begin, end)
        longestAndShortestTuple = test.getShortestAndLongest(begin, end)
        explicitAndCountTuple = test.getPercentageExplicitAndSongCount(begin, end)
        numberOfArtists = test.getNumberOfArtists(begin, end)

        #Set plot title - varies depending on allTimeFlag value
        if (allTimeFlag):
            plot.text(0.05, 0.975, f'Other Statistics', fontsize = 15, bbox ={'facecolor':'red', 'alpha':0.6, 'pad':0.6, 'boxstyle':'round4'})
        else:
            plot.text(0.05, 0.975, f'Other {begin}s Statistics', fontsize = 15, bbox ={'facecolor':'red', 'alpha':0.6, 'pad':0.6, 'boxstyle':'round4'})

        #Plot each statistic on it's own line
        plot.text(0.05, 0.85, (f"Total # of songs = {explicitAndCountTuple[1]}"), fontsize = 12)
        plot.text(0.05, 0.7, (f"Percentage of explicit songs = {explicitAndCountTuple[0]}%"), fontsize = 12)
        plot.text(0.05, 0.55, (f"Total # of artists = {numberOfArtists}"), fontsize = 12)
        plot.text(0.05, 0.4, (f"Average song length = {avgDuration} minutes"), fontsize = 12)
        plot.text(0.05, 0.25, (f"Longest song length = {longestAndShortestTuple[0]} minutes"), fontsize = 12)
        plot.text(0.05, 0.1, (f"Shortest song length = {longestAndShortestTuple[1]} minutes"), fontsize = 12)

        return

    #Query and return a string containing the average song length in minutes for a given period of time
    def getAvgSongDuration(begin, end):
        #Connect to the database
        db = lite.connect('SpotifyDB.db')
        cur = db.cursor()

        avgLengthQuery = (f"""SELECT ROUND(AVG(duration_ms) /1000 / 60.0, 2) AS average_time_in_minutes FROM characteristics JOIN songs ON 
                            songs.characteristic_id = characteristics.characteristic_id WHERE songs.year >= {begin} AND songs.year <= {end}""")

        #Execute and extract data from query
        for row in cur.execute(avgLengthQuery):
            averageLength = row[0]

        #Close database connection
        db.close()
        
        return (averageLength)

    #Query and return a tuple of strings -> (explicitPercentage, totalSongs) for a given period of time
    def getPercentageExplicitAndSongCount(begin, end):
        #Connect to database
        db = lite.connect('SpotifyDB.db')
        cur = db.cursor()

        #Calculate total number of explicit songs
        for row in cur.execute('SELECT COUNT(*) FROM songs WHERE explicit = 1 AND songs.year >= ' + begin + ' AND songs.year <= ' + end):
            numExplicit = row[0]

        #Calculate total number of songs
        for row in cur.execute('SELECT COUNT(*) FROM songs WHERE songs.year >= ' + begin + ' AND songs.year <= ' + end):
            totalSongs = row[0]

        #Calculate weighted values for pie chart
        explicitPercentage = round(((numExplicit / totalSongs) * 100), 0)

        #Close database connection
        db.close()

        #return returnStr
        return (str(int(explicitPercentage)), str(totalSongs))

    #Query and return a string of the total number of artists for a given period of time
    def getNumberOfArtists(begin, end):
        #Connect to the database
        db = lite.connect('SpotifyDB.db')
        cur = db.cursor()

        #Calculate total number of artists
        for row in cur.execute(f"""SELECT COUNT(*) FROM songs JOIN artists ON artists.artist_id = songs.artist_id WHERE songs.year >= {begin} AND songs.year <= {end}"""):
            numArtists = row[0]

        #Close database connection
        db.close()
        
        #return (returnStr)
        return str(numArtists)

    #Returns the names of the songs with the longest and shortest duration
    def titlesOfShortestAndLongestSongs(begin, end):
        #Connect to database
        db = lite.connect('SpotifyDB.db')
        cur = db.cursor()

        songTitleQueryMaxDuration = (f"""SELECT songs.name AS song_title, MAX(characteristics.duration_ms) AS longest FROM songs JOIN characteristics ON characteristics.characteristic_id = songs.characteristic_id WHERE songs.year >= {begin} AND songs.year <= {end}""")
    
        songTitleQueryMinDuration = (f"""SELECT songs.name AS song_title, MIN(characteristics.duration_ms) AS shortest FROM songs JOIN characteristics ON characteristics.characteristic_id = songs.characteristic_id WHERE songs.year >= {begin} AND songs.year <= {end}""")

        #Extract title for longest song in given time period
        for row in cur.execute(songTitleQueryMaxDuration):
            longestSongTitle = row[0]
        
        #Extract title for shortest song in given time period
        for row in cur.execute(songTitleQueryMinDuration):
            shortestSongTitle = row[0]

        #Close database connection
        db.close()

        #return(str(str(shortestSongTitle), str(longestSongTitle) ))
        return(str(longestSongTitle), str(shortestSongTitle) )



    #Query and return a tuple of strings -> (longestSong, shortestSong) for a given period of time
    def getShortestAndLongest(begin, end):
        #Connect to the database
        db = lite.connect('SpotifyDB.db')
        cur = db.cursor()

        songLengthQuery = (f"""SELECT ROUND(MAX((duration_ms) /1000 / 60.0), 2) AS longest, ROUND(MIN((duration_ms) /1000 / 60.0), 2) AS shortest FROM characteristics 
                            JOIN songs ON songs.characteristic_id = characteristics.characteristic_id WHERE songs.year >= {begin} AND songs.year <= {end}""")

        #Caclulate shortest and longest Songs
        for row in cur.execute(songLengthQuery):
            longestSong = row[0]
            shortestSong = row[1]

        #Close database connection
        db.close()

        return (str(longestSong), str(shortestSong))

    #Query and return string listing the top 10 songs for a given time period
    def popularYearQuery(var):
        #Connect to the database
        db = lite.connect('SpotifyDB.db')
        cur = db.cursor()

        top10Query = (f"""SELECT name, popularity FROM songs JOIN characteristics ON songs.characteristic_id = characteristics.characteristic_id 
                        WHERE songs.year = {var.get()} ORDER BY popularity  DESC LIMIT 10""")

        #Retrieve top 10 songs from certain time period
        listOfTopSongs = []
        for row in cur.execute(top10Query):
            listOfTopSongs.append(row[0])

        #Format string to return
        str1 = f"Top 10 songs in {var.get()}:\n\n"
        i = 1
        for x in listOfTopSongs:
                str1 += (f"{i}. {x}\n")
                i += 1
        
        #Close database connection
        db.close()

        return str1

        


