#A REST API for the JSON reports
This script is for fetching JSON report from a REST API developed using [Flask-RESTful package](https://github.com/flask-restful/flask-restful). In the default mode this api runs on the localhost with port 5000.

##Usage
###Run REST service
<pre><code>python json_report_restapi.py -i host_ip (default:127.0.0.1)
</pre></code>

###Query example
<pre><code>curl 127.0.0.1:5000/json_stats
</pre></code>

##Requirements
<ul>
<li>Python3</li>
<li>[Pandas](http://pandas.pydata.org/)</li>
<li>[Flask](http://flask.pocoo.org/)</li>
<li>[Flask-RESTful](https://github.com/flask-restful/flask-restful)</li>
<li>Json</ul>

