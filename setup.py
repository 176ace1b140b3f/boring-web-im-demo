import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
from web_im import VERSION
project = "web_im"


def get_install_requires():
    with open("requirements.txt") as fhandler:
        lines = []
        for line in fhandler:
            line = line[:line.find("#")].strip()
            if not line:
                continue
            lines.append(line)
        return lines


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ['tests']

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        if isinstance(self.pytest_args, str):
            self.pytest_args = self.pytest_args.split(" ")

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name=project,
    version=VERSION,
    description="Web IM",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=get_install_requires(),
    cmdclass={"test": PyTest},
    tests_require=[
        "pytest",
    ]
)
