from django.contrib import admin
from .models import Planet, Sith, TestAssignment, Question

admin.site.register((Planet, Sith, TestAssignment, Question))
