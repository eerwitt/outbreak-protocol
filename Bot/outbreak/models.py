from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Metadata:
    ToolTip: Optional[str] = None
    Min: Optional[str] = None
    Max: Optional[str] = None


@dataclass_json
@dataclass
class UnderlyingProperty:
    Name: str
    DisplayName: str
    Description: str
    Type: str
    TypePath: str
    ContainerType: str
    KeyType: str
    Metadata: Metadata


@dataclass_json
@dataclass
class OwnerObject:
    Name: str
    Class: str
    Path: str


@dataclass_json
@dataclass
class ModifiedRCProperty:
    DisplayName: str
    ID: str
    UnderlyingProperty: UnderlyingProperty
    Metadata: Metadata
    OwnerObjects: List[OwnerObject]


@dataclass_json
@dataclass
class ModifiedEntities:
    ModifiedRCProperties: List[ModifiedRCProperty] = field(default_factory=list)
    ModifiedRCFunctions: List = field(default_factory=list)
    ModifiedRCActors: List = field(default_factory=list)


@dataclass_json
@dataclass
class RootObject:
    Type: str
    PresetName: str
    PresetId: str
    ModifiedEntities: ModifiedEntities

@dataclass_json
@dataclass
class RelativeLocation:
    X: float
    Y: float
    Z: float

@dataclass_json
@dataclass
class ResponseBody:
    RelativeLocation: RelativeLocation

@dataclass_json
@dataclass
class Response:
    RequestId: int
    ResponseCode: int
    ResponseBody: ResponseBody

@dataclass_json
@dataclass
class WebsocketResponse:
    RequestId: int
    ResponseCode: int
    ResponseBody: Optional[Dict[str, Any]] = None

@dataclass_json
@dataclass
class Parameters:
    RequestId: int
    Url: str
    Verb: str
    Body: Optional[Dict[str, Any]] = None

@dataclass_json
@dataclass
class WebsocketHttpRequest:
    MessageName: str
    Parameters: Parameters

@dataclass_json
@dataclass
class WebsocketRequest:
    MessageName: str
    Parameters: Dict[str, Any]

@dataclass_json
@dataclass
class FunctionHttpRequest:
    objectPath: str
    functionName: str
    parameters: Dict[str, Any]
    generateTransaction: Optional[bool] = False