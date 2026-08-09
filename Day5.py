# Define a function 
def greet():
    print("Hello! 👋")
    print("Welcome to automation!")
# Call the function 
greet()

# Function with a parameter (machine ko input dena)
def greet(name):
    print(f"Hello {name}! 👋")

greet("Vanshika")
greet("Priya")


# Function that returns a value
def add(a, b):
    result = a + b
    return result

total = add(5, 3)
print(f"Total: {total}")

# print vs return gotcha
def add_print(a, b):
    print(a + b)      # sirf screen par dikhata hai

def add_return(a, b):
    return a + b      # value wapas deta hai

x = add_print(1, 1)
y = add_return(1, 1)
print(f"x = {x}, y = {y}")


def calculate_bill(amount, discount):
    final = int(amount - (amount * discount / 100))
    return final

bill1 = calculate_bill(1000, 10)
bill2 = calculate_bill(5000, 20)

print(f"Bill 1: ₹{bill1}")
print(f"Bill 2: ₹{bill2}")
