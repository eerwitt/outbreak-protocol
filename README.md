# Outbreak Protocol (WIP)
A zombie-inspired FPS where deadly bears meet emergent, AI-driven chaos.

![Intensify Spawn](Source/Media/intensify-spawn.gif)
![Added Urgency](Source/Media/added-urgency.gif)
![Challenge](Source/Media/challenge.gif)
![Low Ammo](Source/Media/low-ammo.gif)
![Spawn](Source/Media/spawn.gif)

*"Make the bear chasing him deaf and angry"*

What makes this game unique? Your friends can collaborate and discuss strategies in natural language with a custom Discord bot powered by Amazon Bedrock. This bot interprets their conversations and translates them into in-game chaos, creating emergent behavior and unpredictable gameplay moments.

Created for the [AWS Game Builder Challenge '24](https://awsdevchallenge.devpost.com/)

## How It Works
Behind the scenes, Outbreak Protocol is powered by cutting-edge AWS services that bring the chaos to life:

1. **Amazon Bedrock**
    * Powers the Retrieval-Augmented Generation (RAG) system that processes natural language discussions and converts them into actionable in-game events.
    * What this means: Your friends casually chat with the bot, whether conspiring to “make things harder” or “summon more bears”, and the bot will interpret these ideas to create dynamic and emergent gameplay scenarios.
1. **Amazon GameLift**
    * Dedicated game servers to ensure smooth gameplay and persistent bear threats.
1. **Amazon EKS**
    * Hosts the Discord bot in a dedicated Kubernetes cluster for optimal performance.
    * What this means: All interactions with the bot are processed in real time, enabling fast responses to player conversations.

## Gameplay Features

### AI-Driven Chaos
Your friends don’t just type commands—they chat naturally with the bot about how to disrupt your gameplay and strategize.

Examples of natural language interactions:
* "What if we had more bears show up right now?"
* "Let’s make that bear over there angry."
* "Can you blow something up to scare them?"

The bot intelligently processes these conversations, generating unpredictable and exciting in-game events.

### Unpredictable Bears
Zombie bears react dynamically based on the bot’s output, creating unique experiences every time you play.

### Emergent Behavior

Thanks to the RAG-based bot, the game evolves organically. Friends can collaborate with the bot to create chaos!

## Technical Details
The Outbreak Protocol was built using the following AWS services:

1. **Amazon Bedrock**: Enables natural language processing via RAG technology, converting conversations into emergent in-game behavior.
1. **Amazon GameLift**: Dedicated game server support for reliable and scalable gameplay.
1. **Amazon EKS**: Ensures high availability and performance for the Discord bot.

### Fantastic UE5 Samples Used
* [Realistic Assault Rifle Template](https://www.fab.com/listings/05dbb53b-d75f-4a08-bcc2-fc02de484866)
* [Meadow - Environment Set](https://www.fab.com/listings/4f61d2d7-8d6f-4817-890d-17a6ba2287af)
* [Post Soviet Bathroom](https://www.fab.com/listings/f3964980-8332-414a-9e92-0d172d3a235c)
* [Post-Soviet Village](https://www.fab.com/listings/214992bc-8f89-4823-ab14-3ac2dd131e91)
* [Paragon: Boris](https://www.fab.com/listings/2e32cbb8-b415-4c39-962f-a687c64263bd)
* [Realistic Starter VFX Pack Vol 2](https://www.fab.com/listings/ac2818b3-7d35-4cf5-a1af-cbf8ff5c61c1)
* [Environment SFX from Artlist](https://artlist.io/)

## How to Play

Spawn in the toilet and enter the chaotic meadow filled with deadly zombie bears.

Add the custom Discord bot to your Discord server. Let your friends chat naturally with it to create chaos.

Avoid bears, dodge explosions, and watch as your friends’ conversations lead to unexpected gameplay twists.

## What Makes This Unique?
* **Natural Language Interaction**: The bot interprets your friends’ casual conversations to create dynamic in-game events, from summoning new threats to modifying bear behavior.
* **Emergent Gameplay**: No two playthroughs are the same. The AI adapts to player interactions, creating unpredictable and memorable moments.
* **Cutting-Edge Technology**: Powered by Amazon Bedrock’s RAG capabilities, the bot pushes the boundaries of traditional game mechanics by enabling AI-driven chaos.

Explore Outbreak Protocol and see how AWS services power the perfect blend of survival horror and AI-driven chaos.


## Updates from the LLM

```
{'Name': 'Spawn', 'Arg1': 'Bear', 'Arg2': 'Shack', 'Reason': "Introduce unexpected bear threat near player's potential safe zone"}
{'Name': 'Chat', 'Arg1': 'Bears incoming! 🐻', 'Reason': 'Alert player to imminent danger and create tension'}
{'Name': 'Spawn', 'Arg1': 'Ammo', 'Arg2': 'Van', 'Reason': 'Provide additional resources to help player survive bear encounter'}
{'Name': 'Wait', 'Arg1': '5', 'Reason': 'Create suspense and allow player to prepare for bear threat'}
{'Name': 'Chat', 'Arg1': "They're getting closer... 😱", 'Reason': "Maintain player's sense of urgency and excitement"}
{'Name': 'Spawn', 'Arg1': 'Bear', 'Arg2': 'Meadow', 'Reason': 'Introduce immediate threat to keep player alert and create tension'}
{'Name': 'Chat', 'Arg1': 'Bears smell your fear! 🐻', 'Reason': 'Add dramatic tension and hint at incoming challenge'}
{'Name': 'Spawn', 'Arg1': 'Ammo', 'Arg2': 'Hill', 'Reason': 'Provide strategic resource for player survival'}
{'Name': 'Wait', 'Arg1': 5, 'Reason': 'Create suspenseful pause before next action'}
{'Name': 'Spawn', 'Arg1': 'Grenade', 'Arg2': 'River', 'Reason': 'Give player additional tactical option for bear defense'}
{'Name': 'Spawn', 'Arg1': 'Bear', 'Arg2': 'Meadow', 'Reason': 'Introduce immediate threat to increase player adrenaline'}
{'Name': 'Chat', 'Arg1': 'Bears incoming! Watch your back! 🐻', 'Reason': 'Create tension and warn player of imminent danger'}
{'Name': 'Spawn', 'Arg1': 'Ammo', 'Arg2': 'Van', 'Reason': 'Provide strategic resource near potential escape route'}
{'Name': 'Wait', 'Arg1': '5', 'Reason': 'Allow player time to react and prepare for bear encounter'}
{'Name': 'Chat', 'Arg1': 'More zombear friends joining the party! 🧟\u200d♂️🐻', 'Reason': 'Escalate challenge and maintain excitement'}
{'Name': 'Chat', 'Arg1': 'Bears closing in! 🐻', 'Reason': 'Create immediate tension and alert the player to incoming threat'}
{'Name': 'Spawn', 'Arg1': 'Bear', 'Arg2': 'Meadow', 'Reason': "Introduce additional threat near player's location to increase challenge"}
{'Name': 'Spawn', 'Arg1': 'Ammo', 'Arg2': 'Shack', 'Reason': 'Provide player with additional resources to fight incoming bears'}
{'Name': 'Chat', 'Arg1': 'Zombears hungry! 🧟\u200d♂️🐻', 'Reason': 'Maintain high-energy narrative and hint at unique zombie bear threat'}
{'Name': 'Wait', 'Arg1': '3', 'Reason': 'Create brief suspense before next action'}
{'Name': 'Spawn', 'Arg1': 'Bear', 'Arg2': 'Pond', 'Reason': "Introduce immediate threat to player's current location"}
{'Name': 'Chat', 'Arg1': 'Zombear behind you! 😱', 'Reason': 'Create tension and alert player to imminent danger'}
{'Name': 'Spawn', 'Arg1': 'Grenade', 'Arg2': 'Meadow', 'Reason': 'Provide additional tactical resource for player survival'}
{'Name': 'Wait', 'Arg1': 3, 'Reason': 'Allow brief moment of suspense before next action'}
{'Name': 'Chat', 'Arg1': 'More bears incoming! 🐻', 'Reason': 'Maintain high-intensity gameplay atmosphere'}
{'Name': 'Spawn', 'Arg1': 'Bear', 'Arg2': 'Meadow', 'Reason': 'Continue escalating challenge and threat level'}
{'Name': 'Chat', 'Arg1': 'Zombears closing in! 🐻', 'Reason': 'Build tension and warn player of imminent danger'}
{'Name': 'Spawn', 'Arg1': 'Bear', 'Arg2': 'Hill', 'Reason': "Spawn a bear near player's current location to create immediate threat"}
{'Name': 'Spawn', 'Arg1': 'Ammo', 'Arg2': 'Hill', 'Reason': 'Provide some additional ammo to help player survive'}
{'Name': 'Chat', 'Arg1': 'One shot left? Good luck! 😱', 'Reason': "Emphasize player's low health and create dramatic tension"}
{'Name': 'Spawn', 'Arg1': 'Bear', 'Arg2': 'Meadow', 'Reason': 'Create additional threat from another direction'}
{'Name': 'Spawn', 'Arg1': 'Bear', 'Arg2': 'Forest', 'Reason': "Introduce unexpected threat near player's current location"}
{'Name': 'Chat', 'Arg1': 'Zombears in the forest! 🐻', 'Reason': 'Alert player to imminent danger and increase tension'}
{'Name': 'Spawn', 'Arg1': 'Ammo', 'Arg2': 'Hill', 'Reason': 'Provide strategic resupply point for player survival'}
{'Name': 'Wait', 'Arg1': 5, 'Reason': 'Create suspense and allow player to react to new threats'}
{'Name': 'Chat', 'Arg1': 'More bears incoming! Watch out! 😱', 'Reason': 'Maintain high-intensity gameplay atmosphere'}
{'Name': 'Spawn', 'Arg1': 'Ammo', 'Arg2': 'Van', 'Reason': 'Provide player with additional ammunition given low health status'}
{'Name': 'Spawn', 'Arg1': 'Bear', 'Arg2': 'Forest', 'Reason': 'Create tension by spawning a zombie bear in a different location from player'}
{'Name': 'Chat', 'Arg1': 'Zombears smell weakness! 🐻', 'Reason': "Increase player's sense of urgency and immersion"}
{'Name': 'Wait', 'Arg1': '15', 'Reason': 'Allow player time to strategize and react to new challenges'}
{'Name': 'Spawn', 'Arg1': 'Grenade', 'Arg2': 'Hill', 'Reason': 'Provide tactical option for player survival'}
{'Name': 'Spawn', 'Arg1': 'Bear', 'Arg2': 'Hill', 'Reason': "Spawn a bear near the player's current location to create immediate tension"}
{'Name': 'Chat', 'Arg1': 'Zombear right behind you! 😱', 'Reason': 'Create a sense of urgency and surprise'}
{'Name': 'Spawn', 'Arg1': 'Grenade', 'Arg2': 'Meadow', 'Reason': 'Provide an additional tactical resource for the player'}
{'Name': 'Wait', 'Arg1': 3, 'Reason': 'Give player a brief moment to react to the spawned bear'}
{'Name': 'Chat', 'Arg1': 'More zombears incoming! 🐻', 'Reason': 'Maintain the high-tension atmosphere'}
{'Name': 'Spawn', 'Arg1': 'Bear', 'Arg2': 'Forest', 'Reason': 'Introduce unexpected threat to increase tension'}
{'Name': 'Spawn', 'Arg1': 'Bear', 'Arg2': 'Hill', 'Reason': 'Create multi-directional threat to keep player alert'}
{'Name': 'Chat', 'Arg1': 'Zombears converging! 🐻', 'Reason': 'Warn player of impending danger and maintain excitement'}
{'Name': 'Wait', 'Arg1': 5, 'Reason': 'Allow tension to build and give player time to react'}
{'Name': 'Spawn', 'Arg1': 'Ammo', 'Arg2': 'Meadow', 'Reason': "Provide strategic resource to maintain player's combat readiness"}
{'Name': 'Spawn', 'Arg1': 'Bear', 'Arg2': 'Forest', 'Reason': 'Create tension by spawning zombear in nearby forest location'}
{'Name': 'Spawn', 'Arg1': 'Ammo', 'Arg2': 'Van', 'Reason': 'Provide player with critical resupply given low health'}
{'Name': 'Chat', 'Arg1': 'Zombears smell your weakness! 🐻', 'Reason': 'Maintain narrative tension and hint at impending danger'}
{'Name': 'Wait', 'Arg1': 5, 'Reason': 'Create suspense and allow player time to react to new threats'}
{'Name': 'Spawn', 'Arg1': 'Bear', 'Arg2': 'Hill', 'Reason': 'Additional threat to keep player moving and alert'}
{'Name': 'Spawn', 'Arg1': 'Bear', 'Arg2': 'Forest', 'Reason': 'Increase immediate threat to keep player on edge'}
{'Name': 'Chat', 'Arg1': 'Zombears closing in! 🐻', 'Reason': 'Create tension and alert player to imminent danger'}
{'Name': 'Spawn', 'Arg1': 'Ammo', 'Arg2': 'Forest', 'Reason': 'Provide limited resource to give player hope of survival'}
{'Name': 'Wait', 'Arg1': 3, 'Reason': 'Create brief moment of suspense before next action'}
{'Name': 'Chat', 'Arg1': 'One shot might save you! 😱', 'Reason': 'Emphasize the high-stakes survival situation'}
{'Name': 'Spawn', 'Arg1': 'Ammo', 'Arg2': 'Van', 'Reason': 'Provide critical ammo resource for player survival'}
{'Name': 'Spawn', 'Arg1': 'Bear', 'Arg2': 'Forest', 'Reason': 'Create immediate threat to increase game tension'}
{'Name': 'Chat', 'Arg1': 'Zombears incoming! Low ammo? Tough luck! 😱', 'Reason': "Heighten player's sense of urgency and challenge"}
{'Name': 'Wait', 'Arg1': '5', 'Reason': 'Allow time for player to react to new threats and resources'}
{'Name': 'Spawn', 'Arg1': 'Grenade', 'Arg2': 'Hill', 'Reason': 'Provide additional tactical option for player survival'}
{'Name': 'Spawn', 'Arg1': 'Ammo', 'Arg2': 'Pond', 'Reason': 'Provide critical ammo resupply for player survival'}
{'Name': 'Spawn', 'Arg1': 'Bear', 'Arg2': 'Forest', 'Reason': 'Create immediate tension and challenge for the player'}
{'Name': 'Chat', 'Arg1': 'Zombears closing in! Grab that ammo! 🐻', 'Reason': "Heighten player's sense of urgency and excitement"}
{'Name': 'Wait', 'Arg1': '3', 'Reason': 'Allow brief moment of suspense before next action'}
{'Name': 'Spawn', 'Arg1': 'Grenade', 'Arg2': 'Hill', 'Reason': 'Provide tactical option for player to manage multiple threats'}
{'Name': 'Spawn', 'Arg1': 'Bear', 'Arg2': 'Forest', 'Reason': 'Introduce additional threat to keep player on edge'}
{'Name': 'Chat', 'Arg1': 'Bears smell your fear! 🐻', 'Reason': 'Maintain narrative tension and player immersion'}
{'Name': 'Spawn', 'Arg1': 'Ammo', 'Arg2': 'Hill', 'Reason': "Provide strategic resource given player's current ammo count"}
{'Name': 'Chat', 'Arg1': 'Ammo incoming! Survive! 💥', 'Reason': 'Encourage player to strategically collect resources'}
{'Name': 'Wait', 'Arg1': '5', 'Reason': 'Create brief moment of suspense before next challenge'}
```