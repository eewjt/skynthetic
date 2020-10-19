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
    packages=['skynthetic'],  #same as name
    install_requires=['matplotlib==3.2.2', 'bruges', 
    'numpy==1.18.5', 'Pillow==8.0.0', 'IPython', 'jupyter==1.0.0'] #external packages as dependencies
)