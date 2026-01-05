from django.contrib import admin
from django.contrib.sessions.models import Session
import pprint

class SessionAdmin(admin.ModelAdmin):
    # Wyświetlaj klucz sesji, datę wygaśnięcia i co jest w środku
    list_display = ['session_key', 'expire_date', 'get_decoded_data']
    
    # Funkcja pomocnicza, żeby odkodować "krzaczki" i pokazać czytelne dane
    def get_decoded_data(self, obj):
        data = obj.get_decoded()
        # Wyświetlamy tylko to, co nas interesuje (żeby było czytelnie)
        return pprint.pformat(data)
    
    get_decoded_data.short_description = "Zawartość sesji (Zdekodowana)"

# Rejestrujemy model Sesji w panelu
admin.site.register(Session, SessionAdmin)