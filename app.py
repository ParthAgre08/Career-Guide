from flask import Flask,render_template,request,redirect, session,url_for
import requests
import pymysql
from datetime import datetime
from stream_profiles import STREAM_PROFILES
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from degree_profiles import COMMERCE_DEGREE_PROFILES, PCB_DEGREE_PROFILES, PCM_DEGREE_PROFILES
import markdown

app = Flask(__name__)# __name__ = It tells the Flask application that this file’s location is the main folder where static, templates, and other files are located.


app.secret_key = "super_secret_key"
# Without this → session will not work.

connector = pymysql.connect(
host="localhost",
user="flaskuser",
password="12345",
database="carrier_guider" )
cur = connector.cursor()


#We then use the route() deco    rator to tell Flask what URL should trigger our function.
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
    

@app.route("/main",methods=["GET","POST"])
def main():
   return render_template("main.html")
 

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
            english = (english*0.85) + (n_eng*0.15)
            

         if(request.form.get("n_math")):
            n_math = int(request.form.get("n_math"))
            math = (math*0.85) + (n_math*0.15)
         if(request.form.get("n_sci")):
            n_sci = int(request.form.get("n_sci"))
            science = (science*0.85) + (n_sci*0.15)
         if(request.form.get("n_social")):            
            n_social = int(request.form.get("n_social"))
            socialscience = (socialscience*0.85) + (n_social*0.15)
         if(request.form.get("n_second")):            
            n_second = int(request.form.get("n_second"))
            secondlanguage = (secondlanguage*0.85) + (n_second*0.15)
         
         # storing the marks in session
         session["English"] = english
         session["Math"] = math
         session["Science"] = science
         session["Social Science"] = socialscience
         session["Second Language"] = secondlanguage
         session["Language"] = ((english*0.7)+(secondlanguage*0.3))

         session["student_vector"] = {
            "Math": math/100,
            "Science": science/100,
            "Social": socialscience/100,
            "Language": ((english*0.7)+(secondlanguage*0.3))/100
         }

         # storing the marks in student_marks table 
         cur.execute(f"INSERT INTO student_marks (email,education,subject,marks) VALUES ('{session['email']}', '{education}', 'Language', {session['Language']})")
         connector.commit()

         cur.execute(f"INSERT INTO student_marks (email,education,subject,marks) VALUES ('{session['email']}', '{education}', 'Math', {math})")
         connector.commit()

         cur.execute(f"INSERT INTO student_marks (email,education,subject,marks) VALUES ('{session['email']}', '{education}', 'Science', {science})")
         connector.commit()

         cur.execute(f"INSERT INTO student_marks (email,education,subject,marks) VALUES ('{session['email']}', '{education}', 'Social Science', {socialscience})")
         connector.commit()

         # cur.execute(f"INSERT INTO student_marks (email,education,subject,marks) VALUES ('{session['email']}', '{education}', 'Second Language', {secondlanguage})")
         connector.commit()

         print(f"Math :- {math} \nScience :- {science} \nSocial Science :- {socialscience} \nLanguage :- {session['Language']} ")
      
      
      elif(education == 'Grade 12 Science(PCM)'):
         english = int(request.form.get("english"))
         mathematics = int(request.form.get("math"))
         physics = int(request.form.get("physics"))
         chemistry = int(request.form.get("chemistry"))
         
         n_eng = n_math = n_phy = n_chem = 0
         if(request.form.get("n_eng")):
            n_eng = int(request.form.get("n_eng"))
            english = (english*0.85) + (n_eng*0.15)

         if(request.form.get("n_math")):
            n_math = int(request.form.get("n_math"))
            mathematics = (mathematics*0.85) + (n_math*0.15)
         
         if(request.form.get("n_phy")):
            n_phy = int(request.form.get("n_phy"))
            physics = (physics*0.85) + (n_phy*0.15)

         if(request.form.get("n_chem")):  
            n_chem = int(request.form.get("n_chem"))
            chemistry = (chemistry*0.85) + (n_chem*0.15)

         #storing the marks in session
         session["English"] = english
         session["Math"] = mathematics
         session["physics"] = physics
         session["chemistry"] = chemistry

         session["student_vector"] = {
            "Math": mathematics/100,
            "Physics": physics/100,
            "Chemistry": chemistry/100,
            "English": english/100
         }

         cur.execute(f"INSERT INTO student_marks (email,education,subject,marks) VALUES ('{session['email']}', '{education}', 'English', {english})")
         connector.commit()   

         cur.execute(f"INSERT INTO student_marks (email,education,subject,marks) VALUES ('{session['email']}', '{education}', 'Math', {mathematics})")
         connector.commit()

         cur.execute(f"INSERT INTO student_marks (email,education,subject,marks) VALUES ('{session['email']}', '{education}', 'Physics', {physics})")
         connector.commit()

         cur.execute(f"INSERT INTO student_marks (email,education,subject,marks) VALUES ('{session['email']}', '{education}', 'Chemistry', {chemistry})")
         connector.commit()

         
         print(f"English :- {english} \nMathematics :- {mathematics} \n physics :- {physics} \n chemistry  :- {chemistry} ")
      

      elif(education == 'Grade 12 Science(PCB)'):
         english = int(request.form.get("english"))
         biology = int(request.form.get("bio"))
         physics = int(request.form.get("physics"))
         chemistry = int(request.form.get("chemistry"))

         n_eng = n_bio = n_phy = n_chem = 0
         if(request.form.get("n_eng")):  
            n_eng = int(request.form.get("n_eng"))
            english = (english*0.90) + (n_eng*0.10)

         if(request.form.get("n_bio")):
            n_bio = int(request.form.get("n_bio"))
            biology = (biology*0.90) + (n_bio*0.10)
         
         if(request.form.get("n_phy")):
            n_phy = int(request.form.get("n_phy"))
            physics = (physics*0.90) + (n_phy*0.10)

         if(request.form.get("n_chem")):
            n_chem = int(request.form.get("n_chem"))
            chemistry = (chemistry*0.90) + (n_chem*0.10)

         #storing the marks in session
         session["English"] = english
         session["Biology"] = biology 
         session["physics"] = physics
         session["chemistry"] = chemistry

         session["student_vector"] = {
            "Biology": biology/100,
            "Physics": physics/100,
            "Chemistry": chemistry/100,
            "English": english/100
         }
         cur.execute(f"INSERT INTO student_marks (email,education,subject,marks) VALUES ('{session['email']}', '{education}', 'English', {english})")
         connector.commit()   

         cur.execute(f"INSERT INTO student_marks (email,education,subject,marks) VALUES ('{session['email']}', '{education}', 'Biology', {biology})")
         connector.commit()

         cur.execute(f"INSERT INTO student_marks (email,education,subject,marks) VALUES ('{session['email']}', '{education}', 'Physics', {physics})")
         connector.commit()

         cur.execute(f"INSERT INTO student_marks (email,education,subject,marks) VALUES ('{session['email']}', '{education}', 'Chemistry', {chemistry})")
         connector.commit()


         print(f"English :- {english} \nBiology :- {biology} \nPhysics :- {physics} \nChemistry :- {chemistry} ")
      
      elif(education == 'Grade 12 Science(PCMB)'):
         english = int(request.form.get("english"))
         mathematics = int(request.form.get("math"))
         physics = int(request.form.get("physics"))
         chemistry = int(request.form.get("chemistry"))
         biology = int(request.form.get("biology"))

         n_eng = n_math = n_phy = n_chem = n_bio = 0
         if(request.form.get("n_eng")):
            n_eng = int(request.form.get("n_eng"))
            english = (english*0.85) + (n_eng*0.15)

         if(request.form.get("n_math")):
            n_math = int(request.form.get("n_math"))
            mathematics = (mathematics*0.85) + (n_math*0.15)

         if(request.form.get("n_phy")):
            n_phy = int(request.form.get("n_phy"))
            physics = (physics*0.85) + (n_phy*0.15)
         
         if(request.form.get("n_chem")):
            n_chem = int(request.form.get("n_chem"))
            chemistry = (chemistry*0.85) + (n_chem*0.15)

         if(request.form.get("n_bio")):
            n_bio = int(request.form.get("n_bio"))
            biology = (biology*0.85) + (n_bio*0.15)

         #storing the marks in session
         session["English"] = english
         session["Math"] = mathematics
         session["physics"] = physics
         session["chemistry"] = chemistry
         session["Biology"] = biology
         session["student_vector"] = {
            "Math": mathematics/100,
            "Physics": physics/100,
            "Chemistry": chemistry/100,
            "Biology": biology/100,
            "English": english/100
         }

         cur.execute(f"INSERT INTO student_marks (email,education,subject,marks) VALUES ('{session['email']}', '{education}', 'English', {english})")
         connector.commit()
         
         cur.execute(f"INSERT INTO student_marks (email,education,subject,marks) VALUES ('{session['email']}', '{education}', 'Mathematics', {mathematics})")
         connector.commit()

         cur.execute(f"INSERT INTO student_marks (email,education,subject,marks) VALUES ('{session['email']}', '{education}', 'Physics', {physics})")
         connector.commit()

         cur.execute(f"INSERT INTO student_marks (email,education,subject,marks) VALUES ('{session['email']}', '{education}', 'Chemistry', {chemistry})")
         connector.commit()

         cur.execute(f"INSERT INTO student_marks (email,education,subject,marks) VALUES ('{session['email']}', '{education}', 'Biology', {biology})")
         connector.commit()

         print(f"English :- {english} \nMath :- {mathematics} \nScience :- {physics} \nSocial Science :- {chemistry} \nBiology :- {biology}")
      
      elif(education == 'Grade 12 Commerce'):

        accounts = float(request.form.get("accounts"))
        economics = float(request.form.get("economics"))
        business = float(request.form.get("business"))
        maths = request.form.get("maths")
        english = float(request.form.get("english"))

        if maths:
            maths = float(maths)
        else:
            maths = 0

        session["student_vector"] = {
            "Accounts": accounts/100,
            "Economics": economics/100,
            "Business": business/100,
            "Maths": maths/100,
            "English": english/100
        }
        cur.execute(f"INSERT INTO student_marks (email,education,subject,marks) VALUES ('{session['email']}', '{education}', 'Accounts', {accounts})")
        connector.commit()

        cur.execute(f"INSERT INTO student_marks (email,education,subject,marks) VALUES ('{session['email']}', '{education}', 'Economics', {economics})")
        connector.commit()

        cur.execute(f"INSERT INTO student_marks (email,education,subject,marks) VALUES ('{session['email']}', '{education}', 'Business', {business})")
        connector.commit()

        if maths:
            cur.execute(f"INSERT INTO student_marks (email,education,subject,marks) VALUES ('{session['email']}', '{education}', 'Maths', {maths})")
            connector.commit()

        cur.execute(f"INSERT INTO student_marks (email,education,subject,marks) VALUES ('{session['email']}', '{education}', 'English', {english})")
        connector.commit()  

        print(f"Accounts :- {accounts} \nEconomics :- {economics} \nBusiness :- {business} \nMaths :- {maths} \nEnglish :- {english}")


    
      
      elif(education == 'Grade 12 Arts'):
         english = int(request.form.get("english"))
         mathematics = int(request.form.get("mathematics"))
         physics = int(request.form.get("physics"))
         chemistry = int(request.form.get("chemistry"))
         
         print(f"English :- {english} \nMath :- {mathematics} \nScience :- {physics} \nSocial Science :- {chemistry} ")
      
      elif(education == 'Diploma/Polytechnic'):
         english = int(request.form.get("english"))
         mathematics = int(request.form.get("mathematics"))
         physics = int(request.form.get("physics"))
         chemistry = int(request.form.get("chemistry"))
         
         print(f"English :- {english} \nMath :- {mathematics} \nScience :- {physics} \nSocial Science :- {chemistry} ")
      
      elif(education == 'UG'):
         english = int(request.form.get("english"))
         mathematics = int(request.form.get("mathematics"))
         physics = int(request.form.get("physics"))
         chemistry = int(request.form.get("chemistry"))
         
         print(f"English :- {english} \nMath :- {mathematics} \nScience :- {physics} \nSocial Science :- {chemistry} ")
         
      # return render_template("personality_assessment.html",Education = education,english=english,math=mathematics,science=science,socialscience=socialscience,secondlanguage=secondlanguage,n_eng=n_eng,n_math=n_math,n_sci=n_sci,n_social=n_social,n_second=n_second)
      return render_template("personality_assessment.html")

   else:
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


