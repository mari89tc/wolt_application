from flask import Flask, session, render_template, redirect, url_for, make_response, request, send_from_directory
from flask_session import Session
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import x
import uuid 
import time
import redis
import os

from icecream import ic
ic.configureOutput(prefix=f'***** | ', includeContext=True)

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'  # or 'redis', etc.
Session(app)


# app.secret_key = "your_secret_key"

##############################
##############################
##############################

def _________GET_________(): pass

##############################
##############################

##############################
@app.get("/images/<image_id>")
def view_image(image_id):
    return send_from_directory("./images", image_id)



##############################
@app.get("/test-set-redis")
def view_test_set_redis():
    redis_host = "redis"
    redis_port = 6379
    redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)    
    # TODO: Get most populatar restaurants from mysql
    # restaurants [{},{},{}]
    # To interact with REDIS from vscode: docker exec -it fulldemo_redis_exam redis-cli
    # To interact with REDIS from vscode: docker exec -it CONTAINER_NAME_HERE redis-cli
    """

    for restaursnt in restaurants:
        HSET restaurant:restaurant["user_pk"] name restaurant["user_name"] cuisine "Italian" location "New York" 
    """
    redis_client.set()
    redis_client.set("name", "Santiago", ex=10)
    # name = redis_client.get("name")
    return "name saved"

@app.get("/test-get-redis")
def view_test_get_redis():
    redis_host = "redis"
    redis_port = 6379
    redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)    
    name = redis_client.get("name")
    if not name: name = "no name"
    return name

##############################
@app.get("/")
def view_index():
    name = "X"
    return render_template("view_index.html", name=name)

##############################
@app.get("/signup")
@x.no_cache
def view_signup():  
    id = request.args.get("id", "")
    # ic(session)
    # if session.get("user"):
    #     if len(session.get("user").get("roles")) > 1:
    #         return redirect(url_for("view_choose_role")) 
    #     if "restaurant" in session.get("user").get("roles"):
    #         return redirect(url_for("view_restaurant_page"))
    #     if "customer" in session.get("user").get("roles"):
    #         return redirect(url_for("view_customer")) 
    #     if "partner" in session.get("user").get("roles"):
    #         return redirect(url_for("view_partner"))  
    return render_template("view_signup.html", x=x, id=id, title="Signup")


##############################
@app.get("/login")
@x.no_cache
def view_login():  
    ic(session)  
    if session.get("user"):
        # if len(session.get("user").get("roles")) > 1:
        #     return redirect(url_for("view_choose_role")) 
        if "admin" in session.get("user").get("roles"):
            return redirect(url_for("view_admin"))
        if "customer" in session.get("user").get("roles"):
            return redirect(url_for("view_customer")) 
        if "partner" in session.get("user").get("roles"):
            return redirect(url_for("view_partner"))         
    return render_template("view_login.html", x=x, title="Login", message=request.args.get("message", ""))


##############################
@app.get("/customer")
@x.no_cache
def view_customer():
    if not session.get("user", ""): 
        return redirect(url_for("view_login"))
    user = session.get("user")
    # if len(user.get("roles", "")) > 1:
    #     return redirect(url_for("view_choose_role"))
    return render_template("view_customer.html", user=user)

##############################
@app.get("/partner")
@x.no_cache
def view_partner():
    if not session.get("user", ""): 
        return redirect(url_for("view_login"))
    user = session.get("user")
    # if len(user.get("roles", "")) > 1:
    #     return redirect(url_for("view_choose_role"))
    return render_template("view_partner.html", user=user)


##############################
@app.get("/admin")
@x.no_cache
def view_admin():
    if not session.get("user", ""): 
        return redirect(url_for("view_login"))
    user = session.get("user")
    # if not "admin" in user.get("roles", ""):
    #     return redirect(url_for("view_login"))
    
    db, cursor = x.db()
    cursor.execute("SELECT * FROM users ORDER BY user_created_at DESC") #Get all users
    users = cursor.fetchall()

    cursor.execute("SELECT * FROM items ORDER BY item_created_at DESC") #Get all items
    items = cursor.fetchall()
    return render_template("view_admin.html", user=user, users=users, items=items)

