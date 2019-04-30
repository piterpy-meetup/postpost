import typing

# Recursive types are not supported yet https://github.com/python/mypy/issues/731
JSON = typing.Union[  # type: ignore
    str,
    int,
    float,
    bool,
    None,
    typing.Mapping[str, 'JSON'],
    typing.List['JSON'],
]
