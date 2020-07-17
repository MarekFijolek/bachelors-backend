from app.models import Tag, MentionsInFile, Excerpt

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

def get_all_tag_data_and_stamp_version(dir_path, version_to_stamp):
    tags = {}
    mentions_all = []
    excerpts_all = []
    files = get_adocs_list(dir_path)

    for file in files:
        if (tag_data := get_all_tag_data_in_file(file)):
            for tag, excerpts in tag_data.items():
                if tag in tags:
                    tags[tag].occurrences_count += len(excerpts)
                else:
                    tags[tag] = Tag(tag_name=tag, occurrences_count=len(excerpts), version=version_to_stamp)

                file_name_relative = file.split("/", 1)[1]

                excerpts_models = [Excerpt(text=excerpt, version=version_to_stamp) for excerpt in excerpts]
                mentions_models = MentionsInFile(file_name=file_name_relative,occurrences_in_file_count=len(excerpts_models),excerpts=excerpts_models, version=version_to_stamp)

                tags[tag].mentions.append(mentions_models)
                mentions_all.append(mentions_models)
                excerpts_all.extend(excerpts_models)
    return {"tags": list(tags.values()), "mentions": mentions_all, "excerpts": excerpts_all}