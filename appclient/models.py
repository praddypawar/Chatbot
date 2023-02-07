from django.db import models
from  appbase import validator_messages
from appbase.models import Base
# Create your models here.
class ClientRegistration(Base):
    choices = (
    ("Student","Student"),
    ("Developer","Developer"),
    ("Businessman","Businessman")
    )
    fname = models.CharField(max_length=200)
    lname = models.CharField(max_length=200)
    email = models.EmailField(validators=[validator_messages.email_validator])
    mobile = models.CharField(max_length=11,validators=[validator_messages.phone_validator])
    designation = models.CharField(max_length=200,choices=choices)
    password = models.CharField(max_length=250)

    def __str__(self) -> str:
        return f"{self.fname} {self.lname}"
    
        
class ChatbotRegister(Base):
    client_id = models.ForeignKey(ClientRegistration,on_delete=models.CASCADE)
    chatbot_name = models.CharField(max_length=100)
    category = models.CharField(max_length=200)
    logo=models.ImageField(upload_to="chatbot-img/")
    url_link= models.CharField(max_length=200,null=True,blank=True)

    def __str__(self) -> str:
        return f"{self.chatbot_name} - {self.url_link}"