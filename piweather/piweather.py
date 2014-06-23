"""
piweather.py

A Web based Temperature/Humidity monitor using Raspberry Pi and DHT11.

Author: Mahesh Venkitachalam
"""

from bottle import route, run, request, response
from bottle import static_file
import random
import RPi.GPIO as GPIO
from time import sleep  
import Adafruit_DHT

@route('/hello')
def hello():
    return "Hello Bottle World!"

@route('/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='flot')

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
	<script language="javascript" type="text/javascript" 
       src="jquery.js"></script>
	<script language="javascript" type="text/javascript" 
       src="jquery.flot.js"></script>
    <script language="javascript" type="text/javascript">

$(document).ready(function() {

    // plot options
    var options = {
        series: {
		  lines: {
			show: true
		  },
		  points: {
			show: true
		  }
		},
	    yaxis: {min: 0, max: 100},
        xaxis: {min: 0, max: 100}
    };
    
    // create empty plot
	var plot = $.plot("#placeholder", [[]], options);

    // initialize data arrays
    var RH = [];
    var T = []; 
    
    // get data from server
    function getData() {
        // AJAX callback
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
            plot.setData([{label: "RH", data: RH}, T]);
            plot.draw();
		}

        // AJAX error handler
        function onError(){
            $('#ajax-panel').html('<p><strong>Ajax error!</strong> </p>');
        }
        
        // make the AJAX call
		$.ajax({
		    url: "getdata",
			type: "GET",
			dataType: "json",
			success: onDataReceived,
            error: onError
		});        
     }

     // define an update function
	 function update() {
        // get data
        getData();
        // set timeout
		setTimeout(update, 1000);
	 }

     // call update
	 update();
 
     // define click handler for LED ctrl
     $('#ckLED').click(function() {
         var isChecked = $("#ckLED").is(":checked") ? 1:0;
         $.ajax({
           url: '/ledctrl',
           type: 'POST',
           data: { strID:'ckLED', strState:isChecked }
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
    
@route('/ledctrl', method='POST')
def ledctrl():
    val = request.forms.get('strState')
    on = bool(int(val))
    GPIO.output(18, on) 

# main() function
def main():
    print 'starting piweather...'
    # setup GPIO
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(18, GPIO.OUT)
    GPIO.output(18, False)
    # start server
    run(host='192.168.4.31', port='8080', debug=True)

# call main
if __name__ == '__main__':
    main()
