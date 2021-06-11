import requests,json, time,os,subprocess
from datetime import datetime

url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id=670&date=16-05-2021"
url2 = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id=670&date=16-05-2021"

flag = True
url_flag = True
skip_count = 0
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

while flag:
    try:
        if url_flag:
            print(url)
            r = requests.get(url, headers=head)
            url_flag = False
        else:
            print(url2)
            r = requests.get(url2, headers=head)
            url_flag = True
        print("request sent " + datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
        # print(r.text)
        #valid_pin = [226028, 226010, 226016]
        valid_pin = []
        exclude_hosp = ['Charak Hospital']
        # exclude_pin = []
        center_list= json.loads(r.text)
        vaccine_available = False
        for center in center_list['centers']:
            if center['pincode'] not in valid_pin:
                for session in center['sessions']:
                    if session['min_age_limit'] < 45 and session['available_capacity'] > 1:
                        print(center['name'] + "-" + str(center["pincode"]) + " : " + session['date'] + " : slots- " +
                              str(session['available_capacity']) + " : " + str(session['vaccine'] + " : age " + str(session['min_age_limit'])))
                        # print(center)
                        if center['name'] not in exclude_hosp:
                            vaccine_available = True
        if vaccine_available:
            os.system('say "Vaccine Slot Available"')
            subprocess.call(["afplay", "alert.wav"])
            # flag = False
            time.sleep(60)
            exit(0)
        else:
            print("no slot")
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
    time.sleep(30)
