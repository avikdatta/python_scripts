# Load FTP File information in Database
This script can read an index file present in FTP server and load the required information in an local MySQL database.
It also checks if the file urls are accessible or not. 

## Usage

 ` python3 python_scripts/scripts/ftp_index_stats.py \`
 `            --index_file 20160816.data.index \`
 `            --work_dir /path/work \`
 `            --dbuser user \`
 `            --dbpass pass \`
 `            --dbname db`

## Options

  `-f / --ftp_url    : FTP url, default: 'ftp.ebi.ac.uk'`
  `-l / --url_prefix : URL prefix for files  default='http://ftp.ebi.ac.uk/pub/databases/'`
  `-d / --dir_path   : FTP path, default: '/pub/databases/blueprint/releases/current_release/homo_sapiens/'`
  `-i / --index_file : Name of index file from FTP`
  `-w / --work_dir   : Path to temp directory`
  `-o / --dbhost     : MySQL db hostname, default: localhost`
  `-P / --dbport     : MySQL db port`
  `-u / --dbuser     : MySQL db user name`
  `-p / --dbpass     : MySQL db password`
  `-b / --dbname     : MySQL db name`


