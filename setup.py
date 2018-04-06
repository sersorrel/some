from setuptools import setup

setup(
    name="some",
    version="0.1.0",
    description="A pager… sometimes.",
    author="Josh Holland",
    author_email="anowlcalledjosh@gmail.com",
    url="https://github.com/anowlcalledjosh/some",
    license="MIT",
    classifiers=[
        "Environment :: Console",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    keywords="pager",
    python_requires=">=3.6",
    py_modules=["some"],
    entry_points={"console_scripts": ["some=some:main"]},
    zip_safe=True,
)
