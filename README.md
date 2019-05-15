# collection_collator

Adapted from https://vtechworks.lib.vt.edu/handle/10919/83211

This project scrapes all the Digital Library collections from dlib.vt.edu

For each collection, it searches wikipedia using its collection terms and grabs the corresponding wiki page and its description

## Installation
clone the repository then pip install it
```bash
pip install collection_collator
```

## Usage
the package includes the script `annotate_tweets`

Usage is as simple as:
```bash
annotate_tweets
```
This will update the csv file `collection_collator/collection_collator/annotated.csv`
