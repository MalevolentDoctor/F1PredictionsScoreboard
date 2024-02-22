import requests
from pyray import *

url = 'https://www.formula1.com/en/results.html/2023/drivers.html'

driver = {
    "initial":      "NUL",
    "name":         "No Name",
    "search_name":  "desktop>NUL<",
    "search_index": 0,
    "points":       0,
    "position":     0
}

guess = {
    "name":     "No Name",
    "guess":    [],
    "score":    0

}

# Define drivers names
drivers_names = {
    "ALB": "Alex Albon",
    "ALO": "Fernando Alonso",
    "BOT": "Valtteri Bottas",
    "GAS": "Pierre Gasly",
    "HAM": "Lewis Hamilton",
    "HUL": "Nico Hulkenberg",
    "LEC": "Charles Leclerc",
    "MAG": "Kevin Magnussen",
    "NOR": "Lando Norris",
    "OCO": "Esteban Ocon",
    "PER": "Sergio Perez",
    "PIA": "Oscar Piastri",
    "RIC": "Daniel Riccardo",
    "RUS": "George Russel",
    "SAI": "Carlos Sainz",
    "SAR": "Logan Sargeant",
    "STR": "Lance Stroll",
    "TSU": "Yuki Tsunoda",
    "VER": "Max Verstappen",
    "ZHO": "Zhou Guanyu"
}

drivers = []
guesses = []

def main():
    global logo
    init_window(500, 900, "F1 Predictions 2024")

    program_state = "starting"

    while not window_should_close():


        begin_drawing()
        clear_background(WHITE)
        
        if program_state == "starting":
            drawLoading()

        if program_state == "running":
            drawMain()

        if program_state == "connection_error":
            drawConnectionError()

        end_drawing()

        if program_state == "starting":
            success = initialise()

            if success == -1:
                program_state = "connection_error"

            elif success == 0:
                # Load assets
                logo_img = load_image("resources/f1logo.png")
                logo = load_texture_from_image(logo_img)
                unload_image(logo_img)

                loadGuesses()
                getDriverData()
                computeScores()

                # Switch program state
                program_state = "running"

    close_window()


def initialise():
    global f1data
    try:
        f1data = requests.get(url)
    except:
        return -1
    
    return 0

def loadGuesses():
    global guesses, guess, drivers_names, driver

    # Load data from file
    f = open("resources/guesses.ini")

    for L in f:
        # Split comma separated values
        vals = L.split(",")

        # Get the name of the guess from the first element in the array
        guess_name = vals[0].strip()

        # Clean up the rest of the values in the array, the initials of the drivers
        guess_initials = vals[1::]
        for i,v in enumerate(guess_initials):
            guess_initials[i] = v.strip()

        # Create the guess structure
        g = guess.copy()
        g["name"] = guess_name
        drivers = []

        # Get the driver data for the guess
        for k in drivers_names:
            d = driver.copy()
            d["initial"] = k
            d["name"] = drivers_names[k]
            d["position"] = guess_initials.index(k)
            drivers.append(d)

        g["guess"] = drivers

        # Add the guess to the global array
        guesses.append(g)


def getDriverData():
    global f1data, drivers, drivers_names, driver

    # Initialise 'drivers' array
    p = 1
    for k in drivers_names:
        d = driver.copy()
        d["name"] = drivers_names[k]
        d["initial"] = k
        d["search_name"] = 'desktop">' + k + "<"
        d["position"] = p
        drivers.append(d)
        p += 1


    # Loop through the HTML code to find where each of the drivers are
    i = 0
    p = 1
    for _ in f1data.text:
        name = f1data.text[i:i + 13]
        
        for d in drivers:
            if d["search_name"] == name:
                d["search_index"] = i + 9
                d["position"] = p
                p += 1

        
        i = i + 1
    
    # Get the number of points each driver has
    for d in drivers:

        if d["search_index"] == 0:
            continue
        
        ind = d["search_index"]
        while f1data.text[ind:ind + 18] != 'class="dark bold">':
            ind += 1
        
        ind += 18
        cont = False
        for j in [3,2,1]:
            if cont == True:
                continue

            if f1data.text[ind:ind+j].isnumeric():
                d["points"] = int(f1data.text[ind:ind+j])
                cont = True


def drawLoading():
    draw_rectangle(0, 0, get_screen_width(), get_screen_height(), DARKGRAY)
    loading_msg = "Loading..."
    loading_font_size = 32
    loading_len = measure_text(loading_msg, loading_font_size)
    draw_text(loading_msg, int(get_screen_width()/2 - loading_len/2), int(get_screen_height()/2 - 50), loading_font_size, RAYWHITE)

