import io
from datetime import datetime

# import openai
import requests
from PIL import Image
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings

from .models import *

@login_required(login_url='/')
def home(request):
    user = User.objects.all()
    uc=user.count()
    request.session['uc']=uc
    review = Review.objects.all()
    rc = review.count()
    request.session['rc'] = rc
    complaint = Complaint.objects.all()
    cc = complaint.count()
    request.session['cc'] = cc
    payment = Payment.objects.all()
    pc = payment.count()
    request.session['pc'] = pc

    payment = Payment.objects.aggregate(total_amount=Sum('amount'))  # Replace 'amount' with your payment field name
    total_payment = payment['total_amount'] if payment['total_amount'] is not None else 0
    request.session["total_payment"] = total_payment

    # fetch latest five users
    latest_user = User.objects.order_by('-id')[:5][::-1]

    return render(request,"admin/dashboard.html",{'users':latest_user,'uc':uc,'rc':rc,'cc':cc,'total_payment':total_payment})

def login(request):
    return render(request,"login.html")

# def login_submit(request):
#     uname=request.POST['username']
#     passwd=request.POST['password']
#     try:
#         ob=Login.objects.get(username=uname,password=passwd)
#         request.session['lid']=ob.id
#         if ob.type=='admin':
#               ob1 = auth.authenticate(username='admin',password='admin')
#               if ob1 is not None:
#                   auth.login(request,ob1)
#               return  HttpResponse('''<script>window.location='/admin-dashboard'</script>''')
#         elif ob.type=='user':
#             ob1 = auth.authenticate(username='admin', password='admin')
#             if ob1 is not None:
#                 auth.login(request, ob1)
#             return HttpResponse('''<script>window.location='/user_home'</script>''')
#         else:
#             return HttpResponse('''<script>alert('Invalid');window.location='/'</script>''')
#     except Login.DoesNotExist:
#         return render(request, "login.html",{"error": "Invalid username or password..."})

from django.shortcuts import redirect

def login_submit(request):
    uname = request.POST.get('username', '').strip()
    passwd = request.POST.get('password', '')
    next_url = request.GET.get('next', '/')

    try:
        ob = Login.objects.get(username=uname, password=passwd)
        request.session['lid'] = ob.id

        if ob.type == 'admin':
            ob1 = auth.authenticate(username='admin', password='admin')
            if ob1 is not None:
                auth.login(request, ob1)
            return redirect(next_url if next_url != '/' else '/admin-dashboard')

        elif ob.type == 'user':
            ob1 = auth.authenticate(username='admin', password='admin')
            if ob1 is not None:
                auth.login(request, ob1)
            return redirect(next_url if next_url != '/' else '/user_home')

        else:
            return HttpResponse('''<script>alert('Invalid');window.location='/'</script>''')

    except Login.DoesNotExist:
        return render(request, "login.html", {"error": "Invalid username or password..."})
    except Exception:
        return render(request, "login.html", {"error": "Something went wrong. Please try again."})


def logout(request):
    auth.logout(request)
    return render(request,'login.html')

def forget_password(request):
    return render(request, "User/forgotpassword.html")

from django.core.mail import send_mail


def forget_password_post(request):
    em = request.POST['email']
    import random
    import string
    # password = random.randint(000000, 999999)
    user = User.objects.get(email=em)

    log = Login.objects.get(id=user.LOGIN.id)



    length = 10 # Adjust the password length as needed
    chars = string.ascii_letters + string.digits
    password = ''.join(random.choice(chars) for _ in range(length))

    if log:
        logg = log
        subject = 'Your temporary password'
        message = f'Your new temporary password is: {password}'
        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER, [em], fail_silently=False)
        except Exception:
            return HttpResponse('<script>alert("Email send failed. Please try again later.");window.location="/forget_password"</script>')
        logg.password = password
        logg.save()
        return HttpResponse('<script>alert("Please check your email for the new password.");window.location="/"</script>')
    else:
        return HttpResponse('<script>alert("invalid");window.location="/forget_password"</script>')


