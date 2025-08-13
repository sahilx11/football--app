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
    
    

# ----- main -----
input_player_name = input("Please Enter the Football Player's Name: ")
exact_player_name, exact_player_id = fetch_player_name(input_player_name) 

eyd = fetch_player_trophies(exact_player_id)

# sorted, simple output (alphabetical by honour name)
for honour in sorted(eyd):  #so what happens here is eyd is the ultimate result of counting trophies so  the dictionary gets sorted by keys in alphabetical order.
    print(honour, eyd[honour])# and then the honour is printed which is the tournament names and the eyd of honour which is basically the amount of times the tournament name is won by the player.









