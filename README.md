# BudgetTool

Budgeting app that allows you to track your expenses and receive saving suggestions based on your spending habbits.

App is written in Python3.8, saves data in a PostgreSQL database, and allows the user to operate on the database utilising SQLAlchemy engine, pandas dataframes.
General purpose is to visualise accumulated data with matlab plots.

DISCLAIMER: Screens below do not contain real-world data nor do they reflect it, I wrote a program to generate around 1500 randomised entries for configured persons in the database.



database structure:

![image](https://user-images.githubusercontent.com/112565629/192290349-e488cbbe-2c83-4aa2-abb6-f5010f3b30ef.png)



app has barebone GUI, requires a running postgreSQL server on your machine and has listed options:

![image](https://user-images.githubusercontent.com/112565629/192290470-c1de1a77-f25b-4c30-b2ef-98cc7aea23f7.png)



using search will return a popup with database-query results:

empty filters show all payments:

![image](https://user-images.githubusercontent.com/112565629/189525912-e117b91e-fa39-4376-8b1b-444ec9d55b79.png)
![image](https://user-images.githubusercontent.com/112565629/192290538-8b5b122c-33f1-422a-bdd6-09c5ca6e2d8e.png)


more strict filtering will narrow the results down:

![image](https://user-images.githubusercontent.com/112565629/192291023-dadbe5aa-dc7b-47da-9af8-ad004fe2fb4d.png)
![image](https://user-images.githubusercontent.com/112565629/192291062-7a2a5a8b-8a56-4000-a3f1-682ff4a3dcf7.png)

Visualisation menu:

![image](https://user-images.githubusercontent.com/112565629/192291232-08d1031c-c6e5-4fc1-9442-f6b961450609.png)

One out of 7 available visualisation options:

![image](https://user-images.githubusercontent.com/112565629/192291443-3c758d46-a088-4b82-a47b-8a81d76f7a4c.png)





Planned functionality:

Redash connection and dashboard
