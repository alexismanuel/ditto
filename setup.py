from setuptools import setup, find_packages

setup(
    name='ditto',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[],
    url='https://github.com/alexismanuel/ditto',
    author='Alexis Manuel',
    author_email='alexis.manuelpro@gmail.com',
    description='A simple dependency injection tool',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)