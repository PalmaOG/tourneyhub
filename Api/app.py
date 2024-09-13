import os
from flask import Flask,redirect,render_template, request, session
from werkzeug.security import generate_password_hash,check_password_hash
from ConnectDB import Connect,ConnectSocial
from datetime import date,datetime
from rss import Parser, LiveMatches  


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'Api/static/img/Profiles'

app.secret_key = "I'm secret key"

@app.route("/")
def start():
    Parser()
    # Получение всех постов
    conn = ConnectSocial()
   
    with conn.cursor() as cursor:
        curr_query = "SELECT * FROM posts ORDER BY idPost DESC"
        cursor.execute(curr_query)
        post_out = cursor.fetchall()
    
    # Получение всех постов
    return render_template("index.html" , news_data = post_out)

@app.route("/register")
def Regist():
    conn = ConnectSocial()
    if (conn):
        Reg_email = request.args['email']
        Reg_password = generate_password_hash(request.args['passwd'])
        Reg_nickname = request.args['nick']
        Reg_date = date.today()
        with conn.cursor() as cursor:
            curr_query = f"SELECT * FROM `social`.`users` WHERE Email = '{Reg_email}' OR Nickname = '{Reg_nickname}'"
            cursor.execute(curr_query)
            if cursor.rowcount == 1:
                return "Пользователь c такой почтой или никнеймом уже существует!"
            elif cursor.rowcount == 0:
                curr_query = "INSERT INTO `social`.`users` " \
                    "(`Nickname`, `AvatarSrc`, `Email`, `Password`, `RegDate`) VALUES " \
                    f'("{Reg_nickname}", "/static/img/Profiles/avatar.png","{Reg_email}", "{Reg_password}", "{Reg_date}");'
                cursor.execute(curr_query)
                conn.commit()
                curr_query = f"SELECT Nickname,idUser FROM `social`.`users` WHERE Email = '{Reg_email}'"
                cursor.execute(curr_query)
                result = cursor.fetchone()
                session['LoggedIn'] = True
                session['ID'] = result['idUser']
                session['Username'] = result['Nickname']
                return start()
    else:
        return "Ошибка!" 

@app.route("/login",methods=['GET','POST'])
def Login():
    conn = ConnectSocial()
    Log_email = request.form['email']
    Log_password = request.form['passwd']
    with conn.cursor() as cursor:
        curr_query = f"SELECT * FROM `social`.`users` WHERE Email = '{Log_email}'"
        cursor.execute(curr_query)
        if cursor.rowcount == 1:
            curr_query = f"SELECT Nickname,Password,idUser, AvatarSrc FROM `social`.`users` WHERE Email = '{Log_email}'"
            cursor.execute(curr_query)
            result = cursor.fetchone()
            if check_password_hash(result['Password'],Log_password):
                session['LoggedIn'] = True
                session['ID'] = result['idUser']
                session['Username'] = result['Nickname']
                session['Avatar'] = result['AvatarSrc']
                return redirect('/')
            else:
                return "Неверный пароль!"
        else:
            return "Такого пользователя не существует!"

@app.route("/logout",methods=['GET','POST'])
def Logout():
    session['LoggedIn'] = False
    session.pop('ID', None)
    session.pop('Username', None)
    return redirect('/')

@app.route('/profile/<idProfile>')
def Profile_Page(idProfile):
    conn = ConnectSocial()
    with conn.cursor() as cursor:
        curr_query = f"SELECT * FROM `users` WHERE idUser = '{idProfile}'"
        cursor.execute(curr_query)
        user_info = cursor.fetchone()
    return render_template('Profile.html', info = user_info, id = idProfile)

