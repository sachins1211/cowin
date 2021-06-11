import requests,json, time
from datetime import datetime
# https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id=670&date=31-05-2021&vaccine=COVAXIN
url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id=670&date=24-05-2021"
url2 = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id=670&date=31-05-2021"
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

flag = True
url_flag = True

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
            flag = False
        print("request sent " + datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
        # print(r.text)

        # valid_pin = [226028, 226010, 226016]
        valid_pin = []
        exclude_hosp = []
        center_list= json.loads(r.text)
        abc = True
        for center in center_list['centers']:
            if center['pincode'] not in valid_pin:
                for session in center['sessions']:
                    if session['min_age_limit'] < 45 and session['available_capacity'] >= 0 and 'cova'.casefold() in session['vaccine'].casefold(): #== 'covaxin'.casefold():
                        print(center['name'] + "-" + str(center["pincode"]) +"-" + str(center["address"])+ " : " + session['date'] + " \nTotal slots- "+str(session['available_capacity'])+ ": dose1- "+str(session["available_capacity_dose1"]) +  ": dose 2- "+ str(session["available_capacity_dose2"]) + ": "+str(session['vaccine']) + " : age " + str(session['min_age_limit'])+"\n")
                        if center["fee_type"].casefold() == 'paid'.casefold():
                            print("fees::"+ str(center["vaccine_fees"])+"\n")
                        if center['name'] not in exclude_hosp:
                            abc = False
        if not abc:
            print("Vaccine Slot Available")
        else:
            print("No slot available")
    except Exception as e:
        print(e)
        print("Program failed")
        time.sleep(1)
    time.sleep(10)
    # exit(0)
