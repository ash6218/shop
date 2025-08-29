from kavenegar import *
from django.contrib.auth.mixins import UserPassesTestMixin
from django.conf import settings

def send_otp_code(phone_number, code, request):
    try:
        if request.session['sms_p']['0']:
            print(request.session['sms_p'])
            rs = request.session['sms_p']['0']
        else:
            rs = '6D594336547453695931705838726556703369506F6F3269542F363735382B79677650424F355A6C3352773D'
        api = KavenegarAPI(rs)
        params = { 'sender' : '2000660110', 'receptor': phone_number, 'message' :f'کد تایید شما: {code}' }
        response = api.sms_send(params)

        print(response)
    except APIException as e: 
        print(e)
        # e.decode('utf-8')
    except HTTPException as e: 
        print(e)


class IsAdminUserMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin
    
def generate_token(form):
    url2 = 'http://127.0.0.1:8000/accounts/api-token-auth/'
    response2 = requests.post(url2, json=form.cleaned_data).json()
    token = f'token {response2['token']}'
    return token
    #print(token)

def get_api_headers(request):
    return {'Authorization':request.session['token']}

def get_api_user(request):
    url3 = 'http://127.0.0.1:8000/accounts/user'
    headers3 = get_api_headers(request)
    json_response = requests.get(url3, headers=headers3).json()
    api_user1 = next((i for i in json_response if i['username']==request.session['api_username']), None)
    request.session['api_id']=api_user1['id']
    return request.session['api_id']





    """
    from sms_ir import SmsIr
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