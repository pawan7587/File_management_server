"""
This module contains classes named User_services and Admin_services
"""
import os
import datetime
import time
#from pathlib import Path
import shutil

class Userservices:
    """This module contains the class User_services
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
            stores Current working Directory
        read_file : string
            stores the previously read file
        start_point : integer
            stores the postions of the file to start reading
    Methods:
    --------------
        __init__(self):
            Initialises all the attributes

        list_files(self):
            list the file in the directory

        create_folder(self, folder_name, privilage):
            creates a new folder

        create_user_log(self, directory):
            creates a log file and adds user name

        create_admin_log(self, directory):
            adds admin names to the log

        modify_file(self, directory, file_name, input_val):
            modifies log files

        write_file(self, file_name, input_string=None):
            edits or creates file with the given input

        start_read(self, file_name):
            contains logic for reading from files

        view_file(self, file_name, startpoint):
            reads and returns a specific part of the file

        reverse(self, val):
            returns a reversed string

        change_directory(self, folder_name, privilage):
            changes current working directory
    """
    def __init__(self, root_directory, curr_directory, username, password):
        """Initializing variables"""
        self.username = username
        self.password = password
        self.root_directory = root_directory
        self.curr_directory = curr_directory
        self.read_file = ''
        self.start_point = 0

    def list_files(self):
        """
        Files are listed along with their size and last date modified
        """
        path = self.curr_directory
        files = list(os.listdir(path))
        data = {}
        size_date = ['', '']
        reply = ''
        for file in files:
            file_path = os.path.join(path, file)
            date_created = os.stat(file_path).st_ctime
            date_format = str("{}".format(datetime.datetime.strptime(time.ctime(date_created),
                                                                     "%a %b %d %H:%M:%S %Y")))
            thestats = os.stat(file_path)
            data[file] = size_date.copy()
            data[file][0] = thestats.st_size
            data[file][1] = date_format
        reply += '{:25}\t{:10}\t{:10}'.format('Name', 'Size', 'Date Created \n')
        reply += '-------------------------------------------------------------------\n'
        for key in data:
            reply += str('{:20s}\t{:10} Bytes\t{:10}\n'.format(key, data[key][0], data[key][1]))
        return reply

    def create_folder(self, folder_name, privilage):
        """Creating a folder
        Parameters:
            folder_name : string
                name of the folder to create
            privilage : string
                this is used to check privilages of client
        """
        try:
            path = os.path.join(self.curr_directory, folder_name)
            os.mkdir(path)
            if privilage == 'admin':
                self.create_admin_log(path)
            else:
                self.create_user_log(path)
        except:
            reply = 'failed to create folder'
            return reply
        reply = 'folder created'
        return reply

    def create_user_log(self, directory):
        """Creates user log
        Parameters:
            directory : string
                stores the directory location where log file have to be created

            this function creates log file and writes username in log so that it
            can be accessed by the user
        """
        file_name = str(f'{directory}\\log.txt')
        file = open(file_name, "w")
        data = self.username
        user_data = [data, "\n"]
        file.writelines(user_data)
        file.close()
        self.create_admin_log(directory)

    def create_admin_log(self, directory):
        """
        Parameters:
            directory : string
                stores the directory location where log file have to be created

            this function adds admin names to the log file in user directory
            so that admin can also have access to the user files
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

    def modify_file(self, directory, file_name, input_val):
        """
        this function adds names to log file
        Parameters:
            directory : string
                stores the directory location
            file_name : string
                stores the file name
            input_val : string
                stores the input that has to be written in the file
        """
        file_name = str(f'{directory}\\{file_name}')
        file = open(file_name, 'a')
        user_data = [input_val, "\n"]
        file.writelines(user_data)
        file.close()

    def write_file(self, file_name, input_string=None):
        """
        writes client input into the file
        Parameters:
            file_name : string
                stores the file name
            input_string : string
                stores the input that has to be written in the file
                if there is no input it is initilized as None
        """
        path = os.path.join(self.curr_directory, file_name)
        if input_string is None:
            file = open(path, 'w')
            file.close()
            reply = 'File cleared'
            return reply

        file = open(path, 'a')
        user_data = [input_string, "\n"]
        file.writelines(user_data)
        file.close()
        reply = 'file edited successfully'
        return reply

    def start_read(self, file_name):
        """
        Reads the values from the file and returns exactly 100 character
        it also saves the file name and checks if the new file name is similar
        to the privious file. if both are similar it returns the next 100 chracters

        Parameters:
            file_name : string
                stores the file name that has to be read
        """
        if file_name is None:
            if self.read_file != '':
                self.read_file = ''
                reply = 'File Closed'
                return reply
            reply = 'Invalid argument'
            return reply
        path = os.path.join(self.curr_directory, file_name)
        try:
            if os.path.exists(path):
                if self.read_file == file_name:
                    self.start_point = self.start_point+100
                    reply = self.view_file(path, self.start_point)
                    return reply
                self.read_file = file_name
                self.start_point = 0
                reply = self.view_file(path, self.start_point)
                return reply
            reply = 'file doesnot exist'
            return reply
        except PermissionError:
            reply = 'Requested file is a folder'
            return reply
        except:
            reply = 'error occured'
            return reply

    def view_file(self, file_name, startpoint):
        """
        view the file
        Parameters:
            file_name : string
                stores the file name that has to be read
            startpoint : integer
                it stores the location from where the file has to be read
        """
        strt = startpoint+100
        file = open(file_name, "r")
        value = file.read()
        if strt >= len(value):
            self.start_point = 0
        return str(value[startpoint:strt])

    def reverse(self, val):
        """
        reverse the string
        Parameters:
            val : string
                stores the string that has to be reversed
        """
        string = ""
        for i in val:
            string = i + string
        return string
    def change_directory(self, folder_name, privilage):
        """
        Changes the directory
        Parameters:
            folder_name : string
                name of the folder to change
            privilage : string
                this is used to check privilages of client
        """
        path = self.reverse(self.root_directory)
        num = path.find('\\')+1
        final_path = path[num:]
        print(final_path)
        inp = '..'
        try:
            if folder_name == inp:
                reval = self.reverse(self.curr_directory)
                num = reval.find('\\')+1
                new_path = reval[num:]
                if self.reverse(new_path) == self.root_directory and privilage != 'admin':
                    return 'access denied'
                if self.reverse(new_path) == self.reverse(final_path):
                    return 'access denied'
                self.curr_directory = self.reverse(new_path)
                reply = 'directory changed to '+self.curr_directory
                return reply
            user_directory = os.path.join(self.curr_directory, folder_name)
            if os.path.isdir(user_directory):
                self.curr_directory = user_directory
                reply = 'directory changed to '+self.curr_directory
                return reply
            return 'file not found'
        except Exception as error:
            reply = f'Exception occured : {error}'
            return reply
        return 'error'

class Adminservices(Userservices):
    """
    Admin_services class is created which inherits from user_services

    Attributes:
    --------------
        read_file : string
            stores the previously read file
        start_point : integer
            stores the postions of the file to start reading
    Methods:
    --------------
        __init__(self):
            Initialises all the attributes

        delete_user(self, folder_name, password):
            deletes the user and all the contents of the folder
    """
    def __init__(self, root_directory, curr_directory, username, password):
        """Initializing variables"""
        super().__init__(root_directory, curr_directory, username, password)
        self.read_file = ''
        self.start_point = 0

    def delete_user(self, folder_name, password, privalage):
        """
        this methods deletes the user and user directory
        this method is only available to the client with admin privilages
        Parameters:
            folder_name : string
                name of the folder to delete
            password : string
                this is used to check if password matches the admin password
        """
        if password == self.password:
            try:
                if folder_name == self.username:
                    reply = 'You cannot delete your self'
                    return reply
                if privalage == 'admin':
                    file_name = 'adminlog.txt'
                else:
                    file_name = 'userlog.txt'
                name = os.path.join(self.root_directory, file_name)
                open_file = open(name, 'r')
                file_lines = open_file.readlines()
                for i in range(len(file_lines)):
                    if folder_name in file_lines[i]:
                        pos = i
                open_file.close()
                open_file = open(name, 'w')
                for i in range(len(file_lines)):
                    if pos != i:
                        open_file.writelines(file_lines[i])
                open_file.close()
                rem = os.path.join(self.root_directory, folder_name)
                shutil.rmtree(rem)
                reply = 'User Deleted'
                return reply
            except:
                reply = 'error occured'
                return reply
        reply = 'Un-Authorized'
        return reply
