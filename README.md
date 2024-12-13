# FieldVision-AI
AI-Based MLB Outfielder Recommendation

## Introduction

This project, FieldVision AI, introduces an innovative AI-powered system designed to optimize outfielder positioning in baseball. Inspired by the movie "Moneyball", we developed a tool that leverages machine learning and statistical analysis to recommend ideal outfielder placements based on real-time game situations and historical player data. By accurately predicting ball landing locations and dynamically adjusting defensive strategies, FieldVision AI aims to assist coaches and enhance on-field performance in the MLB.

## Description
> For more details about the methods used and their results, please read the "report.pdf" in the docs dir.

### Data Parsing/API

Our project leverages the Pybaseball API to access comprehensive MLB data, including individual game events, player statistics, and season averages. To optimize data retrieval and processing, we implemented a vectorized approach using the Pandas library. This method significantly reduced the processing time for our large dataset (over 310,000 game events) by applying operations to entire DataFrames simultaneously, instead of individual events. This efficient data handling enabled us to extract and format 54 relevant features for each game event, which were then used to train and evaluate our neural network model.

### Model Architecture

We designed a neural network with three fully connected dense layers, each containing 512 neurons, to predict the landing position of a baseball hit. The model takes 54 input features extracted from the Pybaseball API and outputs a probability heatmap of size 125x125 representing the field. To improve model performance and prevent overfitting, we incorporated batch normalization after each dense layer and applied dropout layers.

#### Outfielder Positioning Loss (OPL)

To address the limitations of standard loss functions for our spatial prediction task, we developed a novel loss function called "Outfielder Positioning Loss" (OPL). OPL combines categorical cross-entropy with distance and confidence regularization components. This approach encourages the model to accurately predict the ball's trajectory while considering the proximity of predictions to the true landing spot and promoting high confidence in the top predictions. OPL significantly improved predictive accuracy compared to traditional methods, demonstrating the importance of incorporating spatial awareness into the loss function.

### Rule-Based Logic

We implemented a rule-based system to translate the model's predicted landing probabilities into actionable outfielder positions. This system identifies the highest probability areas on the heatmap and shifts outfielders toward those spots. Additionally, it allows coaches to adjust positioning based on the current game situation and their desired strategy (defensive, neutral, or aggressive). This flexibility enables coaches to adapt their tactics dynamically and optimize outfielder placement for specific game contexts.

### Results

Our model, trained on a comprehensive dataset of MLB game events, achieved a top-9 accuracy of 2.1%, meaning it correctly predicted at least one of the top nine landing spots for the ball in 2.1% of the test cases. This performance represents a significant improvement over random guessing **(30x better)** and baseline approaches **(10x better)**. Furthermore, our outfielder positioning recommendations effectively reduced the distance between the closest fielder and the actual ball landing location in **90.5%** of the simulated game scenarios. These results demonstrate the potential of our AI-driven system to enhance on-field decision-making and improve defensive performance in baseball.

### Application

To facilitate practical use of our system, we developed a user-friendly graphical user interface (GUI). The application allows coaches to input game-specific information, such as the inning, number of balls and strikes, and current score. It then displays a heatmap visualizing the predicted ball landing probabilities and suggests optimal outfielder positions based on the chosen strategy. This interactive tool empowers coaches to leverage AI insights in real-time, enabling them to make data-driven decisions and optimize defensive strategy throughout the game.

## Installation and Execution
### Install
To install the required Python libraries, run the following command from the src directory:
```bash
pip install -r .\requirements.txt
```
*You need to have pip installed to PATH*

### Running the Program
To start the Tkinter program, run the following command from the src directory:
```bash
python ./main
#OR
python3 ./main
```

## Using the program
...
