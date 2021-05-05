import django
from twilio.rest import Client
from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from functools import wraps
from twilio.twiml.voice_response import VoiceResponse
from twilio.twiml.messaging_response import MessagingResponse
import re
# from twilio.util import RequestValidator
from twilio.request_validator import RequestValidator
import os
from langdetect import detect
from . import message_template
from .models import WhatsAppUsers, CoordinatingBodies, RankMaster
from datetime import datetime as dt
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from twilio.http.http_client import TwilioHttpClient
from google.cloud import translate_v2 as translate
from message.number_translate import get_pincode

proxy_client = TwilioHttpClient()
#proxy_client.session.proxies = {'https': os.environ['https_proxy']}

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN, http_client=proxy_client)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r''

def validate_twilio_request(f):
    """Validates that incoming requests genuinely originated from Twilio"""
    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        # Create an instance of the RequestValidator class
        validator = RequestValidator(settings.TWILIO_AUTH_TOKEN)
        absolute_url = request.build_absolute_uri()
        absolute_url = absolute_url.replace("http://", "https://")
        # Validate the request using its URL, POST data,
        # and X-TWILIO-SIGNATURE header
        request_valid = validator.validate(
            absolute_url,
            request.POST,
            request.META.get('HTTP_X_TWILIO_SIGNATURE', ''))
        
        # Continue processing the request if it's valid, return a 403 error if
        # it's not
        if request_valid or settings.DEBUG:
            return f(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()
    return decorated_function


def broadcast_sms(request):
    message_to_broadcast = ("Message Text")
    for recipient in settings.SMS_BROADCAST_TO_NUMBERS:
        if recipient:
            client.messages.create(to=recipient,
                                   from_=settings.TWILIO_NUMBER,
                                   body=message_to_broadcast)
    return True #HttpResponse("messages sent!", 200)


def ses_set(request, number, language_code):
    di = {"Question": [],"Answer": [],}
    if language_code in message_template.lang_templates.keys():
        di["Question"].append(message_template.lang_templates[language_code]['question'])
        di["User_Message"] = message_template.lang_templates[language_code]['user_template']
        di['User_Language'] = language_code
    else:
        di["Question"].append(message_template.lang_templates['en']['question'])
        di["User_Message"] = message_template.lang_templates['en']['user_template']
        di['User_Language'] = 'en'

    request.session[number] = di
    return True

def ses_get(request, number):
    if number in request.session:
        return request.session[number]
    else:
        return None
    # return session.get(number, None)


def create_user(request, username, contact_number, address, pincode,  purpose, other_details, rank):
    """Create a user."""

    if contact_number:
        existing_user = WhatsAppUsers.objects.filter(contact_number=contact_number).filter(pincode=pincode)
        if existing_user:
            return False
        new_user = WhatsAppUsers(username=username, contact_number=contact_number, address=address, pincode=pincode, purpose=purpose, other_details=other_details, rank=rank, status=True)
        new_user.save()
        return True
    return False


def getResponse(request, pincode, msg_from, user_details):
    username = user_details[0]
    usr_pincode = user_details[2].strip()
    address = user_details[1]
    purpose = user_details[3]
    other_details = user_details[4]

    resp_message = "Name: "+username+"\n" \
                   "Location: "+address+",​"+str(usr_pincode)+"\n" \
                   "Purpose: "+purpose+"\n" \
                   "Contact Number: "+msg_from+"\n​"+other_details+"\n "
    update_user_obj = CoordinatingBodies.objects.filter(pincode = pincode)
    for record in update_user_obj:
        if str(record.pincode).strip() == pincode.strip():
            msg_to = 'whatsapp:'+str(record.contact_number)
            send_message(request, resp_message, 'whatsapp:+14155238886', msg_to)

def get_rank(request,purpose, other_details):
    raw_data = ' '.join([purpose, other_details])
    # tokens = word_tokenize(raw_data)
    tokens = raw_data.split()
    rank_obj = RankMaster.objects.all()
    rank = None
    if rank_obj:
        for row in rank_obj:
            kewords = row.keywords
            kewords = map(lambda x: x.strip(), kewords.split(','))
            check = any(item in tokens for item in kewords)
            if check:
                rank = row.rank_name
    return rank


@require_POST
@csrf_exempt
@validate_twilio_request
def incoming_message(request):
    try:
        incoming_msg = request.POST['Body']  # request.values.get('Body', '').lower()
        msg_from = request.POST['From']  # request.values.get('From', '')
        msg_to = request.POST['To']  # request.values.get('To', '')
        from_number = msg_from.split('whatsapp:')[1]
        try:
            # language_code = detect(incoming_msg)
            translate_client = translate.Client()
            result = translate_client.translate(
                incoming_msg)
            language_code = result['detectedSourceLanguage']
        except:
            language_code = 'en'

        question = None
        if ses_get(request, from_number) is None:
            ses_set(request, from_number, language_code)
        user_session = ses_get(request, from_number)
        # print(session[from_number])
        if len(user_session["Question"]) > 0:
            if user_session['User_Language'] == language_code:
                user_session = ses_get(request, from_number)
            elif language_code in message_template.lang_templates.keys() and user_session[
                'User_Language'] != language_code:
                ses_set(request, from_number, language_code)
                user_session = ses_get(request, from_number)
            else:
                ses_set(request, from_number, 'en')
                user_session = ses_get(request, from_number)
            question = user_session["Question"].pop(-len(user_session["Question"]))
            request.session.modified = True
            send_message(request, question, msg_to, msg_from)
            print("IN IF", user_session['User_Language'])
        else:
            print("IN ELSE", user_session['User_Language'])
            answers = incoming_msg.split(';')
            try:
                username = answers[0].strip()
                address = answers[1].strip()
                pincode = answers[2].strip()
                purpose = answers[3].strip()
                other_details = answers[4]
                valid_input = True
                if username == '' or address == '' or pincode == '' or purpose == '':
                    valid_input = False
                    invalid_msg = "Details cannot be empty. Please enter all valid information again."
                    invalid_msg = translate_client.translate(
                        invalid_msg, target_language=user_session['User_Language'])
                    print(invalid_msg)
                    send_message(request, invalid_msg['translatedText'], msg_to,
                                 msg_from)
                regex_user = re.findall(r'[!@#$%^&*(),?":{}|<>]', username)
                if len(regex_user)>0:
                    valid_input = False
                    invalid_msg = "Username cannot contain special characters. Please enter all valid information again."
                    invalid_msg = translate_client.translate(
                        invalid_msg, target_language=user_session['User_Language'])
                    print(invalid_msg)
                    send_message(request, invalid_msg['translatedText'], msg_to,
                                 msg_from)
                print("PINCODE1",pincode)
                try:
                     if user_session['User_Language'] != 'en':
                         pincode = get_pincode(pincode, user_session['User_Language'])
                except:
                     print("English pincode")
                print("PINCODE2", pincode)
                if not (pincode.isdigit() and len(pincode) == 6 and pincode[0] != '0'):# and trans_pincode['translatedText'] != '0'):
                    valid_input = False
                    invalid_msg = "Pincode is incorrect. Please enter all valid information again."
                    invalid_msg = translate_client.translate(
                        invalid_msg, target_language=user_session['User_Language'])
                    print(invalid_msg)
                    send_message(request, invalid_msg['translatedText'], msg_to,
                                 msg_from)
                if valid_input:
                    #try:
                    #    if user_session['User_Language'] != 'en':
                    #        pincode = get_pincode(pincode, user_session['User_Language'])
                    #except:
                    #    print("English pincode")
                    getResponse(request, pincode, from_number, answers)
                    rank = get_rank(request, purpose, other_details)
                    resp_message = user_session["User_Message"].format(username, address, answers[2].strip(), purpose,
                                                                       other_details)
                    ses_set(request, from_number, user_session["User_Language"])
                    request.session.modified = True
                    send_message(request, resp_message, msg_to, msg_from)
                    create_user(request, username, from_number, address, pincode, purpose, other_details, rank)
            except:
                ses_set(request, from_number, user_session["User_Language"])
                user_session = ses_get(request, from_number)
                question = user_session["Question"].pop(-len(user_session["Question"]))
                send_message(request, question, msg_to, msg_from)
        # Return the TwiML
    except:
        if from_number in request.session:
            del request.session[from_number]
            request.session.modified = True
    return HttpResponse('Message Sent!', 200)


def send_message(request,response_msg, msg_from, msg_to):

    message = client.messages.create(
                                  body=response_msg,
                                  from_=msg_from,
                                  to=msg_to
                                )
    #'Hi!, Jagadisa Here. This is a testing message from Whatsapp',
    # from_ = 'whatsapp:+14155238886',
    # to = 'whatsapp:+918130141308'
    print(message.sid)

def get_number(pincode,user_lang):
    lang_number={'hi':['.','.','.','.','.','.','.','.','.','.'],
             'gu':['.','.','.','.','.','.','.','.','.','.'],
             'en':['0','1','2','3','4','5','6','7','8','9'],
             'mr':['.','.','.','.','.','.','.','.','.','.'],
             'bn':['.','.','.','.','.','.','.','.','.','.'],
             'te':['.','.','.','.','.','.','.','.','.','.'],
             'ta':['0','.','.','.','.','.','.','.','.','.'],
             'pa':['.','.','.','.','.','.','.','.','.','.'],
             'ml':['.','.','.','.','.','.','.','.','.','.'],
             'or':['.','.','.','.','.','.','.','.','.','.'],
             'kn':['.','.','.','.','.','.','.','.','.','.']
             }
    list_pincode=list(pincode)
    lang_list=lang_number[user_lang]
    res = [(lang_list).index(i) for i in list_pincode]
    english_pincode = str("".join([str(i) for i in res]))
    print(english_pincode)
    return english_pincode


