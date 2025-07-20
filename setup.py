from setuptools import setup, find_packages

setup(
    name="sunny",
    version="1.0.2",
    description="A minimal CLI tool to see weather on your terminal",
    author="Sagar Sharma",
    author_email="sagar292905@gmail.com",
    url="https://github.com/bremsstrahlung-57/sunny",
    packages=find_packages(),
    include_package_data=True,
    entry_points={"console_scripts": ["sunny=sunny.__main__:main"]},
    install_requires=["requests", "rich", "toml"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Utilities",
    ],
    python_requires=">=3.9",
)
