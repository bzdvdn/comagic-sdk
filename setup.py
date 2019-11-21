from setuptools import setup, find_packages

setup(
    name='comagic-data-api-sdk',
    version='0.0.3',
    packages=find_packages(),
    install_requires=[
        'requests>=2.18.2',
        'pytz>=2019.3'
    ],
    description='Comagic data api sdk',
    author='bzdvdn',
    author_email='bzdv.dn@gmail.com',
    url='https://github.com/bzdvdn/comagic-sdk',
    license='MIT',
    python_requires=">=3.6",
)
