import os
import requests

from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

if os.path.exists(os.path.join(os.getcwd(), "config.py")):
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.py"))
else:
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.env.py"))

db = SQLAlchemy(app)
from parking.models import *  # pylint: disable=wrong-import-position

migrate = Migrate(app, db)


@app.route("/")
def index():
    """
    Renders the initial landing page.
    """
    return render_template("index.html")


@app.route("/booking", methods=['POST'])
def bookings():

    apt_info = requests.post(
        url="http://pass2parktx.com/index.php/Pages/getApartmentByName",
        data={"apt_no": app.config["APT_NO"],
              "owner_phone": app.config["PHONE"]}
    )

    apt_id = apt_info.json()[0]["AptId"]

    slot_number = requests.post(
        url="http://pass2parktx.com/index.php/Pages/getSlotidBySlotno",
        data={
            "apt_id": apt_id,
            "slot_no": "Guest"
        }
    )

    slot_id = slot_number.json()[0]["SlotId"]

    booking = requests.post(
        url="http://pass2parktx.com/index.php/Pages/slotBooking",
        data={
            "vehicle_model": request.form.get("model"),
            "flat_no": app.config["APT_NO"],
            "slot_id": slot_id,
            "plate": request.form.get("plate"),
            "color": request.form.get("color"),
            "user_name": request.form.get("name"),
            "user_email": "",
            "apt_id": apt_id
        }
    )

    booking_id = booking.json()["BookingId"]
    
    new_booking = Booking(
        id=booking_id,
        model=request.form.get("model"),
        name=request.form.get("name"),
        color=request.form.get("color"),
        plate=request.form.get("plate")
    )
    db.session.add(new_booking)
    db.session.commit()
    
    flash("Registration successful. Thank you!")
    return redirect("/booking/" + booking_id)


@app.route("/booking/<booking_id>")
def get_booking(booking_id):
    booking_info = requests.post(
        url="http://pass2parktx.com/index.php/Pages/userBookingList",
        data={
            "booking_id": booking_id
        }
    )

    return render_template(
        "confirmation.html",
        booking=booking_info.json()[0],
        booking_id=booking_id)


@app.route("/booking/<booking_id>/cancel")
def cancel_booking(booking_id):
    cancel = requests.post(
        url="http://pass2parktx.com/index.php/Pages/bookingCancellation",
        data={
            "booking_id": booking_id
        }
    )
    if "EndDate" not in cancel.json()[0]:
        return "Error Cancelling Reservation", 500
    
    booking_data = Booking.query.filter_by(id=booking_id).first()
    booking_data.cancelled = True
    db.session.commit()
    
    flash("Registration successfully cancelled. Please make sure your car is not left unattended.")
    return redirect("/")


@app.route("/list")
def list_bookings():
    booking_list = Booking.query.order_by(Booking.created.desc()).limit(10).all()
    return render_template("list.html", bookings=booking_list)
