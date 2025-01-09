"""
Test script used to connect to the UE5 remote and watch for preset fields changing.

python main.py --hostname localhost --port 30020
"""
import argparse
import asyncio
import json
import logging

from outbreak.client import UE5RemoteControlClient, add_uepie_prefix
from outbreak.models import RootObject, Response

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


async def process_preset_message(message, client):
    """
    Example callback function to process each preset message.

    Args:
        message (dict): The preset message received from the WebSocket.
    """
    logger.info("Processing preset message.")
    to_watch = set()
    if type(message) == RootObject:
        for property in message.ModifiedEntities.ModifiedRCProperties:
            for owner in property.OwnerObjects:
                relative_location_response = await client.read_object_property(object_path=owner.Path, property_name="RelativeLocation")
                relative_location = Response.from_dict(relative_location_response)
                logger.info(f"{property.DisplayName} {owner.Path} {relative_location.ResponseBody.RelativeLocation}")
                to_watch.add(owner.Path)
    else:
        logger.info(json.dumps(message))

    try:
        timeout = 5.0  # Maximum wait time for a response in seconds
        for _ in range(1):
            for object_path in to_watch:
                response = await client.read_object_property(object_path=add_uepie_prefix(object_path), property_name="RelativeLocation", timeout=timeout)
                logger.info(f"{object_path} {response}")
            await asyncio.sleep(2)
    except asyncio.TimeoutError:
        logger.error("Failed to receive a response within the specified timeout.")


def main():
    """
    Parse command-line arguments and start the UE5 Remote Control WebSocket client.
    """
    parser = argparse.ArgumentParser(description="UE5 WebSocket Remote Control client.")
    parser.add_argument("--hostname", type=str, default="localhost", help="The hostname of the WebSocket server.")
    parser.add_argument("--port", type=int, default=30020, help="The port of the WebSocket server.")
    args = parser.parse_args()

    # Create the client and perform tasks asynchronously
    client = UE5RemoteControlClient(args.hostname, args.port)

    async def run_client():
        try:
            await client.connect()
            response = await client.call_object_function("/Game/LBG/Maps/L_LBG_Medow.L_LBG_Medow:PersistentLevel.BorisPlayerCharacter_C_0", "GetClosestLocationName", {})
            logger.info(response)
            logger.info("Starting loop to read object property...")
            await client.register_preset("SurvivalManagerPreset", lambda message: process_preset_message(message, client))

            # Example creating a thumbnail
            # response = await client.get_object_thumbnail(object_path="/Game/ParagonBoris/Characters/Heroes/Boris/BorisPlayerCharacter.BorisPlayerCharacter", timeout=5.0)
            # with open("thumbnail.png", "wb") as f:
            #     import base64
            #     f.write(base64.b64decode(response["ResponseBody"]))
        finally:
            await client.disconnect()

    asyncio.run(run_client())


if __name__ == "__main__":
    main()