from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

from account.forms import CustomUserRegistrationForm
from account.models import CustomUser


def home(request):
    return render(request, 'home.html')

def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser().objects.get(pk=uid)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return HttpResponse("Hesabınız uğurla təsdiq edildi. İndi daxil ola bilərsiniz.")
        else:
            return HttpResponse("Təsdiq linki etibarsızdır.")
    except (TypeError, ValueError, OverflowError, CustomUser().DoesNotExist):
        return HttpResponse("Təsdiq linki etibarsızdır.")
    
    

def register(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = CustomUser().objects.create_user(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                is_active=False)

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(str(user.pk).encode())
            current_site = get_current_site(request)
            mail_subject = 'Hesabınızı təsdiq edin'
            message = render_to_string('account/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            })
            send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

            messages.success(request, "Qeydiyyatınız uğurla tamamlandı. Emailinizə təsdiq linki göndərildi.")
            return redirect('login')
        else:
            messages.error(request, "Formda səhvlər var. Zəhmət olmasa yenidən yoxlayın.")
    else:
        form = CustomUserRegistrationForm()

    return render(request, 'account/register.html', {'form': form})




def user_login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        print(user)
        if user:
            if user.is_active:
                print("aktivdir  ########################")
                login(request, user)
                return redirect("home")
            else:
                print("aktiv deyil #############")
                messages.error(request, "Hesabınız təsdiqlənməyib. Zəhmət olmasa emailinizi yoxlayın.")
                return redirect('login')
        else:
            messages.error(request,"Please try again")
    return render(request, 'account/login.html', )





def user_logout(request):
    logout(request)
    return redirect('home')
