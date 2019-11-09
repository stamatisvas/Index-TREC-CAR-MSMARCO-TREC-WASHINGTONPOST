import jsonlines
import sys
from process_data import clean_wapo_paragraph,json_object_wapo

def main(path):
    """
    Reads the Wapo collection line by line, cleans and writes the data in the file
    :return: wapo.jsonl
    """
    with jsonlines.open("wapo.jsonl", mode="w") as writer:
        with jsonlines.open(path) as reader:
            
            for obj in reader:
                doc_id = obj["id"]
                contents = obj["contents"]
                title = obj["title"]
                if type(doc_id)==str and type(contents)==list and type(title)==str:
                    paragraphs = []
                    for line in contents:
                        if type(line) == dict:
                            if 'content' in line.keys():
                                paragraphs.append(line["content"])

                    paragraphs = clean_wapo_paragraph(paragraphs)

                    collection = "WAPO"

                    for i in range(len(paragraphs)):
                        par_index = (str(i))
                        paragraph = str(paragraphs[i])
                        writer.write(json_object_wapo(collection, doc_id, title, par_index, paragraph))
                else:
                    continue
            


if __name__ == "__main__":
    path = sys.argv[1]
    print("Processing Wapo data......")
    main(path)
