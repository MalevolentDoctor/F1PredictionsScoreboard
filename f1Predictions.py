import requests
from pyray import *

url = 'https://www.formula1.com/en/results.html/2024/drivers.html'

drivers = {
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
points = {}
standings = []

guesses = {}

scores = {}

def main():
    global logo
    init_window(500, 850, "F1 Predictions 2024")

    program_state = "starting"

    while not window_should_close():


        begin_drawing()
        clear_background(WHITE)
        
        if program_state == "starting":
            drawLoading()

        if program_state == "running":
            drawMain()

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
                analyse()
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

def analyse():
    global f1data, drivers, standings, points, guesses

    # get the initial in the form (desktop">VER<)
    driver_names_ext = {}
    for key in drivers:
        driver_names_ext[key] = 'desktop">' + key + "<"

    # loop through the HTML code to find where each of the drivers are
    driver_indices = {}
    i = 0
    for _ in f1data.text:
        name = f1data.text[i:i + 13]
        
        for k in driver_names_ext:
            if driver_names_ext[k] == name:
                driver_indices[k] = i + 9
        
        i = i + 1
    
    # get the number of points each driver has
    for k in drivers:
        if k not in driver_indices.keys():
            points[k] = 0
            continue

        if driver_indices[k] == 0:
            points[k] = 0
            continue
        
        ind = driver_indices[k]
        while f1data.text[ind:ind + 18] != 'class="dark bold">':
            ind += 1
        
        ind += 18
        cont = False
        for j in [3,2,1]:
            if cont == True:
                continue
            if f1data.text[ind:ind+j].isnumeric():
                points[k] = int(f1data.text[ind:ind+j])
                cont = True

    # Set the drivers standings
    # Set the default to the alphabetical order
    for k in drivers:
        standings.append(k)

    print(driver_indices)
    
    # Update with the points order
    c = 0
    for k in driver_indices:
        standings[c] = k
        c += 1

def drawLoading():
    draw_rectangle(0, 0, get_screen_width(), get_screen_height(), DARKGRAY)
    loading_msg = "Loading..."
    loading_font_size = 32
    loading_len = measure_text(loading_msg, loading_font_size)
    draw_text(loading_msg, int(get_screen_width()/2 - loading_len/2), int(get_screen_height()/2 - 50), loading_font_size, RAYWHITE)

def drawMain():
    global logo, standings, drivers, points, scores

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
    c = 0
    for i in standings:
        y = standings_table_offset_y + c*(standings_table_text_size + standings_table_spacing)
        if c%2 == 0:
            draw_rectangle(0, y - int(standings_table_spacing/2), get_screen_width(), standings_table_text_size + standings_table_spacing, offline_colour)

        c += 1
        draw_text(str(c), standings_table_offset_x + standings_number_offset_x, y, standings_table_text_size, GRAY)
        draw_text(drivers[i], standings_table_offset_x + standings_name_offset_x, y, standings_table_text_size, LIGHTGRAY)
        draw_text(str(points[i]), standings_table_offset_x + standings_points_offset_x, y, standings_table_text_size, GRAY)

    # Guesses Header
    guesses_table_spacing = 5
    guesses_table_offset_y = y + standings_table_text_size + standings_table_spacing + 70
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
    for k in scores:
        y = guesses_table_offset_y + c * (guesses_table_text_size + guesses_table_spacing)
        if c%2 == 0:
            draw_rectangle(0, y - int(guesses_table_spacing/2), get_screen_width(), guesses_table_text_size + guesses_table_spacing, offline_colour)

        draw_text(k, standings_table_offset_x + guesses_name_offset_x, y, guesses_table_text_size, GRAY)
        draw_text("{:5.2f}".format(scores[k]), standings_table_offset_x + guesses_points_offset_x, y, guesses_table_text_size, GRAY)
        c += 1


def loadGuesses():
    global guesses
    f = open("resources/guesses.ini")
    for L in f:
        vals = L.split(",")
        k = vals[0].strip()
        arr = vals[1::]
        for i,v in enumerate(arr):
            arr[i] = v.strip()
        
        guesses[k] = arr


def computeScores():
    global guesses, standings
    for k in guesses:
        scores[k] = score(standings, guesses[k])

def getDifferences(standings, guess):
    differences = []
    cs = 0
    for s in standings:
        cg = 0
        for g in guess:
            if g == s:
                differences.append(abs(cs - cg))
            cg += 1
        cs += 1
    return differences


def score(standings, guess):
    a = 0
    diff = getDifferences(standings, guess)
    for i in range(20):
        a += abs(diff[i])**2/25
        
    b = 100 - a
    return b

if __name__ == "__main__":
    main()