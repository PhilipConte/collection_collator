import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="collection_collator",
    version="0.0.1",
    author="Philip Conte",
    author_email="philipmconte@gmail.com",
    description="finds information about VT DLRL tweet collections",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PhilipConte/collection_collator",
    packages=setuptools.find_packages(),
    install_requires=[
        'beautifulsoup4',
        'mediawiki-parser',
        'pandas',
        'pysolr',
        'wordninja',
    ],
    include_package_data=True,
    keywords='Virginia Tech Digital Library Research Laboratory Tweets',
    classifiers=("Programming Language :: Python :: 3",),
)
