from django.db import models
from django.contrib.auth.models import User

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member', null=True, blank=True)
    fname = models.CharField(max_length=50, null=True)
    lname = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=15, null=True)
    m_email = models.EmailField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    passwd = models.CharField(max_length=50) 

    def __str__(self):
        return self.fname + ' ' + self.lname

class Organizer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='organizer', null=True, blank=True)
    fname = models.CharField(max_length=50, null=True)
    lname = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=15, null=True)
    o_email = models.EmailField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    passwd = models.CharField(max_length=50)

    def __str__(self):
        return self.fname + ' ' + self.lname
    
class Event(models.Model):
    image = models.ImageField(default='bg.jpeg',upload_to='event_images/', blank=True)
    date_time = models.DateTimeField()
    title = models.CharField(max_length=50, null=True)
    location = models.CharField(max_length=50, null=True)
    description = models.TextField(blank=True)
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE, related_name='events')

    def __str__(self):
        return f"{self.title} ({self.organizer})"


class Ticket(models.Model):
    TYPE = (
        ('Early Bird', 'Early Bird'),
        ('Regular', 'Regular'),
        ('VIP', 'VIP'),
        ('Gate Ticket', 'Gate Ticket'),
        ('Group of 3', 'Group of 3'),
        ('Group of 5', 'Group of 5'),
    )
    
    name = models.CharField(max_length=50, null=True, choices=TYPE)
    price = models.FloatField(null=True)
    qavailable = models.PositiveIntegerField(verbose_name="Quantity Available")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')

    def reduce_quantity(self, quantity):
        """Reduce the quantity of tickets available."""
        if quantity > self.qavailable:
            raise ValueError("Not enough tickets available")
        self.qavailable -= quantity
        self.save()
        
        
    def __str__(self):
        return f"{self.name} - {self.event.title} (${self.price})"

class Order(models.Model):
    member = models.ForeignKey(Member, null=True, on_delete=models.SET_NULL, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return f"Order by {self.member.fname} {self.member.lname} on {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        """Override save to check ticket availability and reduce quantity."""
        if self.pk is None:  # Only validate on creation
            if self.quantity > self.ticket.qavailable:
                raise ValueError("Not enough tickets available")
            self.ticket.reduce_quantity(self.quantity)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.quantity} x {self.ticket.name} ({self.ticket.event.title})"