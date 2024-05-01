from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import requests

from dictionary.dictapi import *

from dotenv import load_dotenv
import os


def send_message(user_number, message):
    account_sid = os.environ.get("ACCOUNT_SID")
    auth_token = os.environ.get("AUTH_TOKEN")
    twilio_number = "whatsapp:+14155238886"
    client = Client(account_sid,auth_token)

    client.messages.create(
        from_ = twilio_number,
        body = message,
        to = user_number 
    )
    


@csrf_exempt
def home(request):

    if request.method == "POST":
        user_number = request.POST.get("From")
        user_message = request.POST.get("Body")

        message = get_definition(user_message)
        word_meaning = message["definition"]
        if len(word_meaning) >= 1600:
            substring = ""
            index = 0

            while index < len(word_meaning) and len(substring) < 1600:
                substring += word_meaning[index]
                if word_meaning[index] == '.':
                    last_full_stop_index = index
                index += 1
            send_message(user_number, substring[:last_full_stop_index + 1])
        elif len(word_meaning) == 0:
            send_message(user_number, "Word not found in the dictionary.")
        else:
            send_message(user_number,word_meaning)

    return render(request, "home.html")