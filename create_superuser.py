import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'techfest.settings')
django.setup()

from django.contrib.auth.models import User

# Delete existing 'srinivas' user if it exists
User.objects.filter(username='srinivas').delete()

# Create new superuser
user = User.objects.create_superuser('srinivas', 'srinivas@techfest.com', 'srinivas')
print(f'✓ Superuser created: {user.username}')
print(f'✓ Email: {user.email}')
print(f'✓ Password: srinivas')
