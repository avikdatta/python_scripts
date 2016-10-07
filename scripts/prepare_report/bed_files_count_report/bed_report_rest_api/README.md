# A REST Api for generating peak counts for bed file
This rest api can read an [index file]() and an experiment id and fetch the bed file from Blueprint FTP site and preoduce the peak count stats for each chromosome. It can generate either a JSON output dump or a png plot for the primary chromosomes.

##Usage
###Run Api script

  <pre><code>
    python3 prepare_ftp_bed_report_rest_api.py -w WORK_DIR -i INDEX_FILE  -p HOST_IP
  </pre></code>

###REST Query example
####Using curl
  <pre><code>
    curl 127.0.0.1:5000/bed_stats -X GET -d "exp_id=ERX0001" -d "mode=json"
  or
    curl 192.168.0.8:5000/bed_stats -X GET -d "exp_id=ERX0001" -d "mode=png" > ERX0001.png
  </pre></code>

####Using browser
  <pre><code>
    http://127.0.0.1:5000/bed_stats?exp_id=ERX00001&mode=json
  or
    http://127.0.0.1:5000/bed_stats?exp_id=ERX00001&mode=png
  </pre></code>

##Options

  <pre><code>
    -h / --help                  : Show this help message and exit
    -w / --work_dir WORK_DIR     : Work directory
    -f / --ftp_url FTP_URL       : FTP host, default: ftp.ebi.ac.uk
    -d / --ftp_dir FTP_DIR       : FTP directory path, default: /pub/databases/
    -i / --index_file INDEX_FILE : Index file contataining the bed file path
    -p / --host HOST_IP          : IP of the host server, default 127.0.0.1
  </pre></code>

##Requirements
* Python3
* Pandas
* Ftplib
* Tempfile
* Matplotlib
* Urllib

