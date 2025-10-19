# CSV Import Guide for TechFest Management System

## Overview
The TechFest Management System now supports bulk data import via CSV files. This feature allows administrators to quickly add multiple records at once instead of manually entering them one by one.

## Accessing CSV Import
1. Login as an admin/staff user
2. Navigate to the **CSV Import** section from:
   - The navigation menu (CSV Import link)
   - The dashboard homepage card

## Supported Data Types
You can import the following types of data:
- Departments
- Students
- Venues
- Events
- Registrations
- Winners
- Organizers

## CSV Format Requirements

### General Rules
- **First row** must contain column headers (exactly as shown below)
- Headers are **case-sensitive**
- Use **UTF-8** encoding for the CSV file
- Date format: **YYYY-MM-DD**
- Empty lines will be skipped
- Foreign key fields must reference existing records

### 1. Departments CSV Format
```csv
name,hod_name
Computer Science,Dr. Smith
Electronics,Dr. Johnson
Mechanical,Dr. Williams
```

**Fields:**
- `name`: Department name (required)
- `hod_name`: Head of Department name (required)

---

### 2. Students CSV Format
```csv
name,roll_number,email,department
John Doe,CS001,john@example.com,Computer Science
Jane Smith,CS002,jane@example.com,Electronics
Bob Wilson,ME001,bob@example.com,Mechanical
```

**Fields:**
- `name`: Student's full name (required)
- `roll_number`: Unique roll number (required, must be unique)
- `email`: Student's email address (required)
- `department`: Department name (required, must exist in database)

---

### 3. Venues CSV Format
```csv
name,location,capacity
Main Hall,Building A,500
Auditorium,Building B,1000
Conference Room,Building C,50
```

**Fields:**
- `name`: Venue name (required)
- `location`: Location description (required)
- `capacity`: Maximum capacity (required, must be a number)

---

### 4. Events CSV Format
```csv
title,description,date,venue,department
Coding Contest,Programming competition,2025-10-25,Main Hall,Computer Science
Robotics,Robot building event,2025-10-26,Auditorium,Electronics
Tech Talk,Industry expert talk,2025-10-27,,Computer Science
```

**Fields:**
- `title`: Event title (required)
- `description`: Event description (required)
- `date`: Event date in YYYY-MM-DD format (required)
- `venue`: Venue name (optional, must exist if provided)
- `department`: Department name (required, must exist)

**Note:** Leave venue empty (no space) if not assigned yet

---

### 5. Registrations CSV Format
```csv
student_roll_number,event_title
CS001,Coding Contest
CS002,Robotics
ME001,Tech Talk
```

**Fields:**
- `student_roll_number`: Student's roll number (required, must exist)
- `event_title`: Event title (required, must exist)

**Note:** Each student can only register once per event

---

### 6. Winners CSV Format
```csv
event_title,student_roll_number,position
Coding Contest,CS001,1
Coding Contest,CS002,2
Robotics,CS002,1
```

**Fields:**
- `event_title`: Event title (required, must exist)
- `student_roll_number`: Student's roll number (required, must exist)
- `position`: Winner position/rank (required, must be a number)

---

### 7. Organizers CSV Format
```csv
name,phone,event_title
Alice Brown,1234567890,Coding Contest
Bob Wilson,0987654321,Robotics
Carol Davis,5551234567,Tech Talk
```

**Fields:**
- `name`: Organizer's name (required)
- `phone`: Phone number (required)
- `event_title`: Event title (required, must exist)

---

## Import Process

1. **Prepare your CSV file** following the format above
2. **Navigate** to CSV Import page
3. **Select the data type** you want to import
4. **Review the format** requirements on the page
5. **Upload your CSV file**
6. **Review the results** - the system will show:
   - Number of successful imports
   - Any errors encountered
   - Details of the first few errors (if any)

## Error Handling

The import process will:
- **Skip rows** with errors and continue processing
- **Display error messages** for failed rows
- **Show line numbers** where errors occurred
- **Continue importing** valid rows even if some fail

Common errors:
- Missing required fields
- Referenced records don't exist (e.g., department name not found)
- Duplicate entries (e.g., same roll number)
- Invalid data types (e.g., text in a number field)
- Invalid date formats

## Best Practices

1. **Start with dependencies first:**
   - Import Departments before Students
   - Import Students and Venues before Events
   - Import Events before Registrations, Winners, and Organizers

2. **Test with small files first** (5-10 rows) to verify format

3. **Keep backups** of your original data

4. **Use the sample download** feature on each import page

5. **Check for duplicate data** before importing

6. **Verify foreign key values** exist (e.g., department names)

## Tips

- Use spreadsheet software (Excel, Google Sheets) to prepare CSV files
- Save as CSV UTF-8 format
- Remove any extra spaces before/after values
- Use consistent naming (exact matches for foreign keys)
- Don't include ID columns - they're auto-generated

## Troubleshooting

**Problem:** "Department not found"
- **Solution:** Make sure the department name exactly matches an existing department

**Problem:** "Duplicate roll number"
- **Solution:** Check for duplicate entries in your CSV or database

**Problem:** "Invalid date format"
- **Solution:** Use YYYY-MM-DD format (e.g., 2025-10-25)

**Problem:** "File is not CSV type"
- **Solution:** Ensure file extension is .csv and format is correct

---

## Contact Support

If you encounter issues not covered in this guide, please contact the system administrator.
