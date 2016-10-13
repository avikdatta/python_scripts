# A REST Api for preparing ChIP-Seq peak count boxplot
This script can read a csv file containing the per chromosome peak counts for each ChIP-Seq bed file and an index file containing the experiment metadata (similar to this [file](http://ftp.ebi.ac.uk/pub/databases/blueprint/releases/current_release/homo_sapiens/20160816.data.index)). CSV dataframe can be prepared using the [get_all_ftp_bed_files_to_dataframe.py](https://github.com/avikdatta/python_scripts/blob/master/scripts/prepare_dataframe/bed_dataframe_script/get_all_ftp_bed_files_to_dataframe.py) script.

## Usage

### Run Api script
  <pre><code>
  python plot_bed_peak_for_group_rest_api.py -w /path/work_dir -i INDEX_FILE -d CSV_DATA -p HOST_IP
  </pre></code>

### REST Query example

#### Using browser

* Generate a boxplot of peak counts for all experiments
<pre><code>
http://127.0.0.1:5000/all_histone
</pre></code>

* Get a boxplot for selected histone mark 
<pre><code>
http://127.0.0.1:5000/histone_peak?histone=H3K27ac
</pre></code>

* Generate a boxplot for selected chromosome
<pre><code>
http://127.0.0.1:5000/all_histone?chr=chr1&chr=chr2&chr=chr3&chr=chr4&chr=chr6&chr=chr21
</pre></code>

* Change dimension of the boxplot
<pre><code>
http://192.168.0.8:5000/all_histone?chr=chr1&chr=chr2&chr=chr3&chr=chr4&fig_font=12&fig_width=12&fig_height=8
</pre></code>

#### Using curl

* Generate a boxplot of peak counts for all experiments
  <pre><code>
  curl http://127.0.0.1:5000/all_histone > plot.png
  </pre></code>

* Get a boxplot for selected histone mark
  <pre><code>
  curl 127.0.0.1:5000/histone_peak?histone=H3K27ac > plot.png
  </pre></code>


* Generate a boxplot for selected chromosome
  <pre><code>
  curl 127.0.0.1:5000/all_histone?chr=chr1&chr=chr2&chr=chr3&chr=chr4&chr=chr6&chr=chr21 -X GET >plot.png
  </pre></code>

* Change dimension of the boxplot
  <pre><code>
  curl 127.0.0.1:5000/all_histone?chr=chr1&chr=chr2&chr=chr3&chr=chr4&fig_font=12&fig_width=12&fig_height=8 -X GET >plot.png
  </pre></code>

## Option

<pre><code>
  -h /--help                   : Show this help message and exit
  -w /--work_dir WORK_DIR      : Work directory
  -i /--index_file INDEX_FILE  : Index file contataining the bed file path
  -d /--csv_data CSV_DATA      : CSV dataframe containing BED peak counts per chromosome
  -p /--host HOST              : REST api host ip
</pre></code>

## Requirement

* Python3
* Pandas
* Flask-RESTful
* Matplotlib

