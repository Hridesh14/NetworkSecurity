from setuptools import find_packages,setup
from typing import List

def get_requirements()->List[str]:
    '''This function will get the requirements '''
    requirements_list:List[str]=[]
    
    try:
        with open('requirements.txt','r') as file_obj:
            lines = file_obj.readlines()
            for line in lines:
                requirements = line.strip()
                if requirements and requirements != '-e .':
                    requirements_list.append(requirements)
        

    except FileNotFoundError:
        print('The file requirements.txt does not exist')
    
    return requirements_list
print(get_requirements())

setup(
    name='NetworkSecurity',
    version='0.0.0.1',
    description='xyz',
    author='Hridesh Maithani',
    author_email='maithanihridesh9012@gmail.com',
    packages= find_packages(),
    install_requires = get_requirements()
    
)

