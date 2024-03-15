from django.shortcuts import render, redirect
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import numpy as np
from . models import *
import os
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import pandas as pd


# Create your views here.

def index(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def login(request):
    if request.method == 'POST':
        lemail = request.POST['useremail']
        lpassword = request.POST['psw']

        d = Register.objects.filter(
            remail=lemail, rpassword=lpassword).exists()
        print(d)
        if d:
            return render(request, "upload.html")

    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        email = request.POST['useremail']
        password = request.POST['psw']
        conpassword = request.POST['conpassword']
        print(email, password, conpassword)
        if password == conpassword:
            a = Register(remail=email, rpassword=password)
            a.save()
            msg = "succesfully registered"
            return render(request, 'login.html', {"message": msg})
        else:
            msg = 'Register failed!!'
            return render(request, 'register.html')

    return render(request, 'register.html')



def graphs(request):
    return render(request, "graphs.html")


def upload(request):
    if request.method == 'POST':
        Classes = []
        m1 = int(request.POST['alg'])
        paths = os.listdir('app/Data/train/')
        for i in paths:
            Classes.append(i)
            print(Classes)
        File = request.FILES['brain']
        s = Brain(image=File)
        s.save()
        path1 = 'app/static/saved/' + s.Imagename()

        print(path1)

        if m1 == 1:
            model_path = os.path.abspath("app/model/Mobilenet.h5")
            model = load_model(model_path, compile=False)
            # model = load_model(r'app/model/Mobilenet.h5', compile=False)
            x1 = image.load_img(path1, target_size=(256, 256))
            x1 = image.img_to_array(x1)
            x1 = np.expand_dims(x1, axis=0)
            x1 /= 255

        result = model.predict(x1)
        # a = classes[]
        b = np.argmax(result)
        results = Classes[b]

        # if results == 'authorised':
        #     data = pd.read_excel("app/static/fingervein.xlsx")
        #     # print(data)
        #     data1 = pd.read_excel("app/static/student.xlsx")
        #     # print(data1)
        #     return render(request, "important.html", {'cols': data.columns.values, 'rows': data.values.tolist(), 'cols1': data1.columns.values, 'rows1': data1.values.tolist()})
        # else:
        #     return render(request, "noaccess.html")

        return render(request, "result.html", {"message": results, "path": '/static/saved/' + s.Imagename()})

    return render(request, "upload.html")
