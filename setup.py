from setuptools import setup, find_packages

setup(
    name="sunny",
    version="0.1.3",
    description="A minimal CLI weather tool 🌤️",
    author="Sagar Sharma",
    author_email="sagarsharma.ai@protonmail.com",
    url="https://github.com/bremsstrahlung-57/sunny",
    packages=find_packages(),
    include_package_data=True,
    entry_points={"console_scripts": ["sunny=sunny.main:main"]},
    install_requires=["requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
)
