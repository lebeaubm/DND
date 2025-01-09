from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CharacterSheet
from django.core.paginator import Paginator
from django.db.models import Q  # For filtering
from django.contrib import admin
from .models import Monster
from .utils.text_parser import parse_text_to_monster
from .models import CharacterSheet, BasicMonster, Monster
from combat.combat_engine import Entity, run_combat
from django.http import JsonResponse


# Signup View
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "accounts/signup.html", {"form": form})


# Login View
def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "accounts/login.html")


# Logout View
def user_logout(request):
    logout(request)
    return redirect("login")


@login_required
def dashboard(request):
    # Get query parameters for sorting and filtering
    sort_by = request.GET.get(
        "sort", "created_at"
    )  # Default to sorting by creation date
    filter_class = request.GET.get("class", "")  # Filter by class name
    filter_level = request.GET.get("level", "")  # Filter by level

    # Start with the user's character sheets
    character_sheets = CharacterSheet.objects.filter(user=request.user)

    # Apply filtering
    if filter_class:
        character_sheets = character_sheets.filter(class_name__icontains=filter_class)
    if filter_level:
        character_sheets = character_sheets.filter(level=filter_level)

    # Apply sorting
    if sort_by in ["name", "level", "created_at"]:
        character_sheets = character_sheets.order_by(sort_by)

    # Paginate the results (10 sheets per page)
    paginator = Paginator(character_sheets, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "accounts/dashboard.html",
        {
            "page_obj": page_obj,
            "sort_by": sort_by,
            "filter_class": filter_class,
            "filter_level": filter_level,
        },
    )


# List Character Sheets
@login_required
def character_list(request):
    sheets = CharacterSheet.objects.filter(user=request.user)
    return render(request, "accounts/character_list.html", {"sheets": sheets})


# Create Character Sheet
@login_required
def character_create(request):
    if request.method == "POST":
        # Required Field
        name = request.POST.get("name", "Unnamed Character")

        # Optional Fields with Default Values
        class_name = request.POST.get("class_name", "")
        level = int(request.POST.get("level", 1) or 1)
        race = request.POST.get("race", "")
        alignment = request.POST.get("alignment", "")

        hit_points = int(request.POST.get("hit_points", 10) or 10)
        armor_class = int(request.POST.get("armor_class", 10) or 10)
        initiative = int(request.POST.get("initiative", 0) or 0)
        speed = int(request.POST.get("speed", 30) or 30)

        strength = int(request.POST.get("strength", 10) or 10)
        dexterity = int(request.POST.get("dexterity", 10) or 10)
        constitution = int(request.POST.get("constitution", 10) or 10)
        intelligence = int(request.POST.get("intelligence", 10) or 10)
        wisdom = int(request.POST.get("wisdom", 10) or 10)
        charisma = int(request.POST.get("charisma", 10) or 10)

        primary_attack_name = request.POST.get("primary_attack_name", "")
        primary_attack_type = request.POST.get("primary_attack_type", "")
        primary_attack_damage = request.POST.get("primary_attack_damage", "")
        primary_attack_damage_type = request.POST.get("primary_attack_damage_type", "")

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
            primary_attack_damage_type=primary_attack_damage_type,
        )

        # Automatically evaluate 'finished' status
        sheet.save()

        messages.success(request, "Character sheet created successfully!")
        return redirect("character_list")

    return render(request, "accounts/character_form.html")


