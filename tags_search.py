class Excerpt:
    text = ""

class MentionsInFile:
    file_name = ""
    occurences_in_file_count = 0
    excerpts = []

class Tag:
    tag_name = ""
    occurences_count = 0
    mentions = []

#============================================

def get_all_tag_data_in_file(file_path):
    import re

    tags_data = {}
    tags_beginning_indices = {}
    tag_start_regex = re.compile("\/\/tag::((.*,?)*)\[\]")
    tag_end_regex = re.compile("\/\/end::((.*,?)*)\[\]")

    with open(file_path) as adoc:
        lines = adoc.readlines()
        for index, line in enumerate(lines):
            if (tag_start := tag_start_regex.match(line)):
                tags = tag_start.group(1).split(",")
                for tag in tags:
                    tags_beginning_indices[tag] = index + 1
            elif (tag_end := tag_end_regex.match(line)):
                tags = tag_end.group(1).split(",")
                for tag in tags:
                    tags_data.setdefault(tag, []).append("".join(lines[tags_beginning_indices[tag]:index]))
                    tags_beginning_indices.pop(tag)
    return tags_data

def get_adocs_list(dir_name):
    from os import walk

    adocs = []
    for (dirpath, dirnames, filenames) in walk(dir_name):
        for filename in filenames:
            if filename.endswith(".adoc"):
                adocs.append(dirpath+"/"+filename)
    
    return adocs

def get_all_tag_data(dir_path):
    all_tag_data = {}
    files = get_adocs_list("example_doc")
    for file in files:
        if (tag_data := get_all_tag_data_in_file(file)):
            all_tag_data[file] = tag_data
    return(all_tag_data)