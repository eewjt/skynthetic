import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="skynthetic", # Replace with your own username
    version="1.0",
    author="Euan Soutter",
    author_email="euan.soutter@manchester.ac.uk",
    description="sketch to seismic",
    long_description="turn images into synthetic seismograms",
    long_description_content_type="text/markdown",
    url="https://github.com/eslrgs/skynthetic.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)