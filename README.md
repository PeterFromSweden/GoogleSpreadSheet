# GoogleSpreadSheet

## Credentials
https://console.developers.google.com/apis  
Create/select project in top bar  
Dashboard | Enable APIs and services. Drive & Sheet  
Credentials|Create Service Account Key role=project editor  
Rename json to 'Credentials.json' and put into script folder  

## Raspberry
### Install python3, pip  
sudo apt install python3 python3-pip

### Install python packages for google-api  
(pip3 install google-api-core)  
pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib oauthclient
