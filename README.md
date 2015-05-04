# pop-webhelp
PKSU Projekt 2015

## Installation
* Vær sikker på at du har `pip` og `python` installeret
* Kør `git clone https://github.com/christiankjaer/pop-webhelp`
* Kør `pip install -r requirements.txt`

##
Applikationen kan så køres med `python run.py`
Først skal der dog lige oprettes en database med `python create_db.py`.
Databasen kan udfyldes med dummy-data med `python fillout_db.py`. Det giver mulighed for at kunne logge ind med:
* id=abc123
* pw=pwd

Derudover skal der sættes gmail bruger/password

På Linux/Mac er det med
* `export APP_MAIL_USERNAME="gmail-user"`
* `export APP_MAIL_PASSWORD="gmail-password"`

På Windows fra cmd
* `set APP_MAIL_USERNAME=gmail-user`
* `set APP_MAIL_PASSWORD=gmail-password`

På Windows fra PowerShell
* `$env:APP_MAIL_USERNAME="gmail-user"`
* `$env:APP_MAIL_PASSWORD="gmail-password"`
