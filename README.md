# collection_collator

Adapted from https://vtechworks.lib.vt.edu/handle/10919/83211

This project scrapes all the Digital Library collections from dlib.vt.edu

For each collection, it searches wikipedia using its collection terms and grabs the corresponding wiki page and its description

## Development
### Installation
cd into the uppermost directory and run
```bash
python3 -m venv env
source env/bin/activate

pip install -e .
```

### Usage
You can directly run [solr.py](collection_collator/solr.py) from the command-line
```bash
cd collection_collator

python solr.py "my query here" # (quotes optional)
```