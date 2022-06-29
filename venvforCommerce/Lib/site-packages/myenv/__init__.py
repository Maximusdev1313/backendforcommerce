# This file is part of the myenv project
# https://gitlab.com/mbarkhau/myenv
#
# Copyright (c) 2019 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT
"""Environment variable parsing using type annotations.

NOTE: Normally you don't need to declare environ, since the
default is to just use os.environ. For this doctest however, we
don't want to manipulate the os.environ and so we create a mock
instead.

Usage:

>>> mock_environ = {
...     'CREDENTIALS_USER': "franz",
...     'CREDENTIALS_KEY': "supersecret",
... }
>>> class Credentials(BaseEnv):
...     _environ_prefix = "CREDENTIALS_"
...     user : str = "user"
...     key : str
...
>>> creds = Credentials(environ=mock_environ)
>>> creds == Credentials(user='franz', key='supersecret')
True
>>> creds.user
'franz'
>>> creds.key
'supersecret'
>>> creds._varnames()
['CREDENTIALS_USER', 'CREDENTIALS_KEY']
>>> creds._asdict()
{'user': 'franz', 'key': 'supersecret'}
>>> Credentials(environ=mock_environ) is Credentials(environ=mock_environ)
True
"""

import os
import pathlib as pl
import typing as typ


__version__ = "v201902.0007"


Environ = typ.MutableMapping[str, str]


EnvType = typ.TypeVar('EnvType', bound='BaseEnv')


def _iter_env_config(env_name: str) -> typ.Iterable[typ.Tuple[str, str]]:
    env_config_dir = os.getenv('ENV_CONFIG_DIR', ".")
    CONFIG_DIR     = pl.Path(env_config_dir) / "config"
    config_files   = [CONFIG_DIR / (env_name + ".env")]
    if env_name != 'prod':
        config_files.append(CONFIG_DIR / "prod.env")

    for config_file in config_files:
        if not config_file.exists():
            continue

        fh: typ.IO[str]

        with config_file.open(mode="rt", encoding="utf-8") as fh:
            config_lines = fh.readlines()

        for line in config_lines:
            if "=" in line and not line.startswith("#"):
                name, value = line.strip().split("=", 1)
                yield name.strip(), value


_environ_initialized: typ.Set[int] = set()


def _init_environ(environ: Environ = None) -> None:
    if id(environ) in _environ_initialized:
        return

    if environ is None:
        environ = os.environ

    env_name = os.getenv('ENV', 'prod').lower()

    for name, value in _iter_env_config(env_name):
        if name not in environ:
            environ[name] = value.strip()

    _environ_initialized.add(id(environ))


__fallback_sentinel__ = '__fallback_sentinel__'

# NOTE (2018-11-30 mb): I couldn't find out how to express
#   that a parameter one of a few type itself, rather than
#   an instance of one of a few types.
FieldType = typ.Any

# FieldValue = typ.Union[str, int, float, bool, pl.Path]
FieldValue     = typ.Any
ListFieldValue = typ.List[typ.Any]


def _parse_bool(val: str) -> bool:
    if val.lower() in ("1", "true"):
        return True
    elif val.lower() in ("0", "false"):
        return False
    else:
        raise ValueError(val)


def _parse_list_val(val: str, ftype: FieldType) -> ListFieldValue:
    maybe_args: typ.Optional[typ.Tuple[type]] = getattr(ftype, '__args__', None)
    if maybe_args is None:
        raise TypeError(ftype)

    if len(maybe_args) == 1:
        member_type: type = maybe_args[0]
    else:
        raise TypeError(ftype)

    list_strvals = [strval for strval in val.split(os.pathsep)]

    if issubclass(member_type, str):
        return list_strvals
    elif issubclass(member_type, pl.Path):
        return [pl.Path(listval) for listval in list_strvals]
    elif issubclass(member_type, int):
        return [int(listval, 10) for listval in list_strvals]
    elif issubclass(member_type, float):
        return [float(listval) for listval in list_strvals]
    elif issubclass(member_type, bool):
        return [_parse_bool(listval) for listval in list_strvals]
    else:
        raise TypeError(ftype)


