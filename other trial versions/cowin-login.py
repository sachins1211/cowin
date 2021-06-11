from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import sqlite3
import pandas as pd


def get_text_otp():
    conn = sqlite3.connect("/Users/sachinsharma/Library/Messages/chat.db")

    messages = pd.read_sql_query("select * from message order by ROWID desc limit 1", conn)
    handles = pd.read_sql_query("select * from handle order by ROWID desc limit 1", conn)

    messages.rename(columns={'ROWID': 'message_id'}, inplace=True)
    handles.rename(columns={'id': 'phone_number', 'ROWID': 'handle_id'}, inplace=True)
    imessage_df = pd.merge(messages[['text', 'handle_id', 'date', 'is_sent', 'message_id']],
                           handles[['handle_id', 'phone_number']], on='handle_id', how='left')

    for index, row in imessage_df.iterrows():
        verification_code_text = row['text']
        return verification_code_text

    return "Some error occurred"


def get_otp():
    flag_otp= True
    while(flag_otp):
        data = get_text_otp()
        if data is not None and "Your OTP to register/access CoWIN is " in data:
            a = data.split('.')
            otp=a[0].replace("Your OTP to register/access CoWIN is ", "").strip()
            print(otp)
            flag_otp= False
            return(otp)
        else:
            pass

cowin_url='https://selfregistration.cowin.gov.in/'


flag = True

while(flag):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.maximize_window()

    driver.get(cowin_url)
    mob = driver.find_element_by_id("mat-input-0")
    mob.send_keys('') #mobile number here
    time.sleep(1.4)
    driver.find_element_by_class_name('covid-button-desktop.ion-text-center').click()
    otp = get_otp()
    # otp="377166"
    time.sleep(0.3)
    # time.sleep(2)
    inp_otp = driver.find_element_by_id("mat-input-1")
    inp_otp.send_keys(otp)
    time.sleep(0.5)
    driver.find_element_by_class_name('covid-button-desktop.ion-text-center').click()

    flag=False


