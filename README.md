# Security Operations & Access Monitoring Dashboard

The Problem: Security Operations Center (SOC) analysts need practice identifying threats like brute force attacks and resource compromises without risking real data.

The Solution: A simulated security dashboard with Python-generated attack patterns and Power BI visualizations.

The Tech Stack: Python (Log Generation), Power BI (Visualization), DAX (Security Logic), Power Query (Parameterized ETL).

## Installation

```bash
git clone https://github.com/yourusername/soc-dashboard-powerbi.git
cd soc-dashboard-powerbi
python -m venv .venv
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

### Python

The following global variables in the Python script modify the output of the simulated security logs.
```python
#----------Customizable values----------

NUMBER_OF_USERS = 50 # The number of users
DAYS_OF_DATA = 7 # Days simulated
RESOURCE_FAIL_CHANCE = { # The chance that a simulated login attempt will fail where 0 means no failures and 1 means all failures
    'Email': 0.04,
    'VPN': 0.13,
    'Database': 0.11,
    'FileServer': 0.12
}
USER_BRUTE_FORCE_ATTACK_CHANCE = 0.3 # The chance each day that a random user will have brute force failed logins

# Organization specific classifications
DEPARTMENTS = ['IT', 'HR', 'Finance', 'Sales']
ROLES = ['Standard', 'Manager', 'Admin']
RESOURCES = ['Email', 'VPN', 'Database', 'FileServer']

#----------End of customizable values----------
```

#### OUTPUT_FILE Name Complications
IGNORE THIS SECTION IF YOU DO NOT PLAN TO CHANGE THE OUTPUT FILE NAME.
2 Power BI elements depend on the CSV name. CHANGING IS NOT RECOMMENDED.
```python
OUTPUT_FILE = "security_logs.csv" # KEEP .csv
```

The following DAX script depends on the CSV file name. (Model view -> Data -> Model -> Semantic model -> Measures -> Top 20% Failed Users)

```dax
Top 20% Failed Users = 
VAR UserTable =
    ADDCOLUMNS(
        ALLSELECTED('security_logs'[UserID]),
        "FailCount",
            CALCULATE(
                COUNTROWS('security_logs'),
                'security_logs'[Status] = "Failed"
            )
    )

VAR Threshold =
    PERCENTILEX.INC(UserTable, [FailCount], 0.8)

VAR CurrentUserFails =
    CALCULATE(
        COUNTROWS('security_logs'),
        'security_logs'[Status] = "Failed"
    )

RETURN
IF(CurrentUserFails >= Threshold, 1, 0)
```

The SrcFolder also depends on the file name. Follow the steps found below in the Power BI File Path, but modify security_logs.csv to the new name.

### Power BI

#### File Path

You must configure the location of the CSV file on your machine. Go to Power Query editor -> Queries -> SrcFolder. Change the Current Value to the location of the script on your hard drive, followed by the CSV name. C:LOCATION_OF_PYTHON_SCRIPT\security_logs.csv

## Usage

### Python
Enter the soc-dashboard-powerbi folder and run
```bash
python generate_logs.py
```
Expected output:
```bash
Saved 3368 rows of data to security_logs.csv
```
When random brute force attacks occur:
```bash
Brute force attack on U0011 on 2026-04-13 at 19:38
Brute force attack on U0036 on 2026-04-17 at 05:58
Saved 3665 rows of data to security_logs.csv
```

Errors will be given in the format "Type of Exception: ERROR_TYPE"

#### RLS Roles

In a real-world dashboard, users would be signed in with their company-accociated emails and have restricted access to information. Row-level security (RLS) is implemented in this project based on the following demo usernames and roles.

| Username | Role | User ID |
| --- | --- | --- |
soc_analyst@demo.com | SOC Analyst | All
it_manager@demo.com | Department Manager | All
hr_manager@demo.com | Department Manager | All
julian@demo.com | Standard User | U0001
bob@demo.com | Standard User | U0002

- Click on the "View as" feature. (Report View -> View as)
- Select Other user and input a given Username and select its appropriate role.
- This will only display information at their access level.
