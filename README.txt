//Installing links:
https://www.jetbrains.com/pycharm/download/
https://www.python.org/downloads/
https://www.enterprisedb.com/downloads/postgres-postgresql-downloads            //Select 10.12 version
https://www.pgadmin.org/download/


pip install -r requirements.txt  //install requirements libraries
python manage.py startapp article //creating application command
python manage.py makemigrations  //before migrate have to use this command
python manage.py migrate    //migration
python manage.py runserver  //running on localhost

 //Activating Project Environment
-Before running project on windows, you have to enable virtaul environment.
-You must download the python from: https://www.python.org/downloads/ this url.
-Then you must use this commands for enable virtual env:
    cd wvenv/Scripts
    activate
    cd ..
    cd ..
If the virtual environment was enabled, you have to see like this
(wvenv) D:\ceng-407-408-2019-2020-ANKADES-Educational-Social-Sharing-Platform> on terminal (cmd). The important point is (wvenv).


