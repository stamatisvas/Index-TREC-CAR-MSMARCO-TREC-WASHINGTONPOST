import re
import read_trec_data
import string


def remove_url(paragraph):
    """
    Finds all the urls inside a paragraph
    :param paragraph:
    :return: urls
    """
    url = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', paragraph)
    string_split = paragraph.split()
    urls_list = [urls for base_url in url for urls in string_split if base_url in urls]
    clean_string = [word for word in string_split if word not in urls_list]
    paragraph = " ".join(clean_string)
    return paragraph

def reading_qrels(path_qrels):
    """
    reading qrels in msmarco collection and save them in a dictionary
    :return: dictionary qrels
    """
    qrels = {}
    with open(path_qrels, "r") as f:
        for line in f:
            qrels[line.split("\t")[2]] = line.split("\t")[0]
    return qrels

def remove_char(topic):

    index_list = []
    for j in range(len(topic)):
        if '"\"' == topic[j]:
            index_list.append(j)
            index_list.append(j+1)
            index_list.append(j+2)
            index_list.append(j+3)

    topic = [topic[i] for i in range(len(topic)) if i not in index_list]
    topic = "".join(topic)
    return topic

def reading_queries(path_queries):
    """
    reading queries in msmarco collection and save them in a dictionary
    :return: dictionary queries
    """
    queries = {}
    with open(path_queries, "r") as f:
        for line in f:
            queries[line.split("\t")[0]] = line.split("\t")[1]
    return queries

def clean_wapo_paragraph(paragraphs):
    """
    Cleaning the paragraphs in wapo collection i.e. removing urls, special characters, single words etc.
    :param paragraphs:
    :return: cleaned paragraphs
    """
    line_to_remove = []

    for i in range(len(paragraphs)):



        if type(paragraphs[i]) is str:
            paragraphs[i] = remove_url(paragraphs[i])

            if len(paragraphs[i].split())<3:
                line_to_remove.append(paragraphs[i])
            elif paragraphs[i].startswith('<'):
                line_to_remove.append(paragraphs[i])
        else:
            line_to_remove.append(paragraphs[i])


    paragraphs = [par for par in paragraphs if par not in line_to_remove]

    for i in range(len(paragraphs)):

            paragraphs[i] = paragraphs[i].replace("</a>", " ")
            paragraphs[i] = paragraphs[i].replace("\"","")
            split_line = paragraphs[i].split()
            words_to_remove = []
            for j in split_line:
                if "href" in j:
                    words_to_remove.append(j)
                elif "<a" in j:
                    words_to_remove.append(j)
                elif "title=" in j:
                    words_to_remove.append(j)

            split_line = [word for word in split_line if word not in words_to_remove]
            paragraphs[i] = " ".join(split_line)

            symbols = ["(", ")", "!", '"', "'", "#", "$", "%", "&", "*", "+", "-", "/", ":", ";", "<", ">",
                       "=", "?", "@", "[", "]", "^", "_", "`", "{", "}", "|", "~"]
            for symbol in symbols:
                paragraphs[i] = paragraphs[i].replace(symbol,"")
            for space in string.whitespace:
                paragraphs[i] = paragraphs[i].replace(space," ")

    return paragraphs

def clean_msmarco_paragraph(paragraph):
    """
    Removing all special characters from the paragraphs in msmarco collection
    :param paragraph:
    :return: cleaned paragraph
    """
    paragraph = remove_url(paragraph)
    paragraph = paragraph.replace("\x80", " ")

    characters_to_remove = [" â¦ ", "s", "â", "\x93", "\x94", "\n", "\"", "(", ")", "!", '"', "'", "#",
                            "$", "%", "&", "*", "+", "-", "/", ":", ";", "<", ">", "=", "?",
                            "@", "[", "]", "^", "_", "`", "{", "}", "|", "~"]

    for char in characters_to_remove:
        paragraph = paragraph.replace(char, "")
    for y in string.whitespace:
        paragraph = paragraph.replace(y, " ")
    paragraph = remove_char(paragraph)
    return paragraph

def clean_trec_paragraph(paragraph):
    """
    Cleans the paragraphs from special symbols ands returns the clean paragraph
    :param paragraph:
    :return: clean paragraph
    """

    words_to_remove = []
    paragraph = remove_url(paragraph)
    paragraph = paragraph.split()
    for word in paragraph:
        if word.startswith("("):
            words_to_remove.append(word)
    paragraph = [x for x in paragraph if x not in words_to_remove]
    paragraph = " ".join(paragraph)
    symbols = ["\"", "(", ")", "!", '"', "'", "#", "$", "%", "&", "*", "+", "-", "/", ":", ";", "<", ">", "=", "?",
               "@", "[", "]", "^", "_", "`", "{", "}","|", "~"]
    for symbol in symbols:
        paragraph = paragraph.replace(symbol,"")
    for y in string.whitespace:
        paragraph = paragraph.replace(y, " ")


    return paragraph



def json_object(collection, doc_id, title, paragraph):
    """
    Creates a dictionary in the format we want to write the data
    :return:dictionary
    """
    out = {"DocID": collection+"_"+doc_id, "Title": title, "Paragraph": paragraph}
    return out

def json_object_wapo(collection, doc_id, title, par_index, paragraph):
    """
    Creates a dictionary in the format we want to write the data
    :return:dictionary
    """
    out = {"DocID": collection+"_"+doc_id+"-"+par_index, "Title": title, "Paragraph": paragraph}
    return out

def list_of_paragraphs_to_write(skeleton, par_list, id_list, is_in_sk):
    """
    This is a recursive function which iterating inside the skeleton of a page and
    takes the paragraphs and writes them in the file.

    """
    i=len(skeleton)

    for obj in skeleton:

        if type(obj) == read_trec_data.Image:
            pass

        elif type(obj) == read_trec_data.Para:


            if len(obj.paragraph.get_text().split()) > 2:

                paragraph = obj.paragraph.get_text()
                paragraph = clean_trec_paragraph(paragraph)
                doc_id = obj.paragraph.para_id
                par_list.append(paragraph)
                id_list.append(doc_id)


            else:
                continue

        elif type(obj) == read_trec_data.List:

            if len(obj.body.get_text().split()) > 2:

                paragraph = obj.body.get_text()
                paragraph = clean_trec_paragraph(paragraph)
                doc_id = obj.body.para_id
                par_list.append(paragraph)
                id_list.append(doc_id)


            else:
                continue


        elif type(obj) == read_trec_data.Section:

            if len(obj.children) > 0:

                list_of_paragraphs_to_write(obj.children, par_list, id_list, False)

            else:
                pass

        else:
            pass

        if is_in_sk == True:
            i-=1
            if i<5:
                break
