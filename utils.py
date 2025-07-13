from kavenegar import *
from sms_ir import SmsIr

def send_otp_code(phone_number, code):
    
    try:
        api = KavenegarAPI('416964687674356D3756323165612F5170337152684C5636625A6F75452F4C6167364B4336437A4B6F67773D')
        #'09355480293': 55514C3077426359392B2B6266452B5A316749575059544C2B504C2F304E4C394276493231555736466A6B3D
        params = { 'sender' : '2000660110', 'receptor': phone_number, 'message' :f'your verification code is: {code}' }
        response = api.sms_send(params)

        print(response)
    except APIException as e: 
        print(e)
        # e.decode('utf-8')
    except HTTPException as e: 
        print(e)
    """
    try:    
        sms_ir = SmsIr('cynx5aPbmKCpfnhctZJ1mIVUIJBC3hAXoiyf7j9I31wY1HCJ')
        # PN1TVeBeaAehFLJAKU4XdfpsFXsQguYfleO0bV4ceh6diTZid2hRXza3uSkBbDef
        result = sms_ir.send_verify_code(
            number=phone_number,
            template_id=232000,
            parameters=[{"name" : "CODE", "value": str(code),}],
        )
        print(result)
    except APIException as e: 
        print(e)
        # e.decode('utf-8')
    except HTTPException as e: 
        print(e)
    """