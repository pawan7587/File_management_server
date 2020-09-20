"""reads Requests from the server and handles method calls
"""
import os
from server_logic import Adminservices
from server_logic import Userservices

class Server:
    """
    File management for server
    Attributes:
    --------------
        username : string
            stores username
        password : string
            stores password
        root_directory : string
            stores root directory location
        current_directory : string
            stores current working directory
        message : string
            stores the message from the client
        privilege : string
            stores whether the privileges are for admin or a user
    Methods:
    --------------
        __init__(self):
            Initialises all the attributes

        getpassword(self, user_name):
            Passwords for both admin and user

        check(self, given_username, given_password, user, password):
            checks whether username and password are matched with the previous database

        initilise(self):
            Initialises user according to the privileges.If client is
            admin it initialises admin services.If client is user
            it initialises user services.

        login(self, split_message):
            Initialises login for the client
            if successfull:returns 'successfull'
            else: returns 'failure'

        register(self, user_name, password, privilage):
            Initialises registeration for clients

        create_folder(self, user_name, privilage):
            Creating a folder

        create_user_log(self, directory, user_name):
            Creating a user log

        create_admin_log(self, directory)
            login for admin

        modify_file(self, directory, file_name, input1)
            modifying the file

        find(self, user_name, privilage):
            checks whether the user is already registered or not
            if it exists then returns exist or else it returns ok

        start_register(self):
            Checks if registeration request is valid

        split(self, message):
        splits the message from the client into several parts and stores into a list and
        initialises the analysis

        analize(self, split_message):
        Analyses all the requests from the client and calls the file handling methods
         """

    def __init__(self):
        """Initialises all the attributes

        """
        self.username = ''
        self.password = ''
        self.root_directory = os.getcwd()
        self.current_directory = ''
        self.message = ''
        self.privilege = ''

    def getpassword(self, user_name):
        """passwords for both admin and user
            parameters:
                user_name : string
                    stores the username
        """
        admin_log = 'adminlog.txt'
        admin_file = open(admin_log, 'r')
        admin_file_lines = admin_file.readlines()
        admin_line_count = sum(1 for line in open('adminlog.txt'))
        admin_numbers = []
        admin_names = []
        admin_pass = []
        for i in range(admin_line_count):
            file = admin_file_lines[i].strip()
            find = file.find(",")
            admin_numbers.append(find)
            admin_names.append(file[:admin_numbers[i]])
            admin_pass.append(file[admin_numbers[i]+1:])
        for j in range(len(admin_names)):
            if user_name == admin_names[j]:
                out = str(f'{admin_names[j]} {admin_pass[j]} admin')
                return out
        user_log = 'userlog.txt'
        user_file = open(user_log, 'r')
        user_file_lines = user_file.readlines()
        user_line_count = sum(1 for line in open('userlog.txt'))
        user_numbers = []
        user_names = []
        user_pass = []
        for i in range(user_line_count):
            file = user_file_lines[i].strip()
            find = file.find(",")
            user_numbers.append(find)
            user_names.append(file[:user_numbers[i]])
            user_pass.append(file[user_numbers[i]+1:])
        for j in range(0, len(user_names)):
            if user_name == user_names[j]:
                uout = str(f'{user_names[j]} {user_pass[j]} user')
                return uout
        uout = 'failed'
        return uout

    def check(self, given_username, given_password, user, password):
        """checks whether username and password are matched with the previous database
            parameters :
                given_username : string
                    username which is given by the client
                given_password : sting
                    password given by the client
                user : string
                    username which is already stored
                password : string
                    password with respect to their username which is stored previously
        """
        if given_username == user:
            if given_password == password:
                return 'successful'
        return 'failed'

    def initilise(self):
        """Initialises user according to the privileges.If client is
           admin it initialises admin services.If client is user
           it initialises user services.
        """
        if self.privilege == 'admin':
            self.client = Adminservices(
                self.root_directory,
                self.current_directory,
                self.username,
                self.password
            )
        elif self.privilege == 'user':
            self.client = Userservices(
                self.root_directory,
                self.current_directory,
                self.username,
                self.password
            )
    def checklog(self, username):
        """
        checks if the username is already logged in from
        another client
            Parameters:
                username : string
                    stores the users name

        """
        log_file = 'loginlog.txt'
        with open(log_file) as f_r:
            if username in f_r.read():
                return True
        return False

    def login(self, split_message):
        """Initialises login for the client
            if successfull:returns 'successfull'
            else: returns 'failure'
            Parameters:
                split_message : string
                    splits the message
        """
        username = split_message[1]
        if self.checklog(username):
            return 'loggedin'
        password = split_message[2]
        reply = self.getpassword(username)
        split_message_reply = reply.split(' ', 2)  #list
        given_username = split_message_reply[0]
        if given_username == 'failed':
            return 'failed'

        given_password = split_message_reply[1]
        privilege = split_message_reply[2]
        check_reply = self.check(given_username, given_password, username, password)
        if check_reply == 'successful':
            #cwd = str(f'{self.root_directory}\\{username}')
            cwd = os.path.join(self.root_directory, username)
            self.current_directory = cwd
            self.username = username
            self.password = password
            self.privilege = privilege
            self.initilise()
            self.modify_file(self.root_directory, 'loginlog.txt', self.username)
            return 'successful'
        elif check_reply == 'failed':
            return 'failed'

    def register(self, user_name, password, privilage):
        """Initialises registeration for clients
            parameters:
                user_name : string
                    stores the user name
                password : string
                    stores the password
                privilage : string
                    stores whether the privileges are for admin or a user
        """
        if privilage == 'admin':
            file_name = str(f'{self.root_directory}\\adminlog.txt')
        elif privilage == 'user':
            file_name = str(f'{self.root_directory}\\userlog.txt')
        file = open(file_name, "a+")
        user_data = str(f'\n{user_name},{password}')
        file.writelines(user_data)
        file.close()
        self.create_folder(user_name, privilage)

    def create_folder(self, user_name, privilage):
        """
            Creating a folder
            Parameters:
                user_name : string
                    stores the username
                privilage : string
                    stores whether the privileges are for admin or a user
        """
        path = os.path.join(self.root_directory, user_name)
        os.mkdir(path)
        if privilage == 'admin':
            self.create_admin_log(path)
        else:
            self.create_user_log(path, user_name)

    def create_user_log(self, directory, user_name):
        """Creating a user log
            Parameters:
                directory : string
                    stores the directory
                user_name : string
                    returns the username
        """
        file_name = str(f'{directory}\\log.txt')
        file = open(file_name, "w")
        data = user_name
        user_data = [data, "\n"]
        file.writelines(user_data)
        file.close()
        self.create_admin_log(directory)

    def create_admin_log(self, directory):
        """
        login for admin
        Parameters:
            directory : string
                stores the directory
        """
        path = self.root_directory #admin directory
        file_name = str(f'{path}\\adminlog.txt')
        open_file = open(file_name, 'r')
        file_lines = open_file.readlines()
        num_lines = sum(1 for line in open('adminlog.txt'))
        i = 0
        numbers = []
        names = []
        for i in range(num_lines):
            file = file_lines[i].strip()
            find = file.find(",")
            numbers.append(find)
            names.append(file[:numbers[i]])
        for i in names:
            self.modify_file(directory, 'log.txt', i)

    def modify_file(self, directory, file_name, input1):
        """modifying the file
            parameters:
                directory : string
                    stores the directory
                file_name : string
                    stores the filename
                input1 : string
                    stores the userdata
        """
        file_name = str(f'{directory}\\{file_name}')
        input1 = input1
        file = open(file_name, 'a+')
        user_data = [input1, "\n"]
        file.writelines(user_data)
        file.close()

    def find(self, user_name, privilage):
        """checks whether the user is already registered or not
           if it exists then returns exist or else it returns ok
           parameters:
                user_name : string
                    stores the username
                privilage : string
                    stores whether the privileges are for admin or a user
        """
        try:
            if privilage == 'admin':
                log_name = 'adminlog.txt'
            else:
                log_name = 'userlog.txt'
            file_name = str(f'{self.root_directory}\\{log_name}')
            open_file = open(file_name, 'r')
            file_lines = open_file.readlines()
            num_lines = sum(1 for line in open(file_name, 'r'))
            i = 0
            numbers = []
            names = []
            for i in range(num_lines):
                file = file_lines[i].strip()
                find = file.find(",")
                numbers.append(find)
                names.append(file[:numbers[i]])
            if user_name in names:
                return 'exist'
            return 'ok'
        except:
            return 'error occured'

    def start_register(self):
        """Checks if registeration request is valid
        """
        split_message = self.message.split(' ', 3)
        username = split_message[1]
        password = split_message[2]
        privilage = split_message[3]
        reply = self.find(username, privilage)
        if reply == 'exist':
            return reply
        self.register(username, password, privilage)
        split_message = ['login', username, password]
        reply = self.login(split_message)
        return reply

    def analize(self, split_message):
        """Analyses all the requests from the client and calls the file handling methods
            Parameters :
                split_message : list(str, str, str)
                    stores arguments in a form of list
        """
        command = split_message[0]
        if self.username == '':
            if command == 'login':
                try:
                    reply = self.login(split_message)
                    assert reply is not None
                except AssertionError:
                    reply = 'Something went wrong'
                except:
                    reply = 'error occurred'
                return reply
            elif command == 'register':
                try:
                    reply = self.start_register()
                    assert reply is not None
                except AssertionError:
                    reply = 'Something went wrong'
                except:
                    reply = 'error occurred'
                return reply
            return 'failed'
        else:
            if command == 'list':
                try:
                    reply = self.client.list_files()
                    assert reply is not None
                except AssertionError:
                    reply = 'Something went wrong'  
                except:
                    reply = 'error occured'
                return reply

            elif command == 'change_folder':
                try:
                    argument_1 = split_message[1]
                    reply = self.client.change_directory(argument_1, self.privilege)
                    assert reply is not None
                except AssertionError:
                    reply = 'Something went wrong'
                except:
                    reply = 'Failed'
                return reply

            elif command == 'read_file':
                try:
                    argument_1 = split_message[1]
                    reply = self.client.start_read(argument_1)
                    assert reply is not None
                except AssertionError:
                    reply = 'Something went wrong'
                except IndexError:
                    reply = self.client.start_read(None)
                except:
                    reply = 'error occured'
                return reply

            elif command == 'write_file':
                try:
                    argument_1 = split_message[1]
                except IndexError:
                    reply = 'invalid Argument'
                    return reply
                try:
                    argument_2 = split_message[2]
                    reply = self.client.write_file(argument_1, argument_2)
                    assert reply is not None
                except IndexError:
                    reply = self.client.write_file(argument_1)
                    assert reply is not None
                except AssertionError:
                    reply = 'Something went wrong'
                except:
                    reply = 'error occured'
                return reply

            elif command == 'create_folder':
                try:
                    argument_1 = split_message[1]
                    reply = self.client.create_folder(argument_1, self.privilege)
                    assert reply is not None
                except AssertionError:
                    reply = 'Something went wrong'
                except:
                    reply = 'error occured'
                return reply
            elif command == 'delete':
                try:
                    argument_1 = split_message[1]
                    argument_2 = split_message[2]
                    get_privilage = self.getpassword(argument_1)
                    split_message_reply = get_privilage.split(' ', 2)
                    given_username = split_message_reply[0]
                    if given_username == 'failed':
                        return 'Username doesnot exist'
                    user_privilege = split_message_reply[2]
                    reply = self.client.delete_user(argument_1, argument_2, user_privilege)
                    assert reply is not None
                except AssertionError:
                    reply = 'Something went wrong'
                except AttributeError:
                    reply = 'You are not authorised for this service'
                except:
                    reply = 'error occured'
                return reply
            else:
                return 'Invalid input'

    def removelog(self):
        """
        This function is used to remove the user name from the login log when the user
        """
        name = os.path.join(self.root_directory, 'loginlog.txt')
        open_file = open(name, 'r')
        file_lines = open_file.readlines()
        for i in range(len(file_lines)):
            if self.username in file_lines[i]:
                pos = i
        open_file.close()
        open_file = open(name, 'w')
        for i in range(len(file_lines)):
            if pos != i:
                open_file.writelines(file_lines[i])
        open_file.close()

    def split(self, message):
        """splits the message from the client into several parts and stores into a list and
        initialises the analysis
        Parameters :
        message : string
            stores the message
        """
        self.message = message
        split_message = self.message.split(' ', 2)  #list
        print('message split: ', split_message)
        result = self.analize(split_message)
        print('message split reply: ', result)
        return result
