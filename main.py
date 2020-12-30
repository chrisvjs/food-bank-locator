import requests
import json

"""
Steps
Screen 1: User Location
     1. Pick country from dropdown (Done)
     2. Do text box of districts (Done)
     3. Enter postal code (Done)
Screen 2: Choose Food Bank
     1a. If postal is unknown, diplay places in district (Done)
     1b. If postal code field is entered, display top 10 closest food banks (Done)
     2. Allow user to click a food bank (Showing: Name, Distance) (Done)
Screen 3: Display info about food bank
     1. Name, address, postal code, phone, email, url, (Done
"""

# json object from food banks api
jsonResponse = requests.get('https://www.givefood.org.uk/api/1/foodbanks/').json()


def listNamesByDistrict(country, district, data):
    """listNamesByDistrict takes the data and filters it by the district

    arguments 
    -- country : string
    -- district : string
    -- data : json object (list of dictionaries)

    result
    -- list
    """

    foodList = []
    
    # adds the name of the food bank if it is in the district
    for i in range(len(data)):
        if data[i].get('district') == district and data[i].get('country') == country:
           foodList.append(data[i].get('name'))
           
    return foodList
# end of listNamesByDistrict


def listByDistance(postal):
    """listByDistance returns a json object containing the 10 closest food banks (index 0 is closest)
    
       
    arguments
    -- postal : string

    return
    -- json object
    """
    # obtains json object from the givefood.org.uk api
    return requests.get('https://www.givefood.org.uk/api/1/foodbanks/search/?address=' + postal).json()
# end of listByDistance


def listNamesByDistance(userPostal, userRange):
    """listNamesByDistance creates a list of names and distances of the 10 closest food banks

    arguments
    -- userPostal : string
    -- userRange : int

    return
    -- list
    -- list
    """
    
    # obtains json object from listByDistance method
    data = listByDistance(userPostal)

    # initialize returnable lists
    foodList = []
    distList = []

    # obtain and format the name and distance of each food bank within the user's requested range
    for i in range(len(data)):

        distkm = data[i].get('distance_m')/1000

        if(distkm <= userRange):
            foodList.append(data[i].get('name'))
            distList.append(str(round(distkm, 1)) + ' km')

    return foodList, distList


def listNeeds(bankPostal):
    """listNeeds gets the needs of the food bank

    arguments 
    -- bankPostal : string
    
    result
    -- list
    """

    # getting json object of data
    data = listByDistance(bankPostal)

    # string variables
    needsString = ''
    needsListSplit = []

    # adding the needs to the string
    if data[0].get('postcode') == bankPostal:
        needsString = (data[0].get('needs'))
    
    # formatting the string so \r\n are removed and split into a list
    needsListSplit = needsString.split('\r\n')

    # if there is nothing in the list return a n/a list otherwise return the list of needs
    if not needsListSplit:
        return ["N/A"]
    else:
        return needsListSplit
# end of listNeeds()


def getDistricts(country, data):
    """getDistricts gets all the names of the disctrics for each country

    arguments 
    -- country : string
    -- data : json object (list of dictionaries)

    result
    -- list
    """

    # list for districts
    districtList = []

    # goes through the data and adds all the districts to the list 
    for i in range(len(data)):
        if data[i].get('country') == country:
           districtList.append(data[i].get('district'))

    # removes duplicate districts from the list
    districtList = [x for x in districtList if x]
    
    # returns the sort list of districts
    return sorted(list(dict.fromkeys(districtList)))
# end of getDistricts


def charInsert(string, length):
    """charInsert takes a string and inserts characters after a certain amount of characters

    arguments 
    -- string : string
    -- length : int
    
    result
    -- string
    """
    return '-\n'.join(string[i:i+length] for i in range(0,len(string),length))

def getInformation(name, data):
    """getInformation gets the address, phone number, email, link, and banks postal code of a food bank

    arguments 
    -- string : string
    -- json object
    
    result
    -- strings
    """
    # get all the information needed from the json object
    for i in range(len(data)):
        if data[i].get('name') == name:
            address = data[i].get('address')
            phoneNumber = data[i].get('phone')
            email = data[i].get('email')
            link = data[i].get('url')
            bankPostal = data[i].get('postcode')

    # format address to have less lines in GUI
    addressFormat = address.replace('\r\n', ', ')
    addressFormat = charInsert(addressFormat, 40)

    return name, addressFormat, phoneNumber, email, link, bankPostal
# end of getInformation
