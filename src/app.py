import tkinter as tk
from tkinter import Image, ttk
from PIL import Image, ImageTk

class App(tk.Tk): 
    def __init__(self):
        self.form_fields = {}
        self.frame_height = 700
        super().__init__()
        self.title("Field Vision AI")
        self.geometry("1100x1000")
        self.addFrames()
        self.input_form(self.left_frame)
        self.canvas = tk.Canvas(self.right_frame, width=700, height=self.frame_height, bg="#f4dabb")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.add_field_image(self.right_frame)
        self.current_heatmap_id = None 
        self.outfielders = None
        self.heatmap_img = None
        self.heatmap_images = {}

        # Set the window to be on top temporarily
        self.attributes('-topmost', True)
        
        # Bring the window to focus
        self.focus_force()
        
        # Remove the topmost attribute after a short delay
        self.after(100, lambda: self.attributes('-topmost', False))
        
    def addFrames(self):
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill="both", expand=True)

        self.top_frame = tk.Frame(self.main_frame, height=100)
        self.top_frame.pack(side="top", fill="x", expand=False)

        self.left_frame = tk.Frame(self.main_frame, width=300)
        self.left_frame.pack(side="left", fill="y", padx=10, pady=10)

        self.right_frame = tk.Frame(self.main_frame, width=900)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        titleLabel = tk.Label(self.top_frame, text="Field Vision AI", font=("Helvetica", 26))
        titleLabel.pack(pady=10)

    def input_form(self,frame): # uses a grid to place the input fields
        row = 0
        self.addLabel(frame, "Select test case:", row, 0)

        # row+=1
        self.test_case = tk.StringVar(frame)
        self.test_case.set("N/A")
        self.test_case_options = ["N/A", "Test 1", "Test 2", "Test 3"]
        self.test_case_menu = tk.OptionMenu(frame, self.test_case, *self.test_case_options)
        self.test_case_menu.config(width=15)
        self.test_case_menu.grid(row=row, column=1, pady=10)
        row+=1
        
        ttk.Separator(frame, orient='horizontal').grid(row=row, column=0, columnspan=2, sticky="ew", pady=10)
        row+=1

        self.form = {} 
        # pitcher id
        self.addLabel(frame, "Pitcher ID:", row, 0)
        self.pitcher = tk.IntVar(frame)
        pitcher_entry = tk.Entry(frame, textvariable=self.pitcher)
        pitcher_entry.grid(row=row, column=1, sticky="w")
        row+=1

        # batter id
        self.addLabel(frame, "Batter ID:", row, 0)
        self.batter = tk.IntVar(frame)
        batter_input = tk.Entry(frame, textvariable=self.batter)
        batter_input.grid(row=row, column=1)
        row+=1

        # year
        self.addLabel(frame, "Year:", row, 0)
        self.year = tk.IntVar(frame)
        year_entry = tk.Entry(frame, textvariable=self.year)
        year_entry.grid(row=row, column=1)
        row+=1

        # pitch number
        self.addLabel(frame, "Pitch number:", row, 0)
        self.pitch = tk.IntVar(frame)
        pitch_entry = tk.Entry(frame, textvariable=self.pitch)
        pitch_entry.grid(row=row, column=1)
        row+=1

        # bat score
        self.addLabel(frame, "Bat score:", row, 0)
        self.bat_score = tk.IntVar(frame)
        bat_score_entry = tk.Entry(frame, textvariable=self.bat_score)
        bat_score_entry.grid(row=row, column=1)
        row+=1

        # field score
        self.addLabel(frame, "Field score:", row, 0)
        self.field_score = tk.IntVar(frame)
        field_score_entry = tk.Entry(frame, textvariable=self.field_score)
        field_score_entry.grid(row=row, column=1)
        row+=1

        # innings
        self.addLabel(frame, "Inning:", row, 0)
        self.inning = tk.IntVar(frame)
        inning_entry = tk.Entry(frame, textvariable=self.inning)
        inning_entry.grid(row=row, column=1)
        row+=1

        # strikes
        self.addLabel(frame, "Strikes:", row, 0)
        self.strikes = tk.IntVar(frame)
        self.strikes.set(0)
        strike_options = [0, 1, 2, 3]
        strike_menu = tk.OptionMenu(frame, self.strikes, *strike_options)
        strike_menu.config(width=15)
        strike_menu.grid(row=row, column=1, pady=10)
        row+=1

        # balls
        self.addLabel(frame, "Balls:", row, 0)
        self.balls = tk.IntVar(frame)
        self.balls.set(0)
        balls_options = [0, 1, 2]
        balls_menu = tk.OptionMenu(frame, self.balls, *balls_options)
        balls_menu.config(width=15)
        balls_menu.grid(row=row, column=1, pady=10)
        row+=1

        # batter side 
        self.addLabel(frame, "Stand:", row, 0)
        self.stand = tk.StringVar(frame)
        self.stand.set("R") # change to "R"
        batter_side_options = ["R", "L"]
        batter_side_menu = tk.OptionMenu(frame, self.stand, *batter_side_options)
        batter_side_menu.config(width=15)
        batter_side_menu.grid(row=row, column=1, pady=10)
        row+=1

        # Base checkboxes
        self.first_base = tk.IntVar(value=0)
        self.second_base = tk.IntVar(value=0)
        self.third_base = tk.IntVar(value=0)
        first_base_checkbox = tk.Checkbutton(frame, text="First Base", variable=self.first_base)
        first_base_checkbox.grid(row=row, column=0, pady=5, sticky="w")
        
        second_base_checkbox = tk.Checkbutton(frame, text="Second Base", variable=self.second_base)
        second_base_checkbox.grid(row=row, column=1, pady=5, sticky="w")
        row+=1
        third_base_checkbox = tk.Checkbutton(frame, text="Third Base", variable=self.third_base)
        third_base_checkbox.grid(row=row, column=0, columnspan=3, pady=5, sticky="w", padx=0)
        row+=1

        # Add a dropdown for 
        self.game_strategy_label = self.addLabel(frame, "Game Strategy:", row, 0)
        self.game_strategy_label.grid_forget()
        self.game_strategy = tk.StringVar(frame)
        self.game_strategy.set("Neutral")
        game_strategy_options = ["Aggressive", "Neutral", "Defensive"]
        self.game_strategy_menu = tk.OptionMenu(frame, self.game_strategy, *game_strategy_options, command=self.apply_game_strategy)
        self.game_strategy_menu.config(width=15)
        self.game_strategy_menu_row = row
        self.game_strategy_menu.grid_forget()
        row+=1

        ttk.Separator(frame, orient='horizontal').grid(row=row, column=0, columnspan=2, sticky="ew", pady=5)
        row+=1

        # prediction button
        self.action_btn = tk.Button(frame, text="Predict hit location", bg = "#0000FF", width=15) 
        self.action_btn.grid(row=row, column=0, pady=5)

        # Apply game state button
        self.apply_btn = tk.Button(frame, text="Apply Game State", state=tk.DISABLED)
        self.apply_btn.grid(row=row, column=1, pady=5)

        def update_form_fields(*args):
            selected_test = self.test_case.get()
            self.test_cases = {
                "Test 1": {
                    'game_year': 2023,
                    'batter': 527038,
                    'pitcher': 672335,
                    'inning': 6,
                    'stand': "R",
                    'balls': 1,
                    'strikes': 2,
                    'on_1b': True,
                    'on_2b': True,
                    'on_3b': None,
                    'pitch_number': 4,
                    'bat_score': 8,
                    'field_score': 10, 
                    'hc_x': 75.0 * (250/125),
                    'hc_y': 49.0 * (250/125)
                },

                "Test 2": {
                   'game_year': 2023,
                    'batter': 527038,
                    'pitcher': 680694,
                    'inning': 1,
                    'stand': "R",
                    'balls': 0,
                    'strikes': 0,
                    'on_1b': True,
                    'on_2b': None,
                    'on_3b': None,
                    'pitch_number': 1,
                    'bat_score': 15,
                    'field_score': 1, 
                    'hc_x': 42.0 * (2),
                    'hc_y': 15.0 * (2)
                },

                "Test 3": {
                    'game_year': 2023,
                    'batter': 807799,
                    'pitcher': 605280,
                    'inning': 9,
                    'stand': "L",
                    'balls': 0,
                    'strikes': 2,
                    'on_1b': None,
                    'on_2b': None,
                    'on_3b': None,
                    'pitch_number': 5,
                    'bat_score': 3,
                    'field_score': 5, 
                    'hc_x': 76 * (2),
                    'hc_y': 70 * (2)
                },

            }
            selected_test_values = self.test_cases.get(selected_test, {})
            pitcher_entry.delete(0, tk.END)
            pitcher_entry.insert(0, selected_test_values.get("pitcher", ""))
            batter_input.delete(0, tk.END)
            batter_input.insert(0, selected_test_values.get("batter", ""))
            pitch_entry.delete(0, tk.END)
            pitch_entry.insert(0, selected_test_values.get("pitch_number", ""))
            bat_score_entry.delete(0, tk.END)
            bat_score_entry.insert(0, selected_test_values.get("bat_score", ""))
            field_score_entry.delete(0, tk.END)
            field_score_entry.insert(0, selected_test_values.get("field_score", ""))
            year_entry.delete(0, tk.END)
            year_entry.insert(0, selected_test_values.get("game_year", ""))
            inning_entry.delete(0, tk.END)
            inning_entry.insert(0, selected_test_values.get("inning", ""))
            self.stand.set(selected_test_values.get("stand", "R"))
            self.balls.set(selected_test_values.get("balls", 0))
            self.strikes.set(selected_test_values.get("strikes", 0))
            self.first_base.set(1 if selected_test_values.get("on_1b") else 0)
            self.second_base.set(1 if selected_test_values.get("on_2b") else 0)
            self.third_base.set(1 if selected_test_values.get("on_3b") else 0)

        self.test_case.trace_add("write", update_form_fields)
        
    def add_field_image(self, frame):
        margin_x = 20
        img_size = self.frame_height-(2*margin_x)
        field_img = Image.open("src/images/baseball_field.png")
        field_img = self.resize_image(field_img, img_size, img_size)
        img_width, img_height = field_img.size
        field_img = ImageTk.PhotoImage(field_img)
        x1,y1 = (margin_x, (self.frame_height - img_height) // 2)
        x2,y2 = (5, y1-20)
        self.field_img_id = self.canvas.create_image(x1, y1, anchor=tk.NW, image=field_img)
        self.canvas.field_img = field_img
    
    def setHeatmap(self, heatmap_img, heatmap_outfielders_img, heatmap_aggressive_img, heatap_neutral_img, heatmap_defensive_img):
        '''
        Set the heatmap image on the canvas and store a reference to both the heatmap and outfielders heatmap images for easy toggling between the two.
        '''

        self.game_strategy_menu.grid(row=self.game_strategy_menu_row, column=1, pady=5, padx=0)
        self.game_strategy_label.grid(row = self.game_strategy_menu_row, column=0, pady=5, padx=0)
        self.apply_btn.config(state=tk.NORMAL)
        
        # Resize the input image
        img_width, img_height = heatmap_img.size
        margin_x = 20
        img_size = self.frame_height - (2 * margin_x)

        heatmap_aggressive_img_resized = self.resize_image(heatmap_aggressive_img, img_size, img_size)
        heatmap_defensive_img_resized = self.resize_image(heatmap_defensive_img, img_size, img_size)
        heatmap_img_resized = self.resize_image(heatmap_img, img_size, img_size)
        heatmap_outfielders_img_resized = self.resize_image(heatmap_outfielders_img, img_size, img_size)

        # Convert to ImageTk.PhotoImage
        self.heatmap_img_tk = ImageTk.PhotoImage(heatmap_img_resized)
        self.heatmap_outfields_img_tk = ImageTk.PhotoImage(heatmap_outfielders_img_resized)
        self.heatmap_aggressive_img_tk = ImageTk.PhotoImage(heatmap_aggressive_img_resized)
        self.heatmap_defensive_img_tk = ImageTk.PhotoImage(heatmap_defensive_img_resized)

        self.img_height = heatmap_img_resized.size[1]
        x1, y1 = (20, (self.frame_height - img_height) // 2)
        x2, y2 = (15, y1+25)

        self.heatmap_images = {
            "Aggressive": self.heatmap_aggressive_img_tk,
            "Neutral": self.heatmap_outfields_img_tk,
            "Defensive": self.heatmap_defensive_img_tk,
            "Outfielders": self.heatmap_outfields_img_tk,
            "Basic": self.heatmap_img_tk
        }
        self.game_strategy.set("Neutral")
        self.drawImage(self.heatmap_outfields_img_tk, "Neutral")

    def drawImage(self, img, img_type):
        margin_x = 20
        x1, y1 = (margin_x, (self.frame_height - self.img_height) // 2)
        x2, y2 = (15, y1+25)

        self.canvas.delete(self.current_heatmap_id)
        self.current_heatmap_id = self.canvas.create_image(x2, y2, anchor="nw", image=img)
        self.heatmap_images[img_type] = img

    # Event handlers
    def showPrediction(self):
        self.get_form_fields()
        self.canvas.delete(self.current_heatmap_id)
        self.drawImage("field_probabilities.png") # this funcion is slow
        self.game_strategy_menu.grid(row=self.game_strategy_menu_row, column=1, pady=5, padx=0)
        self.game_strategy_label.grid(row = self.game_strategy_menu_row, column=0, pady=5, padx=0)
        self.apply_btn.config(state=tk.NORMAL)

    def apply_game_strategy(self, selected_strategy):
        if self.current_heatmap_id: # remove current heatmap img
            self.canvas.delete(self.current_heatmap_id)
        self.drawImage(self.heatmap_images[selected_strategy], selected_strategy)
       
    ### Helper functions to add widgets to the frame
    def addLabel(self, frame, text, row, col):
        new_label = tk.Label(frame, text=text)
        new_label.grid(row=row, column=col, pady=10, padx=10, sticky="w")
        return new_label
    
    def addEntry(self, frame, row, col):
        new_entry = tk.Entry(frame)
        new_entry.grid(row=row, column=1)
        return new_entry
    
    def resize_image(self, image, new_width, new_height):
        img_width, img_height = image.size
        width_ratio = new_width / img_width
        height_ratio = new_height / img_height
        scale_factor = min(width_ratio, height_ratio)
        new_width = int(img_width * scale_factor)
        new_height = int(img_height * scale_factor)
        resized_image = image.resize((new_width, new_height), Image.LANCZOS)
        return resized_image
    
    def adaptGameState(self, strategy):
        # display a different image based on the strategy
        # check that the images are loaded on the canvas first
        # TODO: implement this function
        pass

    def getActionBtn(self):
        return self.action_btn
    
    def getApplyBtn(self):
        return self.apply_btn
    
    def get_form_fields(self):
        self.form_fields['pitcher'] = self.pitcher.get()
        self.form_fields['batter'] = self.batter.get()
        self.form_fields['game_year'] = self.year.get()
        self.form_fields['pitcher'] = self.pitcher.get()
        self.form_fields['batter'] = self.batter.get()
        self.form_fields['inning'] = self.inning.get()
        self.form_fields['stand'] = self.stand.get()
        self.form_fields['balls'] = self.balls.get()
        self.form_fields['strikes'] = self.strikes.get()
        self.form_fields['on_1b'] = self.first_base.get()
        self.form_fields['on_2b'] = self.second_base.get()
        self.form_fields['on_3b'] = self.third_base.get()
        self.form_fields['pitch_number'] = self.pitch.get()
        self.form_fields['bat_score'] = self.bat_score.get()
        self.form_fields['field_score'] = self.field_score.get()

        test_case = self.test_case.get()
        if test_case == "N/A":
            return self.form_fields
        
        form_fields = self.test_cases[test_case]
        if 'hc_x' in form_fields:
            self.form_fields['hc_x'] = form_fields['hc_x']
            self.form_fields['hc_y'] = form_fields['hc_y']
        return self.form_fields

if __name__ == "__main__":
    app = App()
    app.mainloop()