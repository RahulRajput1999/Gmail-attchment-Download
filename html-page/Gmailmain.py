from __future__ import print_function
import pickle
import os.path
import GmailMethod
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime


SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def main(query,date):
    
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
       
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    
    
    subjectname = []
    subjectname.append(query)
    message = GmailMethod.ListMessagesMatchingQuery(service,'me','')


    todaydate =datetime.date.today().strftime('%Y-%m-%d')
    querydate = date
    counter = 0
    open('Email.txt','w').close()
    for m in message:

        f = open('Email.txt','a+')

        print('********************',counter,'****************************')
        counter =counter+1
        messageid = m['id']
        messagejson =  GmailMethod.GetMessage(service,'me',messageid)
        dateinternal = int(messagejson['internalDate']) / 1000.0
        messagedate = datetime.datetime.fromtimestamp(dateinternal).strftime('%Y-%m-%d')
        if querydate <= messagedate <= todaydate :
            headers = messagejson['payload']['headers']
            subject= [i['value'] for i in headers if i["name"]=="Subject"]
            if subjectname == subject:           
                data = dict()
                for h in headers:
                    data[h['name']]=h['value']
                From = "From :" +data['From'] + '\n'
                f.write(From)
                GmailMethod.GetAttachments(service,'me',messageid,'attach/')
        else:
            break
    f.close()       



        
"""if __name__ == '__main__':
    main()"""