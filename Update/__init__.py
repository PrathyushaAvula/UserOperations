import logging
import csv
import time
from datetime import datetime
import azure.functions as func
import pytz
import json
from SharedCode import connection

timez=pytz.timezone('Asia/Kolkata')
dt=datetime.now(timez)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    req_response = req.get_json() 
    if req_response:
        Id1=req_response.get('id')
        Username=req_response.get('username')
        Surname=req_response.get('surname')
        EmailAddress=req_response.get('emailAddress')
        IsActive=req_response.get('isActive')
        Name=req_response.get('name')
        LastModifierUserId = req_response.get('modifierUserId')
        LastModificationTime=dt.strftime('%Y-%m-%d %H:%M:%S')
        conn = connection.getconnection()
        if conn:
            crsr=conn.cursor()
            query=f"UPDATE [dbo].[Users] SET UserName='{Username}',Surname='{Surname}',EmailAddress='{EmailAddress}', IsActive='{IsActive}',Name='{Name}',LastModificationTime='{LastModificationTime}',LastModifierUserId='{LastModifierUserId}' WHERE id='{Id1}'"
            try:
                crsr.execute(query)    
                crsr.execute("select @@rowcount")
                rowcount = crsr.fetchall()[0][0]
                crsr.commit()
                conn.close()
                if rowcount>0:                    
                    return func.HttpResponse(
                    json.dumps("response"),
                    status_code=200
                    )
            except Exception as ex:
                conn.rollback()
                conn.close()
                logging.exception(f"Exception occurred while updating - {ex}")
                return func.HttpResponse(
                "Something Went Wrong!",
                status_code=500
                )
    else:
        return func.HttpResponse(
            "No Parameters Passed",
            status_code=500
        )
    return func.HttpResponse("status of records are updated",status_code=200)

