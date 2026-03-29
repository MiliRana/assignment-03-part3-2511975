# part3_api_files.py
# Assignment Part 3: File I/O, APIs & Exception Handling

import requests
from datetime import datetime

# --------------------------------------------------
# TASK 4 LOGGER FUNCTION (used throughout program)
# --------------------------------------------------
def log_error(source, error_type, message):
    with open("error_log.txt", "a", encoding="utf-8") as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] ERROR in {source}: {error_type} — {message}\n")


# --------------------------------------------------
# TASK 1 — FILE WRITE & APPEND
# --------------------------------------------------
notes = [
    "Topic 1: Variables store data. Python is dynamically typed.",
    "Topic 2: Lists are ordered and mutable.",
    "Topic 3: Dictionaries store key-value pairs.",
    "Topic 4: Loops automate repetitive tasks.",
    "Topic 5: Exception handling prevents crashes."
]

# Write file
with open("python_notes.txt", "w", encoding="utf-8") as file:
    for note in notes:
        file.write(note + "\n")

print("File written successfully.")

# Append file
with open("python_notes.txt", "a", encoding="utf-8") as file:
    file.write("Topic 6: Functions help reuse code.\n")
    file.write("Topic 7: APIs allow communication between systems.\n")

print("Lines appended.")


# --------------------------------------------------
# TASK 1 — READ FILE
# --------------------------------------------------
print("\n--- Reading File ---")
line_count = 0

with open("python_notes.txt", "r", encoding="utf-8") as file:
    for i, line in enumerate(file, start=1):
        print(f"{i}. {line.strip()}")
        line_count += 1

print("Total number of lines:", line_count)

# Keyword search
keyword = input("Enter a keyword to search in notes: ")

found = False
with open("python_notes.txt", "r", encoding="utf-8") as file:
    for line in file:
        if keyword.lower() in line.lower():
            print(line.strip())
            found = True

if not found:
    print("No matching lines found.")


# --------------------------------------------------
# TASK 3A — SAFE DIVIDE
# --------------------------------------------------
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except TypeError:
        return "Error: Invalid input types"


print("\n--- Safe Divide Tests ---")
print(safe_divide(10, 2))
print(safe_divide(10, 0))
print(safe_divide("ten", 2))


# --------------------------------------------------
# TASK 3B — SAFE FILE READER
# --------------------------------------------------
def read_file_safe(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    finally:
        print("File operation attempt complete.")


print("\n--- Safe File Reader ---")
print(read_file_safe("python_notes.txt"))
print(read_file_safe("ghost_file.txt"))


# --------------------------------------------------
# TASK 2 — API CALLS WITH EXCEPTION HANDLING
# --------------------------------------------------
print("\n--- Fetching Products ---")
url = "https://dummyjson.com/products?limit=20"

try:
    response = requests.get(url, timeout=5)
    data = response.json()
    products = data["products"]

    print("ID | Title | Category | Price | Rating")
    for p in products:
        print(f"{p['id']} | {p['title']} | {p['category']} | ${p['price']} | {p['rating']}")

except requests.exceptions.ConnectionError:
    print("Connection failed. Please check your internet.")
    log_error("fetch_products", "ConnectionError", "No connection")
except requests.exceptions.Timeout:
    print("Request timed out. Try again later.")
    log_error("fetch_products", "Timeout", "Request timed out")
except Exception as e:
    print(e)
    log_error("fetch_products", "Exception", str(e))


# --------------------------------------------------
# FILTER AND SORT
# --------------------------------------------------
print("\n--- Filtered Products (Rating >= 4.5) ---")
filtered = [p for p in products if p['rating'] >= 4.5]
sorted_products = sorted(filtered, key=lambda x: x['price'], reverse=True)

for p in sorted_products:
    print(p['title'], "-", p['price'], "-", p['rating'])


# --------------------------------------------------
# CATEGORY SEARCH
# --------------------------------------------------
print("\n--- Laptops Category ---")
try:
    response = requests.get("https://dummyjson.com/products/category/laptops", timeout=5)
    laptops = response.json()["products"]

    for laptop in laptops:
        print(laptop["title"], "-", laptop["price"])

except Exception as e:
    print(e)
    log_error("category_search", "Exception", str(e))


# --------------------------------------------------
# POST REQUEST
# --------------------------------------------------
print("\n--- POST Request ---")
new_product = {
    "title": "My Custom Product",
    "price": 999,
    "category": "electronics",
    "description": "A product I created via API"
}

try:
    response = requests.post("https://dummyjson.com/products/add", json=new_product, timeout=5)
    print(response.json())
except Exception as e:
    print(e)
    log_error("post_product", "Exception", str(e))


# --------------------------------------------------
# TASK 3D — INPUT VALIDATION LOOP
# --------------------------------------------------
while True:
    user_input = input("\nEnter product ID (1–100) or 'quit': ")

    if user_input.lower() == "quit":
        break

    if not user_input.isdigit():
        print("Invalid input. Enter a number.")
        continue

    product_id = int(user_input)

    if product_id < 1 or product_id > 100:
        print("ID must be between 1 and 100.")
        continue

    try:
        response = requests.get(f"https://dummyjson.com/products/{product_id}", timeout=5)

        if response.status_code == 404:
            print("Product not found.")
            log_error("lookup_product", "HTTPError", f"404 Not Found for product ID {product_id}")
        else:
            product = response.json()
            print(product["title"], "-", product["price"])

    except Exception as e:
        print(e)
        log_error("lookup_product", "Exception", str(e))


# --------------------------------------------------
# TASK 4 — FORCE ERRORS FOR LOGGING
# --------------------------------------------------
print("\n--- Triggering Logging Errors ---")

try:
    requests.get("https://this-host-does-not-exist-xyz.com/api", timeout=5)
except Exception as e:
    log_error("test_connection", "ConnectionError", str(e))

# Trigger 404
response = requests.get("https://dummyjson.com/products/999")
if response.status_code != 200:
    log_error("lookup_product", "HTTPError", "404 Not Found for product ID 999")


# --------------------------------------------------
# PRINT ERROR LOG FILE
# --------------------------------------------------
print("\n--- Error Log Contents ---")
try:
    with open("error_log.txt", "r", encoding="utf-8") as file:
        print(file.read())
except FileNotFoundError:
    print("No log file found.")