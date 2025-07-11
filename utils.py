from kavenegar import *


def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI('416964687674356D3756323165612F5170337152684C5636625A6F75452F4C6167364B4336437A4B6F67773D')
        #'09355480293': 55514C3077426359392B2B6266452B5A316749575059544C2B504C2F304E4C394276493231555736466A6B3D
        params = { 'sender' : '2000660110', 'receptor': phone_number, 'message' :f'youe verification code is: {code}' }
        response = api.sms_send(params)

        print(response)
    except APIException as e: 
        print(e.decode('utf-8'))
    except HTTPException as e: 
        print(e.decode('utf-8'))