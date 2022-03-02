from twilio.rest import Client
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from message.translator import translate
from message.crypto import get_price
from decouple import config


account_sid = config('TWILIO_SID')
account_auth_token = config('TWILIO_AUTH_TOKEN')
client = Client(account_sid, account_auth_token)

translate_keyword = 'gotrans'
crypto_keyword = 'coinfo'


def send_message(reply, sender_number):
    client.messages.create(to=sender_number,
                           from_='whatsapp:your twilio whatsapp number',
                           body=reply)


@csrf_exempt
def message(request):
    sender_name = request.POST["ProfileName"]
    sender_number = request.POST["From"]
    msg = request.POST["Body"]

    if translate_keyword in msg.lower():
        user_reply = msg[len(translate_keyword):].lstrip(' ')
        translated_text = translate(user_reply)
        send_message(translated_text, sender_number)

    elif crypto_keyword in msg.lower():
        user_reply = msg[len(crypto_keyword):].lstrip(' ')
        crypto_info = get_price(user_reply)
        send_message(crypto_info, sender_number)

    else:
        if msg.lower() == 'hi':
            intro_msg = f"Hello there {sender_name}! 😊\n" \
                f"Don't forget to activate the bot first by sending '<your sandbox keyword>' " \
                f"keyword in case you haven't done it yet."
            send_message(intro_msg, sender_number)

        cmd_msg = "Below are the available commands:\n\n" \
                  "gotrans <message to be translated>\n" \
                  "(Example : gotrans Ako ay Pilipino!)\n\n" \
                  "coinfo <cryptocurrency name or symbol>\n" \
                  "(Example : coinfo bitcoin or coinfo btc)\n"
        send_message(cmd_msg, sender_number)

    return HttpResponse(request)
