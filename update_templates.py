import os
import glob

# Find all html files in templates directory
template_files = glob.glob('festapp/templates/festapp/*.html')

# Template tag to load custom filters
load_tag = "{% load custom_filters %}"

for file_path in template_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        with open(file_path, 'r', encoding='latin-1') as f:
            content = f.read()
    
    # Skip if already has the load tag
    if 'load custom_filters' in content:
        print(f'⏭️  Skipped (already updated): {file_path}')
        continue
    
    # Check if file has {% extends
    if '{% extends' in content:
        # Add load tag after first {% extends line
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if '{% extends' in line:
                # Insert after this line
                lines.insert(i+1, load_tag)
                break
        content = '\n'.join(lines)
    
    # Replace all user.is_staff with user|can_edit
    content = content.replace('user.is_staff', 'user|can_edit')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'✓ Updated: {file_path}')

print('\n✅ All templates updated!')
