import tkinter as tk

def executeSubmit():
    print("you submitted")

OptionListDecade = [
    "No Selection",
    "1920",
    "1930",
    "1940",
    "1950",
    "1960", 
    "1970",
    "1980", 
    "1990", 
    "2000",
    "2010",
    "2020",
]

OptionListCharacteristic = [
    "No Selectin",
    "Dancibiliity",
    "Duration",
    "Energy",
    "Instrumental",
    "Key",
    "Liveliness",
    "Mode",
    "Popularity",
    "Speechiness",
    "Tempo",
    "Valence",
]


app = tk.Tk()

labelDecade = tk.Label(app, text = "Choose Decade")
labelDecade.config(font = ('Helvetica', 16))

labelChar = tk.Label(app, text = "Choose Characteristic")
labelChar.config(font = ('Helvetica', 16))

app.geometry('750x750')

variableDecade = tk.StringVar(app)
variableDecade.set(OptionListDecade[0])

variableChar = tk.StringVar(app)
variableChar.set(OptionListCharacteristic[0])
labelDecade.pack()
optDecade = tk.OptionMenu(app, variableDecade, *OptionListDecade)
optDecade.config(width=90, font=('Helvetica', 12))
optDecade.pack()
labelChar.pack()
optChar = tk.OptionMenu(app, variableChar, *OptionListCharacteristic)
optChar.config(width=90, font=('Helvetica', 12))
optChar.pack()

submitButton = tk.Button(app, text = "Submit", width = 10, command = executeSubmit())
submitButton.pack()


app.mainloop()