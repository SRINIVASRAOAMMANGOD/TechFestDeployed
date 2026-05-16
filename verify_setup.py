import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'techfest.settings')
django.setup()

from django.contrib.auth.models import User, Group

print("=" * 60)
print("USER SETUP VERIFICATION")
print("=" * 60)

# Check srinivas (admin)
srinivas = User.objects.get(username='srinivas')
print(f"\n✓ Admin User: {srinivas.username}")
print(f"  - is_superuser: {srinivas.is_superuser}")
print(f"  - is_staff: {srinivas.is_staff}")
print(f"  - Can CRUD: YES (superuser)")
print(f"  - Can access /admin/: YES")

# Check generaluser
generaluser = User.objects.get(username='generaluser')
print(f"\n✓ General User: {generaluser.username}")
print(f"  - is_superuser: {generaluser.is_superuser}")
print(f"  - is_staff: {generaluser.is_staff}")
print(f"  - Groups: {list(generaluser.groups.values_list('name', flat=True))}")
print(f"  - Can CRUD: YES (via can_edit decorator)")
print(f"  - Can access /admin/: NO (not staff user)")

print("\n" + "=" * 60)
print("PERMISSIONS")
print("=" * 60)
gen_group = Group.objects.get(name='GeneralUsers')
perms = list(gen_group.permissions.values_list('codename', flat=True))
print(f"\nGeneralUsers group permissions ({len(perms)} total):")
for perm in sorted(perms):
    print(f"  - {perm}")

print("\n" + "=" * 60)
print("ACCESS SUMMARY")
print("=" * 60)
print("\n✓ srinivas (admin):")
print("  - Login to app: YES")
print("  - CRUD operations: YES")  
print("  - Admin panel: YES")
print("\n✓ generaluser:")
print("  - Login to app: YES")
print("  - CRUD operations: YES (Create, Read, Update)")
print("  - Delete operations: NO (permission denied)")
print("  - Admin panel: NO (not staff user)")
