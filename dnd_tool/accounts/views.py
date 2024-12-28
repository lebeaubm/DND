from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CharacterSheet

# Signup View
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

# Login View
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'accounts/login.html')

# Logout View
def user_logout(request):
    logout(request)
    return redirect('login')

# Dashboard View (Protected Page)
@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

# List Character Sheets
@login_required
def character_list(request):
    sheets = CharacterSheet.objects.filter(user=request.user)
    return render(request, 'accounts/character_list.html', {'sheets': sheets})

# Create Character Sheet
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CharacterSheet

# Create Character Sheet
@login_required
def character_create(request):
    if request.method == 'POST':
        name = request.POST.get('name', 'Unnamed Character')
        class_name = request.POST.get('class_name', 'Unknown Class')
        level = request.POST.get('level', 1)
        hit_points = request.POST.get('hit_points', 10)
        strength = request.POST.get('strength', 10)
        dexterity = request.POST.get('dexterity', 10)
        constitution = request.POST.get('constitution', 10)
        intelligence = request.POST.get('intelligence', 10)
        wisdom = request.POST.get('wisdom', 10)
        charisma = request.POST.get('charisma', 10)

        try:
            CharacterSheet.objects.create(
                user=request.user,
                name=name,
                class_name=class_name,
                level=int(level),
                hit_points=int(hit_points),
                strength=int(strength),
                dexterity=int(dexterity),
                constitution=int(constitution),
                intelligence=int(intelligence),
                wisdom=int(wisdom),
                charisma=int(charisma),
            )
            messages.success(request, "Character sheet created successfully!")
            return redirect('character_list')
        except Exception as e:
            messages.error(request, f"Error creating character sheet: {e}")
            return render(request, 'accounts/character_form.html')

    return render(request, 'accounts/character_form.html')


# @login_required
# def character_create(request):
#     if request.method == 'POST':
#         try:
#             CharacterSheet.objects.create(
#                 user=request.user,
#                 name=request.POST.get('name', ''),
#                 class_name=request.POST.get('class_name', ''),
#                 level=request.POST.get('level', 1),
#                 hit_points=request.POST.get('hit_points', 10),
#                 strength=request.POST.get('strength', 10),
#                 dexterity=request.POST.get('dexterity', 10),
#                 constitution=request.POST.get('constitution', 10),
#                 intelligence=request.POST.get('intelligence', 10),
#                 wisdom=request.POST.get('wisdom', 10),
#                 charisma=request.POST.get('charisma', 10),
#             )
#             messages.success(request, "Character sheet created successfully!")
#             return redirect('character_list')
#         except Exception as e:
#             messages.error(request, f"Error: {e}")
#     return render(request, 'accounts/character_form.html')


# Edit Character Sheet
@login_required
def character_edit(request, sheet_id):
    sheet = get_object_or_404(CharacterSheet, id=sheet_id, user=request.user)
    if request.method == 'POST':
        sheet.name = request.POST['name']
        sheet.class_name = request.POST['class_name']
        sheet.level = request.POST['level']
        sheet.hit_points = request.POST['hit_points']
        sheet.strength = request.POST['strength']
        sheet.dexterity = request.POST['dexterity']
        sheet.constitution = request.POST['constitution']
        sheet.intelligence = request.POST['intelligence']
        sheet.wisdom = request.POST['wisdom']
        sheet.charisma = request.POST['charisma']
        sheet.save()
        messages.success(request, "Character sheet updated successfully!")
        return redirect('character_list')
    return render(request, 'accounts/character_form.html', {'sheet': sheet})

# Delete Character Sheet
@login_required
def character_delete(request, sheet_id):
    sheet = get_object_or_404(CharacterSheet, id=sheet_id, user=request.user)
    sheet.delete()
    messages.success(request, "Character sheet deleted successfully!")
    return redirect('character_list')





