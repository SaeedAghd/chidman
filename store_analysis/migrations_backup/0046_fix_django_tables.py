from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('store_analysis', '0045_add_ai_insights_safe'),
    ]

    operations = [
        # ایجاد جدول django_session اگر وجود ندارد
        migrations.RunSQL(
            """
            CREATE TABLE IF NOT EXISTS django_session (
                session_key varchar(40) NOT NULL PRIMARY KEY,
                session_data text NOT NULL,
                expire_date datetime NOT NULL
            );
            """,
            reverse_sql="DROP TABLE IF EXISTS django_session;"
        ),
        
        # ایجاد ایندکس برای django_session
        migrations.RunSQL(
            """
            CREATE INDEX IF NOT EXISTS django_session_expire_date 
            ON django_session (expire_date);
            """,
            reverse_sql="DROP INDEX IF EXISTS django_session_expire_date;"
        ),
        
        # ایجاد جدول django_migrations اگر وجود ندارد
        migrations.RunSQL(
            """
            CREATE TABLE IF NOT EXISTS django_migrations (
                id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                app varchar(255) NOT NULL,
                name varchar(255) NOT NULL,
                applied datetime NOT NULL
            );
            """,
            reverse_sql="DROP TABLE IF EXISTS django_migrations;"
        ),
        
        # ایجاد جدول django_content_type اگر وجود ندارد
        migrations.RunSQL(
            """
            CREATE TABLE IF NOT EXISTS django_content_type (
                id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                app_label varchar(100) NOT NULL,
                model varchar(100) NOT NULL,
                UNIQUE (app_label, model)
            );
            """,
            reverse_sql="DROP TABLE IF EXISTS django_content_type;"
        ),
        
        # ایجاد جدول django_admin_log اگر وجود ندارد
        migrations.RunSQL(
            """
            CREATE TABLE IF NOT EXISTS django_admin_log (
                id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                action_time datetime NOT NULL,
                object_id text,
                object_repr varchar(200) NOT NULL,
                action_flag smallint unsigned NOT NULL,
                change_message text NOT NULL,
                content_type_id integer,
                user_id integer NOT NULL,
                FOREIGN KEY (content_type_id) REFERENCES django_content_type (id),
                FOREIGN KEY (user_id) REFERENCES auth_user (id)
            );
            """,
            reverse_sql="DROP TABLE IF EXISTS django_admin_log;"
        ),
    ]