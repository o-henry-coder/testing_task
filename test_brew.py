import pytest
from testing_task.brew_package_install import *


@pytest.mark.parametrize("install_pack", ['ffmpeg', 'htop', 'wget'])
def test_installing_positive(install_pack) :
    assert installing(install_pack) is True


@pytest.mark.parametrize("inv_package", [' ', '77787', '@7 '])
def test_installing_negative(inv_package) :
    assert installing(inv_package) is False

"""Check whether package name contains invalid symbols  '!# $%^&*()+='"""

@pytest.mark.parametrize("inv_name", [' ', '!nk77', '#b7', 'ghf*'])
def test_invalid_package_name(inv_name):
    assert check_invalid_package_name(inv_name) == [True]

"""Check if the package exists (without installing)"""


@pytest.mark.parametrize("installed_package", ['ffmpeg', 'sqlite', 'htop'])
def test_check_return_code_0(installed_package):
    installing(installed_package)
    assert check_return_code(installed_package) == 0


@pytest.mark.parametrize("inv_package", ['ffm5peg', 'tcp', 'ahtop'])
def test_check_return_code_256(inv_package) :
    assert check_return_code(inv_package) != 0


"""Check installation of the non-existing package"""


@pytest.mark.parametrize("inv_package", [' ', '7897', '@5 '])
def test_not_existing_package(inv_package) :
    with pytest.raises(NotExistingPackage) as excinfo :
        not_existing_package(inv_package)
    assert str(excinfo.value) == "No formulae found"


"""Check installation of the previously installed package"""


def test_installing_existing_package() :
    installing('yarn')
    with pytest.raises(AlreadyInstalledPackage) :
        assert installing_existing_package('yarn')


def test_invalid_command() :
    with pytest.raises(InvalidCommandUsing) :
        assert invalid_command('isstall', 'htop')


def test_check_process_error() :
    with pytest.raises(ChildProcessError) :
        assert check_process_error('tcp')


def test_check_timeout_error() :
    with pytest.raises(TimeoutError) :
        assert check_timeout_error('htop')
