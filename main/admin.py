from django.contrib import admin
from main.models import Products, Cart, Orders, Payment, Table, Reservation, Notifications


class OrdersAdmin(admin.ModelAdmin):
    list_display = ("user", 'product', 'count', 'total', 'delivered')


class TableAdmin(admin.ModelAdmin):
    list_display = ("id", 'seats', 'reserved')


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'table', 'date', 'time', )


admin.site.register(Products)
admin.site.register(Cart)
admin.site.register(Notifications)
admin.site.register(Orders, OrdersAdmin)
admin.site.register(Payment)
admin.site.register(Table, TableAdmin)
admin.site.register(Reservation, ReservationAdmin)


#------------------logics which should work on server
import datetime
from main.models import Reservation
reservations = Reservation.objects.all()
today = datetime.datetime.now()
for item in reservations:
    item_datetime = datetime.datetime(
    year=item.date.year,
    month=item.date.month,
    day=item.date.day,
    hour=item.time.hour,
    minute=item.time.minute,
    second=item.time.second,
)
    if today>item_datetime+datetime.timedelta(hours=1):
        table =Table.objects.get(id=item.table.id)
        table.reserved=False
        table.save()

notifications = Notifications.objects.all()
for n in notifications:
    if n.seen and today > n.date_created+datetime.timedelta(days=1):
        n.delete()

# orders = Orders.objects.all()
# if orders:
#     for o in orders:
#         if  o.delivered:
#             print(today,o.date_created)
#             if today > o.date_created+datetime.timedelta(seconds=20) :
#                 o.delete()
