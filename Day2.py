#Trial 
for i in range(5):
    print(f"Round number {i}")

#Printing Table using for loop 
num = int(input("Enter the number for the table: "))    #mujhe user se integer input me chahiye that's why int(input))
for i in range (1,21):                    
    print(f"{num} * {i} = {num*i}")
    
#Printing table using while loop
num =int ( input("Enter the no:"))
i = 10
while i>0:
    print(f"{num} * {i} = {num*i}")
    i=i-1
if i<=0:
    print("Blast off! 🚀")    