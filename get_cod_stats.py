import sys
import json
import os
import argparse
from cod_api import API, platforms
import asyncio
import datetime

# Prevent Async error from showing
if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

replacements = {
    # Gamemodes
    "dom": "Domination",
    "hc_dom": "Hardcore Domination",
    "war": "Team Deathmatch",
    "hc_war": "Hardcore Team Deathmatch",
    "hq": "Headquarters",
    "hc_hq": "Hardcore Headquarters",
    "conf": "Kill Confirmed",
    "hc_conf": "Hardcore Kill Confirmed",
    "koth": "Hardpoint",
    "koth_hc": "Hardcore Hardpoint",
    "sd": "Search and Destroy",
    "hc_sd": "Hardcore Search and Destroy",
    "cyber": "Cyber Attack",
    "hc_cyber": "Hardcore Cyber Attack",
    "grnd": "Grind",
    "arm": "Ground War",
    "infect": "Infected",
    "gun": "Gun Game",
    "arena": "Gunfight",
    "br": "Battle Royale (Warzone)",
    "br_dmz": "Plunder",
    "br_all": "Battle Royale (Warzone & Plunder)",
    # Weapons
    "weapon_assault_rifle": "Assault Rifles",
    "weapon_shotgun": "Shotguns",
    "weapon_marksman": "Marksman Rifles",
    "weapon_sniper": "Snipers",
    "tacticals": "Tactical Equipment",
    "lethals": "Lethal Equipment",
    "weapon_lmg": "LMGs",
    "weapon_launcher": "Launchers",
    "supers": "Field Upgrades",
    "weapon_pistol": "Pistols",
    "weapon_other": "Primary Melee",
    "weapon_smg": "SMGs",
    "weapon_melee": "Melee",
    "scorestreakData": "Scorestreaks",
    "lethalScorestreakData": "Lethal Scorestreaks",
    "supportScorestreakData": "Support Scorestreaks",
    # Guns
    ## Assault Rifles
    "iw8_ar_tango21": "RAM-7",
    "iw8_ar_mike4": "M4A1",
    "iw8_ar_valpha": "AS VAL",
    "iw8_ar_falpha": "FR 5.56",
    "iw8_ar_mcharlie": "M13",
    "iw8_ar_akilo47": "AK-47",
    "iw8_ar_asierra12": "Oden",
    "iw8_ar_galima": "CR-56 AMAX",
    "iw8_ar_sierra552": "Grau 5.56",
    "iw8_ar_falima": "FAL",
    "iw8_ar_anovember94": "AN-94",
    "iw8_ar_kilo433": "Kilo 141",
    "iw8_ar_scharlie": "FN Scar 17",
    "iw8_sh_mike26": "VLK Rogue",
    ## Shotguns
    "iw8_sh_charlie725": "725",
    "iw8_sh_oscar12": "Origin 12 Shotgun",
    "iw8_sh_aalpha12": "JAK-12",
    "iw8_sh_romeo870": "Model 680",
    "iw8_sh_dpapa12": "R9-0 Shotgun",
    ## Marksman Rifles
    "iw8_sn_sbeta": "MK2 Carbine",
    "iw8_sn_crossbow": "Crossbow",
    "iw8_sn_romeo700": "SP-R 208",
    "iw8_sn_kilo98": "Kar98k",
    "iw8_sn_mike14": "EBR-14",
    "iw8_sn_sksierra": "SKS",
    ## Sniper Rifles
    "iw8_sn_alpha50": "AX-50",
    "iw8_sn_hdromeo": "HDR",
    "iw8_sn_delta": "Dragunov",
    "iw8_sn_xmike109": "Rytec AMR",
    ## Tactical Equipment
    "equip_gas_grenade": "Gas Grenade",
    "equip_snapshot_grenade": "Snapshot Grenade",
    "equip_decoy": "Decoy Grenade",
    "equip_smoke": "Smoke Grenade",
    "equip_concussion": "Concussion Grenade",
    "equip_hb_sensor": "Heartbeat Sensor",
    "equip_flash": "Flash Grenade",
    "equip_adrenaline": "Stim",
    ## Lethal Equipment
    "equip_frag": "Frag Grenade",
    "equip_thermite": "Thermite",
    "equip_semtex": "Semtex",
    "equip_claymore": "Claymore",
    "equip_c4": "C4",
    "equip_at_mine": "Proximity Mine",
    "equip_throwing_knife": "Throwing Knife",
    "equip_molotov": "Mototov Cocktail",
    ## LMGs
    "iw8_lm_kilo121": "M91",
    "iw8_lm_mkilo3": "Bruen Mk9",
    "iw8_lm_mgolf34": "MG34",
    "iw8_lm_lima86": "SA87",
    "iw8_lm_pkilo": "PKM",
    "iw8_lm_sierrax": "FiNN LMG",
    "iw8_lm_mgolf36": "Holger-26",
    # "": "", ### RAAL LMG not implemented
    ## Launchers
    "iw8_la_gromeo": "PILA",
    "iw8_la_rpapa7": "RPG-7",
    "iw8_la_juliet": "JOKR",
    "iw8_la_kgolf": "Strela-P",
    # "": "", ### Unknown Launcher
    ## Field Upgrades
    "super_emp_drone": "EMP Drone",
    "super_trophy": "Trophy System",
    "super_ammo_drop": "Munitions Box",
    "super_weapon_drop": "Weapon Drop",
    "super_fulton": "Cash Deposit Balloon",
    "super_armor_drop": "Armor Box",
    "super_select": "Field Upgrade Pro (Any)",
    "super_tac_insert": "Tactical Insertion",
    "super_recon_drone": "Recon Drone",
    "super_deadsilence": "Dead Silence",
    "super_supply_drop": "Loadout Drop", ### Unsure if this is Loadout Drop
    "super_tac_cover": "Deployable Cover",
    "super_support_box": "Stopping Power Rounds",
    ## Pistols
    "iw8_pi_cpapa": ".357",
    "iw8_pi_mike9": "Renetti",
    "iw8_pi_mike1911": "1911",
    "iw8_pi_golf21": "X16",
    "iw8_pi_decho": ".50 GS",
    "iw8_pi_papa320": "M19",
    # "": "", ### Sykov not implemented
    ## Primary Melee
    "iw8_me_riotshield": "Riot Shield",
    ## SMGs
    "iw8_sm_mpapa7": "MP7",
    "iw8_sm_augolf": "AUG",
    "iw8_sm_papa90": "P90",
    "iw8_sm_charlie9": "ISO",
    "iw8_sm_mpapa5": "MP5",
    "iw8_sm_smgolf45": "Striker 45",
    "iw8_sm_beta": "PP19 Bizon",
    "iw8_sm_victor": "Fennec",
    "iw8_sm_uzulu": "Uzi",
    # "": "", ### CX9 not implemented
    ## Melee
    "iw8_me_akimboblunt": "Kali Sticks",
    "iw8_me_akimboblades": "Dual Kodachis",
    "iw8_knife": "Knife",
    # Scorestreaks
    "precision_airstrike": "Precision Airstrike",
    "cruise_predator": "Cruise Missile",
    "manual_turret": "Shield Turret",
    "white_phosphorus": "White Phosphorus",
    "hover_jet": "VTOL Jet",
    "chopper_gunner": "Chopper Gunner",
    "gunship": "Gunship",
    "sentry_gun": "Sentry Gun",
    "toma_strike": "Cluster Strike",
    "nuke": "Nuke",
    "juggernaut": "Juggernaut",
    "pac_sentry": "Wheelson",
    "chopper_support": "Support Helo",
    "bradley": "Infantry Assault Vehicle",
    "airdrop": "Care Package",
    "radar_drone_overwatch": "Personal Radar",
    "scrambler_drone_guard": "Counter UAV",
    "uav": "UAV",
    "airdrop_multiple": "Emergency Airdrop",
    "directional_uav": "Advanced UAV",
    # Accolades
    # "accoladeData": "Accolades",
    # "classChanges": "Most classes changed (Evolver)",
    # "highestAvgAltitude": "Highest average altitude (High Command)",
    # "killsFromBehind": "Most kills from behind (Flanker)",
    # "lmgDeaths": "Most LMG deaths (Target Practice)",
    # "riotShieldDamageAbsorbed": "Most damage absorbed with Riot Shield (Guardian)",
    # "flashbangHits": "Most Flashbang hits (Blinder)",
    # "meleeKills": "Most Melee kills (Brawler)",
    # "tagsLargestBank": "Largest bank (Bank Account)",
    # "shotgunKills": "Most Shotgun kills (Buckshot)",
    # "sniperDeaths": "Most Sniper deaths (Zeroed In)",
    # "timeProne": "Most time spent Prone (Grassy Knoll)",
    # "killstreakWhitePhosphorousKillsAssists": "Most kills and assists with White Phosphorus (Burnout)",
    # "shortestLife": "Shortest life (Terminal)",
    # "deathsFromBehind": "Most deaths from behind (Blindsided)",
    # "higherRankedKills": "Most kills on higher ranked scoreboard players (Upriser)",
    # "mostAssists": "Most assists (Wingman)",
    # "leastKills": "Fewest kills (The Fearful)",
    # "tagsDenied": "Denied the most tags (Denied)",
    # "killstreakWheelsonKills": "Most Wheelson kills",
    # "sniperHeadshots": "Most Sniper headshots (Dead Aim)",
    # "killstreakJuggernautKills": "Most Juggernaut kills (Heavy Metal)",
    # "smokesUsed": "Most Smoke Grenades used (Chimney)",
    # "avengerKills": "Most avenger kills (Avenger)",
    # "decoyHits": "Most Decoy Grenade hits (Made You Look)",
    # "killstreakCarePackageUsed": "Most Care Packages called in (Helping Hand)",
    # "molotovKills": "Most Molotov kills (Arsonist)",
    # "gasHits": "Most Gas Grenade hits (Gaseous)",
    # "comebackKills": "Most comebacks (Rally)",
    # "lmgHeadshots": "Most LMG headshots (LMG Expert)",
    # "smgDeaths": "Most SMG deaths (Run and Gunned)",
    # "carrierKills": "Most kills as carrier (Carrier)",
    # "deployableCoverUsed": "Most Deployable Covers used (Combat Engineer)",
    # "thermiteKills": "Most Thermite kills (Red Iron)",
    # "arKills": "Most assault rifle kills (AR Specialist)",
    # "c4Kills": "Most C4 kills (Handle With Care)",
    # "suicides": "Most suicides (Accident Prone)",
    # "clutch": "Most kills as the last alive (Clutched)",
    # "survivorKills": "Most kills as survivor (Survivalist)",
    # "killstreakGunshipKills": "Most Gunship kills (Death From Above)",
    # "timeSpentAsPassenger": "Most time spent as a passenger (Navigator)",
    # "returns": "Most flags returned (Flag Returner)",
    # "smgHeadshots": "Most SMG headshots (SMG Expert)",
    # "launcherDeaths": "Most launcher deaths (Fubar)",
    # "oneShotOneKills": "Most one shot kills (One Shot Kill)",
    # "ammoBoxUsed": "Most Munitions Boxes used (Provider)",
    # #"spawnSelectSquad": "",
    # "weaponPickups": "Most picked up weapons (Loaner)",
    # "pointBlankKills": "Most point blank kills (Personal Space)",
    # "tagsCaptured": "Collected the most tags (Confirmed Kills)",
    # "killstreakGroundKills": "Most ground based killstreak kills (Ground Control)",
    # "distanceTraveledInVehicle": "Longest distance travelled in a vehicle (Cross Country)",
    # "longestLife": "Longest life (Lifer)",
    # "stunHits": "Most Stun Grenade hits (Stunner)",
    # "spawnSelectFlag": "Most FOB Spawns (Objective Focused)", # Unsure
    # "shotgunHeadshots": "Most Shotgun headshots (Boomstick)",
    # "bombDefused": "Most defuses (Defuser)",
    # "snapshotHits": "Most Snapshot Grenade hits (Photographer)",
    # "noKillsWithDeath": "No kills with at least 1 death (Participant)",
    # "killstreakAUAVAssists": "Most Advanced UAV assists (Target Rich Environment)",
    # "killstreakPersonalUAVKills": "Most kills with a Personal Radar active (Nothing Personal)",
    # "tacticalInsertionSpawns": "Most Tactical Insertions used (Revenant)",
    # "launcherKills": "Most Launcher kills (Explosive)",
    # "spawnSelectVehicle": "Most vehicle spawns (Oscar Mike)",
    # "mostKillsLeastDeaths": "Most kills and fewest deaths (MVP)",
    # "mostKills": "Most kills (The Feared)",
    # "defends": "Most defend kills (Defense)",
    # "timeSpentAsDriver": "Most time spent driving (Driver)",
    # "": "" # WIP - Still adding more
}

