import numpy as np
import cv2

# Constants
n = 125
m = 125

# File for helper functions used in main

def blurProbabilities(probabilityMatrix):
  kernel_size = (3, 3)  # Size of the Gaussian kernel
  sigma = 4  # Standard deviation of the Gaussian

  blurred_matrix = cv2.GaussianBlur(np.array(probabilityMatrix), kernel_size, sigma)
  return blurred_matrix

def computeOutfieldersPositions(predmatrix):
    n = len(predmatrix)
    m = len(predmatrix[0])

    #First set all the standard positions  #x,y flipped due to way we are drawing

   # Home Plate Position
    home_plate_x = n // 2 + (n//64)
    home_plate_y = n - (n // 4) + (n//32)
    home_plate = (home_plate_y, home_plate_x)

    first_base = (home_plate_y - (n // 10) , home_plate_x + (n // 8))
    third_base = (home_plate_y - (n // 10) , home_plate_x - (n // 8))

    second_base = (home_plate_y - (n // 5),home_plate_x + (n // 16))
    shortstop = (home_plate_y - (n // 5),home_plate_x - (n // 16))

    pitcher = (home_plate_y - (n // 10), home_plate_x)
    catcher = (home_plate_y, home_plate_x)

    right_field = (home_plate_y - (n // 3), home_plate_x + (n // 4))
    left_field = (home_plate_y - (n // 3), home_plate_x - (n // 4))
    center_field = (home_plate_y - (n // 3) - (n//16), home_plate_x)


    #Now we shift based on the hottest hotspot
    flat_indices = np.dstack(np.unravel_index(np.argsort(-np.array(predmatrix).ravel()), (n, m)))[0]
    hotspot = (flat_indices[0][0], flat_indices[0][1])

    #second base, shortstop
    dist_first_thirdbase = np.linalg.norm(np.array(first_base) - np.array(third_base))

    dist_hotspot_shortstop = np.linalg.norm(np.array(hotspot) - np.array(shortstop))
    dist_hotspot_secbase = np.linalg.norm(np.array(hotspot) -  np.array(second_base))

    if(dist_hotspot_shortstop > dist_hotspot_secbase):  #smaller multiplier = closer
      shortstop = shiftPositionRadially(shortstop,hotspot, 1.2)
      second_base = shiftPositionRadially(second_base,hotspot, 1.1)
    else:
      shortstop = shiftPositionRadially(shortstop,hotspot, 1.1)
      second_base = shiftPositionRadially(second_base,hotspot, 1.2)


    #far fielders
    dist_leftfield_hotspot = np.linalg.norm(np.array(left_field) - np.array(hotspot))
    dist_rightfield_hotspot = np.linalg.norm(np.array(right_field) - np.array(hotspot))
    dist_centerfield_hotspot = np.linalg.norm(np.array(center_field) - np.array(hotspot))

    field_distances = {
        "left_field": dist_leftfield_hotspot,
        "right_field": dist_rightfield_hotspot,
        "center_field": dist_centerfield_hotspot
      }
    
    #Sort by distance
    field_distances = dict(sorted(field_distances.items(), key=lambda item: item[1]))

    # Assign multipliers based on closeness, the closer the more it moves
    multipliers = [0.7, 0.8, 0.9]

        # Iterate and update the original variables
    for index, (field, distance) in enumerate(field_distances.items()):
        if field == "left_field":
            left_field = shiftPositionAlongX(left_field, hotspot, multipliers[index])
        elif field == "right_field":
            right_field = shiftPositionAlongX(right_field, hotspot, multipliers[index])
        elif field == "center_field":
            center_field = shiftPositionAlongX(center_field, hotspot, multipliers[index])


    selected_positions = []
    selected_positions.append(first_base)
    selected_positions.append(third_base)
    selected_positions.append(pitcher)
    selected_positions.append(catcher)
    selected_positions.append(second_base)
    selected_positions.append(shortstop)
    selected_positions.append(right_field)
    selected_positions.append(left_field)
    selected_positions.append(center_field)

    return selected_positions

def shiftPositionAlongX(positiontoshift, magnetposition, multiplier):
    magnet_x = magnetposition[1]

    distance_x = positiontoshift[1] - magnet_x

    shifted_x = magnet_x + distance_x * multiplier
    shifted_y = positiontoshift[0]

    return (int(shifted_y), int(shifted_x))

    

def shiftPositionRadially(positiontoshift, magnetposition, multiplier):
    '''
    Shift a position radially based on a magnet position and a multiplier
    :param positiontoshift: position to shift
    :param magnetposition: position of the magnet
    :param multiplier: multiplier to shift by
    :return: shifted position
    '''
    magnet_x = magnetposition[1]
    magnet_y = magnetposition[0]

    angle = np.arctan2(positiontoshift[1] - magnet_y, positiontoshift[0] - magnet_x)
    distance = np.sqrt((positiontoshift[0] - magnet_x)**2 + (positiontoshift[1] - magnet_y)**2)
    shiftedDistance = distance * multiplier

    # Now keep the same angle, use the new distance, and find the new position x, y
    shifted_x = magnet_x + shiftedDistance * np.cos(angle)
    shifted_y = magnet_y + shiftedDistance * np.sin(angle)

    return (int(shifted_x), int(shifted_y))

def adaptToGameState(outfielder_positions,score, basesLoaded, inning):
    '''
    Adapt outfielder positions based on the current game state
    :return: adapted outfielder positions
    '''

    #score from batters perspective
    depth = 1   #1 is neutral, less is more shallow, more is deeper
    home_plate_x = n // 2
    home_plate_y = n - (n // 4) + (n//32)
    home_plate = (home_plate_x, home_plate_y)

    #if 3rd base loaded, play more shallow to hit them out
    if basesLoaded[2] == 1:
      depth = depth * 0.9

    #if no bases loaded, play deeper to prevent big plays
    # if sum(basesLoaded) == 0:
    if sum(1 for base in basesLoaded if base is not None) == 0:
      depth = depth * 1.1


    #if lead is large, play deeper to prevent big scoring oportunities
    if score > 3:
      depth = depth * 1.1

    outfielder_positions_c = list(outfielder_positions)

     #outfielders are index 6,7,8
    for i in range(6,len(outfielder_positions_c)):
        outfielder_positions_c[i] = shiftPositionRadially(outfielder_positions_c[i],home_plate, depth)

    return outfielder_positions_c

def applyStrategy(score, strategy, outfielder_positions):
    #strategy = -1 means defensive 0 means neutral, and 1 means agressive
    #Agressive: play shallow so we throw out runners getting to home plate
    #Defensive: play deeper to prevent large scorings
    depth = 1
    home_plate_x = n // 2
    home_plate_y = n - (n // 4) + (n//32)
    home_plate = (home_plate_x, home_plate_y)

    #if score is close, favoring the pitching team, or is tied
    if (abs(score) <= 3) or (score == 0):
      match strategy:
        case -1:
          depth = depth * 1.1
        case 1:
          depth = depth * 0.9

    #if lead is large, play deeper to prevent big scoring oportunities
    if score > 3:
      match strategy:
        case -1:
          depth = depth * 1.1
        case 1:
          depth = depth * 1.2


    outfielder_positions_c = list(outfielder_positions)

     #outfielders are index 6,7,8
    for i in range(6,len(outfielder_positions_c)):
        outfielder_positions_c[i] = shiftPositionRadially(outfielder_positions_c[i],home_plate, depth)

    return outfielder_positions_c