# email = "zhiyuan3112@gmail.com"
# password="123456"

# import pyrebase
# import json
# import csv

# firebaseConfig={"apiKey":"AIzaSyC2YV31UO6dqnaqBLJ2iuMWRkt35oU5Mvo",
#                 "authDomain":"fyp-powermonitoring-b2afc.firebaseapp.com",
#                 "databaseURL":"https://fyp-powermonitoring-b2afc-default-rtdb.asia-southeast1.firebasedatabase.app",
#                 "projectID":"fyp-powermonitoring-b2afc",
#                 "storageBucket":"fyp-powermonitoring-b2afc.firebasestorage.app"
# }

# firebase = pyrebase.initialize_app(firebaseConfig)

# auth =firebase.auth()

# userd = auth.sign_in_with_email_and_password(email, password)

# db = firebase.database()
# users = db.child("UsersData").child("zQ7se3Lqr7ZvaYHwruZLMBssrZB2").child("readings").get()



# with open("data.csv", "w", newline="") as f:
#     for user in users.each():
#         w = csv.DictWriter(f, user.val().keys())
#         w.writeheader()
#         w.writerow(user.val())
    
# f.close()


