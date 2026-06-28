from setuptools import find_packages, setup

setup(
    name="w33",
    version="1.0.0",
    description="W(3,3) Theory of Everything Exact Physics Framework",
    author="W(3,3) Program",
    packages=find_packages(),
    py_modules=["holonet_cmd"],
    entry_points={"console_scripts": ["holonet = holonet_cmd:main"]},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics",
        "Programming Language :: Python :: 3",
    ],
)
