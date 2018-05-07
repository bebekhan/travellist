""" Models and database functions for TravelList Project. """

from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()

######################################################################
# Model definitions

class User(db.Model):
    """User of TravelList website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(64), nullable=False)
    lname = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        """ Provide helpful representation when printed. """

        return "<User user_id={} fname={} email={}>".format(self.user_id,
                                                        self.fname, self.email)

class User_trip(db.Model):
    """ Common Table for User and Trip tables. """

    __tablename__ = "user_trips"

    user_trip_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.trip_id'))


class Trip(db.Model):
"""Trip on TravelList website."""

    __tablename__ = "trips"

    trip_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    start_date = db.Column(db.Integer, nullable=True)
    #user may not know when they want to take this trip. So, nullable=True.
    end_date = db.Column(db.Integer, nullable=True)
    city = db.Column(db.Integer, nullable=True)
    state = db.Column(db.String(2), nullable=True)

    user = db.relationship("User",
                             backref=db.backref("trips", order_by=trip_id))
    activity = db.relationship("Activity",
                                backref=db.backref("trips", order_by=trip_id))

    def __repr__(self):
        """ Provide helpful representation when printed. """

        return "<Trip: trip_id={} city={} state={}>".format(self.trip_id,
                                                        self.city, self.state)


class Activity(db.Model):
    """ Activities during Trip on TravelList website. """

    __tablename__ = "activities"

    activity_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.trip_id'))
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(250), nullable=True)
    date = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(200), nullable=True)
    zipcode =  db.Column(db.Integer, nullable=True)


    def __repr__(self):
        """ Provide helpful representation when printed. """

        return "<Trip: trip__id={} activity_id={} name={} date={}>".format(self.trip_id,
                                                        self.activity_id, self.name, self.date)



##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///travellist'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."