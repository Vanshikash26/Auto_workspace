fruits = ["apple", "mango", "banana", "orange"]

print(fruits)
print(fruits[0])
print(fruits[-1])
print(len(fruits))

fruits.append("grapes")
print(f"After appending: {fruits}")

fruits.remove("banana")
print(f"After Removing: {fruits}")

print(f"{len(fruits)}")

products = ["laptop", "phone", "tablet", "watch"]

for item in products:
    print(f"Available: {item}")

# Product ki saari details ek dict mein
product = {
    "name": "iPhone 15",
    "price": 79999,
    "in_stock": True
}

# f-string se sundar print (bahar double quote ", andar single quote ')
print(f"Product: {product['name']}")
print(f"Price: ₹{product['price']}")

# If-Else se stock check
if product["in_stock"] == True:
    print("Stock mein hai ✅")
else:
    print("Out of stock ❌") 


# Create a list with 5 products
products = ["Laptop", "Phone", "Tablet", "Watch", "Earbuds"]

# Loop through the list and print each product
for item in products:
    print(f"Available product: {item}")

# Ask the user for a new product name
new_product = input("Naya product batao: ")

# Add the new product to the end of the list
products.append(new_product)

# Loop again to show all products including the new one
for item in products:
    print(f"Ab available: {item}")

# Create a dictionary with one product's details
product = {
    "name": "iPhone 15",
    "price": 79999,
    "in_stock": True
}

# Print the product name from the dictionary
print(f"Product: {product['name']}")

# Print the product price from the dictionary
print(f"Price: ₹{product['price']}")

# Check if the product is in stock using if-else
if product["in_stock"] == True:
    print("Stock mein hai ✅")
else:
    print("Out of stock ❌")         