# Edit Character Sheet
def character_edit(request, sheet_id):
    sheet = get_object_or_404(CharacterSheet, id=sheet_id, user=request.user)

    if request.method == "POST":
        # Required Field
        sheet.name = request.POST.get("name", sheet.name)

        # Optional Fields
        sheet.class_name = request.POST.get("class_name", sheet.class_name)
        sheet.level = int(request.POST.get("level", sheet.level) or sheet.level)
        sheet.race = request.POST.get("race", sheet.race)
        sheet.alignment = request.POST.get("alignment", sheet.alignment)

        sheet.hit_points = int(
            request.POST.get("hit_points", sheet.hit_points) or sheet.hit_points
        )
        sheet.armor_class = int(
            request.POST.get("armor_class", sheet.armor_class) or sheet.armor_class
        )
        sheet.initiative = int(
            request.POST.get("initiative", sheet.initiative) or sheet.initiative
        )
        sheet.speed = int(request.POST.get("speed", sheet.speed) or sheet.speed)

        sheet.strength = int(
            request.POST.get("strength", sheet.strength) or sheet.strength
        )
        sheet.dexterity = int(
            request.POST.get("dexterity", sheet.dexterity) or sheet.dexterity
        )
        sheet.constitution = int(
            request.POST.get("constitution", sheet.constitution) or sheet.constitution
        )
        sheet.intelligence = int(
            request.POST.get("intelligence", sheet.intelligence) or sheet.intelligence
        )
        sheet.wisdom = int(request.POST.get("wisdom", sheet.wisdom) or sheet.wisdom)
        sheet.charisma = int(
            request.POST.get("charisma", sheet.charisma) or sheet.charisma
        )

        sheet.primary_attack_name = request.POST.get(
            "primary_attack_name", sheet.primary_attack_name
        )
        sheet.primary_attack_type = request.POST.get(
            "primary_attack_type", sheet.primary_attack_type
        )
        sheet.primary_attack_damage = request.POST.get(
            "primary_attack_damage", sheet.primary_attack_damage
        )
        sheet.primary_attack_damage_type = request.POST.get(
            "primary_attack_damage_type", sheet.primary_attack_damage_type
        )

        # Automatically evaluate 'finished' status
        sheet.save()

        messages.success(request, "Character sheet updated successfully!")
        return redirect("character_list")

    return render(request, "accounts/character_form.html", {"sheet": sheet})


# Delete Character Sheet
@login_required
def character_delete(request, sheet_id):
    sheet = get_object_or_404(CharacterSheet, id=sheet_id, user=request.user)
    sheet.delete()
    messages.success(request, "Character sheet deleted successfully!")
    return redirect("character_list")


@admin.register(CharacterSheet)
class CharacterSheetAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "level", "finished")
    list_filter = ("finished",)


@login_required
def upload_monster(request):
    if request.method == "POST":
        text = request.POST.get("monster_text")
        try:
            data = parse_text_to_monster(text)
            monster = Monster.objects.create(**data)
            messages.success(request, f"Monster '{monster.name}' created successfully!")
            return redirect("monster_list")
        except Exception as e:
            messages.error(request, f"Error: {e}")
    return render(request, "accounts/upload_monster.html")


