import setuptools


setuptools.setup(
    name="msgflow",
    packages=setuptools.find_packages(),
    install_requires=[
        "pyyaml==5.3.1",
        "fire==0.3.1",
        "python-twitter==3.5",
        "slackclient==1.2.1",
        "envyaml==0.2060",
        "fastapi~=0.63.0",
        "uvicorn~=0.13.0",
    ],
    extras_require={
        "test": ["pytest~=5.0", "black==20.8b1"],
    },
    version="0.2.1",
    author="Noriyuki Abe",
)
