import csv
from django.core.management.base import BaseCommand
from fleet.models import Car

class Command(BaseCommand):
    help = 'Import cars from a CSV file'

    def handle(self, *args, **kwargs):
        file_path = 'cars.csv'
        
        try:
            with open(file_path, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Changed number_plate to plate_number to match your model
                    # Changed price_per_day to daily_rate to match your model
                    Car.objects.get_or_create(
                        plate_number=row['number_plate'],
                        defaults={
                            'name': row['name'],
                            'brand': row['brand'],
                            'daily_rate': row['price_per_day'], 
                            'is_available': row['is_available'].lower() == 'true'
                        }
                    )
            self.stdout.write(self.style.SUCCESS('Successfully imported cars!'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('cars.csv not found in root directory'))