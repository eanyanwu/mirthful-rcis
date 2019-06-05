import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mirthful-rcis",
    version="0.0.1",
    author="Eze Anyanwu",
    author_email="hello@ezeanyinabia.com",
    description="Rci Forms, Online",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hilarious-capital/mirthful-rcis",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
