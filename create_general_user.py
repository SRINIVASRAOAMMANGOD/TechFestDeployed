import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'techfest.settings')
django.setup()

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from festapp.models import Student, Department, Event, Organizer, Venue, Registration, Winner

# Create or get the group for general users
general_group, created = Group.objects.get_or_create(name='GeneralUsers')

# Define permissions that general users should have
# They can view (read) but cannot delete or change admin-created content
permissions_list = []

# Get ContentTypes for all models
for model in [Student, Department, Event, Organizer, Venue, Registration, Winner]:
    content_type = ContentType.objects.get_for_model(model)
    
    # Add view permission (they can see data)
    view_perm, _ = Permission.objects.get_or_create(
        codename=f'view_{model._meta.model_name}',
        name=f'Can view {model._meta.verbose_name}',
        content_type=content_type
    )
    permissions_list.append(view_perm)
    
    # Add add permission (they can create/add new records)
    add_perm, _ = Permission.objects.get_or_create(
        codename=f'add_{model._meta.model_name}',
        name=f'Can add {model._meta.verbose_name}',
        content_type=content_type
    )
    permissions_list.append(add_perm)
    
    # Add change permission (they can modify their own records)
    change_perm, _ = Permission.objects.get_or_create(
        codename=f'change_{model._meta.model_name}',
        name=f'Can change {model._meta.verbose_name}',
        content_type=content_type
    )
    permissions_list.append(change_perm)

# Assign all permissions to the group
general_group.permissions.set(permissions_list)

# Delete existing 'generaluser' if it exists
User.objects.filter(username='generaluser').delete()

# Create the general user
general_user = User.objects.create_user(
    username='generaluser',
    email='generaluser@techfest.com',
    password='generaluser'
)

# Add user to the GeneralUsers group
general_user.groups.add(general_group)

print('✓ User "generaluser" created successfully')
print(f'✓ Username: generaluser')
print(f'✓ Password: generaluser')
print(f'✓ Group: GeneralUsers')
print(f'✓ Permissions: View, Add, and Change (but NO delete)')
print(f'✓ Admin Access: DENIED (not staff user)')
