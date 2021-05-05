from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date
from django.urls import  reverse

status_choices = [     
        ('Active','Active'),
        ('Deceased','Deceased'),
        ('Article 11.3','Article 11.3'),
        ('Terminated','Terminated'),
    ]
provinces = [
        ('Eastern Cape','EC'),
        ('Free State','FS'),
        ('Gauteng','GP'),
        ('KwaZulu Natal','KZN'),
        ('Limpopo','LP'),
        ('Mpumalanga','MP'),
        ('Northern Cape','NC'),
        ('North West','NW'),
        ('Western Cape','WC')
]

beneficiary_type = [
    ("Spouse","Spouse"),
    ("Child","Child"),
    ("Father","Father"),
    ("Mother","Mother"),
    ("Father-in-Law","Father-in-Law"),
    ("Mother-in-Law","Mother-in-Law"),
    ("Parent Proxy","Parent Proxy"),
]    

beneficiary_status = [
    ('Active','Active'),
    ('Article 20.3','Article 20.3'),
    ('Deceased', 'Deceased'),
    ('Inactive', 'Inactive'),
]

committees =[
    ('Exeutive Committee', 'EXCO'),
    ('Finance Committee','FINCOM'),
    ('Constitutional Committee','CONCOM'),
    ('Disciplinary Committee','DC'),
    ('Events Committee','EC'),
    ('Compassion Committee','COMPCOM')
]

portfolios = [
    ('Chairperson','Chairperson'),
    ('Deputy Chairperson','Deputy Chairperson'),
    ('Secetary-General','Secretary-General'),
    ('Deputy Secretary General', 'Deputy Secretary-General'),
    ('Treasurer', 'Treasurer'),
    ('Events Coordinator', 'Events Cordinator'),
    ('Member of EXCO', 'MEC'),
    ('Convenor','Convenor'),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    middlename = models.CharField(max_length=100, blank = 'True',null='True')
    birth_date = models.DateField(auto_now=False, auto_now_add=False)
    mobile_phone = models.CharField(max_length=20)
    status = models.CharField(choices = status_choices, max_length=20, default='Active')
    status_date = models.DateField(auto_now=False, auto_now_add=False, blank='True',null='True')
    address = models.TextField(max_length=200)
    town_city = models.CharField(max_length=200)
    district_metro = models.CharField(max_length=250)
    province = models.CharField(choices = provinces, max_length=100)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d')
    alt_address = models.TextField(blank='True',null='True')
    alt_phone = models.CharField(max_length=50, blank='True', null='True')
    
    def age(self):
            birth_year = self.date_of_birth.year
            this_year = datetime.now().year
            member_age = this_year - birth_year
            return member_age
    
    
    def __str__(self):
        return f'{self.user.last_name} + {self.user.first_name[:1]} + {self.user.profile.middlename[:1]}'
    def get_absolute_url(self):
        return reverse("member_profile", kwargs={"pk": self.pk})
    
    
class Beneficiary(models.Model):
    member = models.ForeignKey(Profile,on_delete=models.CASCADE, related_name='beneficiaries')
    name = models.CharField(max_length=256)
    beneficiary_type = models.CharField(max_length=100,  choices=beneficiary_type, default="Spouse")
    birth_date = models.DateField()
    beneficiary_status = models.CharField(max_length=100,choices=beneficiary_status, default="Active")
    is_paid = models.BooleanField(default=False)
    paid_date = models.DateField(blank=True, null=True)
    
    def age(self):
            birth_year = self.birth_date.year
            this_year = datetime.now().year
            ben_age = this_year-birth_year
            return ben_age

    def __str__(self):
        return (self.name)
    
class Committee(models.Model):
    member = models.ManyToManyField(User)
    committee_name = models.CharField(max_length=200, choices=committees)
    portfolio = models.CharField(max_length=200, choices=portfolios)
    start_date =models.DateField(blank='False',null='false')
    end_date = models.DateField()
    
    def __str__(self):
        return f'{self.user.surname} + {self.user.last_name[:1]} + {self.user.profile[:1]} Portfolio: {self.committee_name}'
    
    


