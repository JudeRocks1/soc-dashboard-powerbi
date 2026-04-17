# Security Operations & Access Monitoring Dashboard

So far this is a python script that simulates login events, will update this section of the README once the csv is applied.

## Installation

```bash
git clone https://github.com/yourusername/soc-dashboard-powerbi.git
cd soc-dashboard-powerbi
python -m venv .venv
source .venv/bin/activate
pip install pandas
```

## Usage

# Python

```bash
python generate_logs.py
```
The following global variables in the python script modify the output of the simulated security logs.
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

# Organization specific classifications
DEPARTMENTS = ['IT', 'HR', 'Finance', 'Sales']
ROLES = ['Standard', 'Manager', 'Admin']
RESOURCES = ['Email', 'VPN', 'Database', 'FileServer']

#----------End of customizable values----------
```

# Power BI

The following dax script will break or need to be modified if the name of the csv file is changed.

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

To avoid naming conflict issues only modify the Customizable values in Python and use the following steps to visualize a new csv file:
- TODO

