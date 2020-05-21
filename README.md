# am4894bq
> A helper library for some BigQuery related stuff.


[![pypi package](https://img.shields.io/pypi/v/am4894bq.svg)](https://pypi.python.org/pypi/am4894bq/)

## Install

`pip install am4894bq`

## Quickstart

```python
from am4894bq.schema import get_schema

# get a schema for a sample table
schema = get_schema('bigquery-public-data.samples.shakespeare')
schema
```




    [SchemaField('word', 'STRING', 'REQUIRED', 'A single unique word (where whitespace is the delimiter) extracted from a corpus.', ()),
     SchemaField('word_count', 'INTEGER', 'REQUIRED', 'The number of times this word appears in this corpus.', ()),
     SchemaField('corpus', 'STRING', 'REQUIRED', 'The work from which this word was extracted.', ()),
     SchemaField('corpus_date', 'INTEGER', 'REQUIRED', 'The year in which this corpus was published.', ())]



## Examples

You can see some example notebooks in the [examples folder](https://github.com/andrewm4894/am4894bq/tree/master/examples) of the repository.
