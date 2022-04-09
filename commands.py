command_list = {
        '/server_rules',
        '/help',
        '/commands',
        '/youtube "name of video"',
        '/dice_roll',
        '/news',
        '/random_project'
        }
def command_list_function(command_list):
  for element in command_list:
    element = enumerate(command_list)
    new_element = str(dict(element)).replace("{", "").replace("}", "").replace(",", "\n")
    return new_element

    
