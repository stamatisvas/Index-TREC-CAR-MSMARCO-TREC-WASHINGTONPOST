# Index TREC-CAR, MSMARCO, TREC-WASHINGTON-POST Collections
This repository contains the code to reproduce my index for the collections TREC_CAR, MSMARCO, TREC-WASHINGTON-POST. First we need to download the data. We are using TREC-CAR v2.1, MSMARCO v2.1, TREC-WASHINGTON-POST V2. Then we will run the scripts in this repository to create one Jsonl file containing all three collections. Each line in the final Jsonl file will be a Json object and it will have the format:

{Collection, Doc_id, Title, Paragraph_id, Paragraph}

For example one line will be:

{"Collection": "WashigtonPost", "DocID": "b2e89334-33f9-11e1-825f-dabc29fd7071", "Title": "Danny Coale, Jarrett Boykin are a perfect 1-2 punch for Virginia Tech", "ParagraphID": "3", "Paragraph": "Now that Boykin and Coale have only Tuesday’s Sugar Bowl remaining before leaving Virginia Tech with every major school record for a wide receiver, they’ve taken a different stance."}

Having the data in this format we will use lucene4ir, a toolkit for Information retrival to index our data. The orginal repository for lucene4ir can be found here:

https://github.com/lucene4ir/lucene4ir

## Clone the repository

The first step is to clone the repository in your machine. This can be done by opening a terminal in the directory you want to clone the project and type:
```
git clone https://github.com/stamatisvas/One-Index-for-TREC-CAR-MSMARCO-TREC-WASHINGTONPOST
```
## Download and extract the data

For the MSMARCO download the file "Queries, Passages, and Relevance Labels" from:

http://www.msmarco.org/dataset.aspx

For the TREC-CAR download the file unprocessedAllButBenchmark.v2.1.tar.xz from:

http://trec-car.cs.unh.edu/datareleases/

For the TREC-WASHINGTON-POST downlaod the file "Washington Post corpus, version 2" from:

https://ir.nist.gov/wapo/

Having the MSMARCO data downloaded and extracted we need to concatenate all the qrels and queries. The queries will be used as titles when processing the msmarco collection. Open a terminal inside the folder where the data is and type:

```
cat qrels.* >> qrels.all
cat queries.* >> queries.all
```

## Install Required packages

We need two packages for running the scripts. jsonlines and cbor. For installing them open a terminal and type:

```
pip install jsonlines cbor
```

## Run the Scripts

The next step is to run the scripts and have all the data in the correct format. Open a terminal inside the folder where you clone the repository and type:

```
python process_msmarco_data.py path/to/collection.tsv path/to/qrels.all path/to/queries.all

python process_wapo_data.py path/to/TREC_Washington_Post_collection.v2.jl

python process_trec_car_data.py path/to/unprocessedAllButBenchmark.Y2.cbor
```

## Concatenate the three jsonl files to one

The final step in the processing procedure is to concatenate the three jsonl files into one. Open a terminal in the folder where all three collections exist and type:

```
cat trec.jsonl msmarco.jsonl wapo.jsonl >> data.jsonl
```


Now you have all three collections concatenated inside data.jsonl

You can open your terminal and type:

```
wc -l data.jsonl 
```

to count the lines inside the data.jsonl. If the process followed correctly this should show 41219573 lines which are the diffent objects/documents/paragraphs in our collection!

# Indexing

Now we have the data in a format which can be consumed by Lucene4ir. You should just choose the correct index type which is JSONL and index the data!
