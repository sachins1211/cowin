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
        # print(verification_code_text)
        # if row['handle_id'] == 7552:
        #     verification_code_text = row['text']
        #     return verification_code_text
        # else:
        #     print("verification code not found")
        #     return None

    return "Some error occurred"


def get_otp():
    flag= True
    while(flag):
        data = get_text_otp()
        if data is not None and "Your OTP to register/access CoWIN is " in data:
            a = data.split('.')
            print(a[0].replace("Your OTP to register/access CoWIN is ", "").strip())
            flag= False
            return(a[0].replace("Your OTP to register/access CoWIN is ", "").strip())
        else:
            pass


print(get_text_otp())
