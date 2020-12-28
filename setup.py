import setuptools


setuptools.setup(
    name="msgflow",
    packages=setuptools.find_packages(),
    install_requires=[
        "fire~=0.3.1",
        "envyaml==0.2060",
        "pydantic~=1.0",
    ],
    extras_require={
        "test": ["pytest~=5.0", "black~=20.0"],
        "webapi": ["fastapi~=0.63.0", "uvicorn~=0.13.0"],
        "twitter": ["python-twitter==3.5"],
        "slack": ["slackclient~=1.2.0"],
    },
    version="0.2.1",
    author="Noriyuki Abe",
)
