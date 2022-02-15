import mysql.connector

import json
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="anime_database"
)
mycursor = mydb.cursor()

# sql = "CREATE TABLE AnimeUncleanedTable (Name varchar(255),  Description TEXT,  Type varchar(50), Episodes varchar(50), Status varchar(50), AiredFrom varchar(50), AiredTo varchar(50), Premiered varchar(100), Broadcast varchar(255), Producers varchar(255), Licensors varchar(255), Studios varchar(255), Source varchar(255), Genre varchar(255), Themes TEXT, Demographic varchar(255), Duration varchar(255), Rating varchar(255), Score varchar(255), Ranked varchar(255), Popularity varchar(255), Members varchar(255), Favorites varchar(255))"
# mycursor.execute(sql)

f = open('first50.json')
data = json.load(f)
for i in data:
  sql = "INSERT INTO AnimeUncleanedTable (Name, Description, Type, Episodes, Status, AiredFrom, AiredTo, Producers, Licensors, Studios, Source, Duration, Rating, Score, Ranked, Popularity, Members, Favorites) Values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
  val = (i['Name'], i['Description'], i['Type'], i['Episodes'], i['Status'], 
  i['AiredFrom'], i['AiredTo'], i['Producers'], 
  i['Licensors'], i['Studios'], i['Source'], i['Duration'], i['Rating'], i['Score'], i['Ranked'], 
  i['Popularity'], i['Members'], i['Favorites'])

  mycursor.execute(sql, val)

# for j in data:
#   j['Genres']
f.close()

# 
# sql = "SELECT import_data.* FROM OPENROWSET(BULK 'D:\Projects\Personal-Dashboard\first50.json', SINGLE_CLOB) as j CROSS APPLY OPENJSON(BulkColumn) WITH(Name varchar(255),  Description TEXT,  Type varchar(50), Episodes int, Status varchar(50), AiredFrom varchar(50), AiredTo varchar(50), Premiered varchar(100), Broadcast varchar(255), Producers varchar(255), Licensors varchar(255), Studios varchar(255), Source varchar(255), Genre varchar(255), Themes TEXT, Demographic  varchar(255), Duration varchar(255), Rating varchar(255), Score varchar(255), Ranked varchar(255), Popularity varchar(255), Members varchar(255), Favorites varchar(255)) AS import_data"
# mycursor.execute(sql)

mydb.commit()

