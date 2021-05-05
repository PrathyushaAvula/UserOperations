import logging
import pyodbc
import csv
from datetime import datetime
import azure.functions as func
import pytz
import json
from SharedCode import connection
timez=pytz.timezone('Asia/Kolkata')
dt=datetime.now(timez)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Creating a user.')
    req_response = req.get_json() 
    if req_response:
        id1=req_response.get('id')
        EmailAddress=req_response.get('emailaddress')
        IsActive=req_response.get('isActive')
        Name=req_response.get('Name')
        Password=req_response.get('password')
        Surname=req_response.get('surname')
        UserName=req_response.get('username')
        CreationTime=dt.strftime('%Y-%m-%d %H:%M:%S')
        LastModificationTime=dt.strftime('%Y-%m-%d %H:%M:%S')
        conn = connection.getconnection()
        if conn:
            crsr=conn.cursor()
            query="INSERT INTO [dbo].[Users] (AccessFailedCount,AuthenticationSource,CreationTime,CreatorUserId,DeleterUserId,DeletionTime,EmailAddress,EmailConfirmationCode,IsActive,IsDeleted,IsEmailConfirmed,IsLockoutEnabled,IsPhoneNumberConfirmed,IsTwoFactorEnabled,LastModificationTime,LastModifierUserId,LockoutEndDateUtc,Name,Password,PasswordResetCode,PhoneNumber,Surname,UserName) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
            records=[(0,None,CreationTime,None,None,None,EmailAddress,None,IsActive,0,0,1,0,0,LastModificationTime,None,None,Name,Password,None,None,Surname,UserName)]
            try:
                crsr.executemany(query,records)
                response={'id':id1,"emailaddress":EmailAddress,'username':UserName}
                crsr.commit()
                conn.close()
                return func.HttpResponse(json.dumps(response),status_code=200)
            except Exception as ex:
                conn.rollback()
                conn.close()
                logging.exception(f"Exception occurred while creating a user - {ex}")
                return func.HttpResponse(
                "Something Went Wrong!",
                status_code=500
                )
    else:
        return func.HttpResponse(
            "No Parameters Passed",
            status_code=500
        )