# An eHive pipeline for downloading ChIP-Seq peak call bed files from FTP
This is a [eHive](https://github.com/Ensembl/ensembl-hive) configuration file for donwloading ChIP-Seq peak call bed files from Blueprint's FTP site and load them to a MySQL database. This pipeline uses the Python3 wrapper script of the eHive codebase. It utilises an [index file](http://ftp.ebi.ac.uk/pub/databases/blueprint/releases/current_release/homo_sapiens/20160816.data.index) from the Blueprint project for collecting the file url information.

## Setup Pipeline
### Get python_script repo
  <pre><code>
  git clone https://github.com/avikdatta/python_scripts.git
  </pre></code>

### Downlonload eHive from Git
  <pre><code>
  git clone https://github.com/Ensembl/ensembl-hive.git
  </pre></code>

### Set Environment
  <pre><code>
  export PYTHONPATH=$PYTHONPATH:/path/python_scripts/lib
  export PYTHONPATH=$PYTHONPATH:/path/ensembl-hive/wrappers/python3
  export PERL5LIB=$PERL5LIB:/path/python_scripts/lib
  export PERL5LIB=$PERL5LIB:/path/ensembl-hive/modules
  export PATH=$PATH:/path/ensembl-hive/scripts
  </pre></code>

### Create MySQL table for storing files
  <pre><code>
  mysql -hHOST -PPORT -uUSER -pPASS bed_files < python_scripts/scripts/load_ftp_bed_files_in_db/db_table.sql 
  </pre></code>

### Initialise pipeline
  <pre><code>
   init_pipeline.pl Hive::PipeConfig::Get_FTP_bed_files::Get_FTP_bed_files_pyconf \
  -user HIVE_DBUSER \
  -password HIVE_DBPASS \
  -store_dir /path/store_dir \
  -file_dbname DBNAME \
  -file_dbuser DBUSER \
  -file_dbpass DBPASS
  </pre></code>

### Seed pipeline
  <pre><code>
  seed_pipeline.pl \
  -url mysql://HIVE_DBUSER:HIVE_DBPASS@DBHOST/HIVE_DBNAME \
  -logic_name 'bed_file_factory' \
  -input_id '{ "index_file"=>"/path/index_file"}'
  </pre></code>

### Run pipeline
  <pre><code>
  beekeeper.pl -url mysql://HIVE_DBUSER:HIVE_DBPASS@DBHOST/HIVE_DBNAME -loop 
  </pre></code>

## Requirements

* [Ensembl eHive](https://github.com/Ensembl/ensembl-hive)
* Python3
* Python Pandas
* Pymysql

