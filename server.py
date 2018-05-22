"""Travellist."""
from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, UserTrip, Trip, Activity


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("register.html")

@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    # taking user email and password from form
    user_email = request.form.get("email")
    user_password = request.form.get("password")
    user_name = request.form.get("name")

    # checking to see if user already exists in db.
    check_email = User.query.filter_by(email=user_email).first()
    #indexing into the form.

    if check_email:
        flash('Email already exists!')
        return redirect('/login')
        
    # if no user exists add to database.
    else:
        new_user = User(name=user_name, email=user_email, password=user_password) 
        #add user
        db.session.add(new_user)
        #commit this change
        db.session.commit()   

        flash("User {} added. Going forward please user your {} and password to login".format(user_name, user_email))
#should eventually be routed to /user page to create/view trips and activites
    return render_template('user.html')

@app.route('/login', methods=['GET'])
def login_form():
        """Show login form."""
        return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    email = request.form["email"]
    password = request.form["password"]

    # Query for email address in db
    user = User.query.filter_by(email=email).first()
    # check_user_password = User.quesy.filter_by(password=user_password).first()

    if not user:
        flash("No account exists!")
        return redirect("/register")
  
    if user.password != password:
        flash("Incorrect credentials. Please try again.")
        return redirect("/login")

#create a session for this user.
    session["user_id"] = user.user_id
    #flash message to inform user they are logged in.
    flash("Successfully Logged In!")
    #once logged in, the user should be directed to their personal users page.
    return render_template("homepage.html", user=user)

@app.route('/logout', methods=['GET'])
def logout():
    """Log user out of current session."""

    del session["user_id"]
    flash("Logged Out.")
    return render_template("logout.html")


# @app.route('/user', methods=['GET'])
# def user_page():
#     """User can see all current profile data and Trips."""

#     return render_template('user.html') 


@app.route('/user', methods=['GET'])
def view_trip():
    """View all trips for single user."""
    user_id = session.get("user_id")
    user_trips = UserTrip.query.filter_by(user_id=user_id).all()

    print user_trips
    trips = []
    for user_trip in user_trips:
        trips.append(user_trip.trip)

    print trips

    for item in trips:
        print "User trips listing: ", item

    if not user_id:
        return redirect("/login")
    else:
        return render_template("user.html", trips=trips)


@app.route('/add-trip', methods=['GET'])
def add_trip_page_view():
    """Fetches the page for user to add trip.""" 
    return render_template('add-trip.html') 
        

@app.route('/add-trip', methods=['POST'])
def add_trip():
    """Add a trip."""
    if request.form:
        new_trip = Trip(city=request.form.get("city"), state=request.form.get("state"))
        db.session.add(new_trip)
        user = User.query.get(session["user_id"])
        user_trip = UserTrip(user_id=user.user_id, trip_id=new_trip.trip_id)
        
        db.session.add(user_trip)

        db.session.commit()
        print "Trip has been committed to db", new_trip
        flash("Trip has been committed to db!")

    return redirect("/user")

@app.route('/update-trip', methods=['POST']) # NEED HELP WITH THIS ONE!!!
def update_trip_item_search():
    """Search for existing trip to update."""
    if request.form:
        print request.form.get("city")
        print request.form.get("state")
        # getting information from form on user's page relating to city/state
        old_trip_lookup = Trip.query.filter_by(city=request.form.get("city"), state=request.form.get("state")).first()
        flash("Preparing to update this trip!")
        print "This is the trip to update: ", old_trip_lookup
        print "This is the object at city: ", old_trip_lookup.city
        print "This is the object at state: ", old_trip_lookup.state
    
    return render_template("update-trip.html", old_trip_lookup=old_trip_lookup) 

# @app.route('/confirm-update-trip', methods=['POST'])
# def confirm_update_to_trip():
#     """Update trip object in Trip db."""
#     if update_trip_item_search() == True:
#         print request.form.get("city")
#         print request.form.get("state")
#         # getting information from form on user's page relating to city/state
#         new_trip = Trip(city=request.form.get("city"), state=request.form.get("state"))
#         print "new_trip details are: ", new_trip
#         db.session.add(new_trip)
#             #adding & commiting the updated trip city/state to replace old trip
#         db.session.commit()
    
#     return render_template("confirm-update-trip.html", new_trip=new_trip)

@app.route('/delete-trip', methods=['GET'])
def delete_page_view():
    """Fetches the page for user to delete trip.""" 
    return render_template('delete-trip.html') 
        

@app.route('/delete-trip', methods=['POST'])
def delete_trip():
    """Delete a trip."""
    if request.form:
        trip_lookup = Trip.query.filter_by(city=request.form.get("city"), state=request.form.get("state")).first()
        print trip_lookup


        user = User.query.get(session["user_id"])

        # user = session['user'] # one less query method to get the session.
        # print "user", user

        user_trip_middle = UserTrip.query.filter_by(user_id=user.user_id, trip_id=trip_lookup.trip_id).delete()
        db.session.commit()

        user_trip_main = Trip.query.filter_by(trip_id=trip_lookup.trip_id).delete()
        print "THIS IS FROM THE MAIN QUERY THAT I WANT TO DELETE *****", user_trip_main
        db.session.commit()


        # db.session.commit()
        # flash("Trip deleted!")   

    return render_template("delete-trip.html", trip_lookup=trip_lookup)   

# @app.route('/activity', methods=['POST'])
#create the route
# def add_trip_activity():
#     """Add activity to a trip."""
#     if request.form:
#         if trip_id in UserTrip.trip:
#             trip_cat = Activity(category=request.form.get("category"))
#             trip_act = Activity(category=request.form.get("description"))
#             db.session.add(trip_cat)
#             db.session.add(trip.act)
#             db.session.commit()

    # activities_view =  activity.query.all()       

    # return render_template("activity.html")        

     
                  
if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug
    connect_to_db(app)
    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.run(port=5000, host='0.0.0.0')                  
