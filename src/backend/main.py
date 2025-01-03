import numpy as np
from backend.app import App
from backend.playerStats import PlayerStats
from backend.model import Model
from PIL import Image, ImageDraw
from backend.util import blurProbabilities, computeOutfieldersPositions, applyStrategy, adaptToGameState

def main():
    app = App()
    # Create an instance of PlayerStats
    player_stats = PlayerStats()
    model_save_path = './src/Models/pybaseball_nn_model_bestFinal.keras'
    baseball_model = Model(model_save_path).get_model()
   
    action_btn = app.getActionBtn()
    action_btn.config(command=lambda: predictHitLocation(player_stats, baseball_model, app))
    adapt_game_state_btn = app.apply_btn
    adapt_game_state_btn.config(command=lambda: adaptGameStateHeatmap(app))
    app.mainloop() # Start the GUI main loop

def predictHitLocation(playerStats, model, app):
    size = 125 
    scale = size/250
    true_landing = None
    params = app.get_form_fields()
    
    if 'hc_x' in params:
        true_landing = (int(params['hc_x'] * scale), int(params['hc_y']*scale))
        del params['hc_x']
        del params['hc_y']

    event = playerStats.getDataForModel(**params) # get the data for the model from the playerStats object
    if event is None:
        return
    single_event = np.expand_dims(event, axis=0)
    pred = model.predict(single_event).reshape(size, size).T
    pred = blurProbabilities(pred)
    outfielders_coords = computeOutfieldersPositions(pred)
    app.outfielders = outfielders_coords
    
    # score, strategy, outfielder_positions
    score =  params["field_score"] - params["bat_score"]
    outfielders_pos_aggressive = applyStrategy(score, 1, outfielders_coords)
    outfielders_pos_defensive = applyStrategy(score, -1, outfielders_coords)

    # plot the heatmap with/without outfielders and display on the GUI
    heatmap_img = generateHeatmap(pred)
    app.heatmap_img = heatmap_img

    heatmap_img_outfields = placeOutfielderOnImage(heatmap_img, outfielders_coords, true_landing)
    heatmap_img_outfields_aggressive = placeOutfielderOnImage(heatmap_img, outfielders_pos_aggressive, true_landing)
    heatmap_img_outfields_neutral = placeOutfielderOnImage(heatmap_img, outfielders_coords, true_landing)
    heatmap_img_outfields_defensive = placeOutfielderOnImage(heatmap_img, outfielders_pos_defensive, true_landing)
    app.setHeatmap(heatmap_img, heatmap_img_outfields, heatmap_img_outfields_aggressive, heatmap_img_outfields_neutral, heatmap_img_outfields_defensive)

def adaptGameStateHeatmap(app):
    params = app.get_form_fields()
    bases_loaded = [params['on_1b'], params['on_2b'], params['on_3b']]
    score =  params["field_score"] - params["bat_score"]

    true_landing = None
    size = 125 
    scale = size/250
    if 'hc_x' in params:
        true_landing = (int(params['hc_x'] * scale), int(params['hc_y']*scale))
        del params['hc_x']
        del params['hc_y']
    
    outfielders_coords = adaptToGameState(app.outfielders, score, bases_loaded, None)
    outfielders_pos_aggressive = applyStrategy(score, 1, outfielders_coords)
    outfielders_pos_defensive = applyStrategy(score, -1, outfielders_coords)
    heatmap_img = app.heatmap_img

    heatmap_img_outfields = placeOutfielderOnImage(heatmap_img, outfielders_coords, true_landing)
    heatmap_img_outfields_aggressive = placeOutfielderOnImage(heatmap_img, outfielders_pos_aggressive, true_landing)
    heatmap_img_outfields_neutral = placeOutfielderOnImage(heatmap_img, outfielders_coords, true_landing)
    heatmap_img_outfields_defensive = placeOutfielderOnImage(heatmap_img, outfielders_pos_defensive, true_landing)
    app.setHeatmap(heatmap_img, heatmap_img_outfields, heatmap_img_outfields_aggressive, heatmap_img_outfields_neutral, heatmap_img_outfields_defensive)

def placeOutfielderOnImage(image, outfielderCoordinates, true_location=None):
    cell_size = 50 
    copy_image = image.copy()
    draw = ImageDraw.Draw(copy_image)
    
    # Draw outfielders as light blue circles with radius 3
    for x, y in outfielderCoordinates:
        center_x = y * cell_size  # Center of circle (horizontal)
        center_y = x * cell_size  # Center of circle (vertical)
        radius = 2* cell_size   # Circle radius in pixels
        # Draw circle (ellipse with equal width and height)
        draw.ellipse([center_x - radius, center_y - radius, center_x + radius, center_y + radius],
                     fill=(50, 130, 200, 255))  # Light blue color
        
    if true_location:
        x, y = true_location
        center_x = y * cell_size
        center_y = x * cell_size
        radius = int(1.5 * cell_size)
        draw.ellipse([center_x - radius, center_y - radius, center_x + radius, center_y + radius],
                        fill=(50, 200, 50, 255))  # Green color
    
    return copy_image

def generateHeatmap(probabilityMatrix):
    size = 125
    cell_size = 50 
    width = size * cell_size
    height = size * cell_size
    
    max_value = np.max(probabilityMatrix)
    normalized_matrix = probabilityMatrix/max_value
    
    # Create a NumPy array for the image data (RGBA)
    image_array = np.zeros((height, width, 4), dtype=np.uint8) 

    # Define the gradient (white -> yellow -> orange -> red)
    def get_color(value):
        a = int(value / max_value * 255)
        if value <= 0.04:
            r = g = b = 0
            a = 0
        elif value <= 0.33:  # white -> yellow
            r = int(255 * value / 0.33)
            g = b = 0
            a = 100
        elif value <= 0.66:  # yellow -> orange
            r = 255
            g = int(255 * (1 - (value - 0.33) / 0.33))
            b = 0
            a = 150
        else:  # orange -> red
            r = 255
            g = 0
            b = int(255 * (1 - (value - 0.66) / 0.34))
            a = 200
        return (r, g, b, a)

    # Draw the grid
    for i in range(size):
        for j in range(size):
            color = get_color(normalized_matrix[i][j])
            x0 = j * cell_size
            y0 = i * cell_size
            x1 = x0 + cell_size
            y1 = y0 + cell_size
            image_array[y0:y1, x0:x1] = color  # Set color for the cell
    img = Image.fromarray(image_array, 'RGBA')

    return img

if __name__ == "__main__":
    main()