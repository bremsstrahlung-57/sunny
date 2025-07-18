from setuptools import setup

setup(
    name="sunny",
    version="0.1.3",
    scripts=["main.py"],
    py_modules=["configure", "main", "utility", "themes"],
    entry_points={"console_scripts": ["sunny=main:main"]},
    install_requires=["requests"],
)