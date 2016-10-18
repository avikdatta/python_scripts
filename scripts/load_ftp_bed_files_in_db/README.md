# A script for downloading all ChIP-Seq bed files from Blueprint's FTP site
This script can read a [index file](http://ftp.ebi.ac.uk/pub/databases/blueprint/releases/current_release/homo_sapiens/20160816.data.index) from Blueprint's FTP site and download the ChIP-Seq bed files from the [FTP site](http://ftp.ebi.ac.uk/pub/databases/blueprint/data/) to a local directory. Also it can add the experiment_id and the local file path name in a MySQL database. It uses Python pandas and reads the index file in chunks to minimize the memory requirement.

## Usage
### Create MySQL table
  <pre><code>
    mysql -hHOST -PPORT -uUSER -pPASS DBNAME < db_table.sql
  </pre></code>

### Download files and prepare DB
  <pre><code>
    python3 get_all_bed_files.py -i INDEX_FILE -w DOWNLOAD_DIR -n MYSQL_DBNAME -u MYSQL_USER -p MYSQL_PASS 
  </pre></code>

## Options
  <pre><code>
    -h /--help                       Show this help message and exit
    -f /--ftp_url FTP_URL            FTP url,  default=ftp.ebi.ac.uk
    -d /--dir_prefix DIR_PREFIX      FTP directory, default=/pub/databases/
    -i /--index_file INDEX_FILE      Index file containing the experiment and files information
    -w /--download_dir DOWNLOAD_DIR  Bed file download directory
    -m /--mysql_host MYSQL_HOST      MySQL server host name, default: localhost
    -P /--mysql_port MYSQL_PORT      MySQL server port id, default: 3306
    -n /--mysql_dbname MYSQL_DBNAME  MySQL server database name
    -u /--mysql_user MYSQL_USER      MySQL server user name
    -p /--mysql_pass MYSQL_PASS      MySQL server password name
    -t /--mysql_table MYSQL_TABLE    MySQL table name name for loading bed file details
  </pre></code>

## Requirements

* python3
* Python Pandas
* Pymysql
