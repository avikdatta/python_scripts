# Python scripts [![Documentation Status](https://readthedocs.org/projects/python-scripts/badge/?version=latest)](http://python-scripts.readthedocs.io/en/latest/?badge=latest)

This is a repository for python scripts

## List of scripts
* [Load FTP File information in Database](scripts/load_ftp_files).
* [JSON trackhub](scripts/index_to_json_hub).
* JSON report for data release using [script](scripts/prepare_report/index_report/json_report) and [REST api](scripts/prepare_report/index_report/json_report_rest).
* Bed files stats using [script](scripts/prepare_report/bed_files_count_report/bed_report_script) and [REST api](scripts/prepare_report/bed_files_count_report/bed_report_rest_api).
* A [script](scripts/prepare_dataframe) for generation of the ChIP-Seq peak count dataframe.
* A [REST Api](scripts/plot_data/plot_bed_peak_for_group/) for generating ChIP-Seq peak count boxplot.
* A [script](scripts/load_ftp_bed_files_in_db) for downloading all ChIP-Seq peak call bed files from FTP site.
* An [eHive pipeline](/lib/Hive/PipeConfig/Get_FTP_bed_files) for downloading ChIP-Seq peak call bed files from FTP
