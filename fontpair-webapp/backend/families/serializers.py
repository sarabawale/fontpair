from rest_framework import serializers
from .models import *

class FamilySerializer(serializers.ModelSerializer):
  class Meta:
    model = Family
    fields = ('name', 'url')