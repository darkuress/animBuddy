from setuptools import setup, find_packages

setup(
    name = 'animBuddy',
    version = '0.9.0',
    url = 'https://github.com/darkuress/animBuddy.git',
    author = 'Huile De Olive',
    author_email = "huiledolivemaster@gmail.com",
    description = "Anim Buddy for Autodesk Maya",
    packages = find_packages(),
    include_package_data = True,
    package_data = {'animBuddy.config': ['*.yaml']},
    install_requires = [],
)