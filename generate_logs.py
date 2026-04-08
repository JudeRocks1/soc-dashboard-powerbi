import pandas as pd  # For creating and handling data tables (DataFrames)
import random  # For making random choices
from datetime import datetime, timedelta  # For working with dates and times

#globals
OUTPUT_FILE = "security_logs.csv" # KEEP .csv

#----------Customizable values----------

NUMBER_OF_USERS = 50 # The number of users
DAYS_OF_DATA = 7 # Days simulated
RESOURCE_FAIL_CHANCE = { # The chance that a simulated login attempt will fail where 0 means no failures and 1 means all failures
    'Email': 0.04,
    'VPN': 0.13,
    'Database': 0.11,
    'FileServer': 0.12
}

# Organization specific classifications
DEPARTMENTS = ['IT', 'HR', 'Finance', 'Sales']
ROLES = ['Standard', 'Manager', 'Admin']
RESOURCES = ['Email', 'VPN', 'Database', 'FileServer']

#----------End of customizable values----------

def main():
    try:
        generate_data() # fills the login_list data
    except Exception as e:
        print("Type of Exception: ", type(e))
        return 1  # Failure

#generates data and deals with csv output
#params none
#returns none
def generate_data():
    user_list = fill_user_list() # list of users
    login_list = fill_login_list(user_list) # list of simulated login data

    df = pd.DataFrame(login_list) # turn the list of login data into a pandas data frame
    df.to_csv(OUTPUT_FILE, index=False) # turn the data frame into a csv

    print(f"Saved {len(df)} rows of data to {OUTPUT_FILE}") # print success. note this number does not include the output csv's line 1 header


#fills a list of user ids formatted to 4 digits
#params none
#returns user_list
def fill_user_list():
    user_list = []
    for i in range(1, NUMBER_OF_USERS + 1):
        user_list.append(f'U{i:04d}')
    return user_list

#fills a list containing login data Timestamp, UserID, Status, Resource
#params user_list
#returns login_list
def fill_login_list(user_list):
    login_list = []
    start_date = datetime.now() - timedelta(days=DAYS_OF_DATA)

    user_details = {} # create a dictionary that stores the data to be filled before storage in the login_list
    for u in user_list:
        user_details[u] = { # assigns a random department and role to each user
            'Department': random.choice(DEPARTMENTS),
            'Role': random.choice(ROLES)
        }

    # simulation loop
    for day_num in range(DAYS_OF_DATA): # iterates through the days
        current_date = start_date + timedelta(days=day_num) # tracks the current day

        for user in user_list: # iterates through users
            num_logins = random.randint(0,20)

            for attempts in range(num_logins): # iterates through each login
                timestamp = current_date.replace(hour=random.randint(0, 23), minute=random.randint(0, 59)) # timestamp holds the existing current day and replaces the hour and minute with random value

                resource = random.choice(RESOURCES) # randomly access a resource, potential improvement: users role or department influences this probability

                if random.random() > RESOURCE_FAIL_CHANCE[resource]:
                    status = 'Success'
                else:
                    status = 'Failed'

                login_list.append({ # adds the filled dictionary element to the list
                    'Timestamp': timestamp,
                    'UserID': user,
                    'Status': status,
                    'Resource': resource,
                    'Department': user_details[user]['Department'],
                    'Role': user_details[user]['Role']
                })

    return login_list

if __name__ == "__main__":
    main()