# def forget_password_post(request):
#     em = request.POST['email']
#     import random
#     import string
#     # log = Login.objects.filter(username=em)
#     user = User.objects.get(email=em)
#     login_id = user.LOGIN_id
#     log = Login.objects.filter(id=login_id)
#
#     length = 10 # Adjust the password length as needed
#     chars = string.ascii_letters + string.digits + string.punctuation
#     password = ''.join(random.choice(chars) for _ in range(length))
#
#     if log.exists():
#         logg = Login.objects.get(id=login_id)
#         # message = 'temporary Password  is!... ' + str(password)
#         url = 'http://127.0.0.1:8000/new_password/'+ logg.username
#         message = f'Temporary Password is!... {password}. Reset it here: {url}'
#         send_mail(
#             'temporary...! Password',
#             message,
#             settings.EMAIL_HOST_USER,
#             [em, ],
#             fail_silently=False
#         )
#         logg.password = password
#         logg.save()
#         return HttpResponse('<script>alert("..Please check Email...");window.location="/"</script>')
#     else:
#         return HttpResponse('<script>alert("invalid");window.location="/forget_password"</script>')
#
# def new_password(request,username):
#     user = Login.objects.get(username=username)
#     print(user.username)
#     if 'submit' in request.POST:
#         password = request.POST['password']
#         user.password = password
#         user.save()
#         print(password)
#         return HttpResponse('''<script>window.location='/'</script>''')
#     return render(request, "User/new_password.html")



# ADMIN
@login_required(login_url='/')
def view_user(request):
    ob=User.objects.all()
    return render(request,"admin/view_user.html",{'users':ob})

@login_required(login_url='/')
def accept_user(request,id):
    request.session['uid']=id
    ob=Login.objects.get(id=request.session['uid'])
    ob.type='user'
    ob.save()
    return HttpResponse('''<script>;window.location='/view_user'</script>''')

@login_required(login_url='/')
def reject_user(request,id):
    request.session['uid']=id
    ob=Login.objects.get(id=request.session['uid'])
    ob.type='rejected'
    ob.save()
    return HttpResponse('''<script>window.location='/view_user'</script>''')

@login_required(login_url='/')
def edit_user_action(request,id):
    ob=Login.objects.get(id=id)
    ob.type='pending'
    ob.save()
    return HttpResponse('''<script>window.location='/view_user'</script>''')


@login_required(login_url='/')
def view_complaint(request):
    ob=Complaint.objects.all()
    return render(request,"admin/complaint.html",{"data":ob})

@login_required(login_url='/')
def send_reply(request,id):
    ob=Complaint.objects.get(id=id)
    if 'submit' in request.POST:
        reply=request.POST['reply_message']
        id=request.POST['id']
        a=Complaint.objects.get(id=id)
        a.reply=reply
        a.save()
        return HttpResponse('''<script>window.location='/view_complaint'</script>''')

    return render(request, "admin/send_reply.html",{"complaint":ob})

@login_required(login_url='/')
def view_review(request):
    ob=Review.objects.all()
    return render(request,"admin/review.html",{"data":ob})

# USER side

@login_required(login_url='/')
def user_home(request):
    return render(request, "User/user_home.html",)


# def register(request):
#     return render(request,"User/user_register.html")
#
# def register_post(request):
#     username=request.POST['username']
#     password = request.POST['password']
#     email=request.POST['email']
#     # name = request.POST['name']
#     # phone=request.POST['mobile']
#     # image=request.FILES['image']
#     # fs=FileSystemStorage()
#     # fp=fs.save(image.name,image)
#
#     a=Login.objects.filter(username=username)
#     if a.exists():
#         return HttpResponse('''<script>alert('Username Already taken ');window.location='/register'</script>''')
#
#     ob=Login()
#     ob.username=username
#     ob.password=password
#     ob.type="user"
#     ob.save()
#
#     obb=User()
#     obb.LOGIN=ob
#     obb.name='name'
#     obb.email=email
#     obb.phone= 9999999999
#     obb.image=' '
#     obb.save()
#
#     return HttpResponse('''<script>alert('Succefully Registered ');window.location='/'</script>''')

