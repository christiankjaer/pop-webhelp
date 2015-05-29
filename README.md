# pop-webhelp
PKSU Projekt 2015

## Installation
* Vær sikker på at du har `pip`, `python2` og `redis` installeret.
* Kør `git clone https://github.com/christiankjaer/pop-webhelp`.
* Kør `pip install -r requirements.txt`.

##
Applikationen kan så køres med `python run.py`, dog kræver det at der også kører en redis server, hvilket typisk kan startes med `redis-server` afhængig af hvordan det er sat op.

Hvis der ikke allerede er oprettet en database kan det gøres med `python create_db.py`.

Databasen kan udfyldes med dummy-data med `python fillout_db.py`, hvilket giver mulighed for at se de forskellige typer af spørgsmål. 
Det giver desuden mulighed for at kunne logge ind med to brugere; en der skal efterligne en studerende og en der er en admin:

Studerende:
* id=abc123
* pw=pwd

Admin:
* id=def456
* pw=test

Hvis man ønsker at oprette yderligere brugere skal der derudover sættes gmail brugernavn og password. Det er ikke nødvendigt hvis man bare bruger de to ovennævnte brugere.

På Linux/Mac er det med
* `export APP_MAIL_USERNAME="dit gmail-username"`
* `export APP_MAIL_PASSWORD="dit gmail-password"`

På Windows fra cmd
* `set APP_MAIL_USERNAME=dit gmail-username`
* `set APP_MAIL_PASSWORD=dit gmail-password`

På Windows fra PowerShell
* `$env:APP_MAIL_USERNAME="dit gmail-username"`
* `$env:APP_MAIL_PASSWORD="dit gmail-password"`
