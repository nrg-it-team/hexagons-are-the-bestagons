import csv
# [auto_cone, teleop_cone, cycle_time, auto_cube, teleop_cube, auto_balance]
#equipes = {"NRG - 948": [0, 0, 17, 13, 21, 12], "Sushi Squad - 7461": [6, 13, 15, 10, 7, 0], "Jack in the Bot - 2910": [4.5, 16, 13.5, 6, 15, 4.2], "Citrus Circuits - 1678": [7.286, 18.286, 10, 4.714, 11.857, 3.429]}

def get_csv_data(filename):
  fields = []
  match_list = []
  teams = {}
  # Opens data and stores it as a list of lists
  with open(filename + ".csv","r",encoding="utf-8") as csvfile:
    csvreader = csv.reader(csvfile)
    fields = next(csvreader)
    for row in csvreader:
      match_list.append(row)
  for match in match_list:
    # Initialize variable
    match_stats = []

    # Calculates 5 of 6 stats represented in the hexagon
    match_stats.append(int(match[10]) + int(match[11]) + int(match[12])) # Auto cone
    match_stats.append(int(match[21]) + int(match[22]) + int(match[23])) # Teleop cone
    match_stats.append(135 // (match_stats[1] + int(match[18]) + int(match[19]) + int(match[20]))) # Calculates cycle time by dividing 135 (seconds of teleop) by total pieces in teleop
    match_stats.append(int(match[7]) + int(match[8]) + int(match[9])) # Auto cube
    match_stats.append(int(match[18]) + int(match[19]) + int(match[20])) # Teleop cube

    # Calculates auto scoring points (6th stat)
    if match[13] == "1":
      match_stats.append(12)
    elif match[13] == "2":
      match_stats.append(8)
    else:
      match_stats.append(0)

    # Reformats team name
    team_name = match[3].split(",")
    team_name = team_name[3] + " - " + team_name[2]

    # Records data, if multiple instances of same team, records list to be averaged later
    try:
      teams[team_name]
      teams[team_name] = [teams[team_name], match_stats]
    except:
      teams[team_name] = match_stats

  # Replaces stats of teams w/ multiple matches in the dataset with one set of average stats
  for team in teams:
    team_data = teams[team]
    # Checks for a list
    if type(team_data[0]) == type([]):

      # Records total stats from all matches
      total_stats = [0,0,0,0,0,0]
      for datapoint in team_data:
        for stat in range(6):
          total_stats[stat] += datapoint[stat]
      # Divides total stats by number of matches (therefore finding the average)
      average_stats = [0,0,0,0,0,0]
      for i in range(6):
        average_stats[i] = total_stats[i] / len(team_data)
      teams[team] = average_stats
  return(teams)

def findMaxStat(statIndex,local_teams):
  max = 0
  min = 999
  rv = True
  for key in local_teams.keys():
    value = local_teams.get(key)

    if statIndex == 2:
      rv = False
      if value[statIndex] < min:
        min = value[statIndex]
    else:
      if value[statIndex] > max:
        max = value[statIndex]
        
  if rv:
    return max
  return min