'''
Test script to launch a single bot to my private server.
'''
import argparse
from outbreak import bot


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='bot',
        description='Connect and share session information.',
        epilog='Requires an active game session that\'s currently available.')

    parser.add_argument(
        '--discord-token',
        required=True,
        type=str,
        help='API token from Discord for bot')
    parser.add_argument(
        '--game-host',
        required=False,
        type=str,
        default='localhost',
        help='Host of the game server')
    parser.add_argument(
        '--game-port',
        required=False,
        type=int,
        default=30020,
        help='Port of the game server')
    parser.add_argument(
        '--channel-name',
        required=True,
        type=str,
        help='Name of the channel to post to')
    args = parser.parse_args()

    discord_bot = bot.Bot(
        game_host=args.game_host,
        game_port=args.game_port,
        channel_name=args.channel_name
    )
    discord_bot.run(token=args.discord_token)