# Initiating the API class
api = API()
COOKIE_FILE = 'cookie.txt'
DIR_NAME = 'stats'
MATCH_DIR_NAME = 'matches'

def save_to_file(data, filename, dir_name='stats'):
    """Utility function to save data to a JSON file."""
    with open(os.path.join(dir_name, filename), 'w') as json_file:
        json.dump(data, json_file, indent=4)

def get_and_save_data(player_name=None, all_stats=False, season_loot=False, identities=False, maps=False):
    # Create the stats directory if it doesn't exist
    DIR_NAME = 'stats'
    if not os.path.exists(DIR_NAME):
        os.makedirs(DIR_NAME)
    
    # Check if cookie file exists
    if os.path.exists(COOKIE_FILE):
        with open(COOKIE_FILE, 'r') as f:
            api_key = f.read().strip()
    else:
        api_key = input("Please enter your ACT_SSO_COOKIE: ")
        with open(COOKIE_FILE, 'w') as f:
            f.write(api_key)

    # If player_name is not provided via command line, get it from user input
    if not player_name:
        player_name = input("Please enter the player's username (with #1234567): ")

    # Login with sso token
    api.login(api_key)
    
    # Retrieve data from API
    # First, determine if any specific optional arguments were given
    if not (all_stats or season_loot or identities or maps):
        # If no specific optional arguments are given, then default behavior:
        player_stats = api.ModernWarfare.fullData(platforms.Activision, player_name)
        match_info = api.ModernWarfare.combatHistory(platforms.Activision, player_name)
        save_to_file(player_stats, 'stats.json')
        save_to_file(match_info, 'match_info.json')
    elif all_stats:
        # If the all_stats argument is given:
        player_stats = api.ModernWarfare.fullData(platforms.Activision, player_name)
        match_info = api.ModernWarfare.combatHistory(platforms.Activision, player_name)
        player_stats = api.ModernWarfare.fullData(platforms.Activision, player_name)
        match_info = api.ModernWarfare.combatHistory(platforms.Activision, player_name)
        season_loot_data = api.ModernWarfare.seasonLoot(platforms.Activision, player_name)
        map_list = api.ModernWarfare.mapList(platforms.Activision)
        identities_data = api.Me.loggedInIdentities()
        save_to_file(player_stats, 'stats.json')
        save_to_file(match_info, 'match_info.json')
        save_to_file(season_loot_data, 'season_loot.json')
        save_to_file(map_list, 'map_list.json')
        save_to_file(identities_data, 'identities.json')
    else:
        # For other specific optional arguments:
        if season_loot:
            season_loot_data = api.ModernWarfare.seasonLoot(platforms.Activision, player_name)
            save_to_file(season_loot_data, 'season_loot.json')
        if identities:
            identities_data = api.Me.loggedInIdentities()
            save_to_file(identities_data, 'identities.json')
        if maps:
            map_list = api.ModernWarfare.mapList(platforms.Activision)
            save_to_file(map_list, 'map_list.json')

