
import eHive
from db_index import connect_db


class Store_db_file(eHive.BaseRunnable):

  def param_defaults(self):
    return {
      'dbhost': 'localhost',
      'dbport': 3306,
      'dbtable': 'bed_files',
    }

  def run(self):
    experiment_id=self.param_required('experiment_id')
    output_file_path=self.param_required('output_file_path')
    dbname=self.param_required('dbname')
    dbuser=self.param_required('dbuser')
    dbpass=self.param_required('dbpass')
    dbhost=self.param('dbhost')
    dbport=self.param('dbport')
    dbtable=self.param('dbtable')
    
    db_params={'host':dbhost, 'user':dbuser,'password':dbpass,'db':dbname, 'port':dbport}

    try:
      db_cursor=connect_db(db_params)
      db_store_bed_file(db_conn=db_cursor, exp_id=experiment_id, file=output_file_path, table_name=dbtable) 
    except Exception as e:
      self.warning('DB error {0}'.format(e))
    finally:
      db_cursor.close()

 
  def db_store_bed_file(db_conn, exp_id, file, table_name='bed_files'):
    '''
    This function store the bed file information in a MySQL database table
    '''

    sql='''
        INSERT INTO `%s` ( `experiment_id`,  `filename`)
        VALUES (%s,%s)
        '''
    try:
      with db_conn.cursor() as cursor:
        cursor.execute(sql,(table_name, exp_id, file))
    except Exception as e:
      self.warning('Error while storing file {0}, error: {1}'.format(file, e))
    else:
      db_conn.commit()


