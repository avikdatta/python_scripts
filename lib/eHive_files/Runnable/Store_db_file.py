
import eHive, sys
from db_index import connect_db
from warnings import warn

def db_store_bed_file(db_params, exp_id, file):
  '''
  This function store the bed file information in a MySQL database table
  '''

  db_conn=connect_db(db_params)

  sql='''
      INSERT INTO `bed_files` ( `experiment_id`, `filename`)
      VALUES (%s,%s)
      '''
  try:
    with db_conn.cursor() as cursor:
      cursor.execute(sql,(exp_id, file))
  except Exception as e:
    sys.exit('Error while storing file {0}, error: {1}, param is: {2}'.format(file, e, db_params))
  else:
    db_conn.commit()
  finally:
    db_conn.close()



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
    
    db_params={'host':dbhost, 'user':dbuser, 'password':dbpass, 'db':dbname, 'port':dbport}
    try:
      db_store_bed_file(db_params=db_params, exp_id=experiment_id, file=output_file_path) 
    except Exception as e:
      sys.exit('DB error {0}'.format(e))

 