@app.route('/profile/<idProfile>/update_info', methods=['POST'])
def Update_Info(idProfile):
    conn = ConnectSocial()
    idPr = request.form['idProfile']
    Upd_Fname = request.form['Fname']
    Upd_Lname = request.form['Lname']
    Upd_Birth = request.form['Birth']
    if Upd_Birth:
        pass
    else:
        Upd_Birth = '1900-01-01'
    Upd_Discord = request.form['Discord']
    Upd_Nickname = request.form['Nickname']
    Upd_Email = request.form['Email']
     
    f = request.files['file']
    if f:
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], f"Profile_{idPr}.jpg"))
    

    with conn.cursor() as cursor:
        curr_query = f"UPDATE social.users SET Nickname = '{Upd_Nickname}', AvatarSrc = '/static/img/Profiles/Profile_{idPr}.jpg' , Email = '{Upd_Email}', FirstName = '{Upd_Fname}', LastName = '{Upd_Lname}', Birth = '{Upd_Birth}' , Discord = '{Upd_Discord}' WHERE idUser = '{idPr}' ;"
        cursor.execute(curr_query)
    conn.commit()
    session['Username'] = Upd_Nickname
    return redirect(f'/profile/{idPr}')
#redirect( f'/profile/{idProfile}')

@app.route("/dota2")
def Dota_Page():
    LiveMatches()
    conn = Connect()
    with conn.cursor() as cursor:
        curr_query = "SELECT * FROM matches WHERE Game = 'Dota 2' AND Status = 'Live';"
        cursor.execute(curr_query)
        am = cursor.fetchall()
        curr_query = "SELECT idTeam,TeamName,teams.AltName, matches.* FROM matches,teams WHERE matches.Game = 'Dota 2' AND (AltName = FirstTeam or AltName = SecondTeam) AND matches.Status = 'Live';"
        cursor.execute(curr_query)
        t = cursor.fetchall()
    return render_template("Dota_Landing.html", list_live_matches = am, list_teams = t)

@app.route("/dota2/players")
def Dota_Players():
    conn = Connect()
    with conn.cursor() as cursor:
        curr_query = "SELECT * FROM players WHERE Game = 'Dota 2' ORDER BY Country;"
        cursor.execute(curr_query)
        ap = cursor.fetchall()
        curr_query = "SELECT DISTINCT Country FROM players WHERE Game = 'Dota 2' ORDER BY Country;"
        cursor.execute(curr_query)
        cntrs = cursor.fetchall()
    return render_template("AllPlayers.html", list_players = ap, list_countries = cntrs)

@app.route("/dota2/players/<idplayer>")
def Dota_Player(idplayer):
    conn = Connect()
    with conn.cursor() as cursor:
        curr_query = f"SELECT * FROM players WHERE idPlayer = {idplayer}; "
        cursor.execute(curr_query)
        Onep = cursor.fetchone()
        curr_query = f"SELECT TeamName FROM teams WHERE idTeam = {Onep['idTeam']};"
        cursor.execute(curr_query)
        Team_Name = cursor.fetchone()
    return render_template("Player.html" , player = Onep , TeamName = Team_Name)

@app.route("/dota2/teams")
def Dota_Teams():
    conn = Connect()
    with conn.cursor() as cursor:
        curr_query = "SELECT * FROM teams WHERE Game = 'Dota 2';"
        cursor.execute(curr_query)
        at = cursor.fetchall()
    return render_template("AllTeams.html", list_teams = at)

@app.route("/dota2/teams/<idTeam>")
def Dota_Team(idTeam):
    conn = Connect()
    with conn.cursor() as cursor:
        curr_query = f"SELECT * FROM teams WHERE idTeam = {idTeam} ;"
        cursor.execute(curr_query)
        Onet = cursor.fetchone()
        curr_query = f"SELECT Nickname FROM players WHERE idPlayer = '{Onet['idCaptain']}';"
        cursor.execute(curr_query)
        cap = cursor.fetchone()
        curr_query = f"SELECT Nickname FROM players WHERE idPlayer = '{Onet['idCoach']}';"
        cursor.execute(curr_query)
        cch = cursor.fetchone()
        curr_query = f"SELECT * FROM players WHERE idTeam = '{idTeam}' LIMIT 5;"
        cursor.execute(curr_query)
        sost = cursor.fetchall()
    return render_template("Team.html", team = Onet, Captain = cap, Coach = cch, list_tp = sost)

