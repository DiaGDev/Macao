## Imports ##

from tkinter import *
import sqlite3, datetime

conn = sqlite3.connect('database.db')
with conn:
    cur =conn.cursor()
    
## Functions  ##
def register():#the register function is the tkinter part of the registration form by allowing the user to register with a username and password
    screen1= Toplevel(screen)
    screen1.title('Register')
    screen1.geometry('300x250')

    global username#use of global to allow modification of variable 
    global password
    username=StringVar()
    password=StringVar()


    Label(screen1,text='Username ').pack()
    Entry(screen1,textvariable=username).pack()
    Label(screen1,text='Password ').pack()
    Entry(screen1,textvariable=password, show='*').pack()#not visible
    Label(screen1, text='').pack()
    Button(screen1, text='Register', width='10', height='2', command=register_user).pack()


def gameIdUnique():#method used to create a gameID
    string=str(receivedat)
    game=information[2]
    cur.execute("""INSERT OR IGNORE INTO Games
                VALUES(?,?)""",(game, string))#new game records are added to the database
    conn.commit()
    return game

def playedPutIn():#adds data to the linking table
    usableList=information#list with necessary information
    final=finalGameID#gameIdUnique result
    won=False
    if usableList[1]==usableList[3]:#if the player number matches the winner number
        won=True#third variable in linking table is set to 1
    cur.execute("SELECT PlayerID FROM Players WHERE Username=?",(usableList[0],))
    data=cur.fetchall()
    retrievedPlayerId=data[0][0]#uses the username to retrieve the PlayerId
    cur.execute('INSERT OR IGNORE INTO Played VALUES(?,?,?)',(retrievedPlayerId, final, won))
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM Played WHERE Player_ID=? AND Won==True",(retrievedPlayerId,))
    count=cur.fetchall()
    if count:#if they won a game it will count if the new value of winned is bigger and it will update the database accordingly
        cur.execute('INSERT OR IGNORE INTO Highscores VALUES(?,?,?)',(retrievedPlayerId, usableList[0], count[0][0]))
        conn.commit()
        cur.execute("SELECT Points FROM Highscores WHERE Player_ID=?",(retrievedPlayerId,))
        comparable=cur.fetchall()[0][0]
        if count[0][0]>comparable:
            cur.execute('UPDATE Highscores SET Points=? WHERE Player_ID=?',(count[0][0],retrievedPlayerId,))
            conn.commit()
    else:
        cur.execute('INSERT OR IGNORE INTO Highscores VALUES(?,?,?)',(retrievedPlayerId, usableList[0], 0))
        conn.commit()
        cur.execute("SELECT Points FROM Highscores WHERE Player_ID=?",(retrievedPlayerId,))
        comparable=cur.fetchall()[0][0]
    print('successful')
    
    
    
def register_user():#used to connect and create database
    username_info=username.get()
    password_info=password.get()
    registrationDate=datetime.datetime.now().date()
    Identification=username_info+str(registrationDate)#creates an unique PlayerID by adding the Username to the date of registration
    #use of 'IF NOT EXISTS' for testing purposes
    cur.execute(""" CREATE TABLE IF NOT EXISTS Players(
            PlayerID TEXT PRIMARY KEY,
            Username TEXT,
            Password TEXT)""")
    cur.execute(""" CREATE TABLE IF NOT EXISTS Games(
            GamesID INTEGER PRIMARY KEY,
            Time TIME)""")
    cur.execute(""" CREATE TABLE IF NOT EXISTS Played(
            Player_ID TEXT NOT NULL,
            Games_ID INTEGER NOT NULL,
            Won BOOLEAN,
            FOREIGN KEY(Player_ID)
                REFERENCES Player(PlayerID),
            FOREIGN KEY(Games_ID)
                REFERENCES Games(GameID))""")
    cur.execute(""" CREATE TABLE IF NOT EXISTS Highscores(
            Player_ID TEXT NOT NULL PRIMARY KEY,
            Username_ TEXT NOT NULL,
            Points INTEGER,
            FOREIGN KEY(Player_ID)
                REFERENCES Player(PlayerID),
            FOREIGN KEY(Username_)
                REFERENCES Player(Username))""")
    cur.execute("SELECT Username FROM Players WHERE PlayerID=?",(Identification,))
    data=cur.fetchall()
    if len(data)==0:
        #use of 'OR IGNORE' to block the possibility of two identical entries
        cur.execute('INSERT OR IGNORE INTO Players VALUES(?,?,?)',(Identification, username_info, password_info,))
        conn.commit()
        print('Registered successfully!')
        login()
    else:
        print('Username Taken')

    
