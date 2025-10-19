# CSV Import Feature - Quick Start Guide

## What's New? 🎉

The TechFest Management System now supports **bulk data import via CSV files**! You can now import hundreds of records at once instead of entering them manually.

## Quick Access

1. **Login** as admin/staff
2. Click **"CSV Import"** in the navigation menu
3. Choose the data type to import
4. Upload your CSV file

## Supported Data Types

✅ Departments  
✅ Students  
✅ Venues  
✅ Events  
✅ Registrations  
✅ Winners  
✅ Organizers  

## Sample CSV Files

Ready-to-use sample CSV files are available in the `csv_samples/` folder:

- `sample_departments.csv` - Sample departments
- `sample_students.csv` - Sample students with departments
- `sample_venues.csv` - Sample event venues
- `sample_events.csv` - Sample events
- `sample_registrations.csv` - Sample registrations
- `sample_winners.csv` - Sample winners
- `sample_organizers.csv` - Sample organizers

## Import Order (Important!)

Import in this order to avoid errors:

1. **Departments** (no dependencies)
2. **Venues** (no dependencies)
3. **Students** (requires Departments)
4. **Events** (requires Departments and Venues)
5. **Registrations** (requires Students and Events)
6. **Winners** (requires Students and Events)
7. **Organizers** (requires Events)

## Testing the Feature

### Option 1: Use Sample Files
```bash
# The sample files in csv_samples/ are ready to use
# Import them in the order listed above
```

### Option 2: Create Your Own CSV
Each import page shows:
- Required CSV format
- Example data
- Download sample template button

## Features

✨ **Smart Error Handling** - Skips bad rows, continues with good ones  
✨ **Detailed Feedback** - Shows success count and error details  
✨ **Sample Downloads** - Download template from each import page  
✨ **Format Validation** - Clear error messages for format issues  
✨ **Foreign Key Support** - Reference existing records by name/ID  

## CSV Format Requirements

### Quick Reference

| Data Type | Required Columns | Notes |
|-----------|------------------|-------|
| Department | `name`, `hod_name` | - |
| Student | `name`, `roll_number`, `email`, `department` | Department must exist |
| Venue | `name`, `location`, `capacity` | Capacity = number |
| Event | `title`, `description`, `date`, `venue`, `department` | Date: YYYY-MM-DD |
| Registration | `student_roll_number`, `event_title` | Both must exist |
| Winner | `event_title`, `student_roll_number`, `position` | Position = number |
| Organizer | `name`, `phone`, `event_title` | Event must exist |

## Example: Importing Departments

1. Navigate to **CSV Import** → **Import Departments**
2. Use this CSV content:

```csv
name,hod_name
Computer Science,Dr. Smith
Electronics,Dr. Johnson
```

3. Save as `departments.csv`
4. Upload and click **"Upload and Import"**
5. See success message!

## Common Issues & Solutions

**❌ "Department not found"**  
→ Import departments first, use exact names

**❌ "Duplicate roll number"**  
→ Check for duplicates in CSV or database

**❌ "Invalid date format"**  
→ Use YYYY-MM-DD (e.g., 2025-11-15)

**❌ "File is not CSV type"**  
→ Save as CSV format from Excel/Google Sheets

## Tips for Success

1. ✅ Use the provided sample files as templates
2. ✅ Import dependencies first (e.g., departments before students)
3. ✅ Test with small files (5-10 rows) first
4. ✅ Use spreadsheet software to prepare CSV files
5. ✅ Save as "CSV UTF-8" format

## Full Documentation

For complete CSV format specifications and troubleshooting, see:
📄 **[CSV_IMPORT_GUIDE.md](CSV_IMPORT_GUIDE.md)**

## Benefits

⚡ **Fast** - Import 100+ records in seconds  
🎯 **Accurate** - Reduce manual entry errors  
📊 **Efficient** - Bulk operations save time  
🔄 **Flexible** - Update existing data easily  

---

**Need Help?** Check the detailed guide or contact the administrator.
