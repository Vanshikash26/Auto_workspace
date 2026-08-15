# Import the library we just installed using pip
import pyfiglet

# Ask user for a text
text = input("Koi text likho jise bada banana hai: ")

# Generate the big ASCII art using pyfiglet
banner = pyfiglet.figlet_format(text)

# Print the big banner
print("\n" + banner)
print("Terminal's magic! ✨")