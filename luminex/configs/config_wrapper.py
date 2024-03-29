"""config wrapper for luminex."""

import os
from typing import Any, Dict, List, Optional

import yaml
from pkg_resources import resource_filename


def load_cfg(
    yaml_filepath: Optional[str] = None, verbose: bool = False
) -> Dict[str, Any]:
    """
    Load a YAML configuration file.

    Parameters
    ----------
    yaml_filepath : str, optional (default: package config file)

    Returns
    -------
    cfg : Dict[str, Any]
    """
    if yaml_filepath is None:
        yaml_filepath = resource_filename("configs", "config.yaml")
    # Read YAML experiment definition file
    if verbose:
        print(f"Load config from {yaml_filepath}...")
    with open(yaml_filepath) as stream:
        cfg = yaml.safe_load(stream)
    cfg = make_paths_absolute(os.path.dirname(yaml_filepath), cfg)
    return cfg


def make_paths_absolute(dir_: str, cfg: Dict[str, Any]) -> Dict[str, Any]:
    """
    Make all values for keys ending with `_path` absolute to dir_.

    Parameters
    ----------
    dir_ : str
    cfg : Dict[str, Any]

    Returns
    -------
    cfg : Dict[str, Any]
    """
    for key in cfg.keys():
        if hasattr(key, "endswith") and key.endswith("_path"):
            if cfg[key].startswith("~"):
                cfg[key] = os.path.expanduser(cfg[key])
            else:
                cfg[key] = os.path.join(dir_, cfg[key])
            cfg[key] = os.path.abspath(cfg[key])
        if type(cfg[key]) is dict:
            cfg[key] = make_paths_absolute(dir_, cfg[key])
    return cfg