import random, tqdm
import requests
from requests.structures import CaseInsensitiveDict


def get_chess_com_stat(username):
    headers = CaseInsensitiveDict()
    headers["User-Agent"] = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/58.0.3029.110 Safari/537.3")
    url = f"https://api.chess.com/pub/player/{username}/stats"
    response = requests.get(url, headers=headers)
    data = response.json()
    list_of_dicts = [value["record"] for key, value in data.items() if
                     isinstance(value, type({})) and 'record' in value]
    result = {}
    for d in list_of_dicts:
        for key in ["win", "loss", "draw"]:
            result[key] = result.get(key, 0) + d[key]
    return result


def simulate_series(p, N, M, num_simulations):
    success_count = 0
    for _ in tqdm.tqdm(range(num_simulations)):
        series = [random.random() < p for _ in range(N)]
        if any(all(series[i:i + M]) for i in range(N - M + 1)):
            success_count += 1
    return success_count / num_simulations


def chess_com_series_probability(username, M, num_simulations):
    games = get_chess_com_stat(username)
    N = games["win"] + games["loss"] + games["draw"]
    p = games["win"] / N
    return simulate_series(p, N, M, num_simulations)


if __name__ == "__main__":
    username = "Hikaru"
    M = 43
    num_simulations = 3000
    probability = chess_com_series_probability(username, M, num_simulations)
    print(probability)

