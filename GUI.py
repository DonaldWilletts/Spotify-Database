from os import set_inheritable
import tkinter as tk
from tkinter.constants import ANCHOR, BOTH, END, RIGHT, VERTICAL
from typing import Text
#pip install Pillow
from PIL import ImageTk, Image
#importing our backend
import CS4440_SQL_backEnd

#TODO: ADD Spotify logo at top -DONE 
#TODO: Resize Logo -DONE 
#TODO: Create widget's that demonstrate basic needs in python -DONE 
#TODO: Choose: 
#
#             1.   Decade (give many different queries for that specific decade:
#                  number of explicit songs, most popular songs, what characteristics 
#                  were most popular during this time?, average song length.)
#            2.    Choose: Characteristic -> give information about characteristic based on all data. 
#                  (graph chart on years when danacability was most popular, average song length)  
#
#TODO: Figure out how to display graph data in python based on queries from above ^
#TODO: Demontrate how to use another file in python
#TODO(optional): Have that file show how to SQL


#Using a global varible here to keep track and set varibles outside of functions.
class Globals:
    decadeYearVar = 0000 
    userSelectionVar = "" #this is a string, not an int
    selectedYear = 0000

    

class Application(tk.Frame):

    def __init__(self, master = None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.packWidgets()

    def packWidgets(self):

        ######## LOGO FRAME ########
        topFrame = tk.Frame(self)
        topFrame.pack()
        self.createLogo(topFrame).pack()
        #this is a var!
        self.welcomeLabelVar = self.welcomeLabel(topFrame)
        self.welcomeLabelVar.pack()
        self.howToUseLabel(topFrame).pack()
        
        ######## DECADE FRAME ########
        decadeFrame = tk.Frame(self)
        decadeFrame.pack()
        self.decadeLabel(decadeFrame).pack(side = 'left')
        self.chooseYearOptionMenu(decadeFrame).pack(side = 'left')
        self.decadeButtonToDisplayGraph(decadeFrame).pack(side = 'left')
        self.spacerLabel(decadeFrame).pack(side='bottom')

        ####### TEXTBOX SELECTON FRAME ######
        textBoxSelectionFrame = tk.Frame(self)
        textBoxSelectionFrame.pack()
        self.textBeforeSelectionLabel(textBoxSelectionFrame).pack(side = 'left')
        self.chooseTextBoxDropDownMenu(textBoxSelectionFrame).pack(side = 'left')
        #self.choosePopularYearOptionMenu(textBoxSelectionFrame).pack(side = 'left')
        self.chooseYearDropDownMenu(textBoxSelectionFrame).pack(side = 'left')#reuses the original popular year dropdown menu, just name better
        self.selectionLabelButton(textBoxSelectionFrame).pack(side = 'left')

        ### GRAPH DISPLAY FRAME#####
        graphDisplayFrame = tk.Frame(self)
        graphDisplayFrame.pack()

        #self.graphLabelDisplayer is a varible!!
        #need this to be a varible so we can use .configure on it 
        #reference updateDisplayGraph!
        self.graphLabelDisplayer = self.displayGraphLabel(graphDisplayFrame)
        self.graphLabelDisplayer.pack(side='bottom')

        ######Textbox Frame ########
        textBoxFrame = tk.Frame(self)
        textBoxFrame.pack()
        self.textBoxForDisplayVar = self.labelForDisplayingText(textBoxFrame)
        self.textBoxForDisplayVar.pack(side='bottom')

        #### QUIT BUTTON FRAME #####
        quitButtonFrame = tk.Frame(self)
        quitButtonFrame.pack()
        self.quitButton(quitButtonFrame).pack(side='bottom')

        return

    ######################### LOGO Frame Funcitons #########################

    def createLogo(self, frame_location):
        #Citation of .png: https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.stickpng.com%2Fimg%2Ficons-logos-emojis%2Ftech-companies%2Fspotify-green-logo&psig=AOvVaw1cglp9OZhTn9XdPAXmEewi&ust=1618914698909000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCOjUx_2NivACFQAAAAAdAAAAABAD
        loadImage = Image.open("SpotifyLogo")
        #Need to resize image to fit screen (keep in 20x,6x format to keep orginal shape)
        loadImage = loadImage.resize((200,60))
        renderImage = ImageTk.PhotoImage(loadImage)
        #Inserting logo as a label
        img = tk.Label(frame_location, image = renderImage)
        img.image = renderImage
        return(img)

    def welcomeLabel(self, frame_location):
        myText = "\nWelcome to our project!\n\nThis tool gathers data from Spotify to show changes in musical trends over time. \n"
        returnLabel = tk.Label(
            frame_location,
            text = myText,
            width=100,
            font = (("Courier", 16))
            #height=10
        )
        return(returnLabel)

    def howToUseLabel(self, frame_location):
        myText = "Get more information by selecting a drop down:"
        returnLabel = tk.Label(
            frame_location,
            text = myText,
            width=100,
            font = " Helvetica 14 underline"
        )
        return (returnLabel)

    def deleteWelcomeLabel(self):
        if self.welcomeLabelVar:
            self.welcomeLabelVar.destroy()

    def spacerLabel(self, frame_location):
        myText = " "
        returnLabel = tk.Label(
            frame_location,
            text = myText
        )
        return(returnLabel)

    ######################### DECADE Funcitons #########################

    #label before decade option
    def decadeLabel(self, frame_location):
        myText = "Query all data for a Decade:"
        returnLabel = tk.Label(
            frame_location, 
            text = myText
        )
        return(returnLabel)

    #gets the decade the user selected from the decade dropdown menu.
    def chooseYearOptionMenu(self, frame_location):
        optionYearsArray = Application.populateOptionYearsArray()

        Globals.decadeYearVar = tk.StringVar(frame_location)

        returnwidget = tk.OptionMenu(
            frame_location, 
            Globals.decadeYearVar, 
            *optionYearsArray
            )

        return(returnwidget)

    #helper function to create option years array 
    def populateOptionYearsArray():
        optionYears = []

        #dataset starting year 1980
        year = 1920 

        while( year <= 2021):
            optionYears.append(str(year))
            year = year + 10

        #adding All-time option at the end 
        optionYears.append('All-time')

        return(optionYears)

    #funciton that sends opiton picked from optionMenu -> middleman function 
    def decadeButtonToDisplayGraph(self, frame_locaiton):
        returnButton = tk.Button(
            frame_locaiton,
            text = "Submit",
            command = lambda: self.decadeMiddleManfunctionThatSendsToBackEnd(frame_locaiton, Globals.decadeYearVar) #sending Global Var
            )

        return(returnButton)

    #keeping frame location here so we can pass diffent frame to our display functinon. 
    def decadeMiddleManfunctionThatSendsToBackEnd(self, frame_location, varToSend):
        #saving varable here to send to our display funciton 
        pngToSend = CS4440_SQL_backEnd.test.createDecadeGraphics(varToSend)
        
        #sending our saved png to our display function. 
        self.updateDisplayGraphLabel(frame_location, pngToSend)

    def updateDisplayGraphLabel(self, frame_locaiton, sentPNG):
        self.textBoxForDisplayVar.configure(text = '', height = 0, width = 0, relief = "flat") #, background = 'clear') #hides text box
        #self.welcomeLabelVar.configure(text = '', height = 0, width = 0) #Removing welcome label!
        #self.deleteWelcomeLabel()

        #passed in plot.png from our backend need to open and display it 
        loadImage = Image.open(sentPNG)
        loadImage = loadImage.resize((900,600)) # 900, 600 changing size of our image here orginally (1200x800) needs to maintatin 3:2 width:height ratio
        renderImage = ImageTk.PhotoImage(loadImage)

        #using .configure to change what .png is being displayed
        self.graphLabelDisplayer.configure(image = renderImage)
        self.graphLabelDisplayer.image = renderImage

    ######################### TextBox Selection Frame #########################
    def textBeforeSelectionLabel(self, frame_location):
        myText = "Query for a Specific Year:"
        returnLabel = tk.Label(
            frame_location, 
            text = myText
        )
        return(returnLabel)

    def chooseTextBoxDropDownMenu(self, frame_location):
        fooArray = ["10 most popular songs", "Average song duration", "Explicit song information", "Number of artists", "Shortest and Longest song"]
        Globals.userSelectionVar = tk.StringVar(frame_location)

        returnOptionMenu = tk.OptionMenu(
            frame_location,
            Globals.userSelectionVar,
            *fooArray
        )

        return(returnOptionMenu)
    
    def chooseYearDropDownMenu(self, frame_location):
        optionYearsArray = Application.populateOptionYearsPopularArray()
        Globals.selectedYear = tk.StringVar(frame_location)

        returnwidget = tk.OptionMenu(
            frame_location, 
            Globals.selectedYear, 
            *optionYearsArray
            )

        return(returnwidget)

    def selectionLabelButton(self, frame_location):
        returnButton = tk.Button(
            frame_location,
            text = "Submit",
            command = lambda: self.selectionLabelMiddleMan(frame_location, Globals.userSelectionVar, Globals.selectedYear ) # the year dropdown resues popular year implementation
            )                                                                                                               #the year is not being passed correctly to the selectionMiddleMan

        return(returnButton)

    def selectionLabelMiddleMan(self, frame_location, userChoice, userChoiceYear):
        #successfully called by selectinLabelButton
        #print(userChoiceYear.get())#does not print correctly. Its null it appears
        
        if (userChoice.get() == "10 most popular songs"):#successfully enters if loop. Not passing year correctly though
            #print("makes it here")#not getting to this piont
            txtToSend = CS4440_SQL_backEnd.test.popularYearQuery(userChoiceYear)
            self.changeTextBoxText(frame_location, txtToSend)

        elif (userChoice.get() == "Average song duration"):
            returnedStr = CS4440_SQL_backEnd.test.getAvgSongDuration(userChoiceYear.get(), userChoiceYear.get())
            #re-format text to display pretty  
            txtToSend = f"Average song duration in "+ str(userChoiceYear.get()) + ": \n" + str(returnedStr) +" minutes"
            self.changeTextBoxText(frame_location, txtToSend)

        elif (userChoice.get() == "Explicit song information"):
            returnTuple = CS4440_SQL_backEnd.test.getPercentageExplicitAndSongCount(userChoiceYear.get(), userChoiceYear.get())
            #reformat Tuple is (percentage, totalSongs)
            txtToSend = f"Total number of explicit songs in " + str(userChoiceYear.get()) + ": \n" + str(returnTuple[1]) + "\n \n Percentage of explicit songs in "+str(userChoiceYear.get()) + ": \n"+str(int(returnTuple[0]))+"%"
            self.changeTextBoxText(frame_location, txtToSend)

        elif (userChoice.get() == "Number of artists"):
            returnedStr = CS4440_SQL_backEnd.test.getNumberOfArtists(userChoiceYear.get(), userChoiceYear.get())
            #reformat
            txtToSend = f"Total number of artists from " + str(userChoiceYear.get()) + ": \n" + str(returnedStr)
            self.changeTextBoxText(frame_location, txtToSend)

        elif (userChoice.get() == "Shortest and Longest song"):
            #Tuple (longestSong, shortestSong)
            LengthOfSongsTuple = CS4440_SQL_backEnd.test.getShortestAndLongest(userChoiceYear.get(), userChoiceYear.get())
            #Tuple (longestTitle, shortestTitle)
            TitleOfSongsTuple = CS4440_SQL_backEnd.test.titlesOfShortestAndLongestSongs(userChoiceYear.get(), userChoiceYear.get())

            #reformat
            txtToSend = f"The longest song in "+ str(userChoiceYear.get())+ ": \n\""+str(TitleOfSongsTuple[0])+ "\" with a time of "+ str(LengthOfSongsTuple[0]) + " minutes. \n \n The shortest song in " + str(userChoiceYear.get()) + ": \n \""  + str(TitleOfSongsTuple[1])+ "\" with a time of "+ str(LengthOfSongsTuple[1]) + " minutes."

            self.changeTextBoxText(frame_location, txtToSend)
        
        else: print("this")


    ######################### Popular Songs by year Functions #########################

    #label before decade option
    def popularLabel(self, frame_location):
        myText = "Choose a year to get the 10 most popular songs:"
        returnLabel = tk.Label(
            frame_location, 
            text = myText
            #foreground = "red"
        )
        return(returnLabel)

    def choosePopularYearOptionMenu(self, frame_location):
        optionYearsArray = Application.populateOptionYearsPopularArray()
        Globals.selectedYear = tk.StringVar(frame_location)

        returnwidget = tk.OptionMenu(
            frame_location, 
            Globals.selectedYear, 
            *optionYearsArray
            )

        return(returnwidget)

    def populateOptionYearsPopularArray():
        optionYears = []
        #dataset starting year 1980
        year = 1920 

        while( year <= 2021):
            optionYears.append(str(year))
            year = year + 1

        return(optionYears)

    #function that grabs graph from backend after submit button his clicked by the user for the decade.
    def popularYearButtonToDisplayGraph(self, frame_locaiton):
        returnButton = tk.Button(
            frame_locaiton,
            text = "Submit",
            command = lambda: self.popularYearMiddleMan(frame_locaiton, Globals.selectedYear)
            )

        return(returnButton)

    def popularYearMiddleMan(self, frame_location, varToSend):
        txtToSend = CS4440_SQL_backEnd.test.popularYearQuery(varToSend)
        self.changeTextBoxText(frame_location, txtToSend)


    ######################### Graph Display Functions #########################

    def displayGraphLabel(self, frame_locaiton):
        img = tk.Label(frame_locaiton) 
        return(img)

    ######################### Text Box Functions #########################
    
    #height = 15, width = 75. #starting at 0 to hide text box
    def labelForDisplayingText(self, frame_locaiton): 
        returnLabel = tk.Label(
            frame_locaiton,
            height = 0,
            width = 0, 
            wraplength = 1000
        )
        return (returnLabel)

    #Clears and replaces textbox in the top 10 songs text box also clears graph 
    def changeTextBoxText(self, frame_location, sentTxt):
        self.graphLabelDisplayer.configure(image = '') #Allison wants this to be deleted. I think it makes our GUI cleaner lmk - DW
        
        self.textBoxForDisplayVar.configure(text = sentTxt, height = 15, width = 75, foreground = "red", borderwidth = 2, relief = "groove", )   
        

    ######################### Quit Buttion Functions #########################

    def quitButton(self, frame_location):
        quit = tk.Button(frame_location, text="QUIT", fg="red", command=self.master.destroy)
        return(quit)
        
if __name__ == "__main__":

    root = tk.Tk()
    
    #create the application
    app = Application(master=root)

    #add title & figure set predetermined size
    app.master.title("CS:4440 Database Project")
    app.master.geometry("2000x1600")

    #start the program
    app.mainloop()

