'''num = int(input("Number batao: "))
print(f"Tumne {num} kaha")'''

"""try:
    num = int(input("Number batao: "))
    print(f"Tumne {num} kaha")
except ValueError:
    print("Arre, ye number nahi hai! 😅")"""


'''try:
    a = int(input("Pehla number: "))
    b = int(input("Dusra number: "))
    result = a / b
    print(f"Result: {result}")
except ValueError:
    print("Number hi number likho! 😅")
except ZeroDivisionError:
    print("Zero se divide nahi kar sakte! 🚫")'''


'''try:
    x = 10 / 2
except ZeroDivisionError:
    print("Error!")
finally:
    print("Ye line hamesha chalegi ✅") 
'''

# mini project 
while True:
    try:
        a = int(input("Pehla number: "))
        b = int(input("Dusra number: "))
        result = a / b
        print(f"Result: {result}")
        break
    except ValueError:
        print("Sahi number likho! 😅")
    except ZeroDivisionError:
        print("Zero se divide nahi! 🚫")