def _parse_val(val: str, ftype: type) -> FieldValue:
    ftype_type = type(ftype)
    if ftype_type == type:
        if issubclass(ftype, str):
            return val
        elif issubclass(ftype, bool):
            return _parse_bool(val)
        elif issubclass(ftype, int):
            return int(val, 10)
        elif issubclass(ftype, float):
            return float(val)
        elif issubclass(ftype, pl.Path):
            return pl.Path(val)
        else:
            raise TypeError(ftype)
    elif str(ftype).startswith("typing.List["):
        return _parse_list_val(val, ftype)
    elif str(ftype).startswith("typing.Set["):
        return set(_parse_list_val(val, ftype))
    elif callable(ftype):
        return ftype(val)
    else:
        raise TypeError(ftype)


# Cache for already loaded environment configs. Environment
# variables are only parsed once during initialization.

EnvMapKey = typ.Tuple[typ.Type[EnvType], int]
EnvMap    = typ.Dict[EnvMapKey, EnvType]

_envmap: EnvMap = {}


# NOTE (2019-02-24 mb): Could never get this to work,
#   I thought it was more important to spend time on
#   test coverage.
# EnvironKWArgs = mypyext.TypedDict('EnvironKWArgs', {'environ': Environ})


class _Singleton(type):
    def __call__(cls, *args, **kwargs) -> EnvType:
        env_cls = typ.cast(typ.Type[EnvType], cls)

        environ: Environ
        if 'environ' in kwargs:
            environ = kwargs['environ']
        elif not kwargs:
            environ = os.environ
        else:
            # init with kwargs (not via environ)
            return env_cls.__new__(env_cls, *args, **kwargs)

        envmap_key = (env_cls, id(environ))

        if envmap_key not in _envmap:
            _init_environ(environ)
            _envmap[envmap_key] = env_cls.__new__(env_cls, environ=environ)

        return _envmap[envmap_key]


class _Field(typ.NamedTuple):

    fname   : str
    ftyp    : FieldType
    env_key : str
    fallback: FieldValue


InitKWArgs = typ.MutableMapping[str, typ.Any]


class BaseEnv(metaclass=_Singleton):
    """The main Base class.

    Subclasses of BaseEnv are only instantiated once (singleton).
    """

    _environ_prefix: typ.Optional[str] = None

    @classmethod
    def _iter_fields(cls) -> typ.Iterable[_Field]:
        prefix = cls._environ_prefix or ""
        for fname, ftyp in cls.__annotations__.items():
            fallback = getattr(cls, fname, __fallback_sentinel__)
            env_key  = (prefix + fname).upper()
            yield _Field(fname, ftyp, env_key, fallback)

    @classmethod
    def _update_kwargs_from_environ(cls, environ: Environ) -> InitKWArgs:
        typename = cls.__name__
        init_kwargs: InitKWArgs = {}

        for field in cls._iter_fields():
            if field.env_key in environ:
                try:
                    raw_env_val = environ[field.env_key]
                    init_kwargs[field.fname] = _parse_val(raw_env_val, field.ftyp)
                except ValueError as err:
                    raise ValueError(
                        f"Invalid value '{raw_env_val}' for {field.env_key}. "
                        f"Attepmted to parse '{typename}.{field.fname}' with '{field.ftyp}'.",
                        err,
                    )
            elif field.fallback != __fallback_sentinel__:
                init_kwargs[field.fname] = field.fallback
            else:
                raise KeyError(
                    f"No environment variable {field.env_key} "
                    + f"found for field {typename}.{field.fname}"
                )

        return init_kwargs

    def __new__(cls, *args, **kwargs) -> EnvType:
        """Create a new env instance.

        This should not be called from outside of myenv.
        """
        init_kwargs: InitKWArgs

        if 'environ' in kwargs:
            init_kwargs = cls._update_kwargs_from_environ(kwargs['environ'])
        else:
            init_kwargs = kwargs

        env = super(BaseEnv, cls).__new__(cls)
        env.__init__(*args, **init_kwargs)
        return env

    def __init__(self, *args, **kwargs) -> None:
        for key, val in kwargs.items():
            setattr(self, key, val)

    def _varnames(self) -> typ.List[str]:
        """Create list with names as they are read from os.environ and configs.

        >>> creds = Credentials(user='franz', key='supersecret')
        >>> creds._varnames()
        ['CREDENTIALS_USER', 'CREDENTIALS_KEY']
        """
        prefix = self._environ_prefix or ""
        return [
            (prefix + attrname).upper()
            for attrname in type(self).__annotations__
            if not attrname.startswith("_")
        ]

    def _asdict(self) -> typ.Dict[str, typ.Any]:
        """Create a dict populated with keys/values from annotated fields.

        >>> creds = Credentials(user='franz', key='supersecret')
        >>> creds._asdict()
        {'user': 'franz', 'key': 'supersecret'}
        """
        return {
            field.fname: getattr(self, field.fname)
            for field in self._iter_fields()
            if not field.fname.startswith("_")
        }

    def __eq__(self, other: object) -> bool:
        """Deep equality check for all annotated fields."""
        return isinstance(other, BaseEnv) and self._asdict() == other._asdict()


def parse(env_type: typ.Type[EnvType], environ: Environ = os.environ) -> EnvType:
    """Create an instance of an env.

    This is depricated, just instantiate like a normal class
    - myenv.parse(MyEnv)
    + MyEnv()
    """
    return env_type(environ=environ)


class Credentials(BaseEnv):
    """Helper class used in doc tests."""

    _environ_prefix: str = "CREDENTIALS_"
    user           : str = "user"
    key            : str


def __self_test():
    """Some code for mypy to type check.

    Since the unittests are not type checked, this code is to make sure
    that access to the properties of a subclass of BaseEnv are indeed
    detected to be of the declared type. Considering that these fields are
    always populated only after runtime type checks (which are opaque to
    mypy) this bit of code demonstrates that the whole purpose of this
    library is being satisfied.
    """

    class _TestEnv(BaseEnv):
        str_val  : str
        int_val  : int
        bool_val : bool
        float_val: float
        strs_val : typ.List[str]
        ints_val : typ.Set[int]
        path_val : pl.Path
        paths_val: typ.List[pl.Path]

    environ: Environ = {
        'STR_VAL'  : "bar",
        'INT_VAL'  : "123",
        'BOOL_VAL' : "TRUE",
        'FLOAT_VAL': "123.456",
        'STRS_VAL' : "baz:buz",
        'INTS_VAL' : "7:89",
        'PATH_VAL' : "fileA.txt",
        'PATHS_VAL': "fileA.txt:fileB.txt:fileC.txt",
    }

    testenv = _TestEnv(environ=environ)
    str_val: str = testenv.str_val
    assert str_val == "bar"
    int_val: int = testenv.int_val
    assert int_val == 123
    bool_val: bool = testenv.bool_val
    assert bool_val
    float_val: float = testenv.float_val
    assert float_val == 123.456
    strs_val: typ.List[str] = testenv.strs_val
    assert strs_val == ["baz", "buz"]
    ints_val: typ.Set[int] = testenv.ints_val
    assert ints_val == {7, 89}
    path_val: pl.Path = testenv.path_val
    assert path_val == pl.Path("fileA.txt")
    paths_val: typ.List[pl.Path] = testenv.paths_val
    assert paths_val == [pl.Path("fileA.txt"), pl.Path("fileB.txt"), pl.Path("fileC.txt")]
