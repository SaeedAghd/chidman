from django.core.management.base import BaseCommand
from django.db import connection
from django.conf import settings

class Command(BaseCommand):
    help = 'Add authority column to Payment table if it does not exist'

    def handle(self, *args, **options):
        try:
            with connection.cursor() as cursor:
                # Check database engine
                db_engine = settings.DATABASES['default']['ENGINE']
                self.stdout.write(f"🔍 Database engine: {db_engine}")
                
                if 'postgresql' in db_engine.lower():
                    # PostgreSQL specific query
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
                            self.style.SUCCESS('✅ Authority column added successfully to PostgreSQL')
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING('⚠️ Authority column already exists in PostgreSQL')
                        )
                        
                elif 'sqlite' in db_engine.lower():
                    # SQLite specific query
                    cursor.execute("PRAGMA table_info(store_analysis_payment)")
                    columns = [row[1] for row in cursor.fetchall()]
                    
                    if 'authority' not in columns:
                        # Add authority column
                        cursor.execute("""
                            ALTER TABLE store_analysis_payment 
                            ADD COLUMN authority VARCHAR(100)
                        """)
                        self.stdout.write(
                            self.style.SUCCESS('✅ Authority column added successfully to SQLite')
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING('⚠️ Authority column already exists in SQLite')
                        )
                else:
                    self.stdout.write(
                        self.style.ERROR(f'❌ Unsupported database engine: {db_engine}')
                    )
                    
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error: {str(e)}')
            )
            import traceback
            self.stdout.write(traceback.format_exc())
