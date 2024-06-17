import os
from datetime import datetime

# Input number denoting the leetcode weekly contest number
contest = input("Enter the Leetcode weekly contest number: ")

# Generate file path
default_path = "./content/leetcode/"
if not os.path.exists(default_path):
    os.makedirs(default_path)

filename = f"weekly-{contest}.md"
filepath = os.path.join(default_path, filename)

# Get the current date and time
now = datetime.now()
current_date = now.strftime("%Y-%m-%d %H:%M")
current_year_month = now.strftime("%Y-%m")

# Get the script's directory
script_dir = os.path.dirname(__file__)

# Read the template file
template_path = os.path.join(script_dir, "leetcode_template.md")
with open(template_path, "r") as template_file:
    template_content = template_file.read()

# Replace placeholders with actual values
content = template_content.format(
    contest=contest,
    current_date=current_date,
    current_year_month=current_year_month
)

# Write the content to the markdown file
with open(filepath, "w") as file:
    file.write(content)

print(f"Markdown file created at {filepath}")
