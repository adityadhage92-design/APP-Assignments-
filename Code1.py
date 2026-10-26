# Code1.py - File Handling: Count Lines and Copy First Two Lines

# Create input file with sample data
with open("input.txt", "w") as f:
    f.write("Hello Python\\n")
    f.write("Welcome to APP\\n")
    f.write("File Handling\\n")
    f.write("Python Programming\\n")

# Read the file and count lines
with open("input.txt", "r") as f:
    lines = f.readlines()

print("Total number of lines:", len(lines))

# Copy first two lines to output.txt
with open("output.txt", "w") as f:
    f.writelines(lines[:2])

print("First two lines copied successfully")
