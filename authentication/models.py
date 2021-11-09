
from math import exp
from django.db import models
import random
from django.utils.timezone import timedelta
from utils.operations.Errors import *
from utils.authentication.Errors import *
from django.utils.timezone import now
from utils.authentication.user_authentication import User_Authentication
import time

# Create your models here.


class User(models.Model):

    email = models.CharField(default="", max_length=50, blank=True)
    password = models.CharField(
        default="", editable=False, blank=False, null=False, max_length=250)
    code = models.CharField(default="", max_length=6, blank=False, null=False)
    create_on = models.DateTimeField(
        default=now, blank=False, editable=False)
    expires_on = models.IntegerField(
        default=0
    )

    def create_code(self, user_cred):

        def generate_code():
            while True:
                num = str(random.randint(100000, 999999))
                try:
                    exists = User.objects.get(code=num)
                except:
                    break

            return num

        auth = User_Authentication()

        code: str

        # if auth._check_existing_user_with_email(email=user_cred["email"]):
        #     raise UserAlreadyExistError(user_cred["email"])

        # Checks weather the code was previously generated for the user

        try:
            existing_user_request: User = User.objects.get(
                email=user_cred["email"])

            code = generate_code()
            existing_user_request.code = code
            existing_user_request.password = user_cred["password"]
            existing_user_request.expires_on = self.generate_time(expiry=True)

            existing_user_request.save()

        except User.MultipleObjectsReturned as e:
            code = "<Error>"
            existing_user_request = User.objects.filter(
                email=user_cred["email"])
            existing_user_request.delete()
            # Raise an Error here

        except User.DoesNotExist as e:
            print("Exception")
            print(e)
            code = generate_code()
            self.email = user_cred["email"]
            self.password = user_cred["password"]
            self.code = code
            self.expires_on = self.generate_time(expiry=True)

            self.save()

        # TODO: Encrypt the password

        print(code)

        return code

    def auth(self, code):
        try:
            data: User = User.objects.get(code=code)

        except:
            data = None

        if data is None:
            raise NotAllowed("Code Does Not Exist in the Database")
        newData = data.to_dict()

        if (current_time := self.generate_time()) > newData["expires_on"]:
            raise Restricted(
                f"Code has Expired\n{newData['expires_on']}\t{current_time=}\n{current_time > newData['expires_on']}")

        auth = User_Authentication()
        token = auth.signup(user_data=newData)

        data.delete()
        # self.save()
        return token

    def to_dict(self):
        return {"expires_on": self.expires_on, "email": self.email, "password": self.password, "create_on": self.create_on}

    def generate_time(self, expiry=False):
        current_time_milli = time.mktime(now().timetuple())
        expiry_time_milli = current_time_milli + 300
        return int(expiry_time_milli if expiry else current_time_milli)

# user.models.User.DoesNotExist