@app.route("/personality_assessment",methods=["GET","POST"])
def inrest():
   if request.method == "POST":
      total_r = total_i = total_a = total_s = total_e = total_c = 0
      for i in range(1, 7):
         total_r += int(request.form.get(f"q{i}_r", 0))
         total_i += int(request.form.get(f"q{i}_i", 0))
         total_a += int(request.form.get(f"q{i}_a", 0))
         total_s += int(request.form.get(f"q{i}_s", 0))
         total_e += int(request.form.get(f"q{i}_e", 0))
         total_c += int(request.form.get(f"q{i}_c", 0))

      r = total_r/25
      i = total_i/25
      a = total_a/25
      s = total_s/25
      e = total_e/25
      c = total_c/25
      session["riasec_vector"] = {
            "R": r,
            "I": i,
            "A": a,
            "S": s,
            "E": e,
            "C": c
         }
      cur.execute(f"INSERT INTO riasec_vector (email,R, I, A, S, E, C) VALUES ('{session['email']}', {r}, {i}, {a}, {s}, {e}, {c})")
      connector.commit()
      if(session["education"] == 'Grade 10'):
         return render_template("10th_intrest.html") 
      
      elif(session["education"] == 'Grade 12 Science(PCM)'):
         return render_template("12th_pcm_intrest.html")

      elif(session["education"] == 'Grade 12 Science(PCB)'):
         return render_template("12th_pcb_intrest.html")

      elif(session["education"] == 'Grade 12 Science(PCMB)'):
         return render_template("12th_pcmb_intrest.html")

      elif(session["education"] == 'Grade 12 Commerce'):
         return render_template("12th_commerce_intrest.html")

      elif(session["education"] == 'Grade 12 Arts'):
         return render_template("12th_arts_intrest.html")

      elif(session["education"] == 'Diploma/Polytechnic'):
         return render_template("dip_pol_intrest.html")

      elif(session["education"] == 'UG'):
         return render_template("ug_intrest.html")

   return render_template("personality_assessment.html")


