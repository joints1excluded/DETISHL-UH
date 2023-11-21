from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django import forms


from .models import Client
from .models import Login

    
def all_clients(request):
    client_list = Client.objects.raw("SELECT * FROM Client")
    template = loader.get_template("all_clients.html")
    context = {
        "client_list": client_list,
    }
    return HttpResponse(template.render(context, request))


class register_form(forms.Form):
    full_name = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    login = forms.CharField(required=True)
    password = forms.CharField(required=True)
    password_repeat = forms.CharField(required=True)

    def get_name(self):
        data = self.cleaned_data['full_name']
        return data

def register_client(request):
    if request.method == "POST":

        form = register_form(request.POST)
        template = loader.get_template("client_register.html")

        if form.is_valid():
            
            logins = Login.objects.all()
            for log in logins:
                if form.cleaned_data['login'] == log.client_login:
                    context = {
                        "register_form": form,
                        "error": "Login taken"
                    }
                    return HttpResponse(template.render(context, request))
            
            if form.cleaned_data['password'] != form.cleaned_data['password']:
                context = {
                    "register_form": form,
                    "error": "Passwords are not the same"
                }
                return HttpResponse(template.render(context, request))
            else:
                client_id = Client.objects.order_by('-client_id')[0].client_id + 1
                full_name = form.cleaned_data['full_name']
                phone_number = form.cleaned_data['phone']
                client_email = form.cleaned_data['email']
                
                client = Client(client_id=client_id, full_name=full_name, phone_number=phone_number, client_email=client_email)
                client.save()

                client_login = form.cleaned_data['login']
                client_password = form.cleaned_data['password']

                login = Login(client_login = client_login, client_password = client_password, client_id=client_id)
                login.save()

                template = loader.get_template("profile.html")
                context = {'client' : client}
                return HttpResponse(template.render(context, request))

    form = register_form()
    template = loader.get_template("client_register.html")
    context = {
        "register_form": form,
    }
    return HttpResponse(template.render(context, request))


# def profile(request):
#     template = loader.get_template("profile.html")
#     context = {'client' : client}
#     return HttpResponse(template.render(context, request))