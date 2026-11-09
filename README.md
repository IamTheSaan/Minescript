# Minescript

Python scripts for Minecraft built with the Minescript mod.

## Scripts

- `fish.py` – automatic fishing
- `mushroom.py` – automatic mushroom harvesting (works for other farms just has to have the same layout) 
- `utils/` – helper modules (camera rotation, timer, directions)

## Requirements

- Minecraft with the [Minescript](https://minescript.net) mod installed
- The `minescript.py` file that ships with the mod (it is not included in this repo)

## Usage

1. Copy the scripts and the `utils/` folder into the `minescript` folder in your Minecraft directory.
2. In game, type in chat: `\fish` or `\mushroom`.

## Mushroom
Ordinary a zigzag farming script (left, up, right, up) for SkyBlock. Inside is a commented function that outputs a list of corners for the zigzag based on difference in coordinates.
It also catches pests if they are in close proximity to the player and aborts if the player coordinates aren't right.

## Fish
Catches fishes on SkyBlock. Recast if the bobber is stuck for too long and aborts if coordinates change or fishing rod is no longer in hand.
