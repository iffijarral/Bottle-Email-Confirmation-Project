from bottle import get, post, request, response, static_file, template, run
import x
import uuid
import time
import bcrypt

#########################
@get("/mixhtml.js")
def _():
    return static_file("mixhtml.js", ".")

#########################
@get("/app.css")
def _():
    return static_file("app.css", ".")

####################
@get("/")
def _():
    name = request.get_cookie("name", secret="my_secret")
    if name:
        try:
            x.disable_cache()
            
            return template("index")
        except Exception as ex:
            print(ex)
            return ex
            # return "System is under maintaninance"
        finally:
            pass
    else:
        response.status = 303
        response.set_header("Location", "/login")

####################
@get("/login")
def _():
    return template("login", msg = '')
####################
# Get login page
@get("/login/<page>")
def _(page):
    html = template("login", msg = '')
    return f"""
        <template mix-target="#wrapper" mix-replace>                
            {html}
        </template>
    """
####################
@post("/login")
def _():
    try:
        # TODO: validate the email and password
        # validate password
        email = x.validate_user_email()
        password = x.validate_user_password()
        print(email)
        # TODO: Connect to the db and check that the email and password are correct
        db = x.db()        
        
        # db.execute(SELECT * FROM users WHERE user_email = ? AND user_password = ?, (email, password))
        sql = db.execute("SELECT * FROM users WHERE user_email = ? AND is_verified = 1", (email,))

        user = sql.fetchone()

        if user:
            user_password = user['user_password']

            password = password.encode('utf-8')

            if bcrypt.checkpw(password, user_password):                               
                response.set_cookie("name", user['user_name'], secret="my_secret", httponly=True)            
                return """
                    <template mix-redirect="/">
                    </template>            
                """
            else:
                return """
                    <template mix-target="#message" mix-replace>                
                        <div id="message" class="error_message"> Invalid credentials </div>
                    </template>
                """
        else:
            return """
                <template mix-target="#message" mix-replace>                
                    <div id="message" class="error_message"> Invalid credentials </div>
                </template>
            """
    except Exception as ex:
        print(ex)       

        if "user_password" in str(ex):
            return """
            <template mix-target="#message" mix-replace>                
                <div id="message" class="mix-error"> User password invalid</div>
            </template>            
            """
        if "user_email" in str(ex):
            return """
            <template mix-target="#message" mix-replace>
                <div id="message" class="error_message"> User Email Invalid</div>
            </template>
            """        
        return """
        <template mix-target="#message" mix-replace>
            <div id="message"> System under maintainance</div>
        </template>
        """
    finally:
        if "db" in locals(): db.close()
####################
@get("/signup")
def _():    
    return template("signup")
####################
@post("/signup")
def _():
    try:        
        # TODO: Connect to the db and check that the email and password are correct
        db = x.db()
        
        # Validate
        user_name = x.validate_user_name()                

        user_email = x.validate_user_email()

        user_id = uuid.uuid4().hex

        is_verified = 0

        user_verification_key =  uuid.uuid4().hex       

        user_updated_at = 0

        user_created_at = int(time.time())

        # user_password = b'password' # b infront of 'password' is important
        user_password = x.validate_user_password()

        user_password = user_password.encode('utf-8')

        salt = bcrypt.gensalt()

        hashed_password = bcrypt.hashpw(user_password, salt)

        sql = db.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (user_id, user_name, user_email, hashed_password, user_verification_key, is_verified, user_created_at,  user_updated_at))        

        db.commit()

        if x.send_email(user_name, user_email, user_verification_key):
            return """            
                <template mix-target="#message" mix-replace>
                    <div id="message">
                        Thanks for signing up! An email has been sent to your inbox with a verification link. 
                        Please check your email and click on the link to complete the signup process. 
                        Don't forget to check your spam folder if you don't see the email in your inbox.
                    </div>
                </template>            
            """
        else:
             return """            
                <template mix-target="#message" mix-replace>
                    <div id="message"> The system is under maintenance, please try again later  </div>
                </template>            
            """       
    except Exception as ex:
        print(ex)
        if "users.user_email" in str(ex):
            return """
                <template mix-target="#message" mix-replace>
                    <div id="message"> The Email is not available</div>
                </template>
            """
        if "user_email invalid" in str(ex):
            return """
                <template mix-target="#message" mix-replace>
                    <div id="message"> User Email Invalid</div>
                </template>
            """
    finally:
        if "db" in locals(): db.close()
    
####################
@get('/verify/<key>')
def _(key):
    try:
        db = x.db()
        user = db.execute("SELECT * FROM users WHERE user_verification_key = ?", (key,)).fetchone()

        if user:
            sql = db.execute("UPDATE users SET is_verified = 1 WHERE user_pk = ?", (user['user_pk'],))

            db.commit()

            return template("login", msg = "Email verified successfully! You can now login.")
            #return "Email verified successfully! You can now login."
        else:
            # Handle case where no user is found for the given key
            return "Invalid verification key."
    except Exception as ex:                  
         print(ex)
         return """
                <template mix-target="#message" mix-replace>
                    <div id="message"> The system is under maintainence, please try again later.</div>
                </template>
            """  
    finally:
        if "db" in locals(): db.close()
         
                   
#########################
@get("/logout")
def _():  
  response.add_header("Cache-Control", "no-cache, no-store, must-revalidate")
  response.add_header("Pragma", "no-cache")
  response.add_header("Expires", 0)    
  response.delete_cookie("name")
  response.status = 303
  response.set_header("Location", "/login")
  return 
####################
run(host="127.0.0.1", port=8080, debug=True, reloader=True)

##flolrybuytwclchl      gmail password