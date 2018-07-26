'''

Adapted excerpt from Getting Started with Raspberry Pi by Matt Richardson

Modified by Rui Santos
Complete project details: http://randomnerdtutorials.com

'''


import datetime, time
import RPi.GPIO as GPIO
from flask import Flask, render_template
import flask

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)


GPIO.output(26, GPIO.HIGH)

# Create a dictionary called pins to store the pin number name and pin state:
pins = {
   16 : {'name' : 'GPIO 16', 'state' : GPIO.LOW}, # name = GPIO 16 AND  state=low
   }

# Set each pin as an output/input and make it low:
#for pin in pins:
#   GPIO.setup(pin, GPIO.OUT)
#   GPIO.output(pin, GPIO.LOW)
GPIO.setup(20, GPIO.IN)

def event_stream():
    count = 0
    while True:
        mybutton = GPIO.input(20)
        if mybutton == True:
            count += 1
            yield "data: Button press #%d @ %s\n\n" % (count, datetime.datetime.now())
            time.sleep(.2)
           


@app.route('/stream')
def stream():
    return flask.Response(event_stream(), mimetype="text/event-stream")

@app.route("/")
def main():
   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)


   # Put the pin dictionary into the template data dictionary:
   templateData = {
      'pins': pins,
   }



   # Pass the template data into the template main.html and return it to the user
   return render_template('main.html', **templateData)






# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<changePin>/<action>")
def action(changePin, action):
   # Convert the pin from the URL into an integer:
   changePin = int(changePin)
   # Get the device name for the pin being changed:
   deviceName = pins[changePin]['name']
   # If the action part of the URL is "on," execute the code indented below:
   if action == "on":
      # Set the pin high:
      GPIO.output(changePin, GPIO.HIGH)
      # Save the status message to be passed into the template:
      message = "Turned " + deviceName + " on."
   if action == "off":
      GPIO.output(changePin, GPIO.LOW)
      message = "Turned " + deviceName + " off."

   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)

   # Along with the pin dictionary, put the message into the template data dictionary:
   templateData = {
      'pins' : pins
   }


   return render_template('main.html', **templateData)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
