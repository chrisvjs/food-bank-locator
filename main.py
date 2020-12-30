import tkinter as tk
from tkinter import ttk
from tkinter import *
import locationfinder
import webbrowser

def background(pic, frame):
    """background() takes the png image file and places it on the active window
    (Universal method for backgrounds)
    """
    # Takes the background image and add its to the frame
    canvas = Canvas(master=frame, width=360, height=640)
    canvas.pack()
    canvas.create_image(0,0, anchor=NW, image=pic)


def optionMenuCountry():
    """optionMenuContry() creates and places a tkinter option menu for users to select a country
    """
    # Creates an option menu and places it at the coordinates
    optionMenuCountry = OptionMenu(frameOne, countryOption, *countryList )
    optionMenuCountry.place (x=57, y =293 , width = 237, height =30)


def textBoxDistrict():
    """textBoxDistrict() recieves a user input for the district within their selected country
    """
    # Creates a text box that allows for variable input then places it
    districtEntry = ttk.Entry(frameOne, textvariable=districtOption)
    districtEntry.place(x=57, y=369, width = 237)
    

def textBoxPostal():
    """textBoxPostal() creates an entry box to recieve the user's postal code
    """
    # Creates a text box that allows for variable input then places it
    postalEntry = ttk.Entry(frameOne, textvariable=postalOption)
    postalEntry.place(x=57, y=468, width = 237)


def distanceSlider():
    """distanceSlider() creates a tkinter scale for the users to select an integer value for maximum distance
    """
    # Creates a slider then places it then presets the slider value 
    distance = tk.Scale(frameOne, from_=0, to_=250, length=237,  variable=maxDistance, orient=HORIZONTAL)
    distance.place (x=57, y=540)
    distance.set(125)


def continueButton(pic):
    """continueButton() creates and places a button with an image for the information to be checked and proceed to the next screen
    
    arguments
    -- pic : photoImage
    """
    # Creates a continue button then places an image over top to act as a skin for the button and places it
    cont = Button(master=frameOne, text = '', justify = CENTER, command = continueCommand)
    cont.config(image=pic, width=72, height=24)
    cont.pack(side = TOP)
    cont.place(x=145, y=603, width = 72, height = 24)


def continueCommand():
    """continueCommand() is the code which runs upon clicking the continue button (i.e. it validates the infomation and switches from the first screen to the second one
    """
    # Initializes label to be used as invalid field
    invalidField = tk.Label(frameOne, text = "")
    invalidField.place (x=57, y=399)
    
    # Make sure the current fields for country and district are not empty 
    # If it is then give an error and reprompts for entry
    if countryOption.get() == 'Choose a country' or districtOption.get() == '':
        invalidField.config(text="Country and district are required")
    
    # Checks if the given district is in the country or not
    # If it isn't then give an error and reprompts for entry
    elif districtOption.get() not in locationfinder.getDistricts(countryOption.get(), locationfinder.jsonResponse) \
    or districtOption.get().lower() not in locationfinder.getDistricts(countryOption.get(), locationfinder.jsonResponse):
        invalidField.config(text="Invalid district (doesn't exist or not in country)")

    # If all required fields are filled and the district is in the country
    if districtOption.get() in locationfinder.getDistricts(countryOption.get(), locationfinder.jsonResponse) \
    or districtOption.get().lower() in locationfinder.getDistricts(countryOption.get(), locationfinder.jsonResponse):
        # Remove the first frame and place the second
        frameOne.destroy()
        frameTwo.place(x=0,y=0)
        # add the food bank counter text
        infoNum.place(x=255,y=47)
        # Lists the food banks depending on what was inputted
        foodBankListInArea(contPic)

def foodBankListInArea(pic):
    """foodBankList() creates a list of the food banks within the selected area
    
    arguments
    -- pic : photoImage
    """
    # If the postal code field is empty
    if postalOption.get() == "":
        # Creates food bank list by the given district 
        foodList = locationfinder.listNamesByDistrict(countryOption.get(), districtOption.get(), locationfinder.jsonResponse)
        foodList  = sorted(foodList)
        # Set the image of the background and configure the list settings
        backgroundTwo.create_image(0,0, anchor=NW, image=bgPicTwoNoPost)
        foodBankList.config(font='roboto 15', width=24, height=13, bg='#deddb9')
    # If a postal code was inputted
    else:
        # Creates the food bank list by the 10 closest food banks to the postal code and gets the distances from the closest 10
        foodList, distList = locationfinder.listNamesByDistance(postalOption.get(), maxDistance.get())
        # Insert and configure the distances list and the background 
        distListBox.insert(END,*distList)
        distListBox.place(x=240, y=236)
        distListBox.config(font='roboto 15', width=7, height=13, bg='#deddb9')
        backgroundTwo.create_image(0,0, anchor=NW, image=bgPicTwo)
        foodBankList.config(font='roboto 15', width=17, height=13, bg='#deddb9')

    if len(foodList) > 9:
        infoNum.config(text=len(foodList))
    else:
        infoNum.config(text=('0', len(foodList)))
    
    # Insert the food to the list and place it
    foodBankList.insert(END,*foodList)
    foodBankList.place(x=41, y=236)
    
    # Create and configure the continue button 
    foodBankButton = tk.Button(master=frameTwo, text="", command=foodBankListSelect, justify = CENTER)
    foodBankButton.config(image=pic, width=72, height=24, bg='yellow')
    foodBankButton.pack(side = TOP)
    foodBankButton.place(x=144, y=601, width=72, height=24)
    
