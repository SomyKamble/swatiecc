from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class Appointment(models.Model):
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed')], max_length=10)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor')

    def __str__(self):
        return "Patient - {} Doc- {} At {} {}".format(self.patient, self.doctor, self.date, self.time)


class Prescription(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_prescription')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_prescription')
    date = models.DateField(auto_now_add=True)
    symptoms = models.CharField(max_length=200)
    prescription = models.TextField()

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return "Presciption Doc-{} Patient-{}".format(self.doctor, self.patient)

PAYMENT_TYPES = [
    ('I','Individual'),
    ('C','Consulting')
]

class Payment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="patient_payments")
    date = models.DateField(auto_now_add=True)
    paid = models.IntegerField(null=True)
    outstanding = models.IntegerField(null=True)
    total = models.IntegerField(null=True)
    payment_type = models.CharField(choices=PAYMENT_TYPES, max_length=1, default="I")

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return "Payment Patient-{} Amount-{}".format(self.patient, self.total)

class Encfile(models.Model):
    to_user=models.ForeignKey(User,on_delete=models.CASCADE)
    # from_user=models.ForeignKey(User.email,on_delete=models.CASCADE)
    file = models.FileField(upload_to='files')
    from_user = models.CharField(max_length=200,null=True)
    created_at=models.DateTimeField(auto_created=True,auto_now=True,null=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)



class emp_id(models.Model):
    e_id = models.CharField(max_length=200)

    def __str__(self):
        return self.e_id


class Keys(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    private_key=models.CharField(max_length=20000)
    public_key = models.CharField(max_length=20000)