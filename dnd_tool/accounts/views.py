from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CharacterSheet
from django.core.paginator import Paginator
from django.db.models import Q  # For filtering
from django.contrib import admin

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

# # Dashboard View (Protected Page)
# @login_required
# def dashboard(request):
#     return render(request, 'accounts/dashboard.html')


# # Dashboard View (Protected Page)
# @login_required
# def dashboard(request):
#     # Fetch all character sheets belonging to the logged-in user
#     character_sheets = CharacterSheet.objects.filter(user=request.user)
#     return render(request, 'accounts/dashboard.html', {'character_sheets': character_sheets})

@login_required
def dashboard(request):
    # Get query parameters for sorting and filtering
    sort_by = request.GET.get('sort', 'created_at')  # Default to sorting by creation date
    filter_class = request.GET.get('class', '')  # Filter by class name
    filter_level = request.GET.get('level', '')  # Filter by level
    
    # Start with the user's character sheets
    character_sheets = CharacterSheet.objects.filter(user=request.user)
    
    # Apply filtering
    if filter_class:
        character_sheets = character_sheets.filter(class_name__icontains=filter_class)
    if filter_level:
        character_sheets = character_sheets.filter(level=filter_level)
    
    # Apply sorting
    if sort_by in ['name', 'level', 'created_at']:
        character_sheets = character_sheets.order_by(sort_by)
    
    # Paginate the results (10 sheets per page)
    paginator = Paginator(character_sheets, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(
        request,
        'accounts/dashboard.html',
        {
            'page_obj': page_obj,
            'sort_by': sort_by,
            'filter_class': filter_class,
            'filter_level': filter_level,
        }
    )






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
        # Required Field
        name = request.POST.get('name', 'Unnamed Character')
        
        # Optional Fields with Default Values
        class_name = request.POST.get('class_name', '')
        level = int(request.POST.get('level', 1) or 1)
        race = request.POST.get('race', '')
        alignment = request.POST.get('alignment', '')
        
        hit_points = int(request.POST.get('hit_points', 10) or 10)
        armor_class = int(request.POST.get('armor_class', 10) or 10)
        initiative = int(request.POST.get('initiative', 0) or 0)
        speed = int(request.POST.get('speed', 30) or 30)
        
        strength = int(request.POST.get('strength', 10) or 10)
        dexterity = int(request.POST.get('dexterity', 10) or 10)
        constitution = int(request.POST.get('constitution', 10) or 10)
        intelligence = int(request.POST.get('intelligence', 10) or 10)
        wisdom = int(request.POST.get('wisdom', 10) or 10)
        charisma = int(request.POST.get('charisma', 10) or 10)
        
        primary_attack_name = request.POST.get('primary_attack_name', '')
        primary_attack_type = request.POST.get('primary_attack_type', '')
        primary_attack_damage = request.POST.get('primary_attack_damage', '')
        primary_attack_damage_type = request.POST.get('primary_attack_damage_type', '')
        
        # Create Character Sheet
        sheet = CharacterSheet.objects.create(
            user=request.user,
            name=name,
            class_name=class_name,
            level=level,
            race=race,
            alignment=alignment,
            hit_points=hit_points,
            armor_class=armor_class,
            initiative=initiative,
            speed=speed,
            strength=strength,
            dexterity=dexterity,
            constitution=constitution,
            intelligence=intelligence,
            wisdom=wisdom,
            charisma=charisma,
            primary_attack_name=primary_attack_name,
            primary_attack_type=primary_attack_type,
            primary_attack_damage=primary_attack_damage,
            primary_attack_damage_type=primary_attack_damage_type
        )
        
        # Automatically evaluate 'finished' status
        sheet.save()
        
        messages.success(request, "Character sheet created successfully!")
        return redirect('character_list')
    
    return render(request, 'accounts/character_form.html')
    


# Edit Character Sheet
def character_edit(request, sheet_id):
    sheet = get_object_or_404(CharacterSheet, id=sheet_id, user=request.user)
    
    if request.method == 'POST':
        # Required Field
        sheet.name = request.POST.get('name', sheet.name)
        
        # Optional Fields
        sheet.class_name = request.POST.get('class_name', sheet.class_name)
        sheet.level = int(request.POST.get('level', sheet.level) or sheet.level)
        sheet.race = request.POST.get('race', sheet.race)
        sheet.alignment = request.POST.get('alignment', sheet.alignment)
        
        sheet.hit_points = int(request.POST.get('hit_points', sheet.hit_points) or sheet.hit_points)
        sheet.armor_class = int(request.POST.get('armor_class', sheet.armor_class) or sheet.armor_class)
        sheet.initiative = int(request.POST.get('initiative', sheet.initiative) or sheet.initiative)
        sheet.speed = int(request.POST.get('speed', sheet.speed) or sheet.speed)
        
        sheet.strength = int(request.POST.get('strength', sheet.strength) or sheet.strength)
        sheet.dexterity = int(request.POST.get('dexterity', sheet.dexterity) or sheet.dexterity)
        sheet.constitution = int(request.POST.get('constitution', sheet.constitution) or sheet.constitution)
        sheet.intelligence = int(request.POST.get('intelligence', sheet.intelligence) or sheet.intelligence)
        sheet.wisdom = int(request.POST.get('wisdom', sheet.wisdom) or sheet.wisdom)
        sheet.charisma = int(request.POST.get('charisma', sheet.charisma) or sheet.charisma)
        
        sheet.primary_attack_name = request.POST.get('primary_attack_name', sheet.primary_attack_name)
        sheet.primary_attack_type = request.POST.get('primary_attack_type', sheet.primary_attack_type)
        sheet.primary_attack_damage = request.POST.get('primary_attack_damage', sheet.primary_attack_damage)
        sheet.primary_attack_damage_type = request.POST.get('primary_attack_damage_type', sheet.primary_attack_damage_type)
        
        # Automatically evaluate 'finished' status
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

@admin.register(CharacterSheet)
class CharacterSheetAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'level', 'finished')
    list_filter = ('finished',)



