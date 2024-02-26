import os
import pathlib
import re
import traceback
import logging
from datetime import datetime, timedelta
import smtplib as s, ssl
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import pyodbc
import smtplib as s1, ssl
from pretty_html_table import build_table
from pprint import pprint
try:
 connection = pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=NS104787;"
    "DATABASE=vroom_fdb08a2db31047b9b0d6a2d9824abcd2;" #carvana_b7850b5fa4924e1186551da818f84f7f
    "UID=mscience;"
    "PWD=hT$Aey4l%NUs%^e;"
 )

 cursor = connection.cursor()
 cursor.execute("""select * from (
select make_slug as Make, make_count as Site_count ,count(distinct([dbo].[SWSIR ProductList1].Vin)) as File_count from [dbo].[SWSIR modelList] inner join [dbo].[SWSIR ProductList] on
[dbo].[SWSIR modelList].make_slug=[dbo].[SWSIR ProductList].Make inner join [dbo].[SWSIR ProductList1] on
[dbo].[SWSIR ProductList].Make=[dbo].[SWSIR ProductList1].Make inner join [dbo].[SWSIR ProductList2] on
[dbo].[SWSIR ProductList1].Make=[dbo].[SWSIR ProductList2].Make
group by [dbo].[SWSIR modelList].make_slug,[dbo].[SWSIR modelList].make_count) as table12   where  Site_count <> File_count""")

 rows = cursor.fetchall()

 df = pd.DataFrame(columns=['make','Site_count','File_count'])
 #print(rows)


 for row in rows:
    #print(row)
    df = df.append({'make': row[0],'Site_count': row[1],'File_count': row[2]},ignore_index=True) 





 headerdata = "<h3>1. Below are the  missmatch make count : \n\n</h3>"
 outputdata = build_table(df, 'blue_light')

 final_content1 =  headerdata+'\n'+outputdata
except:
 print("connection is failed")
def sent_mail(final_content ):
 ob = s1.SMTP("mail.authsmtp.com",2525)
 ob.starttls()
 ob.login('ac68993','DF2eFe6ds3wF')
################Message Content

 message = MIMEMultipart("alternative")
 message["Subject"] = "Mscience vroom cars agent data count mismatch : "
 #message["From"] = 'hemant.kumar@sequentum.com'
 message["From"] = 'sunil.yadav@sequentum.com'
 message["To"] = 'sunil.yadav@sequentum.com' # receiver_email
 mail_content = MIMEText(final_content, "HTML")
 message.attach(mail_content)

 #ob.sendmail('sunil.yadav@sequentum.com', ['hemant.kumar@sequentum.com', 'sunil.yadav@sequentum.com', 'bhawana.srivastava@sequentum.com ', 'tanuj.sharma@sequentum.com'], message.as_string())#,'sangeeta.mishra@sequentum.com', 'sachin.jain@sequentum.com', 'bhawana.srivastava@sequentum.com'], message.as_string())

 #ob.sendmail('hemant.kumar@sequentum.com',['hemant.kumar@sequentum.com','sunil.yadav@sequentum.com','tanuj.sharma@sequentum.com'],message.as_string())

 ob.sendmail('sunil.yadav@sequentum.com', ['hemant.kumar@sequentum.com','sunil.yadav@sequentum.com','tanuj.sharma@sequentum.com','bhawana.srivastava@sequentum.com','gaurav.bisht@sequentum.com ','karmveer.yadav@sequentum.com '], message.as_string())
 print("Mail sent")
 ob.quit()
sent_mail(final_content1)
