#Problem Log:    Apparently the Browser has a little issue if you dont close the previous try! Then the driver.find_elements_by_xpath("//a[@href]")[0].click() on the second page goes
# out of bounds. Possible fixes might be a try catch method in a while loop until it works
#UPDATE: It seems to work, there hasnt been an incident since calling georg

import sys
from selenium import webdriver
import time

#   Function that checks if the string containing the Name and course are in the txt file or not
#   TODO: Add a function to send an email if not contained in the TXT
def alternateTXT(userstring):
    if userstring in text:
        return True
    else:
        file.write(userstring + "\n")
        return False

#   Function to click the ">" button at the bottom of the page
def nextPage():
    checkNext()
    nextbtn = driver.find_elements_by_xpath("//*[@class='next']/a")
    nextbtn[0].click()

#   If the checkNext Function detects that there is no ">" button available to click it will end the Programm
def checkNext():
    nextdisbtn = driver.find_elements_by_xpath("//*[@class='next disabled']/a")
    if len(nextdisbtn) > 0:
        print(countOLD," have been already in the TXT")
        print(countNEW, " have been added")
        driver.close()
        sys.exit()

#   Function that takes the list of td tags, the index of the last found green bubble and goes backwards through
#   the td tag list to find the course NAME and the NAME and MAIL of the person
#   @param: liste, index
#   @return: string of values
def nameUndKursAuslesen(liste, index):
    answers = liste[index-1].text
    for j in range(index, -1, -1):
        #print(liste[j].get_attribute("class"))
        if liste[j].get_attribute("class") == "":
            answers = answers + "\n" + liste[j].text + "\n"
            return alternateTXT(answers)

#   VARIABLES TO COUNT THE NAMES AND COURSES WHICH ARE NEW AND WHICH HAVE ALREADY BEEN WRITTEN INTO THE TXT
global countOLD
countOLD = 0
countNEW = 0
#   SETTING UP THE DRIVER
driver = webdriver.Firefox(executable_path=r"G:\Python\geckodriver-v0.25.0-win64\geckodriver.exe")
driver.get(r"https://www.lecturio.de/persoenlicher-bereich/uebersicht.html")
#   OPENING THE TXT FILE THE NAMES AND COURSES WILL BE WRITTEN INTO
file = open("RessourcesLecturio.txt", "r+")
text = file.read()

#   Currenty on the first page of the process: Logging into Lecturio
emailElem = driver.find_element_by_id("signin_email")
emailElem.send_keys("INSERT EMAIL HERE")
#emailElem.send_keys(sys.argv[1])
passwElem = driver.find_element_by_id("signin_password")
passwElem.send_keys("INSERT PASSWORD HERE")
#passwElem.send_keys(sys.argv[2])
passwElem.submit()

#---------------------------------------------------------------------------------------------------
# TODO:
#       Catch invalid user input!
#---------------------------------------------------------------------------------------------------

#   Wait for the page to come back
while(driver.current_url == "https://www.lecturio.de/persoenlicher-bereich/uebersicht.html"):
    time.sleep(2.5)
    #-------------------------------------------------------------------------------------------------
    # TODO:
    #       End Thread if loading takes too long!
    #-------------------------------------------------------------------------------------------------
    continue


#Currently on the Second page, clicking the continue button and wait some time for it to come back
driver.find_elements_by_xpath("//a[@href]")[0].click()
time.sleep(1.5)

#   On the third page you are on the home-screen of Lecturio, the funny thing is the <a href> tag of the
#   Progress screen has the class "vnav_label" although ALL other <a href> in the listing have a class name
#   "vnav_link"
#   Might need to fix later
driver.find_elements_by_class_name("vnav_label")[0].click()

#Note: IT FUCKING WORKS
while(True):
    temp = 0
    #grab both a list of td tags and i tags to go through the td tags, check whether or not a td tags class name
    #is "status-icon" or not. Then, when found one of those td tags, grab the first i tag with the corresponding
    #index and check if its a "icon fa-circle completed". Then call the function to get the corresponding course
    #name and user name
    table = driver.find_elements_by_xpath("/html/body/div/div/div/div/div/table/tbody/tr/td")
    i_tags = driver.find_elements_by_xpath("/html/body/div/div/div/div/div/table/tbody/tr/td/i")
    for elem in table:
        if elem.get_attribute("class") == "status-icon":
            if i_tags[temp].get_attribute("class") == "icon fa-circle completed":
                # findet alle 8 grünen bubbles
                isNew = nameUndKursAuslesen(table, table.index(elem))
                countOLD += 1 if isNew else 0
                countNEW +=1 if not isNew else 0
            #the temp variable is important for the i-tag list. You need this variable to properly iterate through
            #the list. In other words, whenever you find an td tag with the classname "status icon" you want to check
            #the corresponding i tag. So the list of i tags will be iterated with the temp variable
            temp += 1
    time.sleep(0.1)
    nextPage()