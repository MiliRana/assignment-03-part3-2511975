# Assignment 3 – Part 3
# File I/O, APIs & Exception Handling
# Name: Mili Rana
# Student ID: 2511975

# requests is used to get all api's
# datetime is used to get the current date and time
import requests
from datetime import datetime


# error logging
# writing errors into a file so we can check later
def log_error(where, err_type, msg):
    with open("error_log.txt", "a", encoding="utf-8") as f:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{now}] ERROR in {where}: {err_type} — {msg}\n")


# =========================================================
# Task 1 — File Read & Write Basics
# =========================================================

# writing notes 
notes = [
    "Topic 1: Variables store data. Python is dynamically typed.",
    "Topic 2: Lists are ordered and mutable.",
    "Topic 3: Dictionaries store key-value pairs.",
    "Topic 4: Loops automate repetitive tasks.",
    "Topic 5: Exception handling prevents crashes."
]

# first writing fresh file
with open("python_notes.txt", "w", encoding="utf-8") as f:
    for line in notes:
        f.write(line + "\n")

print("File written successfully.")

# adding a couple more topics
with open("python_notes.txt", "a", encoding="utf-8") as f:
    f.write("Topic 6: Functions help reuse code.\n")
    f.write("Topic 7: APIs allow communication between systems.\n")

print("Lines appended.")


#  reading the file 
print("\nReading file...\n")

line_count = 0

with open("python_notes.txt", "r", encoding="utf-8") as f:
    for i, line in enumerate(f, start=1):
        print(f"{i}. {line.strip()}")
        line_count += 1

print("Total number of lines:", line_count)

# searching keyword (case insensitive)
key = input("Enter a keyword to search in notes: ")

found = False
with open("python_notes.txt", "r", encoding="utf-8") as f:
    for line in f:
        if key.lower() in line.lower():
            print(line.strip())
            found = True

if not found:
    print("No matching lines found.")



# =========================================================
# Task 3- Exception Handling
# =========================================================

# safe drive
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except TypeError:
        return "Error: Invalid input types"


print("\nTesting divide function...")
print(safe_divide(10, 2))
print(safe_divide(10, 0))
print(safe_divide("ten", 2))


# safe file read 
def read_file_safe(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    finally:
        # this should run no matter what
        print("File operation attempt complete.")


print("\nTrying file reader...")
print(read_file_safe("python_notes.txt"))
print(read_file_safe("ghost_file.txt"))



# =========================================================
# Task 2- API Integration
# =========================================================

# API part 
print("\nGetting product data...")

url = "https://dummyjson.com/products?limit=20"

try:
    r = requests.get(url, timeout=5)
    data = r.json()

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


# filter + sort 
print("\nHigh rated products (>= 4.5):")

# filtering
good = [p for p in products if p['rating'] >= 4.5]

# sorting by price descending
good_sorted = sorted(good, key=lambda x: x['price'], reverse=True)

for p in good_sorted:
    print(p['title'], "-", p['price'], "-", p['rating'])


# category search 
print("\nChecking laptops category...")

try:
    r = requests.get("https://dummyjson.com/products/category/laptops", timeout=5)
    laptops = r.json()["products"]

    for l in laptops:
        print(l["title"], "-", l["price"])

except Exception as e:
    print(e)
    log_error("category_search", "Exception", str(e))


# POST request 
print("\nSending POST request...")

new_product = {
    "title": "My Custom Product",
    "price": 999,
    "category": "electronics",
    "description": "A product I created via API"
}

try:
    r = requests.post("https://dummyjson.com/products/add", json=new_product, timeout=5)
    print(r.json())
except Exception as e:
    print(e)
    log_error("post_product", "Exception", str(e))



# =========================================================
# Task 3 — Exception Handling
# =========================================================

# input loop 
while True:
    user_input = input("\nEnter product ID (1–100) or 'quit': ")

    if user_input.lower() == "quit":
        break

    if not user_input.isdigit():
        print("Invalid input. Enter a number.")
        continue

    pid = int(user_input)

    if pid < 1 or pid > 100:
        print("ID must be between 1 and 100.")
        continue

    try:
        r = requests.get(f"https://dummyjson.com/products/{pid}", timeout=5)

        if r.status_code == 404:
            print("Product not found.")
            log_error("lookup_product", "HTTPError", f"404 Not Found for product ID {pid}")
        else:
            item = r.json()
            print(item["title"], "-", item["price"])

    except Exception as e:
        print(e)
        log_error("lookup_product", "Exception", str(e))



# =========================================================
# Task 4 — Logging to File
# =========================================================

# forcing errors 
print("\nTriggering errors for logging...")

# fake bad URL
try:
    requests.get("https://this-host-does-not-exist-xyz.com/api", timeout=5)
except Exception as e:
    log_error("test_connection", "ConnectionError", str(e))

# manual 404
r = requests.get("https://dummyjson.com/products/999")
if r.status_code != 200:
    log_error("lookup_product", "HTTPError", "404 Not Found for product ID 999")


# show logs 
print("\nReading log file...\n")

try:
    with open("error_log.txt", "r", encoding="utf-8") as f:
        print(f.read())
except FileNotFoundError:
    print("No log file found.")
    
