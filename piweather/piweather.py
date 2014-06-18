"""
piweather.py

A Web based Temperature/Humidity monitor using Raspberry Pi and DHT11.

Author: Mahesh Venkitachalam
"""

from bottle import route, run, request, response
from bottle import static_file
import threading
from collections import deque
import random

import sys
import RPi.GPIO as GPIO
from time import sleep  
import Adafruit_DHT

@route('/hello')
def hello():
    return "Hello Bottle World!"

# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT22, or Adafruit_AM2302.
sensor = Adafruit_DHT.DHT11

# Example using a Raspberry Pi with DHT sensor
# connected to pin 23.
pin = 23

def blink():
    """
    Make LED connected to pin 18 (board) blink
    """
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(18, GPIO.OUT)
    
    while True:
        try:
            GPIO.output(18, True)
            sleep(0.5)
            GPIO.output(18, False)
            sleep(0.5)
        except:
            print 'exiting...'
            # off
            GPIO.output(18, False)
            break

@route('/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='flot')

@route('/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='flot/examples')

@route('/plot')
def plot():
    return '''
<html>
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	<title>Flot</title>
    <style>
     .demo-placeholder {
	width: 80%;
	height: 80%;
	font-size: 14px;
	line-height: 1.2em;
    }
    </style>
	<script language="javascript" type="text/javascript" src="jquery.js"></script>
	<script language="javascript" type="text/javascript" src="jquery.flot.js"></script>
    <script language="javascript" type="text/javascript">

$(function() {

    // plot options
    var options = {
			  series: {
				    shadowSize: 0	
			  },
        lines: {
				    show: true
			  },
			  points: {
				    show: true
			  },
			  yaxis: {
				    min: 0,
				    max: 100
			  },
        xaxis: {
				    min: 0,
				    max: 100
			  }
		};
    
    // empty plot
		var plot = $.plot("#placeholder", [[]], 
                      options);

    var data = [];

    function getData() {

        // ajax callback
        function onDataReceived(jsonData) {
            
            // add data
					  data.push(jsonData.data);
            // removed oldest
            if (data.length > 100) {
                data.splice(0, 1);
            }

            // prepare data
            var res = [];
			      for (var i = 0; i < data.length; ++i) {
				        res.push([i, data[i]])
			      }
            
            // set to plot
            plot.setData([res]);
            plot.draw();
		    }

        // error handler
        function onError(){
            $('#ajax-panel').html('<p><strong>Ajax error!</strong> </p>');
        }
        
        // make ajax call
				$.ajax({
					  url: "getdata",
					  type: "GET",
					  dataType: "json",
					  success: onDataReceived,
            error: onError
				});        
    }

		function update() {

        // get data
        getData();

        // set timeout
			  setTimeout(update, 100);
		}

		update();
});

    </script>

</head>
<body>

	<div id="header">
		<h2>Sensor Data</h2>
	</div>

	<div id="content">

		<div class="demo-container">
			<div id="placeholder" class="demo-placeholder"></div>
		</div>

        <div id="ajax-panel"> </div>
	</div>
</body>
</html>
'''

dataVals = deque()

def genData():
    global deque
    while True:
        val = 100*random.random()
        dataVals.append(val)
        #print dataVals
        sleep(0.1)

def genDH11Data():
    global deque
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        if humidity is not None and temperature is not None:
            dataVals.append(temperature)
        else:
            pass
        sleep(0.5)
        
@route('/getdata', method='GET')
def getdata():
    global dataVals
    val = dataVals[0]
    dataVals.popleft()
    #print val
    return {"label": "A", "data": val}


# main() function
def main():
    # use sys.argv if needed
    print 'starting piweather...'
    
    """
    pinNum = 16
    while True:

        # Try to grab a sensor reading.  
        # Use the read_retry method which will retry up
        # to 15 times to get a sensor reading 
        # (waiting 2 seconds between each retry).
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

        # Note that sometimes you won't get a reading and
        # the results will be null (because Linux can't
        # guarantee the timing of calls to read the sensor).  
        # If this happens try again!
        if humidity is not None and temperature is not None:
            print 'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity)
        else:
            print 'Failed to get reading. Try again!'

        sleep(2)
    """

    thread = threading.Thread(target=getDHT11Data)
    thread.daemon = True
    thread.start()
    run(host='192.168.4.31', port='8080', debug=True)

# call main
if __name__ == '__main__':
    main()
