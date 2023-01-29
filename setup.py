import setuptools


setuptools.setup(
    name="msgflow",
    packages=setuptools.find_packages(),
    install_requires=[
        "fire>=0.3.1,<0.4",
        "envyaml==0.2060",
        "pydantic>=1.0,<2",
        "requests>=2,<3",
        "aiohttp",
        "aioconsole",
        "regex_spm",
    ],
    extras_require={
        "test": ["pytest>=5", "black==20.8b1"],
        "webapi": ["fastapi>=0.70,<0.71", "uvicorn>=0.15,<0.16"],
        "slack": ["slack_bolt>=1.9.2,<2"],
        "cron": ["croniter>=0.3.37,<0.4"],
    },
    version="0.6.0",
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
    ],
)
