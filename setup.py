from setuptools import setup

setup(
    name="sunny",
    version="0.0.1",
    scripts=["main.py"],
    py_modules=["configure", "main", "utility"],
    entry_points={"console_scripts": ["sunny=main:main"]},
    install_requires=["requests"],
)
