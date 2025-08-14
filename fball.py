import requests

# Use free key "3" for v1 API
players_url = "https://www.thesportsdb.com/api/v1/json/3/searchplayers.php"
honours_url = "https://www.thesportsdb.com/api/v1/json/3/lookuphonours.php"



def fetch_player_name(playername):
    params = {'p': playername}
    response = requests.get(players_url, params=params, timeout=10) 

    if response.status_code == 200:
        data = response.json()

        if data["player"] is None: #if player id or player name isnt found basically.
            print("No player found with that name.")
            return None, None  # return None if no player found 
        
        exact_player_name = data["player"][0]['strPlayer']  # this is the player's name
        exact_player_id   = data["player"][0]['idPlayer']   # this is the player's id
   
    else:  
         print("Error fetching data from the API.") 
         return None, None 

    return exact_player_id, exact_player_name  # return the player's id and name                                                                          
  


def fetch_player_trophies(player_id):
    params = {"id": player_id}
    response = requests.get(honours_url, params=params, timeout=10)
    if response.status_code == 200:
        data = response.json()

        if data["honours"] is None: #this case is when the player has an id and a name but has no honours lol.
            print("No honours found for this player.")
            return {} 

        exact_honours = []
        for honour_items in data["honours"]:  # loop each honour dict
            exact_honours.append(honour_items['strHonour'])

        counting_trophies = {}
        for honour in exact_honours:  # count each honour
            if honour in counting_trophies:
                counting_trophies[honour] += 1
            else:
                counting_trophies[honour] = 1

        return counting_trophies  # return the dict (no printing here)
    else:
        print("Error fetching data from the API.")
        return {} 







player1_name = input("Enter Player 1 name: ")
player2_name = input("Enter Player 2 name: ")

exact_player_id1, exact_player_name1 = fetch_player_name(player1_name)
exact_player_id2, exact_player_name2 = fetch_player_name(player2_name)

exact_player_1_trophies = fetch_player_trophies(exact_player_id1)
exact_player_2_trophies = fetch_player_trophies(exact_player_id2)   


player_1_total_trophies = sum(exact_player_1_trophies.values() ) #basiclaly the value function just seperates the values into a list and then the sum well sums it .
player_2_total_trophies = sum(exact_player_2_trophies.values())

print(exact_player_name1, "has", player_1_total_trophies, "trophies.")
print(exact_player_name2, "has", player_2_total_trophies, "trophies.")


if player_1_total_trophies > player_2_total_trophies:
    print(exact_player_name1, "has more trophies than", exact_player_name2) 

elif player_1_total_trophies < player_2_total_trophies:
    print(exact_player_name2, "has more trophies than", exact_player_name1)
    
else:
    print(exact_player_name1, "and", exact_player_name2, "have the same number of trophies.")
    





