email = "zhiyuan3112@gmail.com"
password="123456"

import pyrebase
import pandas as pd
import Ml
firebaseConfig={"apiKey":"AIzaSyC2YV31UO6dqnaqBLJ2iuMWRkt35oU5Mvo",
                "authDomain":"fyp-powermonitoring-b2afc.firebaseapp.com",
                "databaseURL":"https://fyp-powermonitoring-b2afc-default-rtdb.asia-southeast1.firebasedatabase.app",
                "projectID":"fyp-powermonitoring-b2afc",
                "storageBucket":"fyp-powermonitoring-b2afc.firebasestorage.app"
}


def initializeFirebase(date):

    firebase = pyrebase.initialize_app(firebaseConfig)

    auth =firebase.auth()
    users = auth.sign_in_with_email_and_password(email, password)
    db = firebase.database()
    users = db.child("UsersData").child("zQ7se3Lqr7ZvaYHwruZLMBssrZB2").child("readings").child(str(date)).get()

    return users

def retrieveData(users) -> pd.DataFrame:
    df = pd.DataFrame()
    
    for user in users.each():
        print(user.val())
        temp =pd.Series(user.val()).to_frame()
        
        df = pd.concat([df,temp],axis=1)
        
    df = df.transpose()
    df['dateTime']= pd.to_datetime(df['timestamp'],dayfirst=True)
    df.set_index('dateTime', inplace=True)
    df = df.drop(['timestamp'],axis=1).sort_index()

    # df.to_csv('temp.csv')
    return(df)

def test(start,end):
    firebase = pyrebase.initialize_app(firebaseConfig)
    auth =firebase.auth()
    users = auth.sign_in_with_email_and_password(email, password)
    db = firebase.database()
    df = pd.DataFrame()

    for i in range(start,end+1):
        users = db.child("UsersData").child("zQ7se3Lqr7ZvaYHwruZLMBssrZB2").child("readings").child(str(i)).get()


        for user in users.each():
            if users.each() != None:
                temp =pd.Series(user.val()).to_frame()
                
                df = pd.concat([df,temp],axis=1)

            
    df = df.transpose()
    df['dateTime']= pd.to_datetime(df['timestamp'],dayfirst=True)
    df.set_index('dateTime', inplace=True)
    df = df.drop(['timestamp'],axis=1).sort_index()
    df = df[df.index.notna()]
    df.to_csv('temp.csv')
    return (df)
        
        
df = test(1,30)
df.to_csv('temp.csv')

df = Ml.preprocessing(df)



