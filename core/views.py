from django.shortcuts import render,redirect
from .models import ListModel,TaskModel
from django.contrib import messages
from .decorators import unauth_user
from  django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .forms import ListForm,TaskForm,UserForm
from django.shortcuts import render, get_object_or_404,redirect


# Create your views here.
@unauth_user
def register_user(request):
    form=UserForm()
    if request.method=="POST":
        form=UserForm(request.POST)
        if form.is_valid():
            form.save()
            user= form.cleaned_data.get('username')
            messages.success(request,'Аккаунт создан '+user)
            return redirect('../login_page')
    data={'form':form}
    return render(request,'create_user.html',data)

@unauth_user
def login_page(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('../lists')
        else: messages.info(request,'Логин или пароль введен не верно!')
    data={}
    return render(request,'login_page.html',data)

@login_required(login_url='../login_page')
def logout_user(request):
    logout(request)
    return redirect('../login_page')

@login_required(login_url='../login_page')
def lists(request):
    form = TaskForm(request.POST or None, user=request.user)
    lists=ListModel.objects.filter(user=request.user)
    if form.is_valid():
        form.save()
        return redirect('../lists')
    return render(request,'lists.html',{'data':lists,'form':form})

def delete_list(request,id):
    list=ListModel.objects.get(id=id)
    list.delete()
    return redirect('../../lists.html')

def list(request,id):
    list=ListModel.objects.get(id=id)
    form = ListForm(request.POST or None, instance=list)
    get_object_or_404(ListModel, id=id)
    data = {'form': form}
    if list.user==request.user:
        if form.is_valid():
            form.save()
            return redirect('../../lists')
        return render(request, 'list.html', data)
def edit_task(request,lid,id):

    task=TaskModel.objects.get(id=id)
    form=TaskForm(request.POST or None, instance=task,user=request.user)
    get_object_or_404(TaskModel,id=id)
    data={'form':form}


    if form.is_valid():
        form.save()
        return redirect('../../')
    return render(request,'edit_task.html',data)



def view_list(request,id):


    list=ListModel.objects.get(id=id)
    if list.user==request.user:
        return render(request, 'view_list.html', {'data': list})
        get_object_or_404(ListModel,id=id)
    return redirect('../../lists')

def add_task(request):


    form = TaskForm(request.POST or None,user=request.user)
    if form.is_valid():
            form.save()
    data={'form':form}
    return render(request,'add_task.html',data)

def delete_task(request,id):
    task=TaskModel.objects.get(id=id)

    get_object_or_404(TaskModel,id=id)
    task.delete()
    return redirect('../../lists')
