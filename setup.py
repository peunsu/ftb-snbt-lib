import setuptools

if __name__ == "__main__":
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()

    setuptools.setup(
        name="ftb-snbt-lib",
        version="0.2.0",
        author="peunsu",
        author_email="peunsu55@gmail.com",
        description='A python library to parse, edit, and save FTB snbt tag, which is a variant of the "vanilla" snbt tag.',
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/peunsu/ftb-snbt-lib",
        project_urls={
            "Issues Tracker": "https://github.com/peunsu/ftb-snbt-lib/issues",
        },
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires=">=3.9",
    )