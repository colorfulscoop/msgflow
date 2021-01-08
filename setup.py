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
        "test": ["pytest~=5.0", "black==20.8b1"],
        "webapi": ["fastapi~=0.63.0", "uvicorn~=0.13.0"],
        "twitter": ["python-twitter==3.5"],
        "slack": ["slackclient==1.2.1"],
        "cron": ["croniter==0.3.37"]
    },
    version="0.5.0",
    author="Noriyuki Abe",

    # Description info
    url="https://github.com/colorfulscoop/msgflow",
    description=(
        "msgFlow is a simple chatbot framework"
        " for simple configuration, customization"
        " and connection with several services."
    ),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",

    # Additional metadata
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
