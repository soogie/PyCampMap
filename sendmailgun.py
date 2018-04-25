import requests
import mykeys

def sendMessage(subject, message):
    base_url = mykeys.API_BASE
    api_key = mykeys.API_KEY
    from_address = mykeys.FROM_ADDRESS
    to_address = mykeys.TO_ADDRESS
    auth = ('api', api_key)
    data = {
        'from': from_address,
        'to': to_address,
        'subject': subject,
        'text': message
    }
    return requests.post(
        base_url + '/messages',
        auth = auth,
        data = data
    )


if __name__ == '__main__':
    sendMessage('TEST', 'This is a test message. -- sendmailgun.py --')