from django.shortcuts import render
from django.http import HttpResponse
from .models import Login, User  # Ensure your models are correctly imported

def register(request):
    return render(request, "User/user_register.html", {"error": ""})

def register_post(request):
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']

    if Login.objects.filter(username=username).exists():
        return render(request, "User/user_register.html", {"error": "Username already taken. Please choose another one."})

    # Creating a new Login entry
    ob = Login()
    ob.username = username
    ob.password = password
    ob.type = "user"
    ob.save()

    # Creating a new User entry
    obb = User()
    obb.LOGIN = ob
    obb.name = 'name'  # You might want to actually use a valid name input
    obb.email = email
    obb.phone = 9999999999
    obb.image = ''
    obb.save()

    return render(request, "User/user_register.html", {"success": "Successfully registered! You can now log in."})


@login_required(login_url='/')
def profile(request):
    user = User.objects.get(LOGIN_id=request.session['lid'])

    return render(request, 'User/profile.html',{'user': user})

@login_required(login_url='/')
def update_profile(request):
    name = request.POST['full_name']
    # email=request.POST['email']
    phone=request.POST['phone']
    ob = User.objects.get(LOGIN_id=request.session['lid'])
    ob.name = name
    # ob.email=email
    ob.phone = phone
    if "profile_image" in request.FILES:
        image = request.FILES["profile_image"]
        fs = FileSystemStorage()
        fp = fs.save(image.name, image)
        ob.image = fp
    ob.save()
    return HttpResponse('''<script>alert('Profile updated');window.location='/profile/'</script>''')


@login_required(login_url='/')
def all_complaints(request):
    complaints = Complaint.objects.all()
    return render(request, "User/all_complaints.html",{"complaints":complaints})

@login_required(login_url='/')
def send_complaint(request):
    return render(request,"User/send_complaint.html")

@login_required(login_url='/')
def send_complaint_post(request):
    complaint=request.POST['complaint']
    a=Complaint()
    a.complaint=complaint
    a.date=datetime.now().today().date()
    a.reply='pending'
    a.USER=User.objects.get(LOGIN_id=request.session['lid'])
    a.save()
    return HttpResponse('''<script>alert('Successfully send a complaint ');window.location='/all_complaints'</script>''')

@login_required(login_url='/')
def send_review(request):
    return render(request,"User/send_review.html")

@login_required(login_url='/')
def send_review_post(request):
    review = request.POST['review']
    rating = request.POST['rating']
    ob = Review()
    ob.USER = User.objects.get(LOGIN_id=request.session['lid'])
    ob.rating = rating
    ob.review = review
    ob.date = datetime.now().today().date()
    ob.save()

    return HttpResponse('''<script>alert('Thanks for the review');window.location='/user_home'</script>''')

@login_required(login_url='/')
def view_cmp_reply(request):
    ob = Complaint.objects.filter(USER__LOGIN_id=request.session['lid'])
    return render(request,"User/view_reply.html",{"complaint":ob})



import razorpay
@login_required(login_url='/')
def user_pay_proceed(request):

    request.session['pay_amount'] = 100
    amt = 100
    key_id = settings.RAZORPAY_KEY_ID
    key_secret = settings.RAZORPAY_KEY_SECRET
    if not key_id or not key_secret:
        return HttpResponse('<script>alert("Payment configuration missing. Contact support.");window.location="/user_home"</script>')

    client = razorpay.Client(auth=(key_id, key_secret))
    payment = client.order.create({'amount': amt * 100, 'currency': "INR", 'payment_capture': '1'})
    res=User.objects.get(LOGIN__id=request.session['lid'])
    # ob=order_table.objects.get(id=request.session['rid'])
    # ob.status='paid'
    # ob.save()
    return render(
        request,
        'user/UserPayProceed.html',
        {
            'p': payment,
            'val': res,
            'lid': request.session['lid'],
            'RAZORPAY_KEY_ID': key_id,
        },
    )




