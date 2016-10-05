#A REST API for the JSON reports
This script is based on [Flask-RESTful package](https://github.com/flask-restful/flask-restful). In the default mode this api runs on the localhost with port 5000.

##Usage
###Run REST service
<pre><code>python json_report_restapi.py -i host_ip (default:127.0.0.1)
</pre></code>

###Query example
<pre><code>curl 127.0.0.1:5000/json_stats
</pre></code>

##Requirements
<pre><code><ul>
<li>Python3</li>
<li>[Pandas](http://pandas.pydata.org/)</li>
<li>[Flask](http://flask.pocoo.org/)</li>
<li>[Flask-RESTful](https://github.com/flask-restful/flask-restful)</li>
<li>Json</ul></pre></code>

