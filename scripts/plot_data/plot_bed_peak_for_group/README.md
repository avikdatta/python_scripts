# A REST Api for preparing ChIP-Seq peak count boxplot
This script can read a csv file containing the per chromosome peak counts for each ChIP-Seq bed file and an index file containing the experiment metadata (similar to this [file](http://ftp.ebi.ac.uk/pub/databases/blueprint/releases/current_release/homo_sapiens/20160816.data.index)). CSV dataframe can be prepared using the [bed_dataframe_script](https://github.com/avikdatta/python_scripts/blob/master/scripts/prepare_dataframe/bed_dataframe_script/) script.

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
  http://127.0.0.1:5000/all_histone?chr=chr1&chr=chr2&chr=chr3&chr=chr4&fig_font=12&fig_width=12&fig_height=8
  </pre></code>

* Get peak count plot for any specific celltype and histone
  <pre><code>
  http://127.0.0.1:5000/cell_types?cell_type=monocyte&histone=H3K4me1
  </pre></code>

#### Using curl

* Generate a boxplot of peak counts for all experiments
  <pre><code>
  curl 127.0.0.1:5000/all_histone > plot.png
  </pre></code>

* Get a boxplot for selected histone mark
  <pre><code>
  curl 127.0.0.1:5000/histone_peak -d "histone=H3K27ac" -X GET > plot.png
  </pre></code>


* Generate a boxplot for selected chromosome
  <pre><code>
  curl 127.0.0.1:5000/all_histone -d "chr=chr1" -d "chr=chr2" -d "chr=chr3" -d "chr=chr4" -X GET >plot.png
  </pre></code>

* Change dimension of the boxplot
  <pre><code>
  curl 127.0.0.1:5000/all_histone -d "chr=chr1" -d "chr=chr2" -d "chr=chr3" -d "chr=chr4" -d "fig_font=12" -d "fig_width=12 -d "fig_height=8" -X GET >plot.png
  </pre></code>

* Get peak count plot for any specific celltype and histone
  <pre><code>
  curl 127.0.0.1:5000/cell_types -X GET -d "cell_type=monocyte" -d "histone=H3K4me1"
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

