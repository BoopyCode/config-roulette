#!/usr/bin/env python3
"""Config Roulette - Because debugging configs should feel like gambling!"""

import sys
import json
import yaml
import configparser
from pathlib import Path
from difflib import unified_diff

# The only thing more mysterious than your configs is why you're still debugging them

def load_config(filepath):
    """Loads config files with the confidence of a developer who hasn't read the docs."""
    path = Path(filepath)
    if not path.exists():
        print(f"\n🎲 File not found! You've won: confusion!")
        return None
    
    try:
        if path.suffix == '.json':
            return json.loads(path.read_text())
        elif path.suffix in ['.yaml', '.yml']:
            return yaml.safe_load(path.read_text())
        elif path.suffix == '.ini':
            config = configparser.ConfigParser()
            config.read(path)
            return {s: dict(config.items(s)) for s in config.sections()}
        else:
            print(f"\n🎲 Unknown format! Your prize: more googling!")
            return None
    except Exception as e:
        print(f"\n🎲 Parse error! Congratulations, you broke: {e}")
        return None

def compare_configs(file1, file2):
    """Spot the differences! Or don't. We're not your mom."""
    config1 = load_config(file1)
    config2 = load_config(file2)
    
    if not config1 or not config2:
        return
    
    # Convert to comparable strings because computers are picky
    str1 = json.dumps(config1, indent=2, sort_keys=True).split('\n')
    str2 = json.dumps(config2, indent=2, sort_keys=True).split('\n')
    
    diff = list(unified_diff(str1, str2, fromfile=file1, tofile=file2))
    
    if diff:
        print(f"\n🎲 DIFFERENCES FOUND! Your lucky numbers are:")
        print('\n'.join(diff))
    else:
        print(f"\n🎲 JACKPOT! Files are identical! (Probably still broken though)")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("\n🎲 Config Roulette - Spin the wheel of fortune!")
        print("Usage: python config_roulette.py <config1> <config2>")
        print("Example: python config_roulette.py dev.yaml prod.yaml")
        sys.exit(1)
    
    print("\n🎲 Spinning the roulette wheel...")
    print("🎯 Place your bets on which config will break production!\n")
    
    compare_configs(sys.argv[1], sys.argv[2])
    
    print("\n🎲 Good luck debugging! Remember: it's always DNS. Except when it's configs.")