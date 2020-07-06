import setuptools


setuptools.setup(
    name="pybot",
    packages=setuptools.find_packages(),
    install_requires=[
        "pyyaml==5.3.1",
        "pydantic==1.5.1",
        "fire==0.3.1",
        "python-twitter==3.5",
    ],
    version="0.0.0",
    author="Noriyuki Abe",
)
