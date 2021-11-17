from django.shortcuts import render, redirect
from .forms import MinutesForm
from .models import Minutes
# Create your views here.
def minutes_list(request):
    minutes = Minutes.objects.all()
    return render(request, 'docs/minutes.html',{'minutes':minutes})

def upload_minutes(request):
    if request.method == 'POST':
        form = MinutesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('docs:minutes_list')
    else:
        form = MinutesForm()
    context ={
        'form':form,
    }
    return render(request, 'docs/minutes_form.html',context)


                    

