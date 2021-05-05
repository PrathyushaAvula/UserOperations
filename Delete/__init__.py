import logging
import time
import pyodbc
from datetime import datetime
import pytz
import json
import azure.functions as func
from SharedCode import connection

timez=pytz.timezone('Asia/Kolkata')
dt=datetime.now(timez)
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Deleting the user.')   
    req_response = req.get_json() 
    if req_response:
        id1=req_response.get('id')
        lastModificationTime=dt.strftime('%Y-%m-%d %H:%M:%S')
        lastModifierUserId=req_response.get('LastModifierUserId')
        conn = connection.getconnection()
        if conn:
            cursor=conn.cursor()
            query=f"UPDATE [dbo].[Users] SET IsDeleted='1', LastModifierUserId='{lastModifierUserId}',LastModificationTime='{lastModificationTime}' WHERE id='{id1}'"
            try:
                cursor.execute(query)   
                cursor.execute("select @@rowcount")
                rowcount = cursor.fetchall()[0][0]
                if rowcount>0:
                    cursor.commit()
                    conn.close()
                    return func.HttpResponse(("response"),status_code=200)
            except Exception as ex:
                conn.rollback()
                conn.close()
                logging.exception(f"Exception occurred while deleting a user - {ex}")
                return func.HttpResponse(
                "Something Went Wrong!",
                status_code=500
                )

    else:
        return func.HttpResponse(
            "No Parameters Passed",
            status_code=500
        )