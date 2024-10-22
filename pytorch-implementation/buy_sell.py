from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import json
# from main_clone import parameters

def run_selenium():
    # To keep browser window open after performing the task
    options = Options()
    options.add_experimental_option("detach",True)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                            options=options)

    driver.get("https://in.tradingview.com/chart/?symbol=NSE%3AINFY")
    driver.maximize_window()
    time.sleep(5)
    def buy(quantity):
        print("In buy function")
        driver.find_element("xpath","/html/body/div[2]/div[1]/div[2]/div[1]/div/table/tr[1]/td[2]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[2]").click()
        time.sleep(2)
        textBox = driver.find_element(By.CLASS_NAME,"input-RUSovanF")
        textBox.click()
        textBox.send_keys([Keys.BACKSPACE] * 5)
        time.sleep(2)
        textBox.send_keys(quantity)
        time.sleep(2)
        driver.find_element("xpath","/html/body/div[2]/div[1]/div[2]/div[1]/div/table/tr[1]/td[2]/div/div[2]/div[1]/div[2]/div[1]/div[3]").click()
        
        # time.sleep(2)
    def sell(quantity):
        print("In sell function")
        driver.find_element("xpath","/html/body/div[2]/div[1]/div[2]/div[1]/div/table/tr[1]/td[2]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[2]").click()
        time.sleep(5)
        textBox = driver.find_element(By.CLASS_NAME,"input-RUSovanF")
        textBox.click()
        textBox.send_keys([Keys.BACKSPACE] * 5)
        time.sleep(2)
        textBox.send_keys(quantity)
        time.sleep(2)
        driver.find_element("xpath","/html/body/div[2]/div[1]/div[2]/div[1]/div/table/tr[1]/td[2]/div/div[2]/div[1]/div[2]/div[1]").click()
        # time.sleep(2)
    # Click on hamburger
    driver.find_element("xpath","/html/body/div[2]/div[4]/div/div/div/div").click()
    time.sleep(2)
    # Click on Sign in button
    driver.find_element("xpath", "//*[@id='overlap-manager-root']/div/span/div[1]/div/div/div[8]").click()
    time.sleep(2)
    # Click on sign in with Email button
    driver.find_element("xpath","//*[@id='overlap-manager-root']/div/div[2]/div/div/div/div/div/div/div[1]/div[4]/div/span").click()
    time.sleep(2)
    # Inputting id and password
    driver.find_element("xpath","//input[starts-with(@id, 'email-signin__user-name-input__')]").send_keys("chiragt1805@gmail.com")
    time.sleep(2)
    driver.find_element("xpath","//input[starts-with(@id, 'email-signin__password-input__')]").send_keys("Trader@99")
    time.sleep(2)
    # Click on submit
    driver.find_element(By.CLASS_NAME,"tv-button__loader").click()
    time.sleep(2)
    driver.find_element("xpath","//*[@id='footer-chart-panel']/div[2]/button[1]").click()
    time.sleep(2) 
    #object of ActionChains
    driver.find_element("xpath","//*[@id='footer-chart-panel']/div[1]/div[1]/div[4]/button").click()
    time.sleep(2)
    a = ActionChains(driver)
    #identify element
    m = driver.find_element("xpath","//*[@id=\"bottom-area\"]/div[4]/div/div[1]/div[1]/div[2]")
    #hover over element
    a.move_to_element(m).perform()
    time.sleep(2)
    # //*[@id="bottom-area"]/div[4]/div/div[1]/div[1]/div[2]/button
    driver.find_element("xpath","//*[@id=\"bottom-area\"]/div[4]/div/div[1]/div[1]/div[2]/button").click()
    time.sleep(2)
    driver.find_element("xpath","//*[@id=\"overlap-manager-root\"]/div/div/div[2]/div/div[2]/form/button").click()
    # //*[@id="overlap-manager-root"]/div/div/div[2]/div/div[2]/form/button
    time.sleep(2)
    # IT RUNS TILL HERE.
    while True:
        with open('./parameters.json', 'r') as op:
            json_object = json.load(op)
            op.close()
        if(json_object['buy']==1):
            buy(json_object['qty'])
            # In buy edit qty, buy button click
            json_object['buy']=0
            json_object['qty']=0
            with open("./parameters.json", "w") as outfile:
                json.dump(json_object, outfile)
        elif(json_object['sell']==1):
            sell(json_object['qty'])
            # In sell edit qty, buy button click
            json_object['sell']=0
            json_object['qty']=0
            with open("./parameters.json", "w") as outfile:
                json.dump(json_object, outfile)
        elif(json_object['hold']==1):
            json_object['hold']=0
            with open("./parameters.json", "w") as outfile:
                json.dump(json_object, outfile)
        else:
            print("Buy/Sell failed")
        print("Before time sleep")
        time.sleep(20)
run_selenium()

   
