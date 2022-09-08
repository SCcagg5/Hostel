import jwt
import datetime

class Payment():
    def get(data):
        now = datetime.datetime.utcnow()
        exp = now + datetime.timedelta(hours=4)
        return [True, jwt.encode({
            'iat': now,
            'nbf': now,
            'exp': exp,
            'iss': 'hotel:payment',
            'aud': 'hotel:*',
            'payload': data,
            }, "secret", algorithm="HS256"), None]

    def pay(data):
        print(data)
        try:
            payload = jwt.decode(
                data,
                "secret",
                leeway=0,
                audience='hotel:*',
                issuer='hotel:payment',
                algorithms=["HS256"]
            )
            amount = str(payload["payload"]["total"])
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
        except:
            return [False, "", 400]
        return [True, f"<HTML><body>payment page { amount }</body></HTML>", None]
