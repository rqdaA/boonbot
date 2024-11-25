#!/bin/bash

python run.py --token "$TOKEN" --guild-id "$GUILD_ID" --bot-channel-id "$BOT_CHANNEL_ID" --contests-category-ids $CONTESTS_IDS --team-role-ids $TEAM_IDS --team-names $TEAM_NAMES
