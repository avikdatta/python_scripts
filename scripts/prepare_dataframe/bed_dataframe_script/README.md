# A script for preparing peak count for all bed files
This script can read an [index file](ftp://ftp.ebi.ac.uk/pub/databases/blueprint/releases/current_release/homo_sapiens/20160816.data.index) and fetch all the ChIP-Seq bed files from Blueprint's [FTP site](ftp://ftp.ebi.ac.uk/pub/databases/blueprint/data/). Then it generates an individual bed peak counts plot for each experiments and also combine these counts for all the bed file and store it in an output csv file.

##Usage
<pre><code>
  python get_all_ftp_bed_files_to_dataframe.py -w WORK_DIR -o OUTPUT_CSV -i INDEX_FILE
</pre></code>

## Options
<pre><code>

  -h, --help                   : Show this help message and exit
  -w /--work_dir WORK_DIR      : Work directory
  -o /--output_csv OUTPUT_CSV  : Output CVS file
  -i /--index_file INDEX_FILE  : Index file
  -f /--ftp_url FTP_URL        : FTP url, default: ftp.ebi.ac.uk
  -d /--dir_prefix DIR_PREFIX  : FTP directory prefix, default: /pub/databases/

</pre></code>

##Requirements

* Python3
* Python Pandas
* Matplotlib

