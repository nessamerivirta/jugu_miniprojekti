If you wish to change the code to be run in OKD:
- Be sure your code is runnable
- All is committed (and pushed)

OKD and  oc short info
https://github.com/ohjelmistotuotanto-hy/miniprojekti-boilerplate/blob/main/OKD.md

OKD web console
https://console-openshift-console.apps.okd-cs-test-0.k8s.cs.helsinki.fi/


Go to your repo root and execute these commands:

oc apply -k .

That command sees your git history in your local repo and fetches respective version from remote repo and pushes that version to our OKD project.

oc exec deploy/dep -- python src/db_helper.py

The latter command  erases the db in OKD and builds it anew.
