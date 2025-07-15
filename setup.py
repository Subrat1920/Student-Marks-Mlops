from setuptools import setup, find_packages
from typing import List

HYPHEN_E_DOT = '-e .'
def get_requirements()->List[str]:
    requirement_list: List[str] = []
    try:
        with open('requirements.txt', 'r') as file:
            lines = file.readlines()

            for line in lines:
                requirements = line.strip()
                if requirements and not requirements.startswith(HYPHEN_E_DOT):
                    requirement_list.append(requirements)
    except FileNotFoundError:
        print("There is not requirements.txt file found !!!")
    return requirement_list



setup(
    name="Student-Mark-Predictor",
    version="0.0.1",
    author="Subrat Mishra",
    author_email="3subratmishra1sep@gmail.com",
    packages=find_packages(),
    install_requires = get_requirements()
)