@app.route("/interest_assessment",methods=["GET","POST"])
def intrest_assesment():
   if request.method == "POST":
      if(session["education"] == 'Grade 10'):
         math_interest = int(request.form.get("interest_math"))
         science_interest = int(request.form.get("interest_science"))  
         buisness_interest = int(request.form.get("interest_business")) 
         creativity_interest = int(request.form.get("interest_creative"))
         social_interest = int(request.form.get("interest_social"))

         session["intrest_vector"] = {
            "Math": math_interest/5,
            "Science": science_interest/5,
            "Business": buisness_interest/5,
            "Creativity": creativity_interest/5,
            "Social": social_interest/5
         }

         print(f"Math Interest :- {math_interest} \nScience Interest :- {science_interest} \nBusiness Interest :- {buisness_interest} \nCreativity Interest :- {creativity_interest} \nSocial Interest :- {social_interest}")
         return redirect(url_for("generate_career_profile"))#now jump to the next url after intrest submission to calculate the career profile and send to the web page 
         
      
      
      elif(session["education"] == 'Grade 12 Science(PCM)'): 
       

        # 1️ Collect raw interest values (1–5 scale)
        engineering = int(request.form.get("interest_engineering"))
        cs = int(request.form.get("interest_cs"))
        research = int(request.form.get("interest_research"))
        defense = int(request.form.get("interest_defense"))
        business = int(request.form.get("interest_business"))
        creative = int(request.form.get("interest_creative"))

        # 2️ Create Logical Domain Scores (Weighted Overlap Model)

        # Core Engineering Domain
        core_engineering_score = (
            engineering * 0.6 +
            research * 0.2 +
            defense * 0.2
        )

        # Computer & AI Domain
        computer_ai_score = (
            cs * 0.7 +
            creative * 0.2 +
            business * 0.1
        )

        # Pure Science / Research Domain
        research_domain_score = (
            research * 0.7 +
            engineering * 0.2 +
            cs * 0.1
        )

        # Defense & Govt Technical Domain
        defense_domain_score = (
            defense * 0.7 +
            engineering * 0.2 +
            research * 0.1
        )

        # Tech Entrepreneurship Domain
        entrepreneurship_score = (
            business * 0.6 +
            cs * 0.2 +
            creative * 0.2
        )

        # Creative Tech Domain
        creative_tech_score = (
            creative * 0.6 +
            cs * 0.3 +
            business * 0.1
        )

        # 3️ Normalize to 0–1 scale
        session["intrest_vector"] = {
            "Core_Engineering": core_engineering_score / 5,
            "Computer_AI": computer_ai_score / 5,
            "Pure_Science": research_domain_score / 5,
            "Defense_Tech": defense_domain_score / 5,
            "Entrepreneurship": entrepreneurship_score / 5,
            "Creative_Tech": creative_tech_score / 5
        }

        print("PCM Interest Vector:", session["intrest_vector"])

        return redirect(url_for("generate_career_profile"))
            
         
      

      elif(session["education"] == 'Grade 12 Science(PCB)'):

            medical = int(request.form.get("interest_medical"))
            research = int(request.form.get("interest_research"))
            pharma = int(request.form.get("interest_pharma"))
            allied = int(request.form.get("interest_allied"))
            psychology = int(request.form.get("interest_psychology"))
            environment = int(request.form.get("interest_environment"))

            #  Normalize 1–5 → 0–1
            session["intrest_vector"] = {
                "Medical": medical / 5,
                "Research": research / 5,
                "Pharma": pharma / 5,
                "Allied": allied / 5,
                "psychology": psychology / 5,
                "Environment": environment / 5
            }

            print("PCB Interest Vector:", session["intrest_vector"])

            return redirect(url_for("generate_career_profile"))
         
      elif(session["education"] == 'Grade 12 Science(PCMB)'):
         return render_template("generate_career_profile.html")   
      elif(session["education"] == 'Grade 12 Commerce'): 
        ca = int(request.form.get("interest_ca"))
        banking = int(request.form.get("interest_banking"))
        management = int(request.form.get("interest_management"))
        entrepreneur = int(request.form.get("interest_entrepreneur"))
        economics = int(request.form.get("interest_economics"))
        marketing = int(request.form.get("interest_marketing"))
        analytics = int(request.form.get("interest_analytics"))

        session["intrest_vector"] = {
            "CA_Finance": ca/5,
            "Banking": banking/5,
            "Management": management/5,
            "Entrepreneurship": entrepreneur/5,
            "Economics": economics/5,
            "Marketing": marketing/5,
            "Analytics": analytics/5
        }

        return redirect(url_for("generate_career_profile"))
      

      elif(session["education"] == 'Grade 12 Arts'):
         return render_template("generate_career_profile.html")
      elif(session["education"] == 'Diploma/Polytechnic'):
         return render_template("generate_career_profile.html")
      elif(session["education"] == 'UG'):
         return render_template("generate_career_profile.html")
        
   
      
   return redirect (url_for("generate_career_profile"))
   # return render_template("generate_career_profile.html")
   