# Save results to a JSON file inside the stats directory
def recursive_key_replace(obj, replacements):
    if isinstance(obj, dict):
        new_obj = {}
        for key, value in obj.items():
            new_key = replacements.get(key, key)
            if isinstance(value, str):
                new_value = replacements.get(value, value)
                new_obj[new_key] = recursive_key_replace(new_value, replacements)
            else:
                new_obj[new_key] = recursive_key_replace(value, replacements)
        return new_obj
    elif isinstance(obj, list):
        return [recursive_key_replace(item, replacements) for item in obj]
    else:
        return replacements.get(obj, obj) if isinstance(obj, str) else obj

def sort_data(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "mode":
                data[key] = dict(sorted(value.items(), key=lambda item: item[1]['properties']['timePlayed'], reverse=True))
            elif key in ["Assault Rifles", "Shotguns", "Marksman Rifles", "Snipers", "LMGs", "Launchers", "Pistols", "SMGs", "Melee"]:
                data[key] = dict(sorted(value.items(), key=lambda item: item[1]['properties']['kills'], reverse=True))
            elif key in ["Field Upgrades"]:
                data[key] = dict(sorted(value.items(), key=lambda item: item[1]['properties']['uses'], reverse=True))
            elif key in ["Tactical Equipment", "Lethal Equipment"]:
                data[key] = dict(sorted(value.items(), key=lambda item: item[1]['properties']['uses'], reverse=True))
            elif key == "Scorestreaks":
                for subcategory, scorestreaks in value.items():
                    data[key][subcategory] = dict(sorted(scorestreaks.items(), key=lambda item: item[1]['properties']['awardedCount'], reverse=True))
            elif key == "Accolades":
                if 'properties' in value:
                    data[key]['properties'] = dict(sorted(value['properties'].items(), key=lambda item: item[1], reverse=True))
            else:
                # Recursive call to handle nested dictionaries
                data[key] = sort_data(value)
    return data

def replace_time_and_duration_recursive(data):
    """
    Recursively replace epoch times for specific keys in a nested dictionary or list.
    """
    if isinstance(data, list):
        for item in data:
            replace_time_and_duration_recursive(item)

    elif isinstance(data, dict):
        for key, value in data.items():
            if key == "utcStartSeconds":
                data[key] = epoch_to_human_readable(value)
                # For EST conversion: 
                # data[key] = epoch_to_human_readable(value, "EST")
                
            elif key == "utcEndSeconds":
                data[key] = epoch_to_human_readable(value)
                # For EST conversion:
                # data[key] = epoch_to_human_readable(value, "EST")
                
            elif key == "duration":
                data[key] = convert_duration(value)
            
            else:
                replace_time_and_duration_recursive(value)

def epoch_to_human_readable(epoch_timestamp, timezone='GMT'):
    if isinstance(epoch_timestamp, str):
        return epoch_timestamp  # Already converted

    dt_object = datetime.datetime.utcfromtimestamp(epoch_timestamp)
    if timezone == 'GMT':
        date_str = dt_object.strftime("GMT: %A, %B %d, %Y %I:%M:%S %p")
    elif timezone == 'EST':
        dt_object -= datetime.timedelta(hours=4)  # Using 4 hours for EST conversion instead of 5?
        date_str = dt_object.strftime("EST: %A, %B %d, %Y %I:%M:%S %p")
    else:
        raise ValueError("Unsupported timezone.")
    return date_str

def convert_duration(milliseconds):
    if isinstance(milliseconds, str) and "Minutes" in milliseconds:
        return milliseconds  # Already converted
    
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes} Minutes {seconds} Seconds {milliseconds} Milliseconds"

