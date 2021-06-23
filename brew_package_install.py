import os
import subprocess

path = '/usr/local/bin/brew'
command = 'install'


class NotExistingPackage(Exception) :
    pass


class AlreadyInstalledPackage(Exception) :
    pass


class InvalidCommandUsing(Exception) :
    pass


def installing(package) :
    subprocess.run([path, command, package])
    check_path = f"/usr/local/bin/{package}"
    if os.path.exists(check_path) :
        check_path = True
    else :
        check_path = False
    return check_path


def check_return_code(package_name) :
    ret_code = os.system(f'brew list | grep {package_name} ')

    return ret_code


def check_invalid_package_name(package):
    subprocess.run([path, command, package])
    inv_symbols = '!# $%^&*()+='
    a = [True for i in package if i in inv_symbols]
    return a


def not_existing_package(package) :
    result = subprocess.Popen([path, command, package], stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    err = result.communicate()
    a = 'No available formula or cask with the name'.encode()
    if a in err[1] :
        raise NotExistingPackage("No formulae found")


def installing_existing_package(package) :
    result = subprocess.Popen([path, command, package], stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    err = result.communicate()
    a = 'is already installed and up-to-date'.encode()
    if a in err[1] :
        raise AlreadyInstalledPackage("The package is installed")


def check_process_error(package) :
    try :
        result = subprocess.check_output([path, command, package])
    except subprocess.CalledProcessError as e :
        result = e.output
        raise ChildProcessError

    return result


def check_timeout_error(package) :
    filename = f"/usr/local/bin/{package}"
    if os.path.exists(filename) :
        os.system(f"/usr/local/bin/brew uninstall {package}")
    try :
        result = subprocess.check_output([path, command, package], timeout=4)
    except subprocess.TimeoutExpired as e :
        result = e.output
        raise TimeoutError

    return result


def invalid_command(command, package) :
    result = subprocess.Popen([path, command, package], stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    err = result.communicate()
    a = 'Unknown command'.encode()
    if a in err[1] :
        raise InvalidCommandUsing("Invalid command")
