import sys
from read_trec_data import iter_pages
from process_data import list_of_paragraphs_to_write, json_object
import jsonlines


def main(path):
    """
    The Trec Car data is processed page by page and the paragraphs and title of each page are written to the file
    :return: trec.jsonl
    """

    with jsonlines.open("trec.jsonl", mode="w") as writer:
        
        for page in iter_pages(open(path, 'rb')):

            if len(page.skeleton)>0:

                title = ""
                if type(page.page_name) == str:
                    title = page.page_name
                collection = "CAR"

                par_list = []
                id_list = []
                list_of_paragraphs_to_write(page.skeleton, par_list, id_list, True)
                for i in range(len(par_list)):
                    writer.write(json_object(collection, id_list[i], title, par_list[i]))


            else:
                continue

    


if __name__ == "__main__":
    path = sys.argv[1]
    print("Processing Trec Car data.....")
    main(path)
