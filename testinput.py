def printwhattheysay():
    print(input())
for i in range(4):
    name = input("Enter your name: ")
    if name == "":
        print("fake")
    if len(name) > 6:
        print("this name was too long")
    if len(name) > 0 and name[0] == "h":
        print('names beggining with h')
printwhattheysay()
