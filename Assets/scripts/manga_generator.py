import logging
import json
import stringcase
import os
import shutil
import volume_info_retriever as retriever

logger = logging.getLogger('manga generator for obsidian')

# arrays of not admitted char
not_admissible_char = [':', '/', '<', '>', '"', '/', '|', "?", "*", '.', ',', ';', '-']
not_admissible_chat_to_space = ['’', '\'']

# paths of input and output folder
manga_path = "../../Readings/Manga"
template_path = "../Templates"


def to_admissible_resource(resource):
    """
    Given a string replace all 'not_admissible_chat_to_space' with space and
    remove all 'not_admissible_char'
    :param resource: name of resource
    :return: a [[str]] in a desired format
    """
    replace_char_to_space = ''.join(" " if x in not_admissible_chat_to_space else x for x in resource)
    replace_char = ''.join(x for x in replace_char_to_space if x not in not_admissible_char)
    to_array = list(filter(None, replace_char.split(" ")))
    to_return = " ".join([el.capitalize() for el in to_array])
    return to_return


def to_tag(element):
    """
    Change a string in camel case
    :param element: string that represent resource
    :return: a string in a camelCase
    """
    return stringcase.camelcase(to_admissible_resource(element).replace(" ", ""))


def create_folder(path):
    """
    Create a directory if not exist
    :param path: path of folder
    """
    if not os.path.exists(path):
        os.mkdir(path)


def clean_folder(path):
    # delete manga folder
    for root, dirs, files in os.walk(path):
        for f in files:
            os.remove(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))


if __name__ == '__main__':
    # clean_folder(manga_path)
    # load configuration file
    conf = json.load(open("configuration.json", encoding="utf-8"))
    print("LOADED CONFIGURATION FILE")
    # manga conf
    manga_to_generate = conf["manga"]
    generation_template = open(f"{template_path}/manga template manually.md", 'r', encoding="utf-8").read()
    print("LOADED TEMPLATE FILE")
    for manga in manga_to_generate:
        # read info from configuration file
        name = manga
        bought = manga_to_generate[manga]["bought"]
        read_volumes = manga_to_generate[manga]["read_volumes"]
        to_read_volumes = bought - read_volumes
        publisher = manga_to_generate[manga]["publisher"]
        covers = dict(manga_to_generate[manga]["cover"])
        total_volumes = read_volumes + to_read_volumes

        tags = manga_to_generate[manga]["tags"]
        all_tags = tags

        generated_tags: list[str] = [to_tag(tag) for tag in all_tags]
        generated_tags.append(to_tag(name))
        other_tags = ', '.join(generated_tags)
        missing = manga_to_generate[manga]["missing"]

        for num_volume in range(1, total_volumes + 1):
            isbn = covers[str(num_volume)]
            retrieved_infos = retriever.get_needed_info(isbn)
            all_tags.extend(retrieved_infos.authors)
            final_name = retrieved_infos.title if retrieved_infos.title else to_admissible_resource(name)

            new_read_manga = generation_template.format(
                title=final_name,
                manga=final_name,
                volume=num_volume,
                pages=retrieved_infos.pages,
                author=retrieved_infos.authors,
                publisher=publisher,
                cover=retrieved_infos.cover,
                bought=False if num_volume > bought or num_volume in missing else True,
                status="Read" if num_volume <= read_volumes else "Unread",
                isbn=isbn,
                other_tags=other_tags
            )

            file_name = f'{final_name}, Vol {num_volume}.md'
            create_folder(f"{manga_path}/{final_name}/")
            with open(f"{manga_path}/{final_name}/{file_name}", 'w', encoding="utf-8") as f:
                f.writelines(new_read_manga)
                print(f'Created file {file_name}')
    print("ALL MANGA GENERATED")

    print("START COMPLETE MANGA:")
    completed_template = open(f"{template_path}/manga template completed.md", 'r', encoding="utf-8").read()
    for completed in conf["completed"]:
        covers = dict(manga_to_generate[completed]["cover"])
        isbn = covers[str(1)]
        retrieved_infos = retriever.get_needed_info(isbn)
        final_name = retrieved_infos.title if retrieved_infos.title else to_admissible_resource(completed)
        file_name = f'{final_name}.md'

        bought = manga_to_generate[completed]["bought"]
        covers = manga_to_generate[completed]["cover"]

        completed_manga = completed_template.format(
            title=final_name,
            author=retrieved_infos.authors,
            cover=covers,
            total_volume=bought
        )

        create_folder(f"{manga_path}/Complete")
        with open(f"{manga_path}/Complete/{file_name}", 'w', encoding="utf-8") as f:
            f.writelines(completed_manga)
            print(f'Create file {final_name}!')
    print("ALL Completed Manga GENERATED")
