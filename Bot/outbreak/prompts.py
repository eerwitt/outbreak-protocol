import datetime
from outbreak.models import GameContext, GameAction, ChatMessage


class RAGPromptGenerator:
    """
    A class to generate prompts for a RAG system, incorporating game context,
    available actions, and recent chat messages.
    """
    def __init__(self):
        self.contexts = list()
        self.actions = list()
        self.chat_messages = list()
        self.previous_messages = list()

    def clear_contexts(self):
        self.contexts.clear()

    def clear_actions(self):
        self.actions.clear()

    def clear_chat_messages(self):
        self.chat_messages.clear()

    def add_context(self, context: GameContext):
        self.contexts.append(context)

    def add_action(self, action: GameAction):
        self.actions.append(action)

    def add_chat_message(self, message: str, timestamp: datetime.datetime):
        """Adds a new chat message, maintaining a maximum of 10 messages."""
        if len(self.chat_messages) >= 2:
            # Removes a random message, not necessarily the oldest
            self.chat_messages.pop()

        self.chat_messages.append(ChatMessage(message=message, timestamp=timestamp))

    def add_previous_message(self, message: str):
        self.previous_messages.append(ChatMessage(message=message, timestamp=datetime.datetime.now()))

    def generate_prompt(self) -> str:
        """
        Generates a string combining the context, actions,
        and recent chat messages for use in a RAG system.

        Returns:
            A string ready for LLM input.
        """
        context_jsonl = "\n".join([context.to_json() for context in self.contexts])
        actions_jsonl = "\n".join([action.to_json() for action in self.actions])
        chat_messages_jsonl = "\n".join([chat_message.to_json() for chat_message in self.chat_messages])
        previous_messages_jsonl = "\n".join([previous_message.to_json() for previous_message in self.previous_messages])

        prompt_template = f"""
You are responsible for making a player have fun in a Zombie FPS with Bears.
The game consists of surviving in a dangerous meadow where you will spawn chaotic challenges.
Only use the available actions.
Based on the provided context, available actions, and recent chat messages, manage the fun in the game.

Respond in JSON format, suggest actions to create a fun experience.

If you have notes or improvements to the list of available actions, place these details in the Notes section of the header.

Example response schema:
{{
    "Header": {{
        "DescriptionOfWhatToDo": "Summarize actions that will take place.",
        "Notes": "Any additional notes or feedback you have."
    }},
    "Actions": [
    ]
}}

The current game state in JSONl format surrounded by xml markers <context></context>:
<context>
{context_jsonl}
</context>

The available actions in JSONl format surrounded by xml markers <actions></actions>
<actions>
{{"Name": "Wait", "Arg1": "Amount of time to wait in seconds", "Reason": "Reason why to do this action."}}
{{"Name": "Chat", "Arg1": "Very short (under 30 character), sarcastic message to send to the player, can rarely include emojis but keep trying different emojis", "Reason": "Reason why to do this action."}}
{{"Name": "Spawn", "Arg1": "Object friendly name (Bear, GasCan, Ammo, Grenade, Toilet)", "Arg2": "Location friendly name (Pond, Van, Meadow, Hill, River)", "Reason": "Reason why to do this action."}}
{{"Name": "MoveTo", "Arg1": "Object ID", "Arg2": "Location friendly name (Pond, Van, Meadow, Hill, River)", "Reason": "Reason why to do this."}}
{{"Name": "TeleportPlayer", "Arg1": "Player", "Arg2": "Location friendly name (Pond, Van, Meadow, Hill, River), do not use too often.", "Reason": "Reason why to do this."}}
{actions_jsonl}
</actions>

The chat messages in JSONl format surrounded by xml markers <chat_messages></chat_messages>
<chat_messages>
{chat_messages_jsonl}
</chat_messages>

Your previous messages to players, do not repeat in JSONl format surrounded by xml markers <previous_messages></previous_messages>
<previous_messages>
{previous_messages_jsonl}
</previous_messages>

Rules
- Only respond to game queries.
- Never claim to search online, access external data, or use tools besides the game.
- Only the game connection for data. Never guess or make up information.
- Only use the available actions with the provided contexts to make requests.
- If the action doesn't exist in the list of <actions>, do not attempt to take it.
""".strip()

        return prompt_template
