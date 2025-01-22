import os
def registraciya():
    file = open('User.txt','a', encoding = 'ANSI')
    user = input('Введи имя, фамилию и группу')
    user=user+'\n'
    file.write(user)
    file.close()
def printUser():
    file = open('User.txt','r', encoding = 'ANSI')
    for user in file:
        print(user,end='')
def udalenie():
    old = open('User.txt','r', encoding = 'ANSI')
    new = open('tmp.txt', 'x', encoding = 'ANSI')
    user = input('Кого удалить')
    for i in old:
        if user not in i:
            new.write(i)
            
    old.close()
    new.close()
    os.remove('User.txt')
    os.rename('tmp.txt','User.txt')
    print('Пользователь удален')
def foundUser():
    lol = open('User.txt','r', encoding = 'ANSI')
    user = input('Кого найти')
    
    
    
    
