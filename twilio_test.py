from twilio.rest import Client

def send_sms(body, to_number):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages.create(
        body=body,
        from_='+17406756329',
        to=to_number
    )
    print(f"[+] Sent to {to_number}: {message.sid}")
