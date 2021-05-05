import pyodbc
import logging

def getconnection():
    try:
        logging.info('Trying to connect to the Catalog Database.')    
        server='tcp:sqlserverdss.database.windows.net,1433'
        database='catalog'
        username='DSS_ADMIN'
        password='Dddd@123'
        driver='{ODBC Driver 17 for SQL Server}' 
        connection_string = f'''
            Driver={driver};
            Server={server};
            Database={database};
            Uid={username};
            Pwd={password};
            Encrypt=yes;
            TrustServerCertificate=no;
            Connection Timeout=30;
        '''
        conn = pyodbc.connect(connection_string)
        logging.info('Database Connection Successful')    
        return conn
    except Exception as ex:
        logging.exception('Database Connection Failed - '+ str(ex))
        raise ex