from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Longtoshort

# Create your views here.

def index(request):
    context={
        "submit":False,
        "error":False
        }
    if request.method =='POST':
        context["submit"]=True
        data=request.POST
        long_url = data['longurl']
        custom_name=data['custom_name']
        
        #create
        try:
            obj=Longtoshort(long_url=long_url,short_url=custom_name)
            obj.save()

            #Read
            date=obj.date
            click=obj.click
        
            context['long_url']=long_url
            context['short_url']=request.build_absolute_uri()+custom_name
            context['date']=date
            context['clicks']=click
        except:
            context['error']=True
        
    else:
        print("user not sending data")
        
    
    return render(request,'index.html',context)

def all_analytics(request):
    row=Longtoshort.objects.all()
    context={
        'row':row
    }
    return render(request,'all-analytics.html',context)

def analytics(request):
    return render(request,'analytics.html')

#redirecting url 
def redirect_url(request,short_url):      #paas
    row =Longtoshort.objects.filter(short_url = short_url)   #not give if not exist #fetch
    if len(row)==0:
        return render(request,'error.html')    #error handlig
    
    obj=row[0]     #axcis and redirect
    long_url=obj.long_url
    obj.click=obj.click+1
    obj.save()
    print(long_url)
    return redirect(long_url)

