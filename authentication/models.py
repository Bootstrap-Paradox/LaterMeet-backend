
from django.db import models
import random
from datetime import datetime, timedelta
from utils.operations.Errors import *
from utils.authentication.Errors import *
from django.utils.timezone import now
from utils.authentication.user_authentication import User_Authentication

# Create your models here.


class User(models.Model):

    email = models.CharField(default="", max_length=50, blank=True)
    password = models.CharField(
        default="", editable=False, blank=False, null=False, max_length=250)
    code = models.CharField(default="", max_length=6, blank=False, null=False)
    create_on = models.DateTimeField(
        default=datetime.utcnow, blank=False, editable=False)
    expires_on = models.DateTimeField(
        default=datetime.utcnow() + timedelta(minutes=5)
    )

    def create_code(self, user_cred):

        auth = User_Authentication()
        if auth._check_existing_user_with_email(email=user_cred["email"]):
            raise UserAlreadyExistError(user_cred["email"])

        while True:
            num = str(random.randint(100000, 999999))
            try:
                exists = User.objects.get(code=num)
            except:
                break

        # TODO: Encrypt the password
        self.email = user_cred["email"]
        self.password = user_cred["password"]
        self.code = num

        self.save()

        return num

    def auth(self, code):
        try:
            data: User = User.objects.get(code=code)

        except:
            return None

        if data is None:
            raise NotAllowed("Code Does Not Exist in the Database")
        newData = data.to_dict()

        if now() > newData["expires_on"]:
            raise Restricted("Code has Expired")

        auth = User_Authentication()
        token = auth.signup(user_data=newData)

        data.delete()
        # self.save()
        return token

    def to_dict(self):
        return {"expires_on": self.expires_on, "email": self.email, "password": self.password}


# user.models.User.DoesNotExist
