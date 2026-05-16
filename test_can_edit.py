import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'techfest.settings')
django.setup()

from django.contrib.auth.models import User
from festapp.views import can_edit

print("=" * 60)
print("TESTING can_edit() FUNCTION")
print("=" * 60)

# Test with srinivas (admin)
srinivas = User.objects.get(username='srinivas')
result_srinivas = can_edit(srinivas)
print(f"\n✓ can_edit(srinivas): {result_srinivas}")
print(f"  - is_superuser: {srinivas.is_superuser}")
print(f"  - is_staff: {srinivas.is_staff}")
print(f"  - groups: {list(srinivas.groups.values_list('name', flat=True))}")

# Test with generaluser
generaluser = User.objects.get(username='generaluser')
result_generaluser = can_edit(generaluser)
print(f"\n✓ can_edit(generaluser): {result_generaluser}")
print(f"  - is_superuser: {generaluser.is_superuser}")
print(f"  - is_staff: {generaluser.is_staff}")
print(f"  - groups: {list(generaluser.groups.values_list('name', flat=True))}")

if result_generaluser:
    print("\n✅ SUCCESS: generaluser can perform CRUD operations!")
else:
    print("\n❌ ERROR: generaluser cannot perform CRUD operations!")
    print("Debugging info:")
    print(f"  - Check if user is in GeneralUsers group...")
    group_check = generaluser.groups.filter(name='GeneralUsers').exists()
    print(f"  - In GeneralUsers group: {group_check}")
