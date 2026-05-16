import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'techfest.settings')
django.setup()

from django.contrib.auth.models import User, Group

print("=" * 60)
print("SETTING UP USER ACCOUNTS FOR RENDER PRODUCTION")
print("=" * 60)

# Create srinivas (admin)
try:
    User.objects.filter(username='srinivas').delete()
    srinivas = User.objects.create_superuser('srinivas', 'srinivas@techfest.com', 'srinivas')
    print(f"\n✅ Admin user created: srinivas")
except Exception as e:
    print(f"\n❌ Error creating admin user: {e}")

# Create GeneralUsers group
try:
    gen_group, created = Group.objects.get_or_create(name='GeneralUsers')
    
    from django.contrib.contenttypes.models import ContentType
    from django.contrib.auth.models import Permission
    from festapp.models import Student, Department, Event, Organizer, Venue, Registration, Winner
    
    permissions_list = []
    for model in [Student, Department, Event, Organizer, Venue, Registration, Winner]:
        content_type = ContentType.objects.get_for_model(model)
        
        view_perm, _ = Permission.objects.get_or_create(
            codename=f'view_{model._meta.model_name}',
            name=f'Can view {model._meta.verbose_name}',
            content_type=content_type
        )
        permissions_list.append(view_perm)
        
        add_perm, _ = Permission.objects.get_or_create(
            codename=f'add_{model._meta.model_name}',
            name=f'Can add {model._meta.verbose_name}',
            content_type=content_type
        )
        permissions_list.append(add_perm)
        
        change_perm, _ = Permission.objects.get_or_create(
            codename=f'change_{model._meta.model_name}',
            name=f'Can change {model._meta.verbose_name}',
            content_type=content_type
        )
        permissions_list.append(change_perm)
    
    gen_group.permissions.set(permissions_list)
    print(f"✅ GeneralUsers group configured with {len(permissions_list)} permissions")
except Exception as e:
    print(f"❌ Error setting up group: {e}")

# Create generaluser
try:
    User.objects.filter(username='generaluser').delete()
    generaluser = User.objects.create_user(
        username='generaluser',
        email='generaluser@techfest.com',
        password='generaluser'
    )
    generaluser.groups.add(gen_group)
    print(f"✅ General user created: generaluser")
except Exception as e:
    print(f"❌ Error creating general user: {e}")

print("\n" + "=" * 60)
print("USER SETUP COMPLETE")
print("=" * 60)
print("\nCredentials:")
print("  Admin: srinivas / srinivas (Full access including admin panel)")
print("  User:  generaluser / generaluser (CRUD operations only)")
print("\n✅ Ready for production on Render!")
