#!/usr/bin/env python3
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MZtailors.settings')
django.setup()

from tailors.models import Statistics

def create_statistics():
    # Check if statistics already exist
    if Statistics.objects.exists():
        print("Statistics already exist. Updating...")
        stats = Statistics.objects.first()
        stats.happy_customers = 2500
        stats.years_experience = 25
        stats.expert_tailors = 50
        stats.satisfaction_rate = 99
        stats.is_active = True
        stats.save()
        print("Statistics updated successfully!")
    else:
        # Create new statistics
        stats = Statistics.objects.create(
            happy_customers=2500,
            years_experience=25,
            expert_tailors=50,
            satisfaction_rate=99,
            is_active=True
        )
        print("Statistics created successfully!")
    
    print(f"Current stats: {stats.happy_customers} customers, {stats.years_experience} years, {stats.expert_tailors} tailors, {stats.satisfaction_rate}% satisfaction")

if __name__ == '__main__':
    create_statistics()