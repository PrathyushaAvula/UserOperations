import logging
import pyodbc 
import azure.functions as func
import json
import textwrap
from SharedCode import connection

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Getting the information of a user.') 
    req_response = req.get_json() 
    if req_response:
        if 'Id' in req_response.keys():
            Getkey = req_response['Id']
        else:
            return func.HttpResponse("Invalid Parameters to Get a User",status_code=404)
        conn = connection.getconnection()
        if conn:
            crsr = conn.cursor()
            get_sql = f"SELECT * from [dbo].[Users] where Id = {Getkey}"
            try:
                crsr.execute(get_sql)
                response ={}
                for row in crsr.fetchall():
                    response["userName"] = row.UserName
                    response["name"] = row.Name 
                    response["surname"] = row.Surname
                    response["emailAddress"] = row.EmailAddress
                    response["isActive"] = row.IsActive
                    response["id"] = row.Id
                
                crsr.commit()
                conn.close()

                if response:   
                    return func.HttpResponse(
                        json.dumps(response),
                        status_code=200
                    )
                else:
                    return func.HttpResponse(
                        "No Record Found",
                        status_code=404
                    )      
            except Exception as ex:
                conn.rollback()
                conn.close()
                logging.exception(f"Exception occurred while getting the record - {ex}")
                return func.HttpResponse(
                "Something Went Wrong!",
                status_code=500
                )
    else:
        return func.HttpResponse(
            "No Parameters Passed",
            status_code=500
        )