@app.route("/dota2/tournaments")
def Dota_Tournaments():
    conn = Connect()
    with conn.cursor() as cursor:
        curr_query = f"SELECT * FROM tournaments WHERE Game = 'Dota 2';"
        cursor.execute(curr_query)
        at = cursor.fetchall()
    return render_template("AllTournaments.html", list_tournaments = at)

@app.route("/dota2/tournaments/<idTournament>")
def Dota_Tournament(idTournament):
    conn = Connect()
    with conn.cursor() as cursor:
        curr_query = f"SELECT * FROM tournaments WHERE idTournament = '{idTournament}';"
        cursor.execute(curr_query)
        Onet = cursor.fetchone()
        curr_query = f"SELECT * FROM participants WHERE idTournament = '{idTournament}';"
        cursor.execute(curr_query)
        membrs = cursor.fetchall()
    return render_template("Tournament.html", tournament = Onet, list_members = membrs)

@app.route("/dota2/matches/<idMatch>")
def Dota_Match(idMatch):
    conn = Connect()
    with conn.cursor() as cursor:
        curr_query = f"SELECT * FROM matches WHERE idMatch = {idMatch}"
        cursor.execute(curr_query)
        om = cursor.fetchone()
        curr_query = f"SELECT teams.TeamName,teams.AltName,teams.ImgSrc as TeamSrc, players.* FROM matches,teams,players WHERE matches.Game = 'Dota 2' AND (AltName = FirstTeam ) AND teams.idTeam = players.idTeam AND matches.idMatch = {idMatch};"
        cursor.execute(curr_query)
        Team1 = cursor.fetchall()
        curr_query = f"SELECT teams.TeamName,teams.AltName,teams.ImgSrc as TeamSrc, players.* FROM matches,teams,players WHERE matches.Game = 'Dota 2' AND (AltName = SecondTeam ) AND teams.idTeam = players.idTeam AND matches.idMatch = {idMatch};"
        cursor.execute(curr_query)
        Team2 = cursor.fetchall()
    return render_template("Match.html", match_info = om, Team1_info = Team1, Team2_info = Team2)

@app.route("/cs2")
def CS_Page():
    return "Все о кс!"

@app.route("/Valorant")
def Valorant_Page():
    return "Все о валоранте!"


@app.route("/post/<idPost>")
def PostPage(idPost):
    conn = ConnectSocial()
    with conn.cursor() as cursor:
        curr_query = f"SELECT * FROM posts WHERE idPost = {idPost} ;"
        cursor.execute(curr_query)
        post = cursor.fetchone()
        curr_query = f"SELECT comments.*,users.AvatarSrc FROM social.comments, social.users WHERE idPost = {idPost} AND comments.Nickname = users.Nickname;;"
        cursor.execute(curr_query)
        comments = cursor.fetchall()
    return render_template("Post.html", post_data = post, comments_data = comments)

@app.route("/post/<idPost>/WriteComment")
def WriteComment(idPost):
    txt = request.args['text']
    uID = request.args['user_id']
    Comment_date = datetime.now()
    conn = ConnectSocial()
    with conn.cursor() as cursor:
        curr_query = f'SELECT Nickname FROM users WHERE idUser = "{uID}";'
        cursor.execute(curr_query)
        nick = cursor.fetchone()
        N=nick['Nickname']
        curr_query = f'INSERT INTO comments (`Nickname`, `Text`, `idUser`, `idPost`, `Date`) VALUES ("{N}","{txt}", "{uID}", "{idPost}", "{Comment_date}");'
        cursor.execute(curr_query)
    conn.commit()    
    return redirect(f"/post/{idPost}#comm")


if __name__ == "__main__":
    app.run(debug="on")