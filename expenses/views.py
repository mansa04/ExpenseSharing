from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm, GroupForm, MemberForm, ExpenseForm
from .models import Group, Member, ExpenseCategory, Expense


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def features(request):
    return render(request, 'features.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            print(f"User {user.username} registered successfully.")
            return redirect('groups_list')
        else:
            print(form.errors)
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('groups_list')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('groups_list')

@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('groups_list')
    else:
        form = GroupForm()
    return render(request, 'create_group.html', {'form': form})

@login_required
def groups_list(request):
    groups = Group.objects.all()
    return render(request, 'groups_list.html', {'groups': groups})

@login_required
def group_detail(request, group_id):
    group = Group.objects.get(id=group_id)
    members = Member.objects.filter(group=group)
    expenses = Expense.objects.filter(group=group)

    return render(request, 'group_detail.html', {
        'group': group,
        'members': members,
        'expenses': expenses,
    })


@login_required
def add_member(request, group_id):
    group = Group.objects.get(id=group_id)

    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.group = group
            member.save()
            return redirect('groups_list')
    else:
        form = MemberForm()
    return render(request, 'add_member.html', {'form': form, 'group': group})

# def edit_group(request, id):
#     group = get_object_or_404(Group, id=id)

#     if request.method == 'POST':
#         form = GroupForm(request.POST, instance=group)
#         if form.is_valid():
#             form.save()
#             return redirect('group_detail', id=group.id)
#     else:
#         form = GroupForm(instance=group)

#     return render(request, 'edit_group.html', {'form': form, 'group': group})

def delete_group(request, id):
    group = get_object_or_404(Group, id=id)
    if request.method == 'POST':
        group.delete()
        return redirect('groups_list')

    return render(request, 'delete_group.html', {'group': group})


@login_required
def add_expense(request, group_id):
    group = Group.objects.get(id=group_id)
    categories = ExpenseCategory.objects.all()

    if request.method == 'POST':
        form = ExpenseForm(request.POST) 

        if form.is_valid():
            expense = form.save(commit=False) 
            expense.group = group
            expense.save()  
            
            member_names = form.cleaned_data['member_names']
            member_names_list = [name.strip() for name in member_names.split(',')]  

            participants = []
            for name in member_names_list:
                member, created = Member.objects.get_or_create(name=name, group=group)
                participants.append(member)

            expense.participants.set(participants) 

            return redirect('group_detail', group_id=group.id)
    else:
        form = ExpenseForm() 
    return render(request, 'add_expense.html', {'form': form, 'group': group, 'categories': categories})

@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    members = group.members.all()

    expenses = group.expenses.prefetch_related('participants').all()

    
    for expense in expenses:
        
        expense.unique_participants = set(expense.participants.all())

 
        num_participants = len(expense.unique_participants)

       
        if num_participants > 0:
            expense.split_amount_value = expense.split_amount(num_participants)
        else:
            expense.split_amount_value = 0  
    context = {
        'group': group,
        'members': members,
        'expenses': expenses,
    }

    return render(request, 'group_detail.html', context)

