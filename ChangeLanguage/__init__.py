import logging
import pyodbc 
import azure.functions as func
import json
import textwrap
from datetime import datetime
import pytz
from SharedCode import connection

UTC = pytz.utc
timeZ_Kl = pytz.timezone('Asia/Kolkata')
dt_Kl = datetime.now(timeZ_Kl)

def main(req: func.HttpRequest) -> func.HttpResponse:

    req_response = req.get_json()
    if req_response:
        Language = req_response.get('languageName')
        LastModifierUserId = req_response.get('modifierUserId')        
        LastModificationTime = dt_Kl.strftime('%Y-%m-%d %H:%M:%S')
        conn = connection.getconnection()
        if conn:
            crsr = conn.cursor()

            update_sql = f"UPDATE [dbo].[Settings] SET Value = '{Language}',LastModificationTime='{LastModificationTime}', LastModifierUserId = '{LastModifierUserId}' where Name = 'Abp.Localization.DefaultLanguageName' and UserId = '{LastModifierUserId}'"
            try:
                crsr.execute(update_sql)
                crsr.execute("select @@rowcount")
                rowcount = crsr.fetchall()[0][0]
                if rowcount>0:
                    response = {"result": 'true',
                        "targetUrl": 'null',
                        "success": 'true',
                        "error": 'null',
                        "unAuthorizedRequest": 'false',
                        "__abp": 'true'
                        }
                    crsr.commit()
                    conn.close()
                    return func.HttpResponse(
                    json.dumps(response),
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