#checking if new user already exists
def verify():
    username_2=username2.get()
    password_2=password2.get()
    cur.execute("SELECT Username, Password FROM Players WHERE Username=? AND password=?",(username_2, password_2,))
    data=cur.fetchall()
    if len(data)==0:
        print("User doesn't exist, please register first")
    else:
        print('Logged in')
        pick()
    return username_2
        
def pick():#new screen allowing for choices
    c=pickToClose
    screen3= Toplevel(screen)
    screen3.title('Pick')
    screen3.geometry('300x250')
    Label(screen3, width='300', height='2', font=('Comic Sans',13)).pack()
    Label(text='').pack()
    Button(screen3,text='View Your Score', height='2', width='30', command=viewScores).pack()
    Label(screen3,text='').pack()
    Button(screen3,text='Play', height='2',width='30', command=c).pack()
    
def pickToClose():
    c=screen.destroy()
    pick()
    
def viewScores():#display of the game records for username and score
    Username=username2.get()
    cur.execute("SELECT PlayerID FROM Players WHERE Username=?",(Username,))
    data=cur.fetchall()
    print('           ~~~~~~~~Records~~~~~~~~\n')
    for row in cur.execute('SELECT * FROM Played WHERE Player_ID=?' ,(data[0][0],)):
            print('Your PlayerId: ',row[0],', GameId: ',row[1],', 1 for win 0 for loss: ', row[2])
    print('           ~~~~~~~Highscores~~~~~~~\n')
    count=0
    for row in cur.execute('SELECT Username_, Points FROM Highscores ORDER BY Points DESC'):
            count=count+1
            print(count,'. ',row[0],'-',row[1], 'Games Won')
    
    
def Play():#used to store information from client after game ended, by adding to the list containing the Username
    #attempt=username_2
    information=[]
    information.append(username2.get())
    return information
        
        
#similar subroutine as register for login redireting to a new page       
def login():
    screen2= Toplevel(screen)
    screen2.title('Login')
    screen2.geometry('300x250')

    global username2
    global password2
    username2=StringVar()
    password2=StringVar()

    Label(screen2,text='Username ').pack()
    Entry(screen2,textvariable=username2).pack()
    Label(screen2,text='Password ').pack()
    Entry(screen2,textvariable=password2, show='*').pack()
    Label(screen2, text='').pack()
    Button(screen2, text='Login', width='10', height='2', command=verify).pack()
    
def main_screen():
    global screen
    screen= Tk()
    screen.geometry('300x250')
    screen.title('Main')
    Label(text='Login or Register', bg='grey', width='300', height='2', font=('Comic Sans',13)).pack()
    Label(text='').pack()
    Button(text='Login', height='2', width='30', command=login).pack()
    Label(text='').pack()
    Button(text='Register', height='2',width='30', command=register).pack()

    screen.mainloop()
    
##Main##    
main_screen()
information=Play()
exec(open('client.py').read())
receivedat=datetime.datetime.now().replace(minute=0, second=0, microsecond=0)#gets the time at which game ended
for each in this_sendable:
    information.append(each)
information.append(str(receivedat))#creates the final list used in functions containing(in order):[Username,PlayerNumber,GameId(sent by client as integer value), winner, End Game time]
finalGameID=gameIdUnique()
playedPutIn()
conn.close()
