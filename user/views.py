from typing import ContextManager
from django.shortcuts import render ,redirect
#redirect index sayfasina yonlendirmek icin kullandik

from . forms import RegisterForm ,LoginForm


#user modelini dahil ettik hazir django da bulunuyor
from django.contrib.auth.models import User

#login icin
#logout icin 
from django.contrib.auth import authenticate, login ,logout
#authenticate bize veri tabaninda kullanici olup olmadigini kontrol eder

#mesajlar icin 
from django.contrib import messages



def register(request):

    #post veya get request olsada kontrollu bir sekilde biliyoruz
    form = RegisterForm(request.POST or None)

    #requestimiz get ise bos gelecegi icin hic if bloguna girmez render ile context gonderilir
    if form.is_valid(): #form.is_valid() yaptigimizda clean methodu cagirilir ve eger true gelirse bu blog calisir
        #values teki degerler
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        #kullanici veriTabanina kayit etme islemi
        newUser = User(username = username)
        newUser.set_password(password) #parola sifreli olarak gonderildi

        newUser.save() #kayit edildi
        #kayit ettikten sonra sisteme giris yapmasini belirliyoruz
        login(request,newUser) #login edildi
       
        messages.success(request,"Basariyla Kayit Oldunuz")


        #ana sayfaya yonlendirmek icin
        return redirect("index")

    #post gelse bile kayit basariyla gerceklezse ayni sayfayi tekrar render ettik 
    context = {
            "form": form #contexte form bilgimizi verdik
        }
    return render(request,"register.html",context)
   




def loginUser(request):

    form = LoginForm(request.POST or None)

    context = {
        "form":form
    }

    if form.is_valid():
        username =form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        
        #veri tabani kontrolu authenticate metodu 
        user = authenticate(username =  username,password = password)
        
        #veri tabani ile eslesmiyorsa if e girer 
        if user is None:
            messages.info(request,"Kullanici adi Veya parolaniz yanlis !!")
            return render(request,"login.html",context)

        #giris basariliysa
        messages.success(request,"Basariyla giris yaptiniz")
        login(request,user)
        return redirect("index")
    return render(request,"login.html",context)





def logoutUser(request):
    logout(request)
    messages.success(request,"Basariyla Cikis Yapildi")
    return redirect("index")
