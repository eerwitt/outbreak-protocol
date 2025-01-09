"""
UE5 WebSocket Remote Control Client

This module provides a WebSocket client implementation for interacting with the Unreal Engine 5
Remote Control API. The client enables connecting to a WebSocket server, registering and unregistering
for Remote Control presets, writing AI stimuli, and listening for updates related to presets.

Classes:
    UE5RemoteControlClient: A class for managing WebSocket connections and interacting with
                            the Unreal Engine 5 Remote Control API.
"""
import asyncio
import json
import logging
import re
import uuid
import websockets
from websockets.exceptions import ConnectionClosedError, InvalidURI, InvalidHandshake

from outbreak import models

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class UE5RemoteControlClient:
    """
    A class to handle asynchronous WebSocket connections to the Unreal Engine 5 Remote Control server.
    """

    def __init__(self, hostname: str, port: int):
        """
        Initialize the WebSocket client with the given hostname and port.

        Args:
            hostname (str): The hostname of the WebSocket server.
            port (int): The port of the WebSocket server.
        """
        self.hostname = hostname
        self.port = port
        self.uri = f"ws://{hostname}:{port}"
        self.websocket = None

    async def connect(self):
        """
        Connect to the WebSocket server.
        """
        try:
            self.websocket = await websockets.connect(self.uri)
            logger.info(f"Connected to WebSocket server at {self.uri}")
        except InvalidURI:
            logger.error(f"Invalid WebSocket URI: {self.uri}")
            raise
        except InvalidHandshake:
            logger.error(f"Handshake failed while connecting to {self.uri}")
            raise
        except ConnectionRefusedError:
            logger.error(f"Connection refused by the server at {self.uri}")
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred while connecting: {e}")
            raise

    def generate_request_id(self) -> int:
        """
        Generate a unique UUID and return it as an integer.

        Returns:
            int: A unique request ID based on a UUID.
        """
        unique_id = uuid.uuid4()  # Generate a unique UUID
        request_id = unique_id.int  # Convert the UUID to an integer
        return request_id

    async def register_preset(self, preset_name: str, message_callback):
        """
        Register to a Remote Control Preset on the server and start listening for messages.

        Args:
            preset_name (str): The name of the preset to register.
            message_callback (function): A callback function to execute for each message.
        """
        if not self.websocket:
            logger.error("WebSocket is not connected. Please connect first.")
            return
        message = models.WebsocketRequest(
            MessageName="preset.register",
            Parameters={
                "PresetName": preset_name
            }
        )

        try:
            await self.websocket.send(message.to_json())
            logger.info(f"Sent registration message: {message}")

            # Start listening for messages about the preset
            logger.info(f"Listening for updates to preset: {preset_name}")
            async for preset_message in self.on_message():
                await message_callback(preset_message)

        except ConnectionClosedError as e:
            logger.error(f"Connection closed unexpectedly: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")

    async def on_message(self):
        """
        Listen for new messages on the WebSocket and yield them to the caller.

        Yields:
            dict: The parsed JSON message received from the WebSocket.
        """
        try:
            async for message in self.websocket:
                try:
                    parsed_message = json.loads(message)
                    if parsed_message.get("Type") == "PresetEntitiesModified":
                        yield models.RootObject.from_dict(parsed_message)
                    else:
                        yield parsed_message

                except json.JSONDecodeError:
                    logger.warning(f"Failed to decode message: {message}")
        except ConnectionClosedError as e:
            logger.error(f"Connection closed unexpectedly while listening for messages: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred while listening for messages: {e}")

    async def unregister_preset(self, preset_name: str):
        """
        Unregister from a Remote Control Preset on the server.

        Args:
            preset_name (str): The name of the preset to unregister.
        """
        message = models.WebsocketRequest(
            MessageName="preset.unregister",
            Parameters={
                "PresetName": preset_name
            }
        )

        return await self.make_request(message.to_json())

    async def read_object_property(self, object_path: str, property_name: str, timeout: float = 5.0):
        """
        Send a request to read a property of the specified object with READ_ACCESS.

        Args:
            object_path (str): The path of the object to query.
        """
        request_id = self.generate_request_id()
        message = models.WebsocketHttpRequest(
            MessageName="http",
            Parameters=models.Parameters(
                RequestId=request_id,
                Url="/remote/object/property",
                Verb="PUT",
                Body={
                    "ObjectPath": object_path,
                    "PropertyName": property_name,
                    "Access": "READ_ACCESS"
                }
            )
        )

        return await self.make_request(message.to_json(), timeout=timeout)

    async def write_object_property(self, object_path: str, property_name: str, value: float):
        """
        Write an object property.

        Args:
            object_path (str): The object path to target.
            property_name (str): The property to update.
            value (float): The value to write.
        """
        request_id = self.generate_request_id()
        message = models.WebsocketHttpRequest(
            MessageName="http",
            Parameters=models.Parameters(
                RequestId=request_id,
                Url="/remote/object/property",
                Verb="PUT",
                Body={
                    "ObjectPath": object_path,
                    "propertyName": property_name,
                    "access": "WRITE_ACCESS",
                    "value": value
                }
            )
        )
        return await self.make_request(message.to_json())

    async def get_object_thumbnail(self, object_path: str, timeout: float = 5.0):
        """
        Send a request to retrieve the thumbnail image of a specified object.

        Args:
            object_path (str): The path of the object to retrieve the thumbnail for.
            timeout (float): The maximum time to wait for a response, in seconds. Defaults to 5 seconds.

        Returns:
            dict: The JSON response from the WebSocket server containing thumbnail data.

        Raises:
            asyncio.TimeoutError: If the response is not received within the timeout period.
        """
        request_id = self.generate_request_id()
        message = models.WebsocketHttpRequest(
            MessageName="http",
            Parameters=models.Parameters(
                RequestId=request_id,
                Url="/remote/object/thumbnail",
                Verb="PUT",
                Body={
                    "ObjectPath": object_path
                }
            )
        )

        return await self.make_request(message.to_json(), timeout=timeout)

    async def call_object_function(self, object_path: str, function_name: str, parameters: dict, timeout: float = 5.0):
        """
        Send a request to call a function on the specified object with READ_ACCESS.

        Args:
            object_path (str): The path of the object to query.
            function_name (str): The name of the function to call.
            parameters (dict): The parameters to pass to the function.
        """
        request_id = self.generate_request_id()
        message = models.WebsocketHttpRequest(
            MessageName="http",
            Parameters=models.Parameters(
                RequestId=request_id,
                Url="/remote/object/call",
                Verb="PUT",
                Body=models.FunctionHttpRequest(
                    objectPath=object_path,
                    functionName=function_name,
                    parameters=parameters,
                    generateTransaction=False
                ).to_dict()
            )
        )

        response = await self.make_request(message.to_json(), timeout=timeout)
        return models.WebsocketResponse.from_dict(response)

    async def batch_request(self, requests):
        """
        Send a batch of requests to the WebSocket server.

        Args:
            requests (list): A list of dictionaries representing the requests to send.
        """
        request_id = self.generate_request_id()
        message = models.WebsocketHttpRequest(
            MessageName="http",
            Parameters=models.Parameters(
                RequestId=request_id,
                Url="/remote/batch",
                Verb="PUT",
                Body={
                    "Requests": requests
                }
            )
        )

        return await self.make_request(message.to_json())

    async def make_request(self, request: str, timeout: float = 5.0) -> str:
        """
        Send a request to the WebSocket server and return the response.

        Args:
            request (str): The request to send.
            timeout (float): Amount of time to wait before cancelling.

        Returns:
            str: The response from the WebSocket server.
        """
        if not self.websocket:
            logger.error("WebSocket is not connected. Please connect first.")
            raise Exception("WebSocket is not connected. Please connect first.")

        try:
            await self.websocket.send(request)
            logger.debug(f"Sent request: {request}")
            response = await asyncio.wait_for(self.websocket.recv(), timeout=timeout)
            logger.debug(f"Received response: {response}")
            return json.loads(response)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse response as JSON: {e}")
        except asyncio.TimeoutError:
            logger.error(f"Timeout occurred while waiting for response (timeout={timeout}s).")
        except ConnectionClosedError as e:
            logger.error(f"Connection closed unexpectedly: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")

        return None

    async def disconnect(self):
        """
        Disconnect from the WebSocket server.
        """
        if self.websocket:
            await self.websocket.close()
            logger.info("Disconnected from WebSocket server.")
        else:
            logger.warning("WebSocket was not connected.")


def add_uepie_prefix(object_path: str, instance_number: int = 0) -> str:
    """
    Parses an Unreal Engine object path and adds the UEDPIE_<instance_number>_ prefix
    before the map name to support Play In Editor (PIE).

    Args:
        object_path (str): The Unreal Engine object path.
        instance_number (int): The instance number of the map (usually 0).

    Returns:
        str: The updated object path with the UEDPIE_<instance_number>_ prefix.
    """
    # Regular expression to match the object path format
    pattern = r"^(?P<path>.*)/(?P<map_name>[^\./]+)(?P<rest>\.[^/]+)$"
    
    # Match the object path
    match = re.match(pattern, object_path)
    if not match:
        raise ValueError(f"Invalid Unreal Engine object path format: {object_path}")
    
    # Extract parts of the path
    path = match.group("path")
    map_name = match.group("map_name")
    rest = match.group("rest")
    
    # Add the UEDPIE_<instance_number>_ prefix to the map name
    new_map_name = f"UEDPIE_{instance_number}_{map_name}"
    
    # Reconstruct the object path
    updated_path = f"{path}/{new_map_name}{rest}"
    return updated_path
