from django.db import models
from django.db.models import Count, Q
from django.contrib.auth.models import User
from datetime import datetime, date
from django.urls import  reverse
from sorl.thumbnail import ImageField



status_choices = [     
        ('Active','Active'),
        ('Deceased','Deceased'),
        ('Suspended','Suspended'),
        ('Terminated','Terminated'),
    ]
provinces = [
        ('Eastern Cape','Eastern Cape'),
        ('Free State','Free State'),
        ('Gauteng','Gauteng'),
        ('KwaZulu Natal','KwaZulu Natal'),
        ('Limpopo','Limpopo'),
        ('Mpumalanga','Mpumalanga'),
        ('Northern Cape','Northern Cape'),
        ('North West','North West'),
        ('Western Cape','Western Cape')
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
    ('Executive Committee', 'Executive Committee'),
    ('Finance Committee','Finance Committee'),
    ('Constitutional Committee','Constitutional Committee'),
    ('Disciplinary Committee','Disciplinary Committee'),
    ('Events Committee','Events Committee'),
    ('Compassion Committee','Compassion Committee')
]

portfolios = [
    ('Chairperson','Chairperson'),
    ('Deputy Chairperson','Deputy Chairperson'),
    ('Secetary-General','Secretary-General'),
    ('Deputy Secretary-General', 'Deputy Secretary-General'),
    ('Treasurer-General', 'Treasurer-General'),
    ('Events Coordinator', 'Events Cordinator'),
    ('Member of EXCO', 'Member of Exco'),
    ('Convenor','Convenor'),
    ('Member','Member'),
    ('Ex Officio Member','Ex Officio Member'),
]

proxy=[
    ('Father','Father'),
    ('Mother','Mother'),
    ('Father-in_Law','Father-in-Law'),
    ('Mother-in-Law','Mother-in-Law')
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shortname= models.CharField(max_length=150)
    middlename = models.CharField(max_length=100, blank = True,null=True)
    birth_date = models.DateField(auto_now=False, null=True, blank=False)
    mobile_phone = models.CharField(max_length=20)
    status = models.CharField(choices = status_choices, max_length=20, default='Active')
    status_date = models.DateField(auto_now=False, blank=True,null=True)
    address = models.TextField(max_length=200)
    town_city = models.CharField(max_length=200)
    district_metro = models.CharField(max_length=250)
    province = models.CharField(choices = provinces, max_length=100)
    photo = models.ImageField(default='default2.png', upload_to='member_photos/%Y')
    alt_address = models.TextField(blank=True,null=True)
    alt_phone = models.CharField(max_length=50, blank=True, null=True)
    
    def get_absolute_url(self):
        return reverse('pmlprofile:profile_detail' ,kwargs={'pk': self.pk})
    
    def __str__(self):
        return self.shortname
    
    
class Beneficiary(models.Model):
    member = models.ForeignKey(Profile,on_delete=models.CASCADE, related_name='beneficiaries')
    name = models.CharField(max_length=256)
    beneficiary_type = models.CharField(max_length=100,  choices=beneficiary_type, default="Spouse")
    proxy = models.CharField(max_length=100,choices=proxy, null=True,blank=True)
    birth_date = models.DateField()
    beneficiary_status = models.CharField(max_length=100,choices=beneficiary_status, default="Active")
    is_paid = models.BooleanField(default=False)
    paid_date = models.DateField(blank=True, null=True)
    
    class Meta:
        ordering = ('member__id','id')
    
    def age(self):
            birth_year = self.birth_date.year
            this_year = datetime.now().year
            ben_age = this_year-birth_year
            return ben_age
    
    def active_count(self):
        actives= Beneficiary.objects.annotate(active_count=Count("active", filter=Q(beneficiary_status='Active')))

    def __str__(self):
        return self.name
    
class Committee(models.Model):
    name = models.CharField(max_length=200,choices=committees)
    SHORTNAMES = [
        ('EXCO','EXCO'),
        ('FINCOM','FINCOM'),
        ('CONCOM','CONCOM'),
        ('DC','DC'),
        ('COMPCOM','COMPCOM'),
        ('ECOM','ECOM'),
        ]
    shortname = models.CharField(max_length=100, choices=SHORTNAMES)
    term_starts = models.DateField()
    term_ends = models.DateField()
    
    class Meta:
        ordering =['id']
  
    def __str__(self):
        return self.name 
    

class Incumbent(models.Model):
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE, related_name='incumbents')
    member = models.ForeignKey(Profile, on_delete=models.CASCADE)
    portfolio = models.CharField(max_length=200, choices=portfolios)
    term_starts = models.DateField()
    term_ends = models.DateField()
    
    class Meta:
        ordering = ['id']
        
    def __str__(self):
        return f'{self.member} - {self.portfolio} of {self.committee}'
    
    
    


