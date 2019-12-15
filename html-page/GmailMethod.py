import base64
import email
from apiclient import errors


#######################################################################
def ListMessagesMatchingQuery(service, user_id, query=''):
  try:
    response = service.users().messages().list(userId=user_id,
                                               q=query).execute()
    messages = []
    if 'messages' in response:
      messages.extend(response['messages'])

    while 'nextPageToken' in response:
      page_token = response['nextPageToken']
      response = service.users().messages().list(userId=user_id, q=query,
                                         pageToken=page_token).execute()
      messages.extend(response['messages'])

    return messages
  except errors.HttpError:
    print( 'An error occurred: %s')

##############################################################################
def GetMessage(service, user_id, msg_id):
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id).execute()

    #print( 'Message snippet: %s' % message['snippet'])

    return message
  except errors.HttpError:
    print ('An error occurred: %s')

##############################################################################

def GetAttachments(service, user_id, msg_id, store_dir):
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id).execute()
    print(message['payload']['mimeType'])
    for part in message['payload']['parts']:
      if part['filename']:
        print("attachmnet is heres")
        attachment = service.users().messages().attachments().get(userId='me', messageId=message['id'], id=part['body']['attachmentId']).execute()
        file_data = base64.urlsafe_b64decode(attachment['data'].encode('UTF-8'))

        path = ''.join([store_dir, part['filename']])

        f = open(path,'wb')
        f.write(file_data)
        f.close()

  except errors.HttpError:
    print ('An error occurred in messaage attactment' )