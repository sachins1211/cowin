import requests,json, time,os,subprocess
from datetime import datetime

url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id=670&date=02-05-2021"
url2 = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id=670&date=09-05-2021"

flag=True
url_flag = True
while flag:

    try:
        if url_flag:
            print(url)
            r = requests.get(url)
            url_flag = False
        else:
            print(url2)
            r = requests.get(url2)
            url_flag = True
            flag=False
        print("request sent " + datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
        print(r.text)

        # valid_pin = [226028, 226010, 226016]
        exclude_hosp = ['Charak Hospital']
        valid_pin = []
        center_list= json.loads(r.text)
        abc = True
        for center in center_list['centers']:
            if center['pincode'] not in valid_pin:
                for session in center['sessions']:
                    if session['min_age_limit'] < 45 and session['available_capacity'] > 0:
                        print(center['name'] + "-" + str(center["pincode"]) + " : " + session['date'] + " : "+str(session['available_capacity']))
                        print(center)
                        if center['name'] not in exclude_hosp:
                            abc = False
        if not abc:
            os.system('say "Vaccine Slot Available"')
            subprocess.call(["afplay", "alert.wav"])
            flag = False
            time.sleep(60)
    except Exception as e:
        print(e)
        os.system('say "Program failed"')
        time.sleep(80)
        subprocess.call(["afplay", "alert.wav"])

    time.sleep(2)

# print(center[0])