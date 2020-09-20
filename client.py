"""
Initialization of Client
"""
import asyncio

ISSUED = ''
def start():
    """
    this function is responsibale for taking choice for login and register
    """
    print('******* File management System by Pioneers *******')
    while True:
        print('1 : Login ')
        print('2 : Register ')
        choice = input('Enter Choice(1,2): ')
        if choice == '1':
            result = login()
            return result
        elif choice == '2':
            result = register()
            return result
        print('Invalid Input ')

def process(message):
    """
    messages that need to be sent to the server are filtered
    for client commands.
    """
    split_message = message.split(' ', 1)
    command = split_message[0]
    count_arguments = len(split_message)
    global ISSUED
    if command == 'commands':
        if count_arguments == 1:
            c_file = open('commands.txt', 'r')
            content = c_file.read()
            print(content)
            return False
        elif count_arguments == 2:
            argument = split_message[1]
            if argument == 'issued':
                print(ISSUED)
                return False
            elif argument == 'clear':
                ISSUED = ''
                print('Cleared')
                return False
            print('Invalid command')
            return False
        print('invalid arguments')
        return False
    ISSUED += str('\n'+message)
    return True

def login():
    """
    this functions inputs login credential and combines them into an argument
    """
    print('**** Login *****')
    user_name = input('User Name : ')
    password = input('Password : ')
    result = str(f'login {user_name} {password}')
    return result

def register():
    """
    this functions inputs registeration details and combines them into an argument
    """
    print('**** Register *****')
    user_name = input('Create User Name : ')
    password = input('Create Password : ')
    prevelige = input('Enter prevelage(admin/user) : ')
    if prevelige == 'admin' or prevelige == 'user':
        result = str(f'register {user_name} {password} {prevelige}')
        return result
    return 'invalid'

async def tcp_echo_client():
    """
    this functions initilases connection with the server
    """
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 8080)
    message = ''

    while True:
        request = start()
        writer.write(request.encode())
        data = await reader.read(10000)
        message = data.decode()
        if message == 'successful':
            print('Login Successful ')
            break
        elif message == 'Created':
            print('New user Created')
            break
        elif message == 'exist':
            print('User Already Exist ')
            print('Try again with new Username')
            continue
        elif message == 'failed':
            print('Login Failed ')
            print('Try Again')
            continue
        elif message == 'invalid':
            print('invalid input ')
            continue
        elif message == 'loggedin':
            print('user is already loggedin from another client')
            continue
        else:
            print('Error has Occured, Please Try Again ')
            continue

    while True:
        message = input('pioneers.py>')

        if message == 'quit':
            writer.write(message.encode())
            break
        elif message == '':
            continue
        reply = process(message)
        if reply:
            writer.write(message.encode())
            data = await reader.read(10000)
            print(f'{data.decode()}')
    print('Close the connection')
    writer.close()

try:
    asyncio.run(tcp_echo_client())
except ConnectionRefusedError:
    print('Failed to connect to the server')