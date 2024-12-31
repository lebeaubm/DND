from django.contrib import admin
from .models import BasicMonster

@admin.register(BasicMonster)
class BasicMonsterAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'challenge_rating')  # Adjust fields as needed
    list_filter = ('type', 'challenge_rating')  # Add filters for convenience
    search_fields = ('name', 'type')  # Enable search by name and type
    actions = ['delete_selected_basic_monsters']

   











