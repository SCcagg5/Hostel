import requests
import json
import jwt
import uuid
import os
from tinydb import TinyDB, Query

db = TinyDB('/db.json')
SSO_FRONT = os.environ.get("SSO_FRONT", "https://sso.newtechstack.fr")
SSO_BACK = os.environ.get("SSO_BACK", "https://api.sso.newtechstack.fr")
SSO_TOKEN = os.environ.get("SSO_TOKEN", None)
SSO_REGISTRY = os.environ.get("SSO_REGISTRY", None)

class Sso:
    def __init__(self):
        self.apitoken = ""
        self.user = None

    def is_ok(self):
        if SSO_TOKEN is None:
            return [False, "Missing SSO_TOKEN", 500]
        if SSO_REGISTRY is None:
            return [False, "Missing SSO_REGISTRY", 500]
        return [True, {}, None]

    def get_url(self):
        isok = self.is_ok()
        if not isok[0]:
            return isok
        response = requests.request(
            "POST",
            f"{SSO_BACK}/extern/key",
            headers = {
              'Content-Type': 'application/json'
            },
            data = json.dumps(
                {
                  "apitoken": SSO_TOKEN,
                  "valid_until": 600,
                }
            )
        )
        data = json.loads(response.text)
        if not 'data' in data or data['data'] is None:
            return [False, "Error connecting to sso api", 500]
        data = data['data']
        key = data["key"]
        auth = data["auth"]
        id = str(uuid.uuid4())
        data['id'] = id
        db.insert(data)
        url = f"{SSO_FRONT}/sso/extern/{key}/{auth}/accept"
        return [True, {"url": url, "id": id}, None]

    def get_token(self, id):
        isok = self.is_ok()
        if not isok[0]:
            return isok
        r = Query()
        res = db.search(r.id == id)
        db.remove(r.id == id)
        if len(res) != 1:
            return [False, "Invalid id", 404]
        key = res[0]['key']
        secret = res[0]['secret']
        response = requests.request(
            "POST",
            f"{SSO_BACK}/extern/key/{key}/token",
            headers = {
              'Content-Type': 'application/json'
            },
            data = json.dumps(
                {
                  "apitoken": SSO_TOKEN,
                  "secret": secret
                }
            )
        )
        data = json.loads(response.text)
        token = data['data']['usrtoken']
        return self.__decode(token)

    def verify(self, token):
        isok = self.is_ok()
        if not isok[0]:
            return isok
        res = self.__decode(token, get_data = True)
        if not res[0]:
            return res
        self.user = res[1]["data"]["payload"]
        return [True, {}, None]

    def user_by_email(self, email):
        isok = self.is_ok()
        if not isok[0]:
            return isok
        """invite + get user_id"""
        response = requests.request(
            "POST",
            f"{SSO_BACK}/extern/user/invite",
            headers = {
              'Content-Type': 'application/json'
            },
            data = json.dumps(
                {
                  "email": email,
                  "apitoken": SSO_TOKEN,
                }
            )
        )
        data = json.loads(response.text)
        try:
            usr_id = data['data']['usrid']
        except:
            return [False, "Internal Error", 500]
        return [True, {'id': usr_id}, None]

    def __decode(self, token, get_data = False):
        url = f"{SSO_BACK}/extern/public"
        payload = json.dumps({
          "apitoken": SSO_TOKEN,
        })
        headers = {
          'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        public_key = json.loads(response.text)['data']['public_key']
        try:
            data = jwt.decode(
                token,
                public_key,
                leeway=0,
                issuer="auth:back",
                audience=f"auth:{SSO_REGISTRY}",
                algorithms=['RS256']
            )
        except jwt.ExpiredSignatureError:
            return [False, "Signature expired", 403]
        except jwt.InvalidSignatureError:
            return  [False, "Invalid signature", 400]
        except jwt.InvalidIssuedAtError:
            return [False, "Invalid time", 400]
        except jwt.InvalidIssuerError:
            return [False, "Invalid issuer", 403]
        except jwt.InvalidAudienceError:
            return [False, "Invalid audience", 401]
        except jwt.ImmatureSignatureError:
            return [False, "Invalid time", 400]
        except jwt.DecodeError:
            return [False, "Invalid jwt", 400]
        if get_data == True:
            return [True, {"data": data}, None]
        return [True, {"usrtoken": token}, None, {"usrtoken": token}]
