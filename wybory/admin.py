from django.contrib import admin
from wybory.models import *

@admin.register(Osoba)
class OsobaAdmin(admin.ModelAdmin):
    list_display = ('imie', 'nazwisko', 'pesel')
    list_filter = ('imie','nazwisko')
    readonly_fields = ('pesel',)
    search_fields = ('imie', 'nazwisko')
    ordering = ('imie', 'nazwisko', 'pesel')


@admin.register(OsobaWybory)
class OsobaWyboryAdmin(admin.ModelAdmin):
    list_display = ('wyboryId', 'osobaId', 'czyOddalGlos', 'czyKandydat')
    list_filter = ('wyboryId', 'osobaId', 'czyOddalGlos', 'czyKandydat')
    search_fields = ('wyboryId', 'osobaId')
    ordering = ('wyboryId', 'osobaId')

@admin.register(Wybory)
class WyboryAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'maxKandydatow', 'poczatekWyborow', 'koniecWyborow')
    list_filter = ('nazwa', 'poczatekWyborow', 'koniecWyborow')
    search_fields = ('nazwa', 'poczatekWyborow', 'koniecWyborow')
    ordering = ('poczatekWyborow', 'koniecWyborow', 'nazwa', 'maxKandydatow')

@admin.register(Glos)
class GlosAdmin(admin.ModelAdmin):
    list_display = ('wyboryId', 'kandydatOsobaId')
    list_filter = ('wyboryId', 'kandydatOsobaId')
    search_fields = ('wyboryId', 'kandydatOsobaId')
    ordering = ('wyboryId', 'kandydatOsobaId')

#class MyUserAdmin(ModelAdmin):
    # list_display = (’username’, ’name’, ’account_type’, ’is_active’, ’number_of_vi3
    # list_filter = (’account_type’, ’research_groups’, ’is_active’)
    # fieldsets = (
    #                 (None, {’fields’: (’username’, ’password’,)}),
    #                 (_(’Personal data’), {’fields’: (’name’, ’date_of_birth’, ’email’,)}),
    #                 (_(’Permissions’), {’fields’: (’account_type’,’research_groups’,’is_active8 (_(’Login information’), {’fields’: (’last_login’,’number_of_visits’)}),
    # )
    # readonly_fields = (’last_login’,’number_of_visits’,)
    # search_fields = (’username’, ’name’,)
    # ordering = (’username’,)
    # filter_horizontal = ()
    #pass