@app.route("/generate_career_profile",methods=["GET","POST"])
def generate_career_profile():
    if(session.get("education") == 'Grade 10'):
      #we get the student normalize data from the session and we take the values from it because it is save in the dictionary(key values pair) then we convert into the list and then we convert it into the 2d array using numpy becuase cosine similarity expect the 2d array not a list or 1d array 
      academic_dict = session.get("student_vector")
      ability_student = np.array([
         academic_dict["Math"],
         academic_dict["Science"],
         academic_dict["Social"],
         academic_dict["Language"]
      ]).reshape(1, -1)
      
      riasec_dict = session.get("riasec_vector")

      riasec_student = np.array([
         riasec_dict["R"],
         riasec_dict["I"],
         riasec_dict["A"],
         riasec_dict["S"],
         riasec_dict["E"],
         riasec_dict["C"]
      ]).reshape(1, -1)


      interest_dict = session.get("intrest_vector")

      intrest_student = np.array([
         interest_dict["Math"],
         interest_dict["Science"],
         interest_dict["Business"],
         interest_dict["Creativity"],
         interest_dict["Social"]
      ]).reshape(1, -1)


      scores = {}

      #we are finding the matching scores of student ability ,personality ,intrest with the stream vectors int that also we have the ideal probable ability , personality ,intrest vector 
      for stream, profile in STREAM_PROFILES.items():
            stream_ability = np.array(profile["academic"]).reshape(1,-1)
            stream_personality = np.array(profile["personality"]).reshape(1,-1)
            stream_intrest = np.array(profile["interest"]).reshape(1,-1)

            stream_academic_similarity = cosine_similarity(
                ability_student, stream_ability
            )[0][0]

            stream_personality_similarity = cosine_similarity(
                riasec_student, stream_personality
            )[0][0]

            stream_interest_similarity = cosine_similarity(
                intrest_student, stream_intrest
            )[0][0]

            scores[stream] = float(
                (stream_academic_similarity * 0.5) +
                (stream_personality_similarity * 0.3) +
                (stream_interest_similarity * 0.2)
            )

        #  OUTSIDE loop (same indentation level as "for")
      best_stream = max(scores, key=scores.get)
      confidence_level = f"{round(scores[best_stream]*100,2)}%"

      session["best_stream"] = best_stream
      session["confidence_level"] = confidence_level

      sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
      top_2 = sorted_scores[:2]

      session["top_2"] = top_2

      return render_template(
            "generate_career_profile.html",
            best_stream=best_stream,
            confidence_level=confidence_level,
            top_2=top_2
        )
    #   print(f"Ability Vector :- {ability_student} \nRIASSEC Vector :- {riasec_student} \nIntrest Vector :- {intrest_student}\n Score : - {scores}")
    #   return render_template("generate_career_profile.html",best_stream=best_stream,top_2=top_2,confidence_level=confidence_level)
      # return f"Ability Vector :- {ability_student} \nRIASSEC Vector :- {riasec_student} \nIntrest Vector :- {intrest_student} \n Score : - {score}"
      # return render_template("generate_career_profile.html")


    elif(session.get("education") == 'Grade 12 Science(PCM)'):
        
        academic_dict = session.get("student_vector")
        riasec_dict = session.get("riasec_vector")
        interest_dict = session.get("intrest_vector")

        # 🔹 Academic Vector
        ability_student = np.array([
            academic_dict["Math"],
            academic_dict["Physics"],
            academic_dict["Chemistry"]
        ]).reshape(1, -1)

        # 🔹 Personality Vector
        riasec_student = np.array([
            riasec_dict["R"],
            riasec_dict["I"],
            riasec_dict["A"],
            riasec_dict["S"],
            riasec_dict["E"],
            riasec_dict["C"]
        ]).reshape(1, -1)

        # 🔹 Interest Vector
        interest_student = np.array([
            interest_dict["Core_Engineering"],
            interest_dict["Computer_AI"],
            interest_dict["Pure_Science"],
            interest_dict["Defense_Tech"],
            interest_dict["Entrepreneurship"],
            interest_dict["Creative_Tech"]
        ]).reshape(1, -1)

        scores = {}

        for branch, profile in PCM_DEGREE_PROFILES.items():

            branch_academic = np.array(profile["academic"]).reshape(1, -1)
            branch_personality = np.array(profile["personality"]).reshape(1, -1)
            branch_interest = np.array(profile["interest"]).reshape(1, -1)

            academic_similarity = cosine_similarity(
                ability_student, branch_academic
            )[0][0]

            personality_similarity = cosine_similarity(
                riasec_student, branch_personality
            )[0][0]

            interest_similarity = cosine_similarity(
                interest_student, branch_interest
            )[0][0]

            final_score = (
                academic_similarity * 0.4 +
                personality_similarity * 0.3 +
                interest_similarity * 0.3
            )

            scores[branch] = float(final_score)

        #  Best Branch
        best_branch = max(scores, key=scores.get)
        confidence_level = f"{round(scores[best_branch]*100,2)}%"

        session["best_stream"] = best_branch
        session["confidence_level"] = confidence_level
        session["scores"] = scores

        #  Get Top 3 Suggestions
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_2 = sorted_scores[:2]
        session["top_2"] = top_2

        return render_template(
            "generate_career_profile.html",
            best_stream=best_branch,
            confidence_level=confidence_level,
            top_2=top_2
        )
    
    elif(session.get("education") == 'Grade 12 Science(PCB)'):
        academic_dict = session.get("student_vector")
        riasec_dict = session.get("riasec_vector")
        interest_dict = session.get("intrest_vector")
        # 🔹 Academic Vector
        ability_student = np.array([
            academic_dict["Biology"],
            academic_dict["Physics"],
            academic_dict["Chemistry"]
        ]).reshape(1, -1)

        # 🔹 Personality Vector
        riasec_student = np.array([
            riasec_dict["R"],
            riasec_dict["I"],
            riasec_dict["A"],
            riasec_dict["S"],
            riasec_dict["E"],
            riasec_dict["C"]
        ]).reshape(1, -1)

        # 🔹 Interest Vector
        interest_student = np.array([
            interest_dict["Medical"],
            interest_dict["Research"],
            interest_dict["Pharma"],
            interest_dict["Allied"],
            interest_dict["psychology"],
            interest_dict["Environment"]
        ]).reshape(1, -1)

        scores = {}

        for branch, profile in PCB_DEGREE_PROFILES.items():

            branch_academic = np.array(profile["academic"]).reshape(1, -1)
            branch_personality = np.array(profile["personality"]).reshape(1, -1)
            branch_interest = np.array(profile["interest"]).reshape(1, -1)

            academic_similarity = cosine_similarity(
                ability_student, branch_academic
            )[0][0]

            personality_similarity = cosine_similarity(
                riasec_student, branch_personality
            )[0][0]

            interest_similarity = cosine_similarity(
                interest_student, branch_interest
            )[0][0]

            final_score = (
                academic_similarity * 0.4 +
                personality_similarity * 0.3 +
                interest_similarity * 0.3
            )

            scores[branch] = float(final_score)

        #  Best Branch
        best_branch = max(scores, key=scores.get)
        confidence_level = f"{round(scores[best_branch]*100,2)}%"

        session["best_stream"] = best_branch
        session["confidence_level"] = confidence_level
        session["scores"] = scores

        #  Get Top 3 Suggestions
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_2 = sorted_scores[:2]
        session["top_2"] = top_2

        return render_template(
            "generate_career_profile.html",
            best_stream=best_branch,
            confidence_level=confidence_level,
            top_2=top_2
        )

    elif(session["education"] == "Grade 12 Commerce"):
        academic_dict = session.get("student_vector")
        riasec_dict = session.get("riasec_vector")
        interest_dict = session.get("intrest_vector")

        ability_student = np.array([
            academic_dict["Accounts"],
            academic_dict["Economics"],
            academic_dict["Business"]
        ]).reshape(1,-1)

        riasec_student = np.array([
            riasec_dict["R"],
            riasec_dict["I"],
            riasec_dict["A"],
            riasec_dict["S"],
            riasec_dict["E"],
            riasec_dict["C"]
        ]).reshape(1,-1)

        interest_student = np.array([
            interest_dict["CA_Finance"],
            interest_dict["Banking"],
            interest_dict["Management"],
            interest_dict["Entrepreneurship"],
            interest_dict["Economics"],
            interest_dict["Marketing"],
            interest_dict["Analytics"]
        ]).reshape(1,-1)

        scores = {}

        for branch, profile in COMMERCE_DEGREE_PROFILES.items():

            academic_similarity = cosine_similarity(
                ability_student, np.array(profile["academic"]).reshape(1,-1)
            )[0][0]

            personality_similarity = cosine_similarity(
                riasec_student, np.array(profile["personality"]).reshape(1,-1)
            )[0][0]

            interest_similarity = cosine_similarity(
                interest_student, np.array(profile["interest"]).reshape(1,-1)
            )[0][0]

            final_score = (
                academic_similarity * 0.4 +
                personality_similarity * 0.3 +
                interest_similarity * 0.3
            )

            scores[branch] = float(final_score)

        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_2 = sorted_scores[:2]

        best_branch = sorted_scores[0][0]
        confidence_level = f"{round(sorted_scores[0][1]*100,2)}%"

        return render_template(
            "generate_career_profile.html",
            best_stream=best_branch,
            confidence_level=confidence_level,
            top_2=top_2
        )
        
           
       

def inference(prompt):
    print("Thinking ......")
    r = requests.post("http://localhost:11434/api/generate",json={
            "model":"llama3.2",
            "prompt":prompt,
            "stream":False

        })
    response = r.json()
    return response

@app.route("/career_roadmap")
def career_roadmap():
    if(session["education"] == 'Grade 10'):
       
        prompt = f'''You are an AI Career Guidance Expert.\nYou do not change the predicted stream.\nYou do not override the scoring engine.\nYou only explain and expand on the recommendation.\nYou provide structured, practical, realistic guidance.\nYou never force the student to choose a stream.\nYou suggest, justify, and provide roadmap steps \n Student Profile Data:

        Best Recommended Stream: { session.get("best_stream") }
        Confidence Level: { session.get("confidence_level") }

        All Stream Scores:
        Science: { session.get("scores")["Science"] }
        Commerce: { session.get("scores")["Commerce"] }
        Arts: { session.get("scores")["Arts"] }

        Academic Strength Vector (0-1 scale):
        Math: { session.get("student_vector")["Math"] }
        Science: { session.get("student_vector")["Science"] }
        Social Science: { session.get("student_vector")["Social"] }
        Language: {session.get("student_vector")["Language"] }

        RIASEC Personality Scores (0-1 scale):
        Realistic: { session.get("riasec_vector")["R"] }
        Investigative: { session.get("riasec_vector")["I"] }
        Artistic: { session.get("riasec_vector")["A"] }
        Social: { session.get("riasec_vector")["S"] }
        Enterprising: { session.get("riasec_vector")["E"] }
        Conventional: { session.get("riasec_vector")["C"] }

        Interest Scores (0-1 scale):
        Mathematics: { session.get("intrest_vector")["Math"] }
        Science: { session.get("intrest_vector")["Science"] }
        Business: { session.get("intrest_vector")["Business"] }
        Creative: { session.get("intrest_vector")["Creativity"] }
        Social: { session.get("intrest_vector")["Social"] }


        Instructions:

        1. Explain why the recommended stream is suitable based on academic strengths, personality, and interests.
        2. Mention the second-best stream and explain briefly why it is also a possible option.
        3. Provide a 3-year roadmap (11th, 12th, Entrance Exams preparation).
        4. Suggest 5 career options after graduation.
        5. Suggest skill improvement areas based on weaker dimensions.
        6. Keep tone encouraging and practical.
        7. Do not contradict the predicted stream.
        8. Format response in clear sections with headings. 
        so that i can show in the web page in a structured format. every point should be in different section with heading.'''
        
        with open("career_roadmap_prompt.md","w") as f:
            f.write(prompt)

        response = inference(prompt)["response"]
        roadmap_html = markdown.markdown(
        response,
        extensions=["fenced_code", "tables"]
        )
        with open("response.md","w") as f:
            f.write(response)
        return render_template(
        "career_roadmap.html",
        roadmap=roadmap_html
        )

    elif session["education"] == "Grade 12 Science(PCM)":

        prompt = f"""
        You are an AI Career Guidance Expert.

        You must explain the recommended DEGREE BRANCH.
        Do NOT change the predicted branch.

        Best Recommended Career Branch: {session.get("best_stream")}
        Confidence Level: {session.get("confidence_level")}

        top 2 Branch Scores:
        {session["top_2"]}

        Academic Strength (0-1):
        Math: {session.get("student_vector")["Math"]}
        Physics: {session.get("student_vector")["Physics"]}
        Chemistry: {session.get("student_vector")["Chemistry"]}

        RIASEC Personality:
        {session.get("riasec_vector")}

        Interest Vector:
        {session.get("intrest_vector")}

        Instructions:
        1. Explain why this branch suits the student.
        2. Mention second-best branch briefly.
        3. Provide 4-year college roadmap.
        4. Mention entrance exams (JEE, state CET, etc.)
        5. Mention required technical skills.
        6. Mention 5 real job roles after graduation.
        7. Suggest skill improvement areas.
        8. Keep structured headings.
        """
        with open("career_roadmap_prompt.md","w") as f:
            f.write(prompt)

        response = inference(prompt)["response"]
        roadmap_html = markdown.markdown(
        response,
        extensions=["fenced_code", "tables"]
        )
        with open("response.md","w") as f:
            f.write(response)
        return render_template(
        "career_roadmap.html",
        roadmap=roadmap_html
        )
    
    
    elif session["education"] == "Grade 12 Science(PCB)":

        
        prompt = f"""
        You are an AI Career Guidance Expert specializing in medical and life science careers.

        IMPORTANT RULES:
        - Do NOT change the predicted career path.
        - Do NOT override the scoring engine.
        - Only explain and expand the recommendation.
        - Be realistic, structured, and practical.

        --------------------------------------------------

        STUDENT PROFILE DATA

        Best Recommended Career Path:
        {session.get("best_stream")}

        Confidence Level:
        {session.get("confidence_level")}

        top 2 Branch Scores:
        {session["top_2"]}

        Academic Strength (0-1 Scale):
        Biology: {session.get("student_vector")["Biology"]}
        Physics: {session.get("student_vector")["Physics"]}
        Chemistry: {session.get("student_vector")["Chemistry"]}

        RIASEC Personality Scores:
        Realistic: {session.get("riasec_vector")["R"]}
        Investigative: {session.get("riasec_vector")["I"]}
        Artistic: {session.get("riasec_vector")["A"]}
        Social: {session.get("riasec_vector")["S"]}
        Enterprising: {session.get("riasec_vector")["E"]}
        Conventional: {session.get("riasec_vector")["C"]}

        Interest Scores:
        Medical: {session.get("intrest_vector")["Medical"]}
        Research: {session.get("intrest_vector")["Research"]}
        Pharma: {session.get("intrest_vector")["Pharma"]}
        Allied: {session.get("intrest_vector")["Allied"]}
        Psychology: {session.get("intrest_vector")["psychology"]}
        Environment: {session.get("intrest_vector")["Environment"]}

        --------------------------------------------------

        INSTRUCTIONS:

        1. Explain clearly why the recommended career path suits the student 
        based on academics, personality, and interest.

        2. Mention the second-best career option briefly and why it is also strong.

        3. Provide a structured preparation roadmap:
        - Entrance Exams (NEET or relevant exams)
        - 2-year preparation strategy
        - College selection strategy

        4. Provide a degree roadmap:
        - Duration of course
        - Important subjects
        - Internship / Clinical exposure
        - Licensing or certification requirements

        5. Suggest 5 career roles after graduation.

        6. Suggest skill development areas based on weaker dimensions.

        7. Keep tone encouraging and professional.

        8. Format output using clear section headings so it can be displayed properly on a web page.

        --------------------------------------------------
        """
        with open("career_roadmap_prompt.md","w") as f:
            f.write(prompt)

        response = inference(prompt)["response"]
        roadmap_html = markdown.markdown(
        response,
        extensions=["fenced_code", "tables"]
        )
        with open("response.md","w") as f:
            f.write(response)
        return render_template(
        "career_roadmap.html",
        roadmap=roadmap_html
        )

        
    

    elif session["education"] == "Grade 12 Commerce":

        
        prompt = f'''
        You are an AI Career Guidance Expert.

        You do NOT change the predicted career.
        You do NOT override the scoring engine.
        You only explain and expand the recommendation.
        You provide structured, practical, realistic guidance.
        You never force the student to choose a career.
        You suggest, justify, and provide roadmap steps.

        ==============================
        STUDENT PROFILE DATA
        ==============================

        Best Recommended Career: {session.get("best_stream")}
        Confidence Level: {session.get("confidence_level")}

        Top 2 Career Matches:
        {session.get("top_2")}

        Academic Strengths (0-1 scale):
        Accounts: {session.get("student_vector")["Accounts"]}
        Economics: {session.get("student_vector")["Economics"]}
        Business Studies: {session.get("student_vector")["Business"]}
        Maths/SP: {session.get("student_vector")["Maths"]}
        English: {session.get("student_vector")["English"]}

        RIASEC Personality Scores (0-1 scale):
        Realistic: {session.get("riasec_vector")["R"]}
        Investigative: {session.get("riasec_vector")["I"]}
        Artistic: {session.get("riasec_vector")["A"]}
        Social: {session.get("riasec_vector")["S"]}
        Enterprising: {session.get("riasec_vector")["E"]}
        Conventional: {session.get("riasec_vector")["C"]}

        Interest Scores (0-1 scale):
        CA & Finance: {session.get("intrest_vector")["CA_Finance"]}
        Banking: {session.get("intrest_vector")["Banking"]}
        Management: {session.get("intrest_vector")["Management"]}
        Entrepreneurship: {session.get("intrest_vector")["Entrepreneurship"]}
        Economics: {session.get("intrest_vector")["Economics"]}
        Marketing: {session.get("intrest_vector")["Marketing"]}
        Analytics: {session.get("intrest_vector")["Analytics"]}

        ==============================
        INSTRUCTIONS
        ==============================

        1. Explain clearly why the recommended career fits the student’s academic strengths, personality, and interests.
        2. Briefly explain why the second-best career is also a strong alternative.
        3. Provide a 3-year roadmap (FY, SY, TY of graduation).
        4. Mention important entrance exams or certifications (CA Foundation, CS Executive, CMA, CAT, Banking Exams, etc.).
        5. Suggest 5 possible career roles after graduation.
        6. Suggest skill improvement areas based on weaker scores.
        7. Keep tone practical, motivating, and professional.
        8. Format output in clear sections with headings.
        9. Keep explanation specific to Commerce domain only.

        The output must be structured clearly with headings so it can be displayed cleanly on a web page.
        '''
        with open("career_roadmap_prompt.md","w") as f:
            f.write(prompt)

        response = inference(prompt)["response"]

        roadmap_html = markdown.markdown(
        response,
        extensions=["fenced_code", "tables"]
        )
        with open("response.md","w") as f:
            f.write(response)
        return render_template(
        "career_roadmap.html",
        roadmap=roadmap_html
        )


@app.route("/Idont_agree")
def retake_assessment():
    
    return render_template("User_choice.html")

@app.route("/custom_recommendation", methods=["GET","POST"])
def custom_recomendation():
   user_text = request.form.get("user_preference")

   prompt = f"""
    You are an AI Career Guidance Expert.

    Student was recommended: {session.get("best_stream")}
    But student does not agree.

    Student preference description:
    {user_text}

    Based on their academic strengths, personality scores,
    and their preference description,
    suggest a realistic career roadmap.

Give:
    1. Suitable career options
    2. Required degree
    3. Entrance exams
    4. 3-year roadmap
    5. Required skills
    6. Practical advice

Keep it structured with headings.
"""

   response = inference(prompt)["response"]
   roadmap_html = markdown.markdown(
   response,
   extensions=["fenced_code", "tables"])
   with open("response.md","w") as f:   
        f.write(response)
   return render_template(
    "career_roadmap.html",
    roadmap=roadmap_html
    )

@app.route("/explore")
def explore():
    return render_template("blank.html")

@app.route("/show")
def show():
    return render_template("show.html")

    
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/register")

app.run()