def on_payment_success(request):
    # request.session['rid'] = request.GET['id']
    request.session['lid'] = request.GET['lid']
    var = auth.authenticate(username='admin', password='admin')
    if var is not None:
        auth.login(request, var)
    # amt = request.session['pay_amount']
    ob=Payment()
    ob.USER = User.objects.get(LOGIN_id = request.session['lid'])
    ob.date=datetime.today()
    ob.time=datetime.now().time()
    ob.amount =100
    # ob.ORDER=order_table.objects.get(id=request.session['rid'])
    ob.status='paid'
    ob.save()

    return HttpResponse('''<script>alert("Success! Thank you for your Contribution");window.location="/user_home"</script>''')

@login_required(login_url='/')
def my_chatbot(request):
    return render(request,"User/chatbot.html")


@login_required(login_url='/')
@ensure_csrf_cookie
def chatbot(request):
    # user = User.objects.get()
    # return render(request,"User/chatbot.html")
    # return render(request,"User/samplechatgpt.html")
    return render(request,"User/chatbot_interaction.html")



import google.generativeai as genai
from django.shortcuts import render

# Configure Google Gemini API using env-backed settings
model = None
try:
    if settings.GOOGLE_API_KEY:
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        model = genai.GenerativeModel(getattr(settings, 'GENAI_MODEL_NAME', 'gemini-1.5-flash'))
except Exception:
    model = None


def generate_gemini_response(prompt):
    """
    Generate a response using the Gemini model with a context about Sreepathy College.
    """
    context_prompt = f" {prompt}"
    try:
        if not model:
            return "AI is not configured. Please try again later."
        response = model.generate_content(context_prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating response: {str(e)}"



from django.http import JsonResponse
import json

@login_required(login_url='/')
def chatbot_response(request):
    """
    Process user messages and return chatbot responses.
    """
    if request.method == "POST":
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
            print(user_message, "Received message")

            if not user_message:
                return JsonResponse({'response': 'Please enter a valid question.'})

            # Generate a response from Gemini
            gemini_response = generate_gemini_response(user_message)
            user = User.objects.get(LOGIN_id=request.session['lid'])
            ob=Chatbot()
            ob.USER = user
            ob.question = user_message
            ob.reply = gemini_response
            ob.date = datetime.now().today().date()
            ob.type = 'pending'
            ob.save()
            return JsonResponse({'response': gemini_response})

        except json.JSONDecodeError:
            # If JSON is not valid, return an error response
            return JsonResponse({'response': 'Invalid JSON format.'})

    return JsonResponse({'response': 'Invalid request method.'})



@ensure_csrf_cookie
def image_generation(request):
    return render(request,'User/image_generation.html')

def image_generation_post(request):
    data = json.loads(request.body)
    user_message = data.get('message', '').strip()
    print(user_message, "Received message")


    image_data, image_name = generate_design(user_message)
    if not image_name:
        return JsonResponse({'response': 'Image generation is currently unavailable. Please try again later.'}, status=503)
    return JsonResponse({'response': image_name})


def generate_design(prompt):
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    if not settings.HUGGINGFACE_API_TOKEN:
        return None, None
    headers = {"Authorization": f"Bearer {settings.HUGGINGFACE_API_TOKEN}"}

    def query(payload):
        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            response.raise_for_status()

            if response.headers.get("Content-Type") == "application/json":
                # Handle error in JSON response
                error_message = response.json()
                print("Error response:", error_message)
                return None

            return response.content
        except requests.RequestException as e:
            print(f"HTTP Request failed: {e}")
            return None

    def save_image_from_bytes(image_bytes):
        try:
            # Validate it is an image and save raw bytes
            Image.open(io.BytesIO(image_bytes))
            image_name = f"gpt_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
            fs = FileSystemStorage()
            image_path = fs.save(image_name, ContentFile(image_bytes))
            return image_path, image_name

        except IOError as e:
            print(f"Error opening or saving image: {e}")
            return None, None

    # Call the query with the user's prompt
    image_bytes = query({"inputs": prompt})
    if image_bytes:
        return save_image_from_bytes(image_bytes)
    else:
        print("No valid image data received.")
        return None, None
