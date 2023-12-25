from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from api.serializer import MyTokenObtainPairSerializer, RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.http import HttpResponse   
from django.contrib.auth import login, authenticate  
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .token import account_activation_token  
from django.contrib.auth.models import User  
from django.core.mail import EmailMessage
import subprocess
from django.http import JsonResponse
from django.core.files.storage import default_storage, FileSystemStorage
from api.models import EEG_DataM,DemoM
from api.serializer import EEGDSerializer,DEMOSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
import sys
from subprocess import run, PIPE
from django.core.files.storage import FileSystemStorage
from django.template import RequestContext

# Create your views here.
def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('template_activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        message.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
            received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        message.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')

def register(request):
    if request.method == "POST":
        form = RegisterSerializer(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('/')

        else:
            for error in list(form.errors.values()):
                message.error(request, error)

    else:
        form = RegisterSerializer()

    return render(
        request=request,
        template_name="users/register.html",
        context={"form": form}
        )
def signup(request):  
    if request.method == 'POST':  
        form = RegisterSerializer(request.POST)  
        if form.is_valid():  
            # save form in the memory not in database  
            user = form.save(commit=False)  
            user.is_active = False  
            user.save()  
            # to get the domain of the current site  
            current_site = get_current_site(request)  
            mail_subject = 'Activation link has been sent to your email id'  
            message = render_to_string('acc_active_email.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            })  
            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
            email.send()  
            return HttpResponse('Please confirm your email address to complete the registration')  
    else:  
        form = RegisterSerializer()  
    return render(request, 'registerPage.js', {'form': form})  
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')
    
    return redirect('homepage')

    

@csrf_exempt
def SaveFileDemo(request):
    file=request.FILES['file']
    file_name=default_storage.save(file.name,file)
    return JsonResponse(file_name,safe=False)

@csrf_exempt
def SaveFileEEG(request):
    file1=request.FILES['file']
    file_name=default_storage.save(file1.name,file1)
    return JsonResponse(file_name,safe=False)

@csrf_exempt
def DemoApi(request,id=0):
    if request.method=='GET':
        Demo = DemoM.objects.all()
        Demo_serializer=DEMOSerializer(Demo,many=True)
        return JsonResponse(Demo_serializer.data,safe=False)
    elif request.method=='POST':
        Demo_data=JSONParser().parse(request)
        Demo_serializer=DEMOSerializer(data=Demo_data)
        if Demo_serializer.is_valid():
            Demo_serializer.save()
            return JsonResponse("Added Successfully",safe=False)
        return JsonResponse("Failed to Add",safe=False)
    elif request.method=='PUT':
        Demo_data=JSONParser().parse(request)
        Demo=DemoM.objects.get(DFileId=Demo_data['DFileId'])
        Demo_serializer=DEMOSerializer(Demo,data=Demo_data)
        if Demo_serializer.is_valid():
            Demo_serializer.save()
            return JsonResponse("Updated Successfully",safe=False)
        return JsonResponse("Failed to Update")
    elif request.method=='DELETE':
        Demo=DemoM.objects.get(DFileId=id)
        DemoM.delete()
        return JsonResponse("Deleted Successfully",safe=False)
    
@csrf_exempt
def EEGApi(request,id=0):
    if request.method=='GET':
        EEG = EEG_DataM.objects.all()
        EEG_serializer=EEGDSerializer(EEG,many=True)
        return JsonResponse(EEG_serializer.data,safe=False)
    elif request.method=='POST':
        EEG_data=JSONParser().parse(request)
        EEG_serializer=EEGDSerializer(data=EEG_data)
        if EEG_serializer.is_valid():
            EEG_serializer.save()
            return JsonResponse("Added Successfully",safe=False)
        return JsonResponse("Failed to Add",safe=False)
    elif request.method=='PUT':
        EEG_data=JSONParser().parse(request)
        EEG=EEG_DataM.objects.get(EFileId=EEG_data['EFileId'])
        EEG_serializer=EEGDSerializer(EEG,data=EEG_data)
        if EEG_serializer.is_valid():
            EEG_serializer.save()
            return JsonResponse("Updated Successfully",safe=False)
        return JsonResponse("Failed to Update")
    elif request.method=='DELETE':
        EEG=EEG_DataM.objects.get(EFileId=id)
        EEG_DataM.delete()
        return JsonResponse("Deleted Successfully",safe=False)


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token/',
        '/api/register/',
        '/api/token/refresh/',
        '/api/demo',
    ]
    return Response(routes)

def Pred(request):
    return render(request, "Predict.html")

def ERP(request):
    return render(request, "ERP_Data.html")

def Comp(request):
    return render(request, "ERP_Component.html")

def run_script_pred(request):
    # Run the external Python script
    command = ['python', 'D:\\Documents\\FYP\\trial2(backend)\\Uploads\\predict_main.py']
    result = subprocess.run(command, capture_output=True, text=True)
    print(f"Command: {' '.join(command)}")
    print(f"Exit Code: {result.returncode}")
    print(f"Output: {result.stdout}")
    print(f"Error: {result.stderr}")
    # Return the script output as a JSON response
    response_data = {'output': result.stdout}
    return JsonResponse(response_data)

def run_script_comp(request):
    # Run the external Python script
    command = ['python', 'D:\\Documents\\FYP\\trial2(backend)\\Uploads\\ERP_Comp_inp.py']
    result = subprocess.run(command, capture_output=True, text=True)
    print(f"Command: {' '.join(command)}")
    print(f"Exit Code: {result.returncode}")
    print(f"Output: {result.stdout}")
    print(f"Error: {result.stderr}")
    # Return the script output as a JSON response
    response_data = {'output': result.stdout}
    return JsonResponse(response_data)

def run_script_erp(request):
    # Run the external Python script
    command = ['python', 'D:\\Documents\\FYP\\trial2(backend)\\Uploads\\ERP_Data_inp.py']
    result = subprocess.run(command, capture_output=True, text=True)
    print(f"Command: {' '.join(command)}")
    print(f"Exit Code: {result.returncode}")
    print(f"Output: {result.stdout}")
    print(f"Error: {result.stderr}")
    # Return the script output as a JSON response
    response_data = {'output': result.stdout}
    return JsonResponse(response_data)