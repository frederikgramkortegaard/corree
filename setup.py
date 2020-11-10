import setuptools

with open("README.md", 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="Corree - Frederik Gram", # Replace with your own username
    version="2.1",
    author="Frederik Gram",
    author_email="frederikxyz@hotmail.com",
    description="Simple dictionary based command-line argument parser with type validation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/frederikgram/corree",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
