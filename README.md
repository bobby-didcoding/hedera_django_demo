# hedera_django_demo
Django project that uses Hedera Hashgraph HBAR to pay for goods

Note: You need to create a testnet acount with Hedera to follow this tutorial

visit: https://portal.hedera.com/register

1) save your Acc number to your environment varibles as OPERATOR_ID
2) save your privte key to your environmanet variables as OPERATOR_KEY
3) Ensure you have JDK Installed at least version 11
4) Add JAVA_HOME to you environment variables and ensure the path is to your version of JDK - mine is C:\Program Files\Java\jdk-16.0.1
5) Edit 'Path' in environment variables and add %JAVA_HOME%\bin\server

6) cd to development directory
7) mkvirtualenv <env name>
8) mkdir hedera_django_demo
9) clone repository to new directory
10) pip install -r requirements.txt
12) python manage.py makemigrations
13) python manage.py migrate
14) python manage.py runserver
15) https://localhost:8000 - Bob's your uncle!! 

