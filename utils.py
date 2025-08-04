from kavenegar import *
from sms_ir import SmsIr
from django.contrib.auth.mixins import UserPassesTestMixin

def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI('6D594336547453695931705838726556703369506F6F3269542F363735382B79677650424F355A6C3352773D')
        #'09201140293': 416964687674356D3756323165612F5170337152684C5636625A6F75452F4C6167364B4336437A4B6F67773D
        #'09982440293': 6D594336547453695931705838726556703369506F6F3269542F363735382B79677650424F355A6C3352773D
        #'09355480293': 55514C3077426359392B2B6266452B5A316749575059544C2B504C2F304E4C394276493231555736466A6B3D
        params = { 'sender' : '2000660110', 'receptor': phone_number, 'message' :f'کد تایید شما: {code}' }
        response = api.sms_send(params)

        print(response)
    except APIException as e: 
        print(e)
        # e.decode('utf-8')
    except HTTPException as e: 
        print(e)
    """
    try:
        sms_ir = SmsIr('0qUo2QMrpL6ceDATjkO1yXXxxXXxxXXxxFpXg9XBHDKfh6ou5cS6nrCBInUxWGf')
        response = sms_ir.send_verify_code(
            number=phone_number, # 9355480293 (no zero at beginning)
            template_id=232000,
            parameters=[{"name" : "CODE","value": str(code),}],)
        print(response)
    except APIException as e: 
        print(e)
        # e.decode('utf-8')
    except HTTPException as e: 
        print(e)
    try:    
        sms_ir = SmsIr('cynx5aPbmKCpfnhctZJ1mIVUIJBC3hAXoiyf7j9I31wY1HCJ')
        # PN1TVeBeaAehFLJAKU4XdfpsFXsQguYfleO0bV4ceh6diTZid2hRXza3uSkBbDef
        # 0qUo2QMrpL6ceDATjkO1yXXxxXXxxXXxxFpXg9XBHDKfh6ou5cS6nrCBInUxWGf
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

class IsAdminUserMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin