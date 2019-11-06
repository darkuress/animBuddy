from setuptools import setup, find_packages

setup(
    name = 'animBuddy',
    version = '1.0.8',
    url = 'https://github.com/darkuress/animBuddy.git',
    author = 'Syncsketch',
    author_email = "huiledolivemaster@gmail.com",
    description = "Anim Buddy for Autodesk Maya",
    packages = find_packages(),
    include_package_data = True,
    package_data = {'animBuddy.config': ['*.yaml']},
    install_requires = [],
)