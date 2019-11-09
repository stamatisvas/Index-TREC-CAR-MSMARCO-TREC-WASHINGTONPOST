import jsonlines
import sys
from process_data import reading_qrels,reading_queries,clean_msmarco_paragraph,json_object


def main(path_data,path_qrels,path_queries):
    """
    Reads the collection line by line, cleans and writes the data.
    :param path_data: the path to the data
    :param path_qrels: the path to the qrels file
    :param path_queries: the path to the queries file
    :return: msmarco.jsonl
    """
    qrels = reading_qrels(path_qrels)
    queries = reading_queries(path_queries)
    with jsonlines.open("msmarco.jsonl", mode="w") as writer:


        with open(path_data, "r") as file:
      
            for line in file:
                y = line.split("\t")
                paragraph = y[1]
                paragraph = clean_msmarco_paragraph(paragraph)
                doc_id = y[0]
                title = ""
                if doc_id in qrels:
                    title = qrels[doc_id]

                if title in queries:
                    title = queries[title]

                collection = "MARCO"
                writer.write(json_object(collection, doc_id, title, paragraph))
            


if __name__ == "__main__":
    path_data = sys.argv[1]
    qrels_path = sys.argv[2]
    queries_path = sys.argv[3]
    print("Processing MSMarco data.....")
    main(path_data,qrels_path,queries_path)


