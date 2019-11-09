from read_trec_data import iter_paragraphs,iter_pages
import jsonlines
from process_data import *

path= '/home/jjb17194/Downloads/paragraphCorpus/dedup.articles-paragraphs.cbor'


with jsonlines.open("car.jsonl", mode="w") as writer:

    for page in iter_paragraphs(open(path, 'rb')):
        paragraph = page.get_text()
        paragraph = clean_trec_paragraph(paragraph)
        doc_id = page.para_id
        title = ""
        collection = "CAR"
        writer.write(json_object(collection, doc_id, title, paragraph))
