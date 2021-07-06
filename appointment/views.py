from Cryptodome.Cipher import AES
from django.shortcuts import render, redirect
from .models import * 
from .forms import * 
from django.views.generic import ListView, CreateView,DetailView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from user_profile.models import UserProfile
# Create your views here.
from Cryptodome.Util.Padding import pad
from .models import *
import hashlib, secrets, binascii
#from .forms import intake
import sys
from .forms import upload_form,intake,Key_create
from django.contrib.auth import decorators
from tinyec import registry
from django.http import HttpResponse

# Create your views here.


def index(request):
    data = 0
    empid = request.POST.get('empid')
    e_id = emp_id.objects.values('e_id')
    print(sys.maxsize)

    # print(request.session.get('e_id'))
    star = [str(i['e_id']) for i in e_id.values()]
    print(star)
    emp = [request.user.username]
    print(emp)
    if empid in emp:
        sug = "you are valid person"
        request.session['e'] = empid
        print("this is ", empid)
    else:
        sug = "invalid person"

    context = {
        "data": data,
        "sug": sug,
        "empid": empid,
        'star': star
    }

    return render(request, "first.html", context)


def keys(request):
    empid = request.session.get('e')

    print("print", empid)
    curve = registry.get_curve('brainpoolP256r1')
    P1PrivKey = secrets.randbelow(curve.field.n)
    P1PubKey = P1PrivKey * curve.g
    # P1PubKey=str(P1PubKey).split("on")[0].replace(", ","")
    # form = intake()
    try:
        data = Keys.objects.filter(user=request.user)
        if data:
            data.update(private_key=P1PrivKey, public_key=P1PubKey)
        else:
            pass

    except:
        Keys.objects.create_or_update(user=request.user, private_key=P1PrivKey, public_key=P1PubKey)

    data = Keys.objects.get(user=request.user)
    data1 = (Keys.objects.filter(user=request.user))
    # data.save()
    context = {
        "empid": empid,
        "private_key": P1PrivKey,
        "public_key": P1PubKey,
        # 'form':form
    }
    if request.method == "POST":
        form = intake(request.POST, request.FILES)
        print(request.FILES)
        # file=request.FILES['file'].read()

        sharedKey = P1PrivKey * form['public_key'].value()
        pubKey = sharedKey
        print(pubKey)

        sha = hashlib.sha256(int.to_bytes(pubKey.x, 32, 'big'))
        sha.update(int.to_bytes(pubKey.y, 32, 'big'))
        sha.digest()
        key = sha.digest()
        cipher = AES.new(key, AES.MODE_GCM)
        enc_file = cipher.encrypt(pad(file, AES.block_size))
        print(enc_file)
        # print(file)
        print(form['public_key'].value())

    return render(request, "second.html", context)


class AppointmentsForAPatientView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'account:login'

    def get_queryset(self):
        return Appointment.objects.filter(patient=self.request.user)


class AppointmentsForADoctorView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'account:login'

    def get_queryset(self):
        return Appointment.objects.filter(doctor=self.request.user)


class MedicalHistoryView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'account:login'

    def get_queryset(self):
        return Prescription.objects.filter(patient=self.request.user)


class PrescriptionListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'account:login'

    def get_queryset(self):
        return Prescription.objects.filter(doctor=self.request.user)


@login_required(login_url='/login/')
def PrescriptionCreateView(request):
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.doctor = request.user
            prescription.save()
            return redirect('appointment:doc-prescriptions')
    else:
        form = PrescriptionForm()
    return render(request, 'appointment/prescription_create.html', {'form': form})


@login_required(login_url='/login/')
def AppointmentCreateView(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.save()
            return redirect('appointment:r_dashboard')
    else:
        form = AppointmentForm()
    return render(request, 'appointment/appointment_create.html', {'form': form})


@login_required(login_url='/login/')
def rdashboard(request):
    if request.method == "GET" and request.user.user_type == "R":
        context = {
            "totalApp" : len(Appointment.objects.all()),
            "compApp" : len(Appointment.objects.filter(status="Completed")),
            "pendApp" : len(Appointment.objects.filter(status="Pending")),
            "app_list" : Appointment.objects.all(),
            "pat_list" : UserProfile.objects.filter(user__user_type="P")[:5]
        }
        return render(request, 'appointment/r_dashboard.html', context=context)


@login_required(login_url='/login/')
def hrdashboard(request):
    if request.method == "GET" and request.user.user_type == "HR":
        context = {
            "totalPat" : len(User.objects.filter(user_type="P")),
            "totalDoc" : len(User.objects.filter(user_type="D")),
            "ondutyDoc" : len(UserProfile.objects.filter(status="Active").filter(user__user_type="D")),
            "doc_list" : UserProfile.objects.filter(user__user_type="D")
        }
        return render(request, 'appointment/hr_dashboard.html', context=context)


@login_required(login_url='/login/')
def hraccounting(request):
    if request.method == "GET" and request.user.user_type == "HR":
        context = {
            "payment_ind" : Payment.objects.filter(payment_type="I"),
            "payment_cons" : Payment.objects.filter(payment_type="C"),
        }
        return render(request, 'appointment/accounting.html', context=context)


@login_required(login_url='/login/')
def pateintpayments(request):
    if request.method == "GET":
        context = {
            "payment_me" : Payment.objects.filter(patient=request.user),
        }
        return render(request, 'appointment/payment_invoice.html', context=context)



class Dashbaord(LoginRequiredMixin,ListView):
    login_url = 'login'
    template_name = "appointment/encfilelist.html"
    context_object_name = 'Orders'

    def get_queryset(self):
        return Encfile.objects.filter(to_user=self.request.user)




class keymake(LoginRequiredMixin,CreateView):
    login_url = 'login'
    form_class = Key_create
    template_name = 'appointment/appointment_create.html'

    def get_initial(self):
        user1=self.request.user.username
        curve = registry.get_curve('brainpoolP256r1')
        P1PrivKey = secrets.randbelow(curve.field.n)
        P1PubKey = P1PrivKey * curve.g
        return {'private_key': user1+str(P1PrivKey),
                'public_key': user1+str(P1PubKey)}

    def form_valid(self, form):
        obj=form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return HttpResponse('Key_created_and_saved')




class Upload(LoginRequiredMixin,CreateView):
    login_url = 'login'
    form_class = upload_form
    template_name = 'appointment/upload.html'
    success_url = '/'
    context_object_name = 'Keys'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['page_title'] = Keys.objects.filter(user=self.request.user).last()
        return data

    def get_queryset(self):
        return Keys.objects.filter(user=self.request.user).last()

    def form_valid(self, form):
        fam=form.save(commit=False)
        print(fam)
        #data=Encfile(to_user=form['to_user'],file=form['file'],from_user=self.request.user.username)
        fam.from_user=self.request.user.username
        fam.save()
        return super(Upload,self).form_valid(form)


class Decrypt(LoginRequiredMixin,DetailView):
    login_url = 'login'
    template_name = 'appointment/dec.html'
    context_object_name = 'Orders'


    def get_queryset(self):
        return Encfile.objects.filter(to_user=self.request.user)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['page_title'] = Keys.objects.filter(user=self.request.user).last()
        data['obj'] = Encfile.objects.filter(to_user=self.request.user)
        return data





