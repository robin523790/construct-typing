import binascii
import io
import typing as t

import pytest
from construct import (
    Construct,
    Container,
    EnumInteger,
    EnumIntegerString,
    ListContainer,
    SizeofError,
)
from construct.lib import (
    HexDisplayedBytes,
    HexDisplayedDict,
    HexDisplayedInteger,
    HexDumpDisplayedBytes,
    HexDumpDisplayedDict,
)

import construct_typed as cst

xfail = pytest.mark.xfail
skip = pytest.mark.skip
skipif = pytest.mark.skipif

Buffer = bytes | memoryview | bytearray
ParsedType = t.TypeVar("ParsedType")
BuildTypes = t.TypeVar("BuildTypes")
ContainerType = t.TypeVar("ContainerType", bound=cst.TContainerMixin)
T = t.TypeVar("T")

IdentType = t.TypeVar("IdentType")


class ZeroIO(io.BufferedIOBase):
    def read(self, __size: int | None = None) -> bytes:
        if __size is not None:
            return bytes(__size)
        else:
            return bytes(0)

    def read1(self, __size: int = 0) -> bytes:
        return bytes(__size)


def ident(x: IdentType) -> IdentType:
    return x


devzero: t.BinaryIO = ZeroIO()  # type: ignore


def raises(
    func: t.Callable[..., t.Any], *args: t.Any, **kw: t.Any
) -> t.Any | t.Type[Exception]:
    try:
        return func(*args, **kw)
    except Exception as e:
        return e.__class__


@t.overload
def common(
    format: cst.TStruct[ContainerType],
    datasample: Buffer,
    objsample: ContainerType | t.Dict[str, t.Any],
    sizesample: int | t.Type[Exception] = ...,
    **kw: t.Any,
) -> None: ...


@t.overload
def common(
    format: "Construct[ListContainer[ParsedType], t.Any]",
    datasample: Buffer,
    objsample: t.List[ParsedType],
    sizesample: int | t.Type[Exception] = ...,
    **kw: t.Any,
) -> None: ...


@t.overload
def common(
    format: "Construct[Container[t.Any], t.Any]",
    datasample: Buffer,
    objsample: t.Dict[str, t.Any],
    sizesample: int | t.Type[Exception] = ...,
    **kw: t.Any,
) -> None: ...


@t.overload
def common(
    format: "Construct[EnumInteger | EnumIntegerString, t.Any]",
    datasample: Buffer,
    objsample: int | str,
    sizesample: int | t.Type[Exception] = ...,
    **kw: t.Any,
) -> None: ...


@t.overload
def common(
    format: "Construct[HexDisplayedInteger, t.Any]",
    datasample: Buffer,
    objsample: HexDisplayedInteger | int,
    sizesample: int | t.Type[Exception] = ...,
    **kw: t.Any,
) -> None: ...


@t.overload
def common(
    format: "Construct[HexDisplayedBytes, t.Any]",
    datasample: Buffer,
    objsample: HexDisplayedBytes | bytes,
    sizesample: int | t.Type[Exception] = ...,
    **kw: t.Any,
) -> None: ...


@t.overload
def common(
    format: "Construct[HexDisplayedDict[str, t.Any], t.Any]",
    datasample: Buffer,
    objsample: t.Dict[str, t.Any],
    sizesample: int | t.Type[Exception] = ...,
    **kw: t.Any,
) -> None: ...


@t.overload
def common(
    format: "Construct[HexDumpDisplayedBytes, t.Any]",
    datasample: Buffer,
    objsample: HexDumpDisplayedBytes | bytes,
    sizesample: int | t.Type[Exception] = ...,
    **kw: t.Any,
) -> None: ...


@t.overload
def common(
    format: "Construct[HexDumpDisplayedDict[str, t.Any], t.Any]",
    datasample: Buffer,
    objsample: t.Dict[str, t.Any],
    sizesample: int | t.Type[Exception] = ...,
    **kw: t.Any,
) -> None: ...


@t.overload
def common(
    format: "Construct[ParsedType, t.Any]",
    datasample: Buffer,
    objsample: ParsedType,
    sizesample: int | t.Type[Exception] = ...,
    **kw: t.Any,
) -> None: ...


def common(
    format: "Construct[t.Any, t.Any]",
    datasample: Buffer,
    objsample: t.Any,
    sizesample: int | t.Type[Exception] = SizeofError,
    **kw: t.Any,
) -> None:
    obj = format.parse(datasample, **kw)
    assert obj == objsample
    data = format.build(objsample, **kw)
    assert data == datasample
    # following are implied by above (re-parse and re-build)
    # assert format.parse(format.build(obj)) == obj
    # assert format.build(format.parse(data)) == data
    if isinstance(sizesample, int):
        size = format.sizeof(**kw)
        assert size == sizesample
    else:
        size_ex = raises(format.sizeof, **kw)
        assert size_ex == sizesample


def setattrs(obj: T, **kwargs: t.Any) -> T:
    """Set multiple named values of an object"""
    for name, value in kwargs.items():
        setattr(obj, name, value)
    return obj


def commonhex(format: "Construct[t.Any, t.Any]", hexdata: str) -> None:
    commonbytes(format, binascii.unhexlify(hexdata))


def commondumpdeprecated(format: "Construct[t.Any, t.Any]", filename: str) -> None:
    filename = "tests/deprecated_gallery/blobs/" + filename
    with open(filename, "rb") as f:
        data = f.read()
    commonbytes(format, data)


def commondump(format: "Construct[t.Any, t.Any]", filename: str) -> None:
    filename = "tests/gallery/blobs/" + filename
    with open(filename, "rb") as f:
        data = f.read()
    commonbytes(format, data)


def commonbytes(format: "Construct[t.Any, t.Any]", data: bytes) -> None:
    obj = format.parse(data)
    format.build(obj)
