from setuptools import setup, find_packages

setup(
    name="github-star-clone-tool",
    version="1.0.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "starcloner=functions.main:main",
        ],
    },
    install_requires=[
        "requests",
    ],
    python_requires=">=3.10",
)
