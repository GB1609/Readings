import logging
import json
import stringcase
import os

logger = logging.getLogger('take_trial_data')

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


if __name__ == '__main__':
    # load configuration file
    conf = json.load(open("configuration.json", encoding="utf-8"))
    # manga conf
    manga_to_generate = conf["manga"]
    logger.info("CONFIGURATION FILE:\n")
    logger.info(manga_to_generate)
    generation_template = open(f"{template_path}/manga template manually.md", 'r', encoding="utf-8").read()
    logger.info("TEMPLATE FILE:\n")
    logger.info(generation_template)
    for manga in manga_to_generate:
        # read info from configuration file
        name = manga
        bought = manga_to_generate[manga]["bought"]
        read_volumes = manga_to_generate[manga]["read_volumes"]
        to_read_volumes = bought - read_volumes
        publisher = manga_to_generate[manga]["publisher"]
        cover = manga_to_generate[manga]["cover"]
        editor = manga_to_generate[manga]["editor"]
        total_volumes = read_volumes + to_read_volumes
        authors: list[str] = manga_to_generate[manga]["author"]

        tags = manga_to_generate[manga]["tags"]
        all_tags = tags
        if isinstance(authors, list):
            all_tags.extend(authors)
        generated_tags: list[str] = [to_tag(tag) for tag in all_tags]
        generated_tags.append(to_tag(name))
        other_tags = ', '.join(generated_tags)
        missing = manga_to_generate[manga]["missing"]
        admissible_name = to_admissible_resource(name)

        for num_volume in range(1, total_volumes + 1):
            new_read_manga = generation_template.format(
                title=admissible_name,
                manga=admissible_name,
                volume=num_volume,
                author=authors,
                publisher=publisher,
                cover=cover,
                bought=False if num_volume > bought or num_volume in missing else True,
                status="Read" if num_volume <= read_volumes else "Unread",
                editor=editor,
                other_tags=other_tags
            )

            file_name = f'{admissible_name}, Vol {num_volume}.md'
            create_folder(f"{manga_path}/{admissible_name}/")
            with open(f"{manga_path}/{admissible_name}/{file_name}", 'w', encoding="utf-8") as f:
                f.writelines(new_read_manga)
                logger.info(f'Create file {admissible_name}!')
    logger.info("ALL MANGA GENERATED")

    logger.info("START COMPLETE MANGA:")
    completed_template = open(f"{template_path}/manga template completed.md", 'r', encoding="utf-8").read()
    logger.info("TEMPLATE FILE:\n")
    logger.info(completed_template)
    for completed in conf["completed"]:
        admissible_name = to_admissible_resource(completed)
        file_name = f'{admissible_name}.md'

        bought = manga_to_generate[completed]["bought"]
        cover = manga_to_generate[completed]["cover"]
        authors: list[str] = manga_to_generate[completed]["author"]

        completed_manga = completed_template.format(
            title=admissible_name,
            author=authors,
            cover=cover,
            total_volume=bought
        )

        create_folder(f"{manga_path}/Complete")
        with open(f"{manga_path}/Complete/{file_name}", 'w', encoding="utf-8") as f:
            f.writelines(completed_manga)
            logger.info(f'Create file {admissible_name}!')
    logger.info("ALL Completed Manga GENERATED")
