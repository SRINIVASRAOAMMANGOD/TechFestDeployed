# Step-by-Step Tutorial: Using CSV Import Feature

## Part 1: Accessing the Feature

### Step 1: Login
1. Open your browser and go to `http://127.0.0.1:8000/`
2. Click "Login" button in the top right
3. Enter your admin/staff username and password
4. Click "Login"

### Step 2: Navigate to CSV Import
**Option A:** Via Navigation Menu
- Look at the top navigation bar
- Click on "CSV Import" link (icon: 📥)

**Option B:** Via Dashboard
- From the homepage, scroll down
- Find the "CSV Import" card
- Click on it

## Part 2: Importing Your First Dataset

### Example: Importing Departments

**Step 1: Choose Data Type**
- On the CSV Import page, you'll see cards for each data type
- Click "Import Departments" button

**Step 2: Review Format Requirements**
- Left side: File upload form
- Right side: Format requirements and example
- Read the required fields: `name`, `hod_name`
- See the example format displayed

**Step 3: Download Sample (Optional)**
- Click "Download Sample" button
- Open the downloaded file to see the format
- You can use this as a template

**Step 4: Prepare Your CSV**
Create a file named `departments.csv` with this content:
```
name,hod_name
Computer Science,Dr. Rajesh Kumar
Electronics,Dr. Priya Sharma
Mechanical,Dr. Anil Verma
```

**Step 5: Upload the File**
- Click "Choose File" button
- Select your `departments.csv` file
- File name will appear next to the button
- Click "Upload and Import" button

**Step 6: Review Results**
- Green success message: "Successfully imported X departments"
- If there are errors, yellow warning messages will show
- You'll be redirected to the Departments list page
- Verify your imported data is there

## Part 3: Importing Related Data

### Importing Students (Requires Departments)

**Step 1: Create CSV**
File: `students.csv`
```
name,roll_number,email,department
John Doe,CS001,john@example.com,Computer Science
Jane Smith,EC001,jane@example.com,Electronics
```

**Important:** 
- Department names must EXACTLY match existing departments
- Roll numbers must be unique

**Step 2: Import**
1. Go to CSV Import → Import Students
2. Upload `students.csv`
3. Click "Upload and Import"
4. Check the results

### Importing Events (Requires Departments + Venues)

**First, import venues:**
File: `venues.csv`
```
name,location,capacity
Main Hall,Building A,500
Lab 1,Building B,50
```

**Then, import events:**
File: `events.csv`
```
title,description,date,venue,department
Tech Talk,AI Workshop,2025-11-15,Main Hall,Computer Science
Robot Wars,Robotics Competition,2025-11-20,Lab 1,Electronics
```

**Note:** Date must be in YYYY-MM-DD format!

## Part 4: Using Sample Files (Quick Test)

### Easy Way - Use Provided Samples

**Step 1: Locate Sample Files**
- Open folder: `csv_samples/`
- You'll see 7 sample CSV files

**Step 2: Import in Order**
1. Import `sample_departments.csv`
2. Import `sample_venues.csv`
3. Import `sample_students.csv`
4. Import `sample_events.csv`
5. Import `sample_registrations.csv`
6. Import `sample_winners.csv`
7. Import `sample_organizers.csv`

**Step 3: Verify**
- Go to each list page (Departments, Students, etc.)
- Verify the sample data is there

## Part 5: Creating CSV in Excel/Google Sheets

### Using Microsoft Excel

**Step 1: Create Spreadsheet**
1. Open Excel
2. First row: Enter column headers (e.g., `name`, `hod_name`)
3. Following rows: Enter your data

**Step 2: Save as CSV**
1. File → Save As
2. Choose file type: "CSV UTF-8 (Comma delimited) (*.csv)"
3. Name your file
4. Click Save

### Using Google Sheets

**Step 1: Create Spreadsheet**
1. Open Google Sheets
2. First row: Enter column headers
3. Following rows: Enter your data

**Step 2: Download as CSV**
1. File → Download → Comma Separated Values (.csv)
2. File will download to your computer

## Part 6: Troubleshooting Common Issues

### Issue 1: "Department not found"

**Problem:** Student CSV has department "computer science" but database has "Computer Science"

**Solution:** 
- Check exact spelling and capitalization
- Go to Departments list page
- Copy the exact department name
- Use that in your CSV

### Issue 2: "Duplicate roll number"

**Problem:** Trying to import student with roll number that already exists

**Solution:**
- Check your CSV for duplicate roll numbers
- Or check if student already exists in database
- Use unique roll numbers

### Issue 3: "Invalid date format"

**Problem:** Date is in format 15-11-2025 or 11/15/2025

**Solution:**
- Use YYYY-MM-DD format
- Example: 2025-11-15
- Year first, then month, then day

### Issue 4: Some rows fail, some succeed

**This is normal!**
- The system processes each row individually
- Failed rows are skipped
- Successful rows are imported
- Fix errors in your CSV and re-upload failed rows

## Part 7: Best Practices

### 1. Always Import Dependencies First
✅ Correct order:
1. Departments & Venues (no dependencies)
2. Students & Events (need Departments)
3. Registrations, Winners, Organizers (need Students/Events)

### 2. Start Small
- Test with 2-3 rows first
- Verify import works
- Then import full dataset

### 3. Keep Backups
- Save original CSV files
- Use Export feature to backup database

### 4. Verify After Import
- Always check the list pages
- Verify data looks correct
- Check all foreign key relationships

### 5. Use Consistent Naming
- Same capitalization
- Same spelling
- No extra spaces

## Part 8: Advanced Tips

### Handling Large Datasets
- Break into smaller files (100-200 rows each)
- Import in batches
- Monitor for errors after each batch

### Updating Existing Data
- Current version creates new records only
- To update: Export → Modify → Delete old → Import new

### Using Templates
1. Download sample from import page
2. Keep first row (headers) unchanged
3. Replace data rows with your data
4. Save and import

### Checking Before Import
- Open CSV in text editor
- Verify commas are correct
- Check for extra blank lines
- Ensure UTF-8 encoding

## Part 9: Real-World Example

### Scenario: Importing 50 Students for Tech Fest

**Step 1: Plan**
- Ensure all departments exist
- Collect student information
- Prepare Excel sheet

**Step 2: Create Excel File**
| name | roll_number | email | department |
|------|-------------|-------|------------|
| Arjun Kumar | CS2021001 | arjun@example.com | Computer Science |
| Priya Singh | EC2021001 | priya@example.com | Electronics |
| ... (48 more rows) |

**Step 3: Save as CSV**
- File → Save As → CSV UTF-8
- Name: `students_batch1.csv`

**Step 4: Import**
- CSV Import → Import Students
- Upload file
- Review results: "Successfully imported 50 students"

**Step 5: Verify**
- Go to Students list page
- Search for a few students
- Confirm data is correct

**Done!** 50 students imported in minutes instead of manual entry taking hours!

## Part 10: Quick Reference Commands

### File Preparation Checklist
□ First row has column headers
□ Headers match required format exactly
□ No extra blank rows
□ Dates in YYYY-MM-DD format
□ Foreign key values exist in database
□ No duplicate unique fields
□ File saved as .csv
□ UTF-8 encoding

### Import Order Checklist
□ 1. Departments
□ 2. Venues
□ 3. Students
□ 4. Events
□ 5. Registrations
□ 6. Winners
□ 7. Organizers

### After Import Checklist
□ Check success message
□ Review any error messages
□ Verify data in list pages
□ Test relationships (e.g., students have correct departments)
□ Keep CSV file as backup

---

## Summary

You've learned how to:
✅ Access the CSV import feature
✅ Prepare CSV files correctly
✅ Import different types of data
✅ Handle errors and troubleshooting
✅ Use best practices for successful imports

**Time Saved:** What used to take hours of manual entry now takes minutes with CSV import!

**Questions?** Refer to:
- CSV_IMPORT_README.md (Quick guide)
- CSV_IMPORT_GUIDE.md (Detailed documentation)
- QUICK_REFERENCE.txt (One-page cheat sheet)

Happy importing! 🎉
