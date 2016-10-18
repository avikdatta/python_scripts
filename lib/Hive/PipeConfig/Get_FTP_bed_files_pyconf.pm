package Hive::PipeConfig::Get_FTP_bed_files_pyconf;

use strict;
use warnings;

use base ('Bio::EnsEMBL::Hive::PipeConfig::HiveGeneric_conf');

sub default_options {
  my ($self) = @_;
  return {
    %{ $self->SUPER::default_options() },
    'store_dir'  => undef,
    'index_file' => undef,
    'dbhost'     => 'localhost',
    'dbport'     => 3306,
    'dbname'     => undef,
    'dbuser'     => undef,
    'dbpass'     => undef,
    'dbtable'    => 'bed_files,
  ];  
}

sub pipeline_create_commands {
  my ($self) = @_;
  return [
    @{$self->SUPER::pipeline_create_commands},
  ];
}

sub pipeline_wide_parameters {
  my ($self) = @_;
  return {
    %{$self->SUPER::pipeline_wide_parameters},
  };
}

sub hive_meta_table {
  my ($self) = @_;
  return {
    %{$self->SUPER::hive_meta_table},
    'hive_use_param_stack'  => 1,
  };
}

sub pipeline_analyses {
  my ($self) = @_;
  return [
    { -logic_name  => 'bed_file_factory',
      -module      => 'eHive.Runnable.Ftp_bed_file_factory',
      -language    => 'python3',
      -meadow_type => 'LOCAL', 
      ],
      -flow_into => {
        2 => ['fetch_ftp_file'],
      },
    },
    { -logic_name  => 'fetch_ftp_file',
      -module      => 'eHive.Runnable.Fetch_ftp_file',
      -language    => 'python3',
      -meadow_type => 'LOCAL',
      -parameters    => {
        'store_dir' => $self->o('store_dir'),
      },
      -flow_into   => {
         1 => ['store_db_file'],            
      },  
    },
    { -logic_name  => 'store_db_file', 
      -module      => 'eHive.Runnable.Store_db_file',
      -language    => 'python3',
      -meadow_type => 'LOCAL',
      -parameters    => {
        'dbhost' => $self->o('file_dbhost'),
        'dbport' => $self->o('file_dbport'),
        'dbname' => $self->o('file_dbname'),
        'dbuser' => $self->o('file_dbuser'),
        'dbpass' => $self->o('file_dbpass'),
        'dbtable'=> $self->o('file_dbtable'),
      },
    },
  ];
}

1;
