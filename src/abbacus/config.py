import json
import logging
import os
from configparser import ConfigParser
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

DEFAULT_CFG_PATH = Path.home().joinpath(".abbacus", "config.ini")


class UninitialisedException(Exception):
    def __init__(
        self,
        message="Cfg has not been initialised. The first call must specify the input parameter which is the filepath to the config file.",
    ):
        self.message = message
        super().__init__(self.message)


class UnimplementedException(Exception):
    pass


class InvalidIgnoredSections(Exception):
    def __init__(
        self,
        message='Invalid value provided for ignored_sections field, the value provided should be a list of strings, e.g., ["References", "Appendices"]',
    ):
        self.message = message
        super().__init__(self.message)


@dataclass
class CfgOpt:
    name: str
    value: str
    _type: type = None
    _default_off: str = None


class Cfg(object):
    _opts: Dict[str, CfgOpt] = {}
    _DEFAULT_OPTS = [
        CfgOpt(name="headings", value="True", _default_off="False", _type=bool),
        CfgOpt(name="titles", value="True", _default_off="False", _type=bool),
        CfgOpt(name="subtitles", value="True", _default_off="False", _type=bool),
        CfgOpt(name="captions", value="True", _default_off="False", _type=bool),
        CfgOpt(name="bibliography", value="True", _default_off="False", _type=bool),
        CfgOpt(
            name="ignored_sections",
            value='["Appendices", "Appendix", "Bibliography", "References", "Works Cited"]',
            _default_off="[]",
            _type=list,
        ),
    ]
    _DEFAULT_SECT = "DEFAULT"
    _instance = None
    _input = None

    def __new__(cls, input: str = str(DEFAULT_CFG_PATH)):
        if cls._instance is None:
            cls._instance = super(Cfg, cls).__new__(cls)
            cls._input = input or str(DEFAULT_CFG_PATH)
            cfg_opts = cls._instance._load_cfg()
            cls._instance._init_opts(cfg_opts)

        if cls._instance is None and cls._input is None:
            raise UninitialisedException()
        return cls._instance

    @property
    def opts(self) -> Dict[str, CfgOpt]:
        return self._opts

    def _init_opts(self, cfg_opts: List[CfgOpt]) -> None:
        for opt in cfg_opts:
            try:
                if opt._type == bool:
                    opt.value = bool(opt.value.lower() == "true")
                elif opt._type == list:
                    opt.value = json.loads(opt.value)
                else:
                    raise UnimplementedException(f"{opt._type} is not implemented")
            except ValueError:
                logging.error(
                    f"Invalid value set for {opt.name} despite having been initialised"
                )
                raise

            self._opts[opt.name] = opt
        if self._opts is None:
            raise UninitialisedException()

    def _default_cfg(self) -> ConfigParser:
        cfg = ConfigParser()
        for opt in self._DEFAULT_OPTS:
            cfg.set(self._DEFAULT_SECT, opt.name, opt.value)
        return cfg

    def _write_default_cfg(self) -> List[CfgOpt]:
        cfg = self._default_cfg()
        dir = os.path.dirname(self._input)

        try:
            if not os.path.exists(dir):
                os.makedirs(dir)

            with open(self._input, "w") as config_file:
                cfg.write(config_file)

            logging.info(f"Default configuration created at {self._input}")
            return self._DEFAULT_OPTS
        except Exception as e:
            raise Exception(
                f"An error occurred while writing the default configuration: {e}"
            )

    def _read_existing_cfg(self) -> List[CfgOpt]:
        cfg_opts: List[CfgOpt] = []
        cfg = ConfigParser()
        cfg.read(self._input)

        for opt in self._DEFAULT_OPTS:
            if not cfg.has_option(self._DEFAULT_SECT, opt.name):
                logging.info(
                    f"{opt.name} not found in config, defaulting to off value: {opt._default_off}"
                )
                cfg.set(self._DEFAULT_SECT, opt.name, opt._default_off)
                cfg_opts.append(opt)
            else:
                value = cfg.get(self._DEFAULT_SECT, opt.name)
                if value is not None:
                    try:
                        if opt._type == bool:
                            if value.lower() not in ["true", "false"]:
                                raise ValueError
                        elif opt._type == list:
                            try:
                                json.loads(opt.value)
                            except (json.JSONDecodeError, ValueError) as e:
                                raise InvalidIgnoredSections()
                        else:
                            raise UnimplementedException(
                                f"{opt._type} is not implemented"
                            )
                    except ValueError:
                        logging.warn(
                            f"Invalid value set for {opt.name}, defaulting to off: {opt._default_off}"
                        )
                        cfg.set(self._DEFAULT_SECT, opt.name, opt._default_off)
                        cfg_opts.append(
                            CfgOpt(
                                name=opt.name,
                                value=opt._default_off,
                                _type=opt._type,
                                _default_off=opt._default_off,
                            )
                        )
                        continue
                    cfg_opts.append(
                        CfgOpt(
                            name=opt.name,
                            value=value,
                            _type=opt._type,
                            _default_off=opt._default_off,
                        )
                    )

        logging.info(
            "Read config. Running with the following:\n{}".format(
                "\n".join(
                    f"{opt}: {value}" for opt, value in cfg.items(self._DEFAULT_SECT)
                )
            )
        )
        return cfg_opts

    def _load_cfg(self) -> List[CfgOpt]:
        is_file = os.path.isfile(self._input)

        if not is_file and self._input != str(DEFAULT_CFG_PATH):
            raise Exception(f"File {self._input} not found")

        if not is_file:
            logging.info("Writing a new default config")
            return self._write_default_cfg()

        logging.info("Reading config")
        return self._read_existing_cfg()
