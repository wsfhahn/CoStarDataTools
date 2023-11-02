from selenium import  webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from time import sleep

# Fill in CoStar username and password to login
costarUsername = "[CoStar Email]"
costarPassword = "[CoStar Password]"

# Using the Chrome driver, also compatible with FireFox
driver = webdriver.Chrome()
driver.get("https://product.costar.com")

sleep(2)

# Locating all of the elements used for login and entering in appropriate data
usernameBox = driver.find_element(by=By.ID, value="username")
passwordBox = driver.find_element(by=By.ID, value="password")
loginButton = driver.find_element(by=By.ID, value="loginButton")

usernameBox.send_keys(costarUsername)
passwordBox.send_keys(costarPassword)

loginButton.click()

sleep(2)

# Obtaining and entering the SMS one-time login
smsBox = driver.find_element(by=By.ID, value="code")
submitButton = driver.find_element(by=By.ID, value="otpverify")

verificationCode = input("SMS  Verification Code: ")

smsBox.send_keys(verificationCode)

submitButton.click()

sleep(2)

# Navigate to the 'Professionals' tab from the landing page
professionalsButton = driver.find_element(by=By.XPATH, value='//*[@id="costar-header-hydration-root"]/div/header/div[2]/div/nav/div[2]/div/button[7]')
professionalsButton.click()

sleep(2)

# Find data for Tenant Rep companies and Tenant contacts (works with other options)
listboxCompanyPractices = driver.find_element(by=By.ID, value="listboxCompanyPractices")
listboxContactPractices = driver.find_element(by=By.ID, value="listboxContactPractices")
nextButton = driver.find_element(by=By.XPATH, value='//*[@id="oQuerySteps"]/img[2]')

select = Select(listboxCompanyPractices)
select.select_by_visible_text("Tenant Reps (Retail)")

select = Select(listboxContactPractices)
select.select_by_visible_text("Tenant")

nextButton.click()

sleep(2)

# Locating the button to enter the search by state screen
driver.switch_to.frame(driver.find_element(by=By.TAG_NAME, value="iframe"))

marketButton = driver.find_element(by=By.XPATH, value='//*[@id="frmLocationSearch"]/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[3]/td[1]/a/img')
marketButton.click()

sleep(2)

# Selecting the correct user-specified state
driver.switch_to.default_content()

userMarket = input("Enter State: ")

listboxMarkets = driver.find_element(by=By.ID, value="htmlAvailableSelectBox")
select = Select(listboxMarkets)
select.select_by_visible_text(userMarket)

moveoverButton = driver.find_element(by=By.ID, value="Button1")
moveoverButton.click()

nextButton = driver.find_element(by=By.XPATH, value='//*[@id="oQuerySteps"]/img[3]')
nextButton.click()

sleep(2)

# Ask for where to write the file
outputFilePath = input("Output File: ")
outputFile = open(outputFilePath, 'w')

emailList = []
nameList = []


def dumpData():
    iteration = 0
    driver.switch_to.frame(1)
    webData = driver.find_elements(by=By.TAG_NAME, value='a')
    for i in webData:
        if i.get_attribute('onclick') is not None:
            if "@" in i.get_attribute('onclick'):
                # Stripping the raw data down to just the email address
                emailAddress = i.get_attribute('onclick')[4:-17]

                # Iterating through the table data containing the names
                name = driver.find_element(by=By.XPATH, value='//*[@id="row'+str(iteration)+'FC"]/td[3]')
                iteration = iteration + 1

                # Storing all of the data to be written to a file
                nameList.append(name.text)
                emailList.append(emailAddress)
    driver.switch_to.default_content()

# Collect all data on screen and move to the next until out of pages
while True:
    dumpData()
    if driver.find_element(by=By.XPATH, value="//*[@onclick='NextResultsPage()']").is_displayed():
        nextPageButton = driver.find_element(by=By.XPATH, value="//*[@onclick='NextResultsPage()']")
        nextPageButton.click()
        sleep(2)
    else:
        break

# Write the data to a file for the user to access later
def writeData():
    for i in range(0, len(emailList)):
        dataToWrite = '\"' + nameList[i] + '\"' + ', \"' + emailList[i] + '\"\n'
        outputFile.write(dataToWrite)
        print(dataToWrite)

writeData()