def beautify_data():
    file_path = (os.path.join(DIR_NAME, 'stats.json'))
    with open(file_path, 'r') as file:
        data = json.load(file)
    data = recursive_key_replace(data, replacements)
    data = sort_data(data)
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Keys sorted and replaced in {file_path}.")

def beautify_match_data():
    file_path = (os.path.join(DIR_NAME, 'match_info.json'))
    with open(file_path, 'r') as file:
        data = json.load(file)
    replace_time_and_duration_recursive(data)
    data = recursive_key_replace(data, replacements)
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Keys replaced in {file_path}.")

def split_matches_into_files():
    """
    Split the matches in match_info.json into separate files.
    """
    MATCHES_DIR = os.path.join(DIR_NAME, MATCH_DIR_NAME)
    
    # Create matches directory if it doesn't exist
    if not os.path.exists(MATCHES_DIR):
        os.makedirs(MATCHES_DIR)

    # Load the match_info data
    with open(os.path.join(DIR_NAME, 'match_info.json'), 'r') as file:
        data = json.load(file)
        matches = data.get('data', {}).get('matches', [])  # Correct the key to access matches

    # Check if data needs cleaning
    sample_match = matches[0] if matches else {}
    if (isinstance(sample_match.get("utcStartSeconds"), int) or 
        isinstance(sample_match.get("utcEndSeconds"), int) or 
        isinstance(sample_match.get("duration"), int)):
        
        print("Cleaning match data...")
        replace_time_and_duration_recursive(data)
        
        # Save the cleaned data back to match_info.json
        with open(os.path.join(DIR_NAME, 'match_info.json'), 'w') as file:
            json.dump(data, file, indent=4)

    # Split and save each match into a separate file
    for idx, match in enumerate(matches):
        # Create a copy of the match to ensure we don't modify the original data
        match_copy = dict(match)
        # Remove player subkey to avoid the cascading data, if you want to exclude more, add them here
        match_copy.pop('player', None)

        file_name = f"match_{idx + 1}.json"
        with open(os.path.join(MATCHES_DIR, file_name), 'w') as match_file:
            json.dump(match_copy, match_file, indent=4)

    print(f"Matches split into {len(matches)} separate files in {MATCHES_DIR}.")

def main():
    # Define the block of quote text to display in the help command
    help_text = """
    Obtaining your ACT_SSO_COOKIE

    - Go to https://www.callofduty.com and login with your account
    - Once logged in, press F12 for your browsers developer tools. Then go to Application --> Storage --> Cookies --> https://www.callofduty.com and find ACT_SSO_COOKIE
    - Enter the value when prompted
    """

    parser = argparse.ArgumentParser(description="Detailed Modern Warfare (2019) Statistics Tool", epilog=help_text, formatter_class=argparse.RawDescriptionHelpFormatter)

    # Group related arguments
    group_data = parser.add_argument_group("Data Fetching Options")
    group_cleaning = parser.add_argument_group("Data Cleaning Options")

    # Add arguments for Data Fetching Options
    group_data.add_argument("-p", "--player_name", type=str, help="Player's username (with #1234567)")
    group_data.add_argument("-a", "--all_stats", action="store_true", help="Fetch all the different types of stats data")
    group_data.add_argument("-sl", "--season_loot", action="store_true", help="Fetch only the season loot data")
    group_data.add_argument("-i", "--identities", action="store_true", help="Fetch only the logged-in identities data")
    group_data.add_argument("-m", "--maps", action="store_true", help="Fetch only the map list data")

    # Add arguments for Cleaning Options
    group_cleaning.add_argument("-c", "--clean", action="store_true", help="Beautify all data")
    group_cleaning.add_argument("-sm", "--split_matches", action="store_true", help="Split the matches into separate JSON files within the 'matches' subfolder")
    group_cleaning.add_argument("-csd", "--clean_stats_data", action="store_true", help="Beautify the data and convert to human-readable strings in stats.json")
    group_cleaning.add_argument("-cmd", "--clean_match_data", action="store_true", help="Beautify the match data and convert to human-readable strings in match_info.json")

    args = parser.parse_args()

    # Custom error handling
    # try:
    #     args = parser.parse_args()
    # except SystemExit:
    #     # Check if 'player_name' is in sys.argv, if not, raise exception
    #     if '--player_name' not in sys.argv and '-p' not in sys.argv:
    #         print('You must specify a player name!')
    #     # Otherwise, re-raise the error or print the default error message.
    #     sys.exit(1)

    if args.split_matches:
        split_matches_into_files()
    elif args.clean_stats_data:
        beautify_data()
    elif args.clean_match_data:
        beautify_match_data()
    elif args.clean:
        beautify_data()
        beautify_match_data()
    else:
        get_and_save_data(args.player_name, args.all_stats, args.season_loot, args.identities, args.maps)

if __name__ == "__main__":
    main()