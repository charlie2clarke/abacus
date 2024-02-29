import logging
import os
from configparser import ConfigParser
from pathlib import Path
from shutil import copyfile
from tempfile import gettempdir

import click
import docx

DEFAULT_CFG_PATH = Path.home().joinpath(".abbacus", "config.ini")
CFG_OPTS = ["headings", "titles", "subtitles", "figures", "appendices"]


def default_cfg(cfg: ConfigParser) -> ConfigParser:
    for opt in CFG_OPTS:
        cfg.set("DEFAULT", opt, "True")
    return cfg


def write_default_cfg(cfg: ConfigParser, input_path: str) -> ConfigParser:
    cfg = default_cfg(cfg)
    dir = os.path.dirname(input_path)

    try:
        if not os.path.exists(dir):
            os.makedirs(dir)

        with open(input_path, "w") as config_file:
            cfg.write(config_file)

        logging.info(f"Default configuration created at {input_path}")
        return cfg
    except Exception as e:
        raise Exception(
            f"An error occurred while writing the default configuration: {e}"
        )


def load_cfg(input: str) -> ConfigParser:
    cfg = ConfigParser()
    is_file = os.path.isfile(input)

    if not is_file and input != str(DEFAULT_CFG_PATH):
        raise Exception(f"File {input} not found")

    if not is_file:
        logging.info("Writing a new default config")
        return write_default_cfg(cfg, input)

    logging.info("Reading config")
    cfg.read(input)

    for opt in CFG_OPTS:
        if not cfg.has_section(opt):
            logging.info(f"{opt} not found in config, setting it to False")
            cfg.add_section(opt)
            cfg.set("DEFAULT", opt, "False")
        else:
            if cfg.get("DEFAULT", opt).lower() not in ["true", "false"]:
                logging.info(f"Invalid value set for {opt}, setting to False")
                cfg.set("DEFAULT", opt, "False")

    logging.info("Read config")

    return cfg


def copy_doc(input: str) -> str:
    if not os.path.isfile(input):
        raise Exception(f"File {input} not found")
    if os.path.splitext(input)[-1] != ".docx":
        raise Exception(f"{input} is not a .docx file")
    filename = os.path.join(gettempdir(), os.path.basename(input))
    try:
        copyfile(input, filename)
        return filename
    except Exception as e:
        raise Exception(f"An error occurred whilst copying the input file: {e}")


def load_doc(filepath: str) -> docx.Document:
    try:
        doc = docx.Document(filepath)
    except:
        raise
    if doc is None:
        raise Exception(f"Document is null at path: {filepath}")
    return doc


def rm_tmp_doc(filepath: str) -> None:
    try:
        os.remove(filepath)
    except:
        logging.error(f"Error removing temp {filepath} file during cleanup")
        pass


@click.command()
@click.option(
    "--input", "-i", help="The file path to the document", required=True, type=str
)
@click.option(
    "--config", "-c", help="The config file to be read", default=DEFAULT_CFG_PATH
)
def main(input: str, config: str):
    cfg = load_cfg(config)
    try:
        filepath = copy_doc(input)
        doc = load_doc(filepath)
    finally:
        rm_tmp_doc(filepath)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(levelname)s] %(asctime)s - %(pathname)s:%(lineno)d - %(message)s",
        datefmt="%H:%M:%S",
    )
    main()