def callback(url):
    """callback() is used to search a given url in a webbrowser
    
    Arguments
    -- url : String
    """
    webbrowser.open_new(url)

def foodBankListSelect():
    """foodBankListSelect() allows users to select a food bank from the given list to display the specific information for the bank
    """
    # Configure and place an empty invalid label
    invalidField = tk.Label(frameTwo, text = "")
    invalidField.place (x=50, y=575)
    # Gets the name of the selected food back in the list
    selectedName = foodBankList.get(ANCHOR)

    # Label variables for needed information
    addressLabel = tk.Label(frameThree)
    nameLabel = tk.Label(frameThree)
    phoneLabel = tk.Label(frameThree)
    emailLabel = tk.Label(frameThree)
    linkLabel = tk.Label(frameThree)

    # Checks if there is a food bank selected
    if(selectedName != ''):

        # Create background for 3rd screen and destroy the second
        backgroundThree.create_image(0,0, anchor=NW, image=bgPicThree)
        frameTwo.destroy()
        frameThree.place(x=0,y=0)
        # Set needed variables
        name, address, phoneNumber, email, link, bankPostal = locationfinder.getInformation(selectedName, locationfinder.jsonResponse)
        # Gets the foods needed by the food bank
        needsList = locationfinder.listNeeds(bankPostal)

        #Configure all the labels with the variables
        addressLabel.config(text = address, bg="#d9d8be", font="helvetica 10")
        addressLabel.place(x=69,y=170)

        nameLabel.config(text = name, bg="#d9d8be", font="helvetica 10")
        nameLabel.place(x=69,y=138)

        phoneLabel.config(text = phoneNumber, bg="#d9d8be", font="helvetica 10")
        phoneLabel.place(x=69,y=269)

        emailLabel.config(text = email, bg="#d9d8be", font="helvetica 10")
        emailLabel.place(x=69,y=227)

        linkLabel.config(text = "Click here", fg= "dark blue", bg="#d9d8be", cursor="plus", font="helvetica 10")
        linkLabel.place(x=69,y=319)
        # Creates the hyperlink to the website
        linkLabel.bind("<Button-1>", lambda h: callback(link))

        # List for the needs and given foods by the food bank
        needListBox.insert(END,*needsList)
        needListBox.place(x=69, y=396)
        needListBox.config(font='helvetica 10', width=20, height=13, bg='#d9d8be')

    # If not food bank was selected give an error
    else:
        invalidField.config(text="Please select a food bank for more information")

#Create the windows
window = Tk()
window.title("Food Bank Locator UK Edition")

# setup the window
frameWidth = 360
frameHeight = 640
window.minsize(frameWidth, frameHeight)
window.maxsize(frameWidth, frameHeight)

#Create the frames
frameOne=tk.Frame(window, width = frameWidth, height = frameHeight)
frameOne.place(x=0,y=0)
frameInterm=tk.Frame(window, width = frameWidth, height = frameHeight)
frameTwo=tk.Frame(window, width = frameWidth, height = frameHeight)
frameThree=tk.Frame(window, width = frameWidth, height = frameHeight)

#create images (they must be global)
bgPicOne = PhotoImage(file="images\\screen_1.png")
bgPicTwoNoPost = PhotoImage(file="images\\screen_2.png")
bgPicTwo = PhotoImage(file="images\\screen_2_part_2_with_distance.png")
bgPicThree = PhotoImage(file="images\\screen_3.png")
contPic = PhotoImage(file = "images\\button_continue.png")

#Create background and text for second frame, place text on background
backgroundTwo = Canvas(master=frameTwo, width=360, height=640)
backgroundTwo.pack()

#Create background for third frame
backgroundThree = Canvas(master=frameThree, width=360, height=640)
backgroundThree.pack()

# Label for number of food banks
infoNum = tk.Label(master=backgroundTwo, text = '',
                               fg='black',
                               bg='#5088cb',
                               font='helvetica 30',
                               justify = CENTER)

# Country variables
countryOption = tk.StringVar()
countryList = ["England", "Northern Ireland", "Scotland", "Wales"]
countryOption.set("Choose a country")

# District variable input
districtOption = tk.StringVar()

# Postal code variable input
postalOption = tk.StringVar()

# Maximum Distance variable input
maxDistance = tk.IntVar()

# Food bank list (second screen) variables input
selectedBank = tk.StringVar()
foodBankList = tk.Listbox(frameTwo)
distListBox = tk.Listbox(frameTwo)

#Needs list box
needListBox = tk.Listbox(frameThree)

#Calling Functions to display
background(bgPicOne, frameOne)
optionMenuCountry()
textBoxDistrict()
textBoxPostal()
distanceSlider()
continueButton(contPic)

# Run main
window.mainloop()

