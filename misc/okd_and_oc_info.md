If you wish to change the code to be run in OKD:
- Be sure your code is runnable

Go to your repo root and execute these commands:

oc apply -k .

oc exec deploy/dep -- python src/db_helper.py

The latter command  erases the db in OKD and builds it anew.
