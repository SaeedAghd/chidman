from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Add authority column to Payment table if it does not exist'

    def handle(self, *args, **options):
        try:
            with connection.cursor() as cursor:
                # Check if authority column exists
                cursor.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name='store_analysis_payment' 
                    AND column_name='authority'
                """)
                
                if not cursor.fetchone():
                    # Add authority column
                    cursor.execute("""
                        ALTER TABLE store_analysis_payment 
                        ADD COLUMN authority VARCHAR(100) NULL
                    """)
                    self.stdout.write(
                        self.style.SUCCESS('✅ Authority column added successfully')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING('⚠️ Authority column already exists')
                    )
                    
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error: {str(e)}')
            )
