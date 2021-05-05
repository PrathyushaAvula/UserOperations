import logging
import azure.functions as func
import json
from SharedCode import connection


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Getting all the users.')    
    conn = connection.getconnection()
    if conn:
        crsr = conn.cursor()
        get_sql = f"SELECT * from [dbo].[Users]"
        try:
            crsr.execute(get_sql)
            items = []
            for row in crsr.fetchall():
                datarow = {}
                datarow["userName"] = row.UserName
                datarow["name"] = row.Name 
                datarow["surname"] = row.Surname
                datarow["emailAddress"] = row.EmailAddress
                datarow["isActive"] = row.IsActive
                datarow["id"] = row.Id
                items.append(datarow)

            crsr.commit()
            conn.close()
            if items:   
                return func.HttpResponse(
                    json.dumps(items),
                    status_code=200
                )
            else:
                return func.HttpResponse(
                    "No Record Found",
                    status_code=200
                ) 
        except Exception: 
            conn.close()  
            logging.exception(f"Exception occurred while updating - {ex}")            
            return func.HttpResponse(
                "Something Went Wrong!",
                status_code=500
            )
