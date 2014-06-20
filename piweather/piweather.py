"""
piweather.py

A Web based Temperature/Humidity monitor using Raspberry Pi and DHT11.

Author: Mahesh Venkitachalam
"""

from bottle import route, run, request, response
from bottle import static_file
from collections import deque
import random
import threading, time, os, signal, sys, operator
import RPi.GPIO as GPIO
from time import sleep  
import Adafruit_DHT

@route('/hello')
def hello():
    return "Hello Bottle World!"

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
	<title>PiWeather</title>
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

$(document).ready(function() {

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
    
    // create empty plot
	var plot = $.plot("#placeholder", [[]], options);
    // initilaize data arrays
    var RH = [];
    var T = []; 
    
    function getData() {
        // ajax callback
        function onDataReceived(jsonData) {            
            // add RH data
			RH.push([RH.length, jsonData.RH]);
            // removed oldest
            if (RH.length > 100) {
                RH.splice(0, 1);
            }
            // add T data
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
		setTimeout(update, 1000);
	 }

	 update();

     $('#ckLED').click(function() {
         var isChecked = $("#ckLED").is(":checked") ? 1:0;
         $.ajax({
         url: '/action',
         type: 'POST',
         data: { strID:'ckLED', strState:isChecked }
         });
      });

     $('#btnFullPlot').click(function() {
         // error handler
        function onError(){
            $('#ajax-panel').html('<p><strong>Full Plot Ajax error!</strong> </p>');
        }

        // ajax callback
        function onDataReceived2(jsonData) {   
             var RH = [];
             var T = []
             for (var i = 0; i < jsonData.vals.length; ++i) {
				 RH.push([i, jsonData.vals[i][0]]);
                 T.push([i, jsonData.vals[i][1]]);
			 }

            // set to plot
            plot.setData([RH, T]);
            plot.draw();
        }

        // make ajax call
		$.ajax({
		    url: "fullplot",
			type: "GET",
			dataType: "json",
			success: onDataReceived2,
            error: onError
		}); 

     });

});

</script>
</head>

<body>

	<div id="header">
		<h2>Temperature/Humidity</h2>
	</div>

	<div id="content">

		<div class="demo-container">
			<div id="placeholder" class="demo-placeholder"></div>
		</div>

        <div id="ajax-panel"> </div>
	</div>

    <input type="checkbox" id="ckLED" value="on">Enable Lighting.<br>

</body>
</html>
'''
    
@route('/getdata', method='GET')
def getdata():
    RH, T = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 23)
    # return dict
    return {"RH": RH, "T": T}
    
@route('/action', method='POST')
def action():
    val = request.forms.get('strState')
    on = bool(int(val))
    GPIO.output(18, on) 

# main() function
def main():
    # use sys.argv if needed
    print 'starting piweather...'
    # setup GPIO
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(18, GPIO.OUT)
    GPIO.output(18, False)

    run(host='192.168.4.31', port='8080', debug=True)

# call main
if __name__ == '__main__':
    main()