@login_required
def create_monster(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if not name:
            messages.error(request, "Name is required to create a monster.")
            return redirect("create_monster")

        # Ensure numeric fields are correctly set
        armor_class = request.POST.get("armor_class") or None
        hit_points = request.POST.get("hit_points") or None
        strength = request.POST.get("strength") or None
        dexterity = request.POST.get("dexterity") or None
        constitution = request.POST.get("constitution") or None
        intelligence = request.POST.get("intelligence") or None
        wisdom = request.POST.get("wisdom") or None
        charisma = request.POST.get("charisma") or None

        monster = Monster.objects.create(
            name=name,
            armor_class=armor_class,
            hit_points=hit_points,
            strength=strength,
            dexterity=dexterity,
            constitution=constitution,
            intelligence=intelligence,
            wisdom=wisdom,
            charisma=charisma,
        )

        messages.success(request, f"Monster '{monster.name}' created successfully!")
        return redirect("monster_list")

    return render(request, "accounts/create_monster.html")


@login_required
def monster_list(request):
    """
    Display a list of all uploaded monsters.
    """
    monsters = Monster.objects.all()
    return render(request, "accounts/monster_list.html", {"monsters": monsters})


@login_required
def edit_monster(request, monster_id):
    monster = get_object_or_404(Monster, id=monster_id)

    if request.method == "POST":
        monster.name = request.POST.get("name", monster.name)
        monster.size = request.POST.get("size", monster.size)
        monster.type = request.POST.get("type", monster.type)
        monster.alignment = request.POST.get("alignment", monster.alignment)

        # Safely handle numeric fields
        monster.armor_class = int(request.POST.get("armor_class") or 0)
        monster.hit_points = int(request.POST.get("hit_points") or 0)
        monster.strength = int(request.POST.get("strength") or 0)
        monster.dexterity = int(request.POST.get("dexterity") or 0)
        monster.constitution = int(request.POST.get("constitution") or 0)
        monster.intelligence = int(request.POST.get("intelligence") or 0)
        monster.wisdom = int(request.POST.get("wisdom") or 0)
        monster.charisma = int(request.POST.get("charisma") or 0)

        # Text fields
        monster.speed = request.POST.get("speed", monster.speed)
        monster.saving_throws = request.POST.get("saving_throws", monster.saving_throws)
        monster.damage_resistances = request.POST.get(
            "damage_resistances", monster.damage_resistances
        )
        monster.damage_immunities = request.POST.get(
            "damage_immunities", monster.damage_immunities
        )
        monster.condition_immunities = request.POST.get(
            "condition_immunities", monster.condition_immunities
        )
        monster.senses = request.POST.get("senses", monster.senses)
        monster.languages = request.POST.get("languages", monster.languages)
        monster.challenge_rating = request.POST.get(
            "challenge_rating", monster.challenge_rating
        )
        monster.abilities = request.POST.get("abilities", monster.abilities)
        monster.actions = request.POST.get("actions", monster.actions)
        monster.reactions = request.POST.get("reactions", monster.reactions)

        monster.save()
        messages.success(request, f"Monster '{monster.name}' updated successfully!")
        return redirect("monster_list")

    return render(request, "accounts/edit_monster.html", {"monster": monster})


def monster_detail(request, monster_id):
    monster = get_object_or_404(Monster, id=monster_id)
    return render(request, "accounts/monster_detail.html", {"monster": monster})


def basic_monster_list(request):
    search_query = request.GET.get("q", "")
    sort_by = request.GET.get("sort", "name")
    page_number = request.GET.get("page", 1)

    monsters = BasicMonster.objects.all()

    # Search functionality
    if search_query:
        monsters = monsters.filter(
            Q(name__icontains=search_query)
            | Q(type__icontains=search_query)
            | Q(challenge_rating__icontains=search_query)
        )

    # Sorting functionality
    valid_sort_fields = ["name", "type", "challenge_rating"]
    if sort_by in valid_sort_fields:
        monsters = monsters.order_by(sort_by)

    # Pagination functionality
    paginator = Paginator(monsters, 10)  # Show 10 monsters per page
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "accounts/basic_monster_list.html",
        {
            "page_obj": page_obj,
            "search_query": search_query,
            "sort_by": sort_by,
        },
    )


def basic_monster_detail(request, monster_id):
    monster = get_object_or_404(BasicMonster, id=monster_id)
    return render(request, "accounts/basic_monster_detail.html", {"monster": monster})





# def combat_setup(request):
#     characters = CharacterSheet.objects.all()
#     monsters = Monster.objects.all()
#     basic_monsters = BasicMonster.objects.all()
    
#     context = {
#         'characters': characters,
#         'monsters': monsters,
#         'basic_monsters': basic_monsters
#     }
#     return render(request, 'accounts/combat_setup.html', context)

def combat_setup(request):
    characters = CharacterSheet.objects.all()
    monsters = Monster.objects.all()
    basic_monsters = BasicMonster.objects.all()
    return render(
        request, 
        'accounts/combat_setup.html', 
        {
            'characters': characters,
            'monsters': monsters,
            'basic_monsters': basic_monsters
        }
    )




def simulate_combat(request):
    if request.method == 'POST':
        team_a_ids = request.POST.getlist('team_a_combatants')
        team_b_ids = request.POST.getlist('team_b_combatants')

        team_a = [Entity.from_db_object(BasicMonster.objects.get(id=int(id.split('_')[1]))) for id in team_a_ids]
        team_b = [Entity.from_db_object(BasicMonster.objects.get(id=int(id.split('_')[1]))) for id in team_b_ids]

        # Run the combat simulation
        result = run_combat(team_a, team_b)

        # Ensure unpacking matches the return values from run_combat
        if isinstance(result, tuple) and len(result) == 2:
            winner, combat_log = result
        else:
            raise ValueError("run_combat must return exactly two values: winner and combat_log")

        return render(request, 'accounts/combat_result.html', {
            'winner': winner,
            'combat_log': combat_log
        })