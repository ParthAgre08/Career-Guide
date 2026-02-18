from flask import Flask,render_template,request,redirect, session
import pymysql
from datetime import datetime

app = Flask(__name__)# __name__ = It tells the Flask application that this file’s location is the main folder where static, templates, and other files are located.


app.secret_key = "super_secret_key"
# Without this → session will not work.

connector = pymysql.connect(
host="localhost",
user="flaskuser",
password="12345",
database="carrier_guider" )
cur = connector.cursor()


#We then use the route() decorator to tell Flask what URL should trigger our function.
@app.route("/")
def starting():
    return render_template("register.html")

@app.route("/login",methods=["GET","POST"])
def already_register():
    if request.method == "POST":
       email = request.form["email"]
       password = request.form["password"]

       cur.execute("SELECT * FROM USERS WHERE Email=%s AND Password=%s", (email, password))
       user = cur.fetchone()
       if user:
          print(user)
          session["user"] = user[1]
          session["email"] = email
          session["education"] = user[4]
          return render_template("main.html", name=user[1], greeting="Welcome back")
       else:
          return render_template("login.html",error = "Incorrect Password")

    return render_template("login.html")


@app.route("/register",methods=["GET","POST"])
def register():
   if request.method == "POST":
      name = request.form["name"] 
      email = request.form["email"]    
      password = request.form["password"] 
      education = (request.form["education"])
      print(f"Name :- {name} \nEmail :- {email} \nPassword :- {password} \nEducation :- {education}")
      

      cur.execute(f"SELECT * FROM USERS WHERE Email = '{email}'")
      user = cur.fetchone()
      
      print(f"user :- {user}")

      if user:
         return render_template("register.html",error= "Email is alredy registerd")

      # cur.execute("use carrier_guider;")
      # connector.commit()
      cur.execute(f"INSERT INTO USERS (name,email,password,education) values ('{name}','{email}','{password}','{education}')")
      connector.commit()
      session["user"] = name
      session["email"] = email
      session["education"] = education
      return render_template("main.html",name=name,greeting="Welcome to Carrier Guider")
   return render_template("register.html")
    

@app.route("/assessment" , methods =["GET","POST"])
def assessment():
   education = session.get("education")
   

   if(request.method == "POST"):
      if(education == 'Grade 10'):
         english = int(request.form.get("english"))
         math = int(request.form.get("math"))
         science = int(request.form.get("science"))
         socialscience = int(request.form.get("socialscience"))
         secondlanguage = int(request.form.get("secondlanguage"))

         n_eng = n_sci =n_math =n_social =n_second = 0
         if(request.form.get("n_eng")): 
            n_eng = int(request.form.get("n_eng"))
            english = (english + n_eng )/2

         if(request.form.get("n_math")):
            n_math = int(request.form.get("n_math"))
            math = (math + n_math )/2  
         if(request.form.get("n_sci")):
            n_sci = int(request.form.get("n_sci"))
            science = (science + n_sci )/2
         if(request.form.get("n_social")):            
            n_social = int(request.form.get("n_social"))
            socialscience = (socialscience + n_social )/2
         if(request.form.get("n_second")):            
            n_second = int(request.form.get("n_second"))
            secondlanguage = (secondlanguage + n_second )/2
         

         print(f"English :- {english} \nMath :- {math} \nScience :- {science} \nSocial Science :- {socialscience} \nSecond Language :- {secondlanguage}")
      
      
      elif(education == 'Grade 12 Science(PCM)'):
         english = request.form["english"]
         mathematics = request.form["mathematics"]
         physics = request.form["physics"]
         chemistry = request.form["chemistry"]
         
         print(f"English :- {english} \nMathematics :- {mathematics} \nScience :- {physics} \nSocial Science :- {chemistry} ")
      
      elif(education == 'Grade 12 Science(PCB)'):
         english = request.form["english"]
         biology = request.form["biology"]
         physics = request.form["physics"]
         chemistry = request.form["chemistry"]
         
         print(f"English :- {english} \nBiology :- {biology} \nPhysics :- {physics} \nChemistry :- {chemistry} ")
      
      elif(education == 'Grade 12 Science(PCMB)'):
         english = request.form["english"]
         mathematics = request.form["mathematics"]
         physics = request.form["physics"]
         chemistry = request.form["chemistry"]
         biology = request.form["biology"]
         
         print(f"English :- {english} \nMath :- {mathematics} \nScience :- {physics} \nSocial Science :- {chemistry} \nBiology :- {biology}")
      
      elif(education == 'Grade 12 Commerce'):
         english = request.form["english"]
         mathematics = request.form["mathematics"]
         physics = request.form["physics"]
         chemistry = request.form["chemistry"]
         
         print(f"English :- {english} \nMath :- {mathematics} \nScience :- {physics} \nSocial Science :- {chemistry} ")
      
      elif(education == 'Grade 12 Arts'):
         english = request.form["english"]
         mathematics = request.form["mathematics"]
         physics = request.form["physics"]
         chemistry = request.form["chemistry"]
         
         print(f"English :- {english} \nMath :- {mathematics} \nScience :- {physics} \nSocial Science :- {chemistry} ")
      
      elif(education == 'Diploma/Polytechnic'):
         english = request.form["english"]
         mathematics = request.form["mathematics"]
         physics = request.form["physics"]
         chemistry = request.form["chemistry"]
         
         print(f"English :- {english} \nMath :- {mathematics} \nScience :- {physics} \nSocial Science :- {chemistry} ")
      
      elif(education == 'UG'):
         english = request.form["english"]
         mathematics = request.form["mathematics"]
         physics = request.form["physics"]
         chemistry = request.form["chemistry"]
         
         print(f"English :- {english} \nMath :- {mathematics} \nScience :- {physics} \nSocial Science :- {chemistry} ")
         
      return render_template()


   if(education == 'Grade 10'):
      return render_template("grade10.html",Education = education)

   elif(education == 'Grade 12 Science(PCM)'):
      return render_template("grade12pcm.html",Education = education)

   elif(education == 'Grade 12 Science(PCB)'):
      return render_template("grade12pcb.html",Education = education)

   elif(education == 'Grade 12 Science(PCMB)'):
      return render_template("grade12pcmb.html",Education = education)

   elif(education == 'Grade 12 Commerce'):
      return render_template("grade12commerce.html",Education = education)

   elif(education == 'Grade 12 Arts'):
      return render_template("grade12arts.html",Education = education)

   elif(education == 'Diploma/Polytechnic'):
      return render_template("dip_pol.html",Education = education)

   elif(education == 'UG'):
      return render_template("ug.html",Education = education)
   return render_template("assessment.html",Education = education)


@app.route("/main",methods=["GET","POST"])
def main():
   return render_template("main.html")
 

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/register")

app.run()
