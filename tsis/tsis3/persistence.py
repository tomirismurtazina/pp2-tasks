import json
import os

def load_json(filename, default):
    if not os.path.exists(filename):
        return default
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return default

def save_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def get_leaderboard():
    return load_json('leaderboard.json', [])

def save_score(name, score, distance):
    data = get_leaderboard()
    data.append({"name": name, "score": score, "distance": distance})
    save_json('leaderboard.json', data)

def get_settings():
    default = {
        "sound": True, 
        "car_color": [255, 0, 0], 
        "difficulty": "Easy"
    }
    settings = load_json('settings.json', default)
    for key in default:
        if key not in settings:
            settings[key] = default[key]
    return settings

def save_settings(settings):   
    save_json('settings.json', settings)