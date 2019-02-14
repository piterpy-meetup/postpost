import typing

JSON = typing.Union[  # type: ignore
    str,
    int,
    float,
    bool,
    None,
    typing.Mapping[str, 'JSON'],
    typing.List['JSON'],
]
