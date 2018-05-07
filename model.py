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
    user_id # is a foreign key
    trip_id # is a foreign key

    # doesn't need a repr function since this table is an association table

class Trip(db.Model):
"""Trip on TravelList website."""

    __tablename__ = "trips"

    trip_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    start_date = db.Column(db.Integer, nullable=True)
    #user may not know when they want to take this trip. So, nullable=True.
    end_date = db.Column(db.Integer, nullable=True)
    city = db.Column(db.Integer, nullable=True)
    state = db.Column(db.String(2), nullable=True)



























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