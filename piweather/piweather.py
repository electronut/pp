"""
piweather.py

A Web based Temperature/Humidity monitor using Raspberry Pi and DHT11.

Author: Mahesh Venkitachalam
"""

from bottle import route, run, request, response
from bottle import static_file
import random, argparse
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
	width: 90%;
	height: 50%;
    }
    </style>
	<script language="javascript" type="text/javascript" 
       src="jquery.js"></script>
	<script language="javascript" type="text/javascript" 
       src="jquery.flot.js"></script>
    <script language="javascript" type="text/javascript" 
       src="jquery.flot.time.js"></script>
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
        grid: {
		  clickable: true
		},
	    yaxes: [{min: 0, max: 100}],
        xaxes: [{min: 0, max: 100}],
    };
    
    // create empty plot
	var plot = $.plot("#placeholder", [[]], options);

    // initialize data arrays
    var RH = [];
    var T = []; 
    var timeStamp = [];    
    // get data from server
    function getData() {
        // AJAX callback
        function onDataReceived(jsonData) {    
            timeStamp.push(Date());
            // add RH data
			RH.push(jsonData.RH);
            // removed oldest
            if (RH.length > 100) {
              RH.splice(0, 1);
            }
            // add T data
            T.push(jsonData.T);
            // removed oldest
            if (T.length > 100) {
              T.splice(0, 1);
            }
            s1 = [];
            s2 = [];
            for (var i = 0; i < RH.length; i++) {
                s1.push([i, RH[i]]);
                s2.push([i, T[i]]);
            }
            // set to plot
            plot.setData([s1, s2]);
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

     $("#placeholder").bind("plotclick", function (event, pos, item) {
          if (item) {
            plot.highlight(item.series, item.datapoint);
            var strData = ' [Clicked Data: ' + 
                           timeStamp[item.dataIndex] + ': T = ' + 
                           T[item.dataIndex] + ', RH = ' + RH[item.dataIndex]
                          + ']';
            $('#data-values').html(strData);
          }
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
    <div>
      <input type="checkbox" id="ckLED" value="on">Enable Lighting.
      <span id="data-values"> </span>
    </div>
    
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
    # create parser
    parser = argparse.ArgumentParser(description="PiWeather...")
    # add expected arguments
    parser.add_argument('--ip', dest='ipAddr', required=True)
    parser.add_argument('--port', dest='portNum', required=True)

    # parse args
    args = parser.parse_args()

    # setup GPIO
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(18, GPIO.OUT)
    GPIO.output(18, False)
    # start server
    run(host=args.ipAddr, port=args.portNum, debug=True)

# call main
if __name__ == '__main__':
    main()
