import datetime
from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True)
class Metadata:
    ToolTip: Optional[str] = None
    Min: Optional[str] = None
    Max: Optional[str] = None


@dataclass_json
@dataclass(frozen=True)
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
@dataclass(frozen=True)
class OwnerObject:
    Name: str
    Class: str
    Path: str


@dataclass_json
@dataclass(frozen=True)
class ModifiedRCProperty:
    DisplayName: str
    ID: str
    UnderlyingProperty: UnderlyingProperty
    Metadata: Metadata
    OwnerObjects: List[OwnerObject]


@dataclass_json
@dataclass(frozen=True)
class ModifiedEntities:
    ModifiedRCProperties: List[ModifiedRCProperty] = field(default_factory=list)
    ModifiedRCFunctions: List = field(default_factory=list)
    ModifiedRCActors: List = field(default_factory=list)


@dataclass_json
@dataclass(frozen=True)
class RootObject:
    Type: str
    PresetName: str
    PresetId: str
    ModifiedEntities: ModifiedEntities

@dataclass_json
@dataclass(frozen=True)
class RelativeLocation:
    X: float
    Y: float
    Z: float

@dataclass_json
@dataclass(frozen=True)
class ResponseBody:
    RelativeLocation: RelativeLocation

@dataclass_json
@dataclass(frozen=True)
class Response:
    RequestId: int
    ResponseCode: int
    ResponseBody: ResponseBody

@dataclass_json
@dataclass(frozen=True)
class WebsocketResponse:
    RequestId: int
    ResponseCode: int
    ResponseBody: Optional[Dict[str, Any]] = None

@dataclass_json
@dataclass(frozen=True)
class Parameters:
    RequestId: int
    Url: str
    Verb: str
    Body: Optional[Dict[str, Any]] = None

@dataclass_json
@dataclass(frozen=True)
class WebsocketHttpRequest:
    MessageName: str
    Parameters: Parameters

@dataclass_json
@dataclass(frozen=True)
class WebsocketRequest:
    MessageName: str
    Parameters: Dict[str, Any]

@dataclass_json
@dataclass(frozen=True)
class FunctionHttpRequest:
    objectPath: str
    functionName: str
    parameters: Dict[str, Any]
    generateTransaction: Optional[bool] = False

@dataclass_json
@dataclass(frozen=True)
class GameContext:
    """
    Represents the general information about a prop in the level.
    """
    context: Dict[str, Any]

@dataclass_json
@dataclass(frozen=True)
class GameAction:
    """
    Represents a possible action available to execute in the game.
    """
    action: Dict[str, Any]

@dataclass_json
@dataclass(frozen=True)
class ChatMessage:
    """
    A Chat message to add to the prompt
    """
    timestamp: datetime.datetime
    message: str

@dataclass_json
@dataclass
class MessageContent:
    type: str
    text: str

@dataclass_json
@dataclass
class Message:
    role: str
    content: List[MessageContent]

@dataclass_json
@dataclass
class RAGRequestPayload:
    anthropic_version: str
    max_tokens: int
    top_k: int
    temperature: float
    top_p: float
    messages: List[Message]

@dataclass_json
@dataclass
class RAGResponseContent:
    type: str
    text: str

@dataclass_json
@dataclass
class Usage:
    input_tokens: int
    output_tokens: int

@dataclass_json
@dataclass
class RAGResponse:
    id: str
    type: str
    role: str
    model: str
    content: List[RAGResponseContent]
    stop_reason: Optional[str]
    stop_sequence: Optional[str]
    usage: Usage

@dataclass_json
@dataclass
class Metadata:
    ToolTip: Optional[str] = None

@dataclass_json
@dataclass
class UnderlyingProperty:
    Name: str
    Description: str
    Type: str
    ContainerType: str
    KeyType: str
    Metadata: Metadata

@dataclass_json
@dataclass
class ExposedProperty:
    DisplayName: str
    UnderlyingProperty: UnderlyingProperty

@dataclass_json
@dataclass
class Argument:
    Name: str
    Description: str
    Type: str
    ContainerType: str
    KeyType: str
    Metadata: Dict = field(default_factory=dict)

@dataclass_json
@dataclass
class UnderlyingFunction:
    Name: str
    Description: str
    Arguments: List[Argument] = field(default_factory=list)

@dataclass_json
@dataclass
class ExposedFunction:
    DisplayName: str
    UnderlyingFunction: UnderlyingFunction

@dataclass_json
@dataclass
class Group:
    Name: str
    ExposedProperties: List[ExposedProperty] = field(default_factory=list)
    ExposedFunctions: List[ExposedFunction] = field(default_factory=list)

@dataclass_json
@dataclass
class Preset:
    Name: str
    Path: str
    Groups: List[Group] = field(default_factory=list)

@dataclass_json
@dataclass
class PresetResponseBody:
    Preset: Preset

@dataclass_json
@dataclass(frozen=True)
class GameState:
    PlayerLocation: str
    PlayerAmmo: int
    PlayerGrenades: int
    PlayerHealth: float
    BearLocations: Dict[str, str] = field(default_factory=dict)  # Mapping object paths to locations
    LocationNames: List[str] = field(default_factory=list)