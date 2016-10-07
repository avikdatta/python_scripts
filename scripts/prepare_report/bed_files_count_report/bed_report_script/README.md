# A script for generating peak counts for bed file
This script accepts an [index file]() and an experiment id and can fetch the bed file from Blueprint FTP site and preoduce the peak count stats for each chromosome. It generates a JSON output dump and a png plot for the primary chromosomes.

##Usage
  <pre><code>
    python3 prepare_ftp_bed_report.py -w WORK_DIR -i INDEX_FILE -e EXPERIMENT ID
  </pre></code>

##Options

  <pre><code>
    -h / --help                  : Show this help message and exit
    -w / --work_dir WORK_DIR     : Work directory
    -f / --ftp_url FTP_URL       : FTP host, default: ftp.ebi.ac.uk
    -d / --ftp_dir FTP_DIR       : FTP directory path, default: /pub/databases/
    -i / --index_file INDEX_FILE : Index file contataining the bed file path
    -e / --id EXPERIMENT_ID      : Experiment id for ChIp-Seq data
  </pre></code>

##Requirements
* Python3
* Pandas
* Ftplib
* Tempfile
* Matplotlib
* Urllib