##############################
@app.get("/restaurant")
@x.no_cache
def view_restaurant_page():
    if not session.get("user", ""):
        return redirect(url_for("view_login"))
    user = session.get("user")
    if not "restaurant" in user.get("roles", ""):
        return redirect(url_for("view_login"))

    db, cursor = x.db()
    cursor.execute("SELECT * FROM items ORDER BY item_created_at DESC") #Get all items
    items = cursor.fetchall()
    return render_template("view_restaurant_page.html", user=user, x=x, title="Restaurant page", items=items)


##############################
# @app.get("/choose-role")
# @x.no_cache
# def view_choose_role():
#     if not session.get("user", ""): 
#         return redirect(url_for("view_login"))
#     if not len(session.get("user").get("roles")) >= 2:
#         return redirect(url_for("view_login"))
#     user = session.get("user")
#     return render_template("view_choose_role.html", user=user, title="Choose role")


##############################
@app.get("/forgot-password")
@x.no_cache
def view_forgot_password():
    return render_template("view_forgot_password.html", x=x, title="Forgot password")


##############################
@app.get("/reset-password")
@x.no_cache
def view_reset_password():
    return render_template("view_reset_password.html", x=x, title="Reset password")


##############################
@app.get("/restaurants")
@x.no_cache
def view_restaurants():
    db, cursor = x.db()
    cursor.execute("SELECT * FROM users ORDER BY user_created_at DESC")
    users = cursor.fetchall()
    return render_template("view_restaurants.html", x=x, title="Restaurants", users=users)

##############################
@app.get("/profile")
@x.no_cache
def view_profile():
    if not session.get("user", ""): 
        return redirect(url_for("view_login"))
    user = session.get("user")

    return render_template("view_profile.html", x=x, title="Profile", user=user)

##############################
##############################
##############################

def _________POST_________(): pass

##############################
##############################
##############################

@app.post("/logout")
def logout():
    # ic("#"*30)
    # ic(session)
    session.pop("user", None)
    # session.clear()
    # session.modified = True
    # ic("*"*30)
    # ic(session)
    return redirect(url_for("view_login"))


##############################
@app.post("/users")
@x.no_cache
def signup():
    try:
        user_name = x.validate_user_name()
        user_last_name = x.validate_user_last_name()
        user_email = x.validate_user_email()
        user_password = x.validate_user_password()
        hashed_password = generate_password_hash(user_password)

        user_role = request.form.get('role')
        if not user_role:
            toast = render_template("___toast.html", message="Role is required")
            return f"""<template mix-target="#toast">{toast}</template>""", 400

        user_pk = str(uuid.uuid4())
        user_avatar = ""
        user_created_at = int(time.time())
        user_deleted_at = 0
        user_blocked_at = 0
        user_updated_at = 0
        user_verified_at = 0
        user_verification_key = str(uuid.uuid4())
        user_reset_key = 0

        db, cursor = x.db()
        q = 'INSERT INTO users VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(q, (user_pk, user_name, user_last_name, user_email,
                            hashed_password, user_avatar, user_created_at, user_deleted_at, user_blocked_at,
                            user_updated_at, user_verified_at, user_verification_key, user_reset_key))
        
        q_role = 'INSERT INTO users_roles (user_role_user_fk, user_role_role_fk) VALUES (%s, %s)'
        cursor.execute(q_role, (user_pk, user_role))

        x.send_verify_email(user_email, user_verification_key)
        db.commit()

        return """<template mix-redirect="/login"></template>""", 201

    except Exception as ex:
        ic(ex)
        if "db" in locals(): db.rollback()
        if isinstance(ex, x.CustomException):
            toast = render_template("___toast.html", message=ex.message)
            return f"""<template mix-target="#toast" mix-bottom>{toast}</template>""", ex.code
        if isinstance(ex, x.mysql.connector.Error):
            ic(ex)
            if "users.user_email" in str(ex):
                toast = render_template("___toast.html", message="email not available")
                return f"""<template mix-target="#toast" mix-bottom>{toast}</template>""", 400
            return f"""<template mix-target="#toast" mix-bottom>System upgrating</template>""", 500
        return f"""<template mix-target="#toast" mix-bottom>System under maintenance</template>""", 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.post("/login")
