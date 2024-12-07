from django.contrib import admin

from .models import Member, Organizer, Event, Order, Ticket, OrderItem

# Register your models here.
admin.site.register(Member)
admin.site.register(Organizer)
admin.site.register(Event)
admin.site.register(Order)
admin.site.register(Ticket)
admin.site.register(OrderItem)