def drawConnectionError():
    draw_rectangle(0, 0, get_screen_width(), get_screen_height(), DARKGRAY)
    loading_msg = "Connection Error"
    loading_font_size = 32
    loading_len = measure_text(loading_msg, loading_font_size)
    draw_text(loading_msg, int(get_screen_width()/2 - loading_len/2), int(get_screen_height()/2 - 50), loading_font_size, RED)


def drawMain():
    global logo, drivers, scores

    # Background
    draw_rectangle(0, 0, get_screen_width(), get_screen_height(), BLACK)

    # Logo
    logo_scale = 0.1
    draw_texture_ex(logo, [20, 20], 0, logo_scale, WHITE)

    # Header Text
    header_text_size = 24
    header_text_spacing = 0
    draw_text("2024", int(logo.width*logo_scale + 40), 20, header_text_size, RAYWHITE)
    draw_text("Championship", int(logo.width*logo_scale + 40), 20 + header_text_size, header_text_size, RAYWHITE)
    draw_text("Predictions", int(logo.width*logo_scale + 40), 20 + header_text_size * 2, header_text_size, RAYWHITE)

    # Standings Header
    standings_table_spacing = 5
    standings_table_offset_y = 150
    standings_table_offset_x = 80

    standings_title_text = "Current Standings"
    standings_title_text_size = 24
    standings_title_text_len = measure_text(standings_title_text, standings_title_text_size)
    draw_text(standings_title_text, int(get_screen_width()/2 - standings_title_text_len/2), standings_table_offset_y - standings_title_text_size - standings_table_spacing, standings_title_text_size, RAYWHITE)

    # Standings table
    standings_table_text_size = 20
    standings_name_offset_x = 70
    standings_number_offset_x = 20
    standings_points_offset_x = 280

    offline_colour = [20, 0, 0, 255]
    for d in drivers:
        c = d["position"] - 1
        y = standings_table_offset_y + c*(standings_table_text_size + standings_table_spacing)
        if c%2 == 0:
            draw_rectangle(0, y - int(standings_table_spacing/2), get_screen_width(), standings_table_text_size + standings_table_spacing, offline_colour)

        draw_text(str(d["position"]), standings_table_offset_x + standings_number_offset_x, y, standings_table_text_size, GRAY)
        draw_text(d["name"], standings_table_offset_x + standings_name_offset_x, y, standings_table_text_size, LIGHTGRAY)
        draw_text(str(d["points"]), standings_table_offset_x + standings_points_offset_x, y, standings_table_text_size, GRAY)

    # Guesses Header
    guesses_table_spacing = 5
    guesses_table_offset_y = y + standings_table_text_size + standings_table_spacing + 100
    standings_table_offset_x = 80

    guesses_title_text = "Current Score"
    guesses_title_text_size = 24
    guesses_title_text_len = measure_text(guesses_title_text, guesses_title_text_size)
    draw_text(guesses_title_text, int(get_screen_width()/2 - guesses_title_text_len/2), guesses_table_offset_y - guesses_title_text_size - guesses_table_spacing, guesses_title_text_size, RAYWHITE)
        
    # Guesses Table
    guesses_table_text_size = 20
    guesses_name_offset_x = 20
    guesses_points_offset_x = 280
    offline_colour = [20, 0, 0, 255]

    c = 0
    for k in guesses:
        y = guesses_table_offset_y + c * (guesses_table_text_size + guesses_table_spacing)
        if c%2 == 0:
            draw_rectangle(0, y - int(guesses_table_spacing/2), get_screen_width(), guesses_table_text_size + guesses_table_spacing, offline_colour)

        draw_text(k["name"], standings_table_offset_x + guesses_name_offset_x, y, guesses_table_text_size, GRAY)
        draw_text("{:5.2f}".format(k["score"]), standings_table_offset_x + guesses_points_offset_x, y, guesses_table_text_size, GRAY)
        c += 1


def computeScores():
    global guesses

    for guess in guesses:
        guess["score"] = score(guess["guess"])

def score(guess):
    global drivers

    a = 0
    for actual in drivers:
        for g in guess:
            if (actual["initial"] == g["initial"]):
                a += abs(actual["position"] - g["position"])**2/25
        
    b = 100 - a
    return b

if __name__ == "__main__":
    main()