def login():
    try:

        user_email = x.validate_user_email()
        user_password = x.validate_user_password()

        db, cursor = x.db()
        q = """ SELECT * FROM users 
                JOIN users_roles 
                ON user_pk = user_role_user_fk 
                JOIN roles
                ON role_pk = user_role_role_fk
                WHERE user_email = %s"""
        cursor.execute(q, (user_email,))

        rows = cursor.fetchall()
        if not rows:
            toast = render_template("___toast.html", message="user not registered")
            return f"""<template mix-target="#toast">{toast}</template>""", 400     
        if not check_password_hash(rows[0]["user_password"], user_password):
            toast = render_template("___toast.html", message="invalid credentials")
            return f"""<template mix-target="#toast">{toast}</template>""", 401
        
        # check if user is verified
        q = " SELECT `user_verified_at` FROM `users` WHERE `user_email` = %s"
        cursor.execute(q, (user_email,))
        verified_rows = cursor.fetchall()
        if verified_rows[0]["user_verified_at"] == 0:
            toast = render_template("___toast.html", message="user not verified")
            return f"""<template mix-target="#toast">{toast}</template>""", 400 
        
        # check if user is blocked
        q = " SELECT `user_blocked_at` FROM `users` WHERE `user_email` = %s"
        cursor.execute(q, (user_email,))
        blocked_rows = cursor.fetchall()
        if blocked_rows[0]["user_blocked_at"] > 0:
            toast = render_template("___toast.html", message="user is blocked. Contact customer service")
            return f"""<template mix-target="#toast">{toast}</template>""", 400 
        
        ## check if user is deleted
        q = " SELECT `user_deleted_at` FROM `users` WHERE `user_email` = %s"
        cursor.execute(q, (user_email,))
        deleted_rows = cursor.fetchall()
        if deleted_rows[0]["user_deleted_at"] > 0:
            toast = render_template("___toast.html", message="user is deleted. Contact customer service")
            return f"""<template mix-target="#toast">{toast}</template>""", 400 
        
        roles = []
        for row in rows:
            roles.append(row["role_name"])
        user = {
            "user_pk": rows[0]["user_pk"],
            "user_name": rows[0]["user_name"],
            "user_last_name": rows[0]["user_last_name"],
            "user_email": rows[0]["user_email"],
            "roles": roles
        }
        ic(user)
        session["user"] = user
        if len(roles) == 1:
            return f"""<template mix-redirect="/{roles[0]}"></template>"""
        return f"""<template mix-redirect="/login"></template>"""
    except Exception as ex:
        ic(ex)
        if "db" in locals(): db.rollback()
        if isinstance(ex, x.CustomException): 
            toast = render_template("___toast.html", message=ex.message)
            return f"""<template mix-target="#toast" mix-bottom>{toast}</template>""", ex.code    
        if isinstance(ex, x.mysql.connector.Error):
            ic(ex)
            return "<template>System upgrating</template>", 500        
        return "<template>System under maintenance</template>", 500  
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.post("/items")
def create_item():
    try:
        item_title = x.validate_item_title()
        item_description = x.validate_item_description()
        item_price = x.validate_item_price()

        item_created_at = int(time.time())
        item_updated_at = 0
        item_blocked_at = 0
        item_deleted_at = 0
        item_pk = str(uuid.uuid4())
        
        file, item_image_name = x.validate_item_image()
        # Save the image
        file.save(os.path.join(x.UPLOAD_ITEM_FOLDER, item_image_name))
        # TODO: if saving the image went wrong, then rollback by going to the exception
        # TODO: Success, commit

        db, cursor = x.db()
        q = """INSERT INTO items VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(q, (item_pk, item_title, item_description, item_price, item_image_name, item_created_at, item_updated_at, item_blocked_at, item_deleted_at))

        db.commit()

        return f"""<template mix-redirect="/restaurant"></template>"""
    except Exception as ex:
        ic(ex)
        if "db" in locals(): db.rollback()
        if isinstance(ex, x.CustomException): 
            toast = render_template("___toast.html", message=ex.message)
            return f"""<template mix-target="#toast" mix-bottom>{toast}</template>""", ex.code    
        if isinstance(ex, x.mysql.connector.Error):
            ic(ex)
            return "<template>System upgrating</template>", 500        
        return "<template>System under maintenance</template>", 500  
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()    


##############################
@app.post("/forgot-password")
def forgot_password():
    try:
        user_email = x.validate_user_email()
        user_reset_key = str(uuid.uuid4())
        user_updated_at = int(time.time())

        db, cursor = x.db()
        q = """ SELECT * FROM users 
                WHERE user_email = %s"""
        cursor.execute(q, (user_email,))
        rows = cursor.fetchall()

        if not rows:
            toast = render_template("___toast.html", message="user not registered")
            return f"""<template mix-target="#toast">{toast}</template>""", 400 

        q = """UPDATE users SET `user_reset_key` = %s, `user_updated_at` = %s  WHERE `user_email` = %s"""
        cursor.execute(q, (user_reset_key, user_updated_at, user_email))
        db.commit()
        
        x.send_new_password_email(user_email, user_reset_key)

        return f"""<template mix-redirect="/reset-password"></template>"""
        # return f"""<template mix-target="#info_text" mix-replace><p class="bg-c-green:-10 pa-4 rounded-md text-c-white">E-mail send. Follow the e-mail for changing your password</p></template>"""

    except Exception as ex:
        ic(ex)
        if "db" in locals(): db.rollback()

        # My own exception
        if isinstance(ex, x.CustomException):
            return f"""<template mix-target="#toast" mix-bottom>{ex.message}</template>""", ex.code
        
        # Database exception
        if isinstance(ex, x.mysql.connector.Error):
            ic(ex)
            if "users.user_email" in str(ex):
                return """<template mix-target="#toast" mix-bottom>email not available</template>""", 400
            return "<template>System upgrading</template>", 500  
    
        # Any other exception
        return """<template mix-target="#toast" mix-bottom>System under maintenance</template>""", 500  
        
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.post("/reset-password")
def reset_password():
    try:
        user_reset_key = x.validate_uuid4(request.form.get("user_reset_key", "").strip())
        user_password = x.validate_user_password()
        hashed_password = generate_password_hash(user_password)
        user_updated_at = int(time.time())

        db, cursor =x.db()

        # q = 'UPDATE users SET `user_password`=%s, `user_updated_at` = %s WHERE `user_reset_key` = %s'
        # cursor.execute(q, (hashed_password, user_updated_at, user_reset_key))
        q = 'UPDATE users SET `user_password`=%s, `user_updated_at` = %s WHERE `user_reset_key` = %s'
        cursor.execute(q, (hashed_password, user_updated_at, user_reset_key))
        rows_affected = cursor.rowcount

        if rows_affected < 1:
            toast = render_template("___toast.html", message="Invalid password reset-key")
            return f"""<template mix-target="#toast">{toast}</template>""", 400 

        db.commit()

        return f"""<template mix-redirect="/login"></template>"""

    except Exception as ex:
        ic(ex)
        if "db" in locals(): db.rollback()

        # My own exception
        if isinstance(ex, x.CustomException):
            return f"""<template mix-target="#toast" mix-bottom>{ex.message}</template>""", ex.code
        
        # Database exception
        if isinstance(ex, x.mysql.connector.Error):
            ic(ex)
            if "users.user_email" in str(ex):
                return """<template mix-target="#toast" mix-bottom>email not available</template>""", 400
            return "<template>System upgrading</template>", 500  
    
        # Any other exception
        return """<template mix-target="#toast" mix-bottom>System under maintenance</template>""", 500  
        
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
##############################
##############################

def _________PUT_________(): pass

##############################
##############################
##############################

@app.put("/users")
def user_update():
    try:
        if not session.get("user"): x.raise_custom_exception("please login", 401)

        user_pk = session.get("user").get("user_pk")
        user_name = x.validate_user_name()
        user_last_name = x.validate_user_last_name()
        user_email = x.validate_user_email()

        user_updated_at = int(time.time())

        db, cursor = x.db()
        q = """ UPDATE users
                SET user_name = %s, user_last_name = %s, user_email = %s, user_updated_at = %s
                WHERE user_pk = %s
            """
        cursor.execute(q, (user_name, user_last_name, user_email, user_updated_at, user_pk))
        if cursor.rowcount != 1: x.raise_custom_exception("cannot update user", 401)
        db.commit()
        user = {
            "user_pk":user_pk,
            "user_name": user_name,
            "user_last_name": user_last_name,
            "user_email": user_email,
            "roles": session.get("user").get("roles")
        }  

        session["user"] = user  

        toast = render_template("___toast_ok.html", message="User updated")
        return """<template>user updated</template>"""
    except Exception as ex:
        ic(ex)
        if "db" in locals(): db.rollback()
        if isinstance(ex, x.CustomException): return f"""<template mix-target="#toast" mix-bottom>{ex.message}</template>""", ex.code
        if isinstance(ex, x.mysql.connector.Error):
            if "users.user_email" in str(ex): return "<template>email not available</template>", 400
            return "<template>System upgrating</template>", 500        
        return "<template>System under maintenance</template>", 500    
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

##############################
@app.put("/items/<item_pk>")
def item_update(item_pk):
    try:
        item_pk = x.validate_uuid4(item_pk)
        item_title = x.validate_item_title()
        item_description = x.validate_item_description()
        item_price = x.validate_item_price()
        # file, item_image_name = x.validate_item_image()

        item_updated_at = int(time.time())

        db, cursor = x.db()
        q = """ UPDATE items
                SET item_title = %s, item_description = %s, item_price = %s, item_updated_at = %s
                WHERE item_pk = %s
            """
        cursor.execute(q, (item_title, item_description, item_price, item_updated_at, item_pk))
        if cursor.rowcount != 1: x.raise_custom_exception("cannot update item", 401)
        db.commit()

        toast = render_template("___toast_ok.html", message="Item updated")
        return f"""<template mix-target="#toast" mix-bottom>{toast}</template>"""
    except Exception as ex:
        ic(ex)
        if "db" in locals(): db.rollback()
        if isinstance(ex, x.CustomException): return f"""<template mix-target="#toast" mix-bottom>{ex.message}</template>""", ex.code
        if isinstance(ex, x.mysql.connector.Error):
            if "users.user_email" in str(ex): return "<template>email not available</template>", 400
            return "<template>System upgrating</template>", 500
        return "<template>System under maintenance</template>", 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.put("/users/block/<user_pk>")
def user_block(user_pk):
    try:        
        if not "admin" in session.get("user").get("roles"): return redirect(url_for("view_login"))
        user_pk = x.validate_uuid4(user_pk)
        user_blocked_at = int(time.time())

        db, cursor = x.db()
        q = 'UPDATE users SET user_blocked_at = %s WHERE user_pk = %s'
        cursor.execute(q, (user_blocked_at, user_pk))
        if cursor.rowcount != 1: x.raise_custom_exception("cannot block user", 400)
        db.commit()
        # return """<template>user blocked</template>"""

        return f"""<template mix-redirect="/admin"></template>"""

    except Exception as ex:
        ic(ex)
        if "db" in locals(): db.rollback()
        if isinstance(ex, x.CustomException): 
            return f"""<template mix-target="#toast" mix-bottom>{ex.message}</template>""", ex.code        
        if isinstance(ex, x.mysql.connector.Error):
            ic(ex)
            return "<template>Database error</template>", 500        
        return "<template>System under maintenance</template>", 500  
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.put("/users/unblock/<user_pk>")
def user_unblock(user_pk):
    try:
        if not "admin" in session.get("user").get("roles"): return redirect(url_for("view_login"))
        user_pk = x.validate_uuid4(user_pk)
        user_blocked_at = 0
        db, cursor = x.db()
        q = 'UPDATE users SET user_blocked_at = %s WHERE user_pk = %s'
        cursor.execute(q, (user_blocked_at, user_pk))
        if cursor.rowcount != 1: x.raise_custom_exception("cannot unblock user", 400)
        db.commit()
        return f"""<template mix-redirect="/admin"></template>"""
    
    except Exception as ex:

        ic(ex)
        if "db" in locals(): db.rollback()
        if isinstance(ex, x.CustomException): 
            return f"""<template mix-target="#toast" mix-bottom>{ex.message}</template>""", ex.code        
        if isinstance(ex, x.mysql.connector.Error):
            ic(ex)
            return "<template>Database error</template>", 500        
        return "<template>System under maintenance</template>", 500  
    
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

##############################
@app.put("/items/block/<item_pk>")
def item_block(item_pk):
    try:
        if not "admin" in session.get("user").get("roles"): return redirect(url_for("view_login"))
        item_pk = x.validate_uuid4(item_pk)
        item_blocked_at = int(time.time())

        db, cursor = x.db()
        q = 'UPDATE items SET item_blocked_at = %s WHERE item_pk = %s'
        cursor.execute(q, (item_blocked_at, item_pk))
        if cursor.rowcount != 1: x.raise_custom_exception("cannot block item", 400)
        db.commit()
        # btn_unblock = render_template("___btn_unblock_user.html", user=user)
        # toast = render_template("__toast.html", message="User blocked")
        # return f"""
        #         <template 
        #         mix-target='#block-{user_pk}' 
        #         mix-replace>
        #             {btn_unblock}
        #         </template>
        #         <template mix-target="#toast" mix-bottom>
        #             {toast}
        #         </template>
        #         """

        # Kan det virkelig være rigtigt kan jeg skal redirect? Kan jeg ikke bare udskifte knappen?
        return f"""
                <template mix-redirect="/admin"></template>
                """

    except Exception as ex:
        ic(ex)
        if "db" in locals(): db.rollback()
        if isinstance(ex, x.CustomException):
            return f"""<template mix-target="#toast" mix-bottom>{ex.message}</template>""", ex.code
        if isinstance(ex, x.mysql.connector.Error):
            ic(ex)
            return "<template>Database error</template>", 500
        return "<template>System under maintenance</template>", 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.put("/items/unblock/<item_pk>")
def item_unblock(item_pk):
    try:
        if not "admin" in session.get("user").get("roles"): return redirect(url_for("view_login"))
        item_pk = x.validate_uuid4(item_pk)
        item_blocked_at = 0
        db, cursor = x.db()
        q = 'UPDATE items SET item_blocked_at = %s WHERE item_pk = %s'
        cursor.execute(q, (item_blocked_at, item_pk))
        if cursor.rowcount != 1: x.raise_custom_exception("cannot unblock item", 400)
        db.commit()
        # toast = render_template("___toast_ok.html", message="User unblocked")
        # return f"""<template mix-target="#toast" mix-bottom>
        #             {toast}
        #         </template>"""
        return f"""
                <template mix-redirect="/admin"></template>
                """

    except Exception as ex:

        ic(ex)
        if "db" in locals(): db.rollback()
        if isinstance(ex, x.CustomException):
            return f"""<template mix-target="#toast" mix-bottom>{ex.message}</template>""", ex.code
        if isinstance(ex, x.mysql.connector.Error):
            ic(ex)
            return "<template>Database error</template>", 500
        return "<template>System under maintenance</template>", 500

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
##############################
##############################

def _________DELETE_________(): pass

##############################
##############################
##############################

##############################
@app.delete("/users/<user_pk>")
def user_delete(user_pk):
    try:
        # Check if user is logged
        if not session.get("user", ""): return redirect(url_for("view_login"))
        # Check if it is an admin
        if not "admin" in session.get("user").get("roles"): return redirect(url_for("view_login"))
        user_pk = x.validate_uuid4(user_pk)
        user_deleted_at = int(time.time())
        db, cursor = x.db()
        q = 'UPDATE users SET user_deleted_at = %s WHERE user_pk = %s'
        cursor.execute(q, (user_deleted_at, user_pk))
        if cursor.rowcount != 1: x.raise_custom_exception("cannot delete user", 400)
        db.commit()
        return """<template>user deleted</template>"""
    
    except Exception as ex:
        ic(ex)
        if "db" in locals(): db.rollback()
        if isinstance(ex, x.CustomException): 
            return f"""<template mix-target="#toast" mix-bottom>{ex.message}</template>""", ex.code        
        if isinstance(ex, x.mysql.connector.Error):
            ic(ex)
            return "<template>Database error</template>", 500        
        return "<template>System under maintenance</template>", 500  
    
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.delete("/items/<item_pk>")
def item_delete():
    try:
        # Check if user is logged
        if not session.get("user", ""): return redirect(url_for("view_login"))
        # Check if it is an partner????
        if not "partner" in session.get("user").get("roles"): return redirect(url_for("view_login"))
        item_pk = x.validate_uuid4(item_pk)
        item_deleted_at = int(time.time())
        db, cursor = x.db()
        q = 'UPDATE items SET item_deleted_at = %s WHERE item_pk = %s'
        cursor.execute(q, (item_deleted_at, item_pk))
        if cursor.rowcount != 1: x.raise_custom_exception("cannot delete item", 400)
        db.commit()
        return """<template>item deleted</template>"""
    except Exception as ex:
        ic(ex)
        if "db" in locals(): db.rollback()
        if isinstance(ex, x.CustomException): 
            return f"""<template mix-target="#toast" mix-bottom>{ex.message}</template>""", ex.code        
        if isinstance(ex, x.mysql.connector.Error):
            ic(ex)
            return "<template>Database error</template>", 500        
        return "<template>System under maintenance</template>", 500  
    
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

##############################
##############################
##############################

def _________BRIDGE_________(): pass

##############################
##############################
##############################


##############################
@app.get("/verify/<verification_key>")
@x.no_cache
def verify_user(verification_key):
    try:
        ic(verification_key)
        verification_key = x.validate_uuid4(verification_key)
        user_verified_at = int(time.time())

        db, cursor = x.db()
        q = """ UPDATE users 
                SET user_verified_at = %s 
                WHERE user_verification_key = %s"""
        cursor.execute(q, (user_verified_at, verification_key))
        if cursor.rowcount != 1: x.raise_custom_exception("cannot verify account", 400)
        db.commit()
        return redirect(url_for("view_login", message="User verified, please login"))

    except Exception as ex:
        ic(ex)
        if "db" in locals(): db.rollback()
        if isinstance(ex, x.CustomException): return ex.message, ex.code    
        if isinstance(ex, x.mysql.connector.Error):
            ic(ex)
            return "Database under maintenance", 500        
        return "System under maintenance", 500  
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()    