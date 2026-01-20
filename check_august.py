count = 0
with open('data/enrolment_merged_cleaned.csv', 'r') as f:
    header = f.readline()
    for line in f:
        if '-08-2025' in line:
            count += 1
            if count <= 5:
                print(f"Sample August record: {line.strip()}")

print(f"\nTotal August 2025 records found: {count}")

if count == 0:
    print("CONCLUSION: There is NO DATA for August 2025 in the source file.")
else:
    print(f"CONCLUSION: Found {count} records for August 2025.")
