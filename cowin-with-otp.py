import requests,json,os,subprocess
from datetime import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import sqlite3
import pandas as pd

# https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id=670&date=31-05-2021&vaccine=COVAXIN
cowin_url='https://selfregistration.cowin.gov.in/'
url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id=670&date=03-06-2021"
# url2 = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id=670&date=30-05-2021"
head = {
    "accept":"application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "origin": "https://www.cowin.gov.in",
    "referer": "https://www.cowin.gov.in/",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "sec-gpc": "1",
    "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
}
skip_count = 0


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


flag = True
url_flag = True

while flag:

    try:
        r = requests.get(url, headers=head)
        print("request sent " + datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
        print(r.text)

        valid_pin = [226028, 226010, 226016]

        exclude_hosp = []
        center_list = json.loads(r.text)
        abc = True
        for center in center_list['centers']:
            if center['pincode'] in valid_pin:
                for session in center['sessions']:
                    if session['min_age_limit'] < 45 and session['available_capacity'] > 0 and 'cova'.casefold() in session['vaccine'].casefold(): #== 'covaxin'.casefold():
                        print(center['name'] + "-" + str(center["pincode"]) +"-" + str(center["address"])+ " : " + session['date'] + " \nTotal slots- "+str(session['available_capacity'])+ ": dose1- "+str(session["available_capacity_dose1"]) +  ": dose 2- "+ str(session["available_capacity_dose2"]) + ": "+str(session['vaccine']) + " : age " + str(session['min_age_limit'])+"\n")
                        if center["fee_type"].casefold() == 'paid'.casefold():
                            print("fees::"+ str(center["vaccine_fees"])+"\n")
                        if center['name'] not in exclude_hosp:
                            abc = False
        if not abc:
            print("Vaccine Slot Available")

            driver = webdriver.Chrome(ChromeDriverManager().install())
            driver.maximize_window()

            driver.get(cowin_url)
            time.sleep(1.5)
            mob = driver.find_element_by_id("mat-input-0")
            mob.send_keys('')  #Provide mobile number here
            driver.find_element_by_class_name('covid-button-desktop.ion-text-center').click()
            otp = get_otp()
            os.system('say "Vaccine Slot Available"')
            time.sleep(0.3)
            inp_otp = driver.find_element_by_id("mat-input-1")
            inp_otp.send_keys(otp)
            time.sleep(0.5)
            driver.find_element_by_class_name('covid-button-desktop.ion-text-center').click()
            subprocess.call(["afplay", "alert.wav"])
            time.sleep(400)
        else:
            print("No slot available")
    except Exception as e:
        if 'Expecting value: line 1 column 1 (char 0)' == str(e) and skip_count < 3:
            print(e)
            os.system('say "Program failed"')
            skip_count += 1
            pass
        else:
            print(e)
            os.system('say "Program failed. Exiting"')
            subprocess.call(["afplay", "alert.wav"])
            exit(-1)
    time.sleep(50)
