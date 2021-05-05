import logging
import azure.functions as func
import json
from datetime import datetime
import pytz
from SharedCode import connection

UTC = pytz.utc
timeZ_Kl = pytz.timezone('Asia/Kolkata')
dt_Kl = datetime.now(timeZ_Kl)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Resetting the password.') 
    req_response = req.get_json() 
    if req_response:
        AdminPassword = req_response.get('adminPassword')
        NewPassword = req_response.get('newPassword')
        UserId = req_response.get('userId')
        LastModificationTime = dt_Kl.strftime('%Y-%m-%d %H:%M:%S')
        LastModifierUserId = req_response.get('modifierUserId')
        conn = connection.getconnection()
        if conn:
            crsr = conn.cursor()
            update_sql = f"UPDATE [dbo].[Users] SET Password = '{NewPassword}',LastModificationTime='{LastModificationTime}', LastModifierUserId = '{LastModifierUserId}' where Id = '{UserId}'"
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
                logging.exception(f"Exception occurred while resetting the password - {ex}")
                return func.HttpResponse(
                "Something Went Wrong!",
                status_code=500
                )
    else:
        return func.HttpResponse(
            "No Parameters Passed",
            status_code=500
        )