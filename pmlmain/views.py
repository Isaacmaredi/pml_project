from django.shortcuts import render, redirect
from django.http import HttpResponse
from pmlprofile.models import Committee, Incumbent
from django.views.generic import ListView, DetailView,CreateView,DeleteView


from .models import Contact

# Create your views here.
def index(request):
    
    qs= Incumbent.objects.all()
    term_qs = Incumbent.objects.first()
    print()
    
    # if request.method == 'POST':
    #     name = request.POST['name']
    #     email = request.POST['email']
    #     phone = request.POST['phone']
    #     message = request.POST['message']
    
    # contact = Contact(name=name, email=email, phone=phone, message=message )
    # print(contact)
    # contact.save()
    # messages.success(request, 'Your message has been submitted, someone from PML will contact you if necessary')

    context = {
        'qs': qs,
        'term_qs': term_qs,
        # 'contact': contact,
    }
    
    return render(request,'pmlmain/index.html', context)

# def contact(request):
#     if request.method == 'POST':
#         name = request.POST['name']
#         email = request.POST['email']
#         phone = request.POST['phone']
#         message = request.POST['message']
    
#     contact = Contact(name=name, email=email, phone=phone, message=message )

#     contact.save()
#     messages.success(request, 'Your message has been submitted, someone represengting PML will contact you if necessary')
#     return redirect('pmlmain/index.html')




# class CreateMessage(CreateView):
#     model = Contact 
#     template_name = 'pmlmain/index.html'
    
    
    
    