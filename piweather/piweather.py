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

    var RH = [];
    var T = []; 

    function getData() {

        // ajax callback
        function onDataReceived(jsonData) {
            
            // add data
			RH.push([RH.length, jsonData.RH]);
            // removed oldest
            if (RH.length > 100) {
                RH.splice(0, 1);
            }

            T.push([T.length, jsonData.T]);
            // removed oldest
            if (T.length > 100) {
                T.splice(0, 1);
            }

            // set to plot
            plot.setData([RH, T]);
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

        
@route('/getdata', method='GET')
def getdata():
    """
    global dataVals
    val = dataVals[0]
    dataVals.popleft()
    #print val
    return {"RH": val[0], "T": val[1]}
    """
    RH, T = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 23)
    return {"RH": RH, "T": T}
    

# main() function
def main():
    # use sys.argv if needed
    print 'starting piweather...'
    
    thread = threading.Thread(target=getdata)
    thread.daemon = True
    thread.start()
    run(host='192.168.4.31', port='8080', debug=True)

# call main
if __name__ == '__main__':
    main()
