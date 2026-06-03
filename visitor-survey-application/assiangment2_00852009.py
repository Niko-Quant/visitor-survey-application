import tkinter as tk
from tkinter import *
from tkinter import messagebox, ttk
import csv
import os
import statistics




# Aeolus Sculpture Survey App 
# This program was made by Nikodem Nowak. It collects survey responses from visitors and stores the results. So it can be used in future for data analysis
# ------------------------------------------------------------

# This class is like a blueprint for storing one person's survey answer, it has all answers to all questions asked on survey 
class SurveyResponse:
    def __init__(self, name, age, sex, ethnicity, disability, enjoyed, curious, more_science): # This function runs every time we recieve a new survey response and stores it as one single object.
        self.name = name   # Saves the persons name 
        self.age = age     # asves the persons age as a integer
        self.sex = sex     # saves the persons sex
        self.ethnicity = ethnicity    #Saves the persons ethnicity 
        self.disability = disability  #Saves any disabilities the person has stated
        self.enjoyed = enjoyed        #Saves response from 1-5 if the person has enjoyed their time 
        self.curious = curious        #Saves response 1-5 if the person is curious about how it works 
        self.more_science = more_science   #saves response 1-5 if the person is more curious about science now  


# This is the main app window
class SurveyApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window title and size
        self.title("The Aeolus Sculpture Survey")  #Gives the GUI a title which is seen at top of GUI
        self.geometry("800x600")                    #This is the default size of the gui on first startup

        # Make the background colour match the white on the logo image
        self.bg_colour = "#FFFFFF"
        self.configure(bg=self.bg_colour)

        # This is where where all survey answers are stored as a list as we are using [] brackets 
        self.responses = []

        # Load previous survey results if CSV exists (so data is not lost when app closes)
        if os.path.isfile("survey_results.csv"):
            with open("survey_results.csv", "r", newline="") as file:
                reader = csv.reader(file)
                next(reader, None)  # skip header row

                for row in reader:
                    try:
                        self.responses.append(SurveyResponse(
                            name=row[0],
                            age=int(row[1]),
                            sex=int(row[2]),
                            ethnicity=int(row[3]),
                            disability=int(row[4]),
                            enjoyed=int(row[5]),
                            curious=int(row[6]),
                            more_science=int(row[7])
                        ))
                    except:
                        pass  # ignore broken rows rather than crashing the application 


        # This creates all the tabs in the GUI
        self.create_tabs()

        # This builds what goes inside each tab 
        self.create_survey_tab()
        self.create_login_tab()
        self.create_host_tab()

    # Creates the notebook widget allowing me to use 3 tabs
    def create_tabs(self):
        # Configure ttk styles so frames/labels use the same background as the window
        style = ttk.Style()
        try:
            style.configure("TFrame", background=self.bg_colour)  # ttk Frame background
            style.configure("TLabel", background=self.bg_colour)  # ttk Label background
        except:
            pass  # if styling fails on this platform/theme, it continues without failing the engine 

        # Notebook = tab control that holds multiple pages
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)  # This makes it fill the whole window

        # Create the three tab pages (they start empty; widgets are added later)
        self.tab_survey = ttk.Frame(self.notebook)  # visitor survey page
        self.tab_login = ttk.Frame(self.notebook)   # host login page where you type password to have acces to host tab to see results 
        self.tab_host = ttk.Frame(self.notebook)    # host dashboard page which is locked by default until passowrd is entered on login tab 

        # Adds tabs to the notebook with visible names in the ""
        self.notebook.add(self.tab_survey, text="Survey")
        self.notebook.add(self.tab_login, text="Host Login")
        self.notebook.add(self.tab_host, text="Host Page")

        # Lock the Host tab until the password is entered correctly 
        self.notebook.tab(self.tab_host, state="disabled")

      
    #-- Below are functions i require further in the code for dashobard so its easier to read statistics 

    def sex_display(self, sex_code): # Converts stored sex code (1/2/3) into a short display letter for the dashboard so it is easier to read 
        return {1: "M", 2: "F", 3: "O"}.get(sex_code, "?")

    def disability_display(self, disability_code):  # Converts stored disability answer into a readable name for the dashboard statistics to make it easier to read
        return {0: "N", 1: "Y"}.get(disability_code, "?")

    def ethnicity_display(self, ethnicity_code):         # Converts stored ethnicity answer into a readable name for the dashboard statistics to make it easier to read
        return {1: "White", 2: "Black", 3: "Chinese", 4: "Asian", 5: "Other"}.get(ethnicity_code, "?")

    def apply_bg(self, widget):    # Applies the same background colour to normal tk widgets. Frames, Labels and Canvas
        try:
            widget.configure(bg=self.bg_colour)
        except:
            pass    # if styling fails on this platform/theme, it continues without failing the engine 

    def create_survey_tab(self): # This function makes sure the tab background matches the logo white
        try:
            self.tab_survey.configure(style="TFrame")  # tries to set a ttk frame style
        except:
            pass  # if style fails, just continue without failing the engine and crashing 


        # Put all survey widgets in a content frame ABOVE the canvas
        content = tk.Frame(self.tab_survey, bg=self.bg_colour)  # makes a normal frame that will sit above the canvas
        content.pack(fill="both", expand=True)  # makes the content frame fill the tab area

        # -----------------------------
        # LOGO (top-left) + TITLE (center)
        # -----------------------------
        header = tk.Frame(content, bg=self.bg_colour)   # header row for logo + title
        header.pack(fill="x", pady=(10, 10))           # place header at top of page

        # Build an absolute path to the logo (so it loads even if you run from a different folder)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(base_dir, "assignment logo for sculpture.png")

        try:
            self.logo_image = tk.PhotoImage(file=logo_path)      # load the logo image
            self.logo_small = self.logo_image.subsample(3, 3)    # make it smaller (try 2,2 or 4,4)
            self.logo_label = tk.Label(header, image=self.logo_small, bg=self.bg_colour)  # show the logo
            self.logo_label.grid(row=0, column=0, sticky="w", padx=(10, 0))               # top-left
        except Exception as e:
            print("Logo load failed:", e)  # shows why it failed in the terminal
            self.logo_image = None
            self.logo_small = None

        # Put the title in the same header row, but centered
        title_label = ttk.Label(header, text="The Aeolus Sculpture Survey", font=("Arial", 20))
        title_label.grid(row=0, column=1, pady=10)

        # Make the title column expand so it stays centered
        header.columnconfigure(1, weight=1)


     
        # NAME text box 
        # -----------------------------
        name_label = ttk.Label(content, text="Your Name:")  # creates the name label
        name_label.pack()  # places the label on the screen
        self.name_entry = ttk.Entry(content)  # creates a text box for typing a name
        self.name_entry.pack()  # places the text box on the screen

       
        # AGE text box 
        # -----------------------------
        age_label = ttk.Label(content, text="Your Age:")  # creates the age label
        age_label.pack()  # places the label on the screen
        self.age_entry = ttk.Entry(content)  # creates a text box for typing age
        self.age_entry.pack()  # places the text box on the screen

       
        # SEX Dropdown box
        # -----------------------------
        sex_label = ttk.Label(content, text="Sex:")  # creates the sex label
        sex_label.pack()  # places the label on the screen

        self.sex_var = tk.IntVar()  # this stores a number for sex choice
        self.sex_var.set(1)  # sets default choice to 1

        # Radiobuttons for sex (more accessible than typing into a dropdown)
        sex_radio_frame = tk.Frame(content, bg=self.bg_colour)  # frame to hold the sex radio buttons
        sex_radio_frame.pack(pady=(0, 10))  # adds a bit of spacing under it

        ttk.Radiobutton(sex_radio_frame, text="Male", variable=self.sex_var, value=1).grid(row=0, column=0, padx=10)  # option 1
        ttk.Radiobutton(sex_radio_frame, text="Female", variable=self.sex_var, value=2).grid(row=0, column=1, padx=10)  # option 2
        ttk.Radiobutton(sex_radio_frame, text="Other", variable=self.sex_var, value=3).grid(row=0, column=2, padx=10)  # option 3

        # ETHNICITY Radiobutton
        # -----------------------------
        ethnicity_label = ttk.Label(content, text="Ethnicity:")  # creates the ethnicity label
        ethnicity_label.pack()  # places the label on the screen

        self.ethnicity_dropdown = ttk.Combobox(  # creates a dropdown menu
            content,  # makes it appear in the content frame
            values=[  # list of ethnicity choices
                "1 - White",
                "2 - Black",
                "3 - Chinese",
                "4 - Asian",
                "5 - Other"
            ],
            state="readonly"  # stops the user typing random text
        )
        self.ethnicity_dropdown.current(0)  # picks the first option as default
        self.ethnicity_dropdown.pack()  # places the dropdown on the screen

        # -----------------------------
        # DISABILITY Radio button 
        # -----------------------------
        disability_label = ttk.Label(content, text="Disability:")  # creates the disability label
        disability_label.pack()  # places the label on the screen

        self.disability_var = tk.IntVar()  # stores disability as 0 or 1
        self.disability_var.set(0)  # default is 0 meaning No

        disability_radio_frame = tk.Frame(content, bg=self.bg_colour)  # frame for disability radio buttons
        disability_radio_frame.pack(pady=(0, 10))  # adds spacing below the buttons

        ttk.Radiobutton(disability_radio_frame, text="No", variable=self.disability_var, value=0).grid(row=0, column=0, padx=10)  # No option
        ttk.Radiobutton(disability_radio_frame, text="Yes", variable=self.disability_var, value=1).grid(row=0, column=1, padx=10)  # Yes option


        # COLOURED BUTTONS SETUP (used for all 3 questions)
        # ------------------------------------------------------
        button_colours = {  # dictionary of colours for each score button
            1: ("#E53935", "#B71C1C"),  # red normal and once selected
            2: ("#FB8C00", "#EF6C00"),  # orange normal and once selected
            3: ("#FDD835", "#FBC02D"),  # yellow normal and once selected
            4: ("#7CB342", "#558B2F"),  # green normal and once selected
            5: ("#43A047", "#1B5E20")   # dark green normal and once selected
        }

        # function to build Likert question 
        def build_likert(parent, question_text, variable_name):
            group = tk.Frame(parent, bg=self.bg_colour)  # holds the whole question block
            group.pack(pady=(10, 30))  # adds spacing between questions

            q_label = ttk.Label(group, text=question_text)  # label for the question
            q_label.pack()  # places the label

            var = tk.IntVar(value=3)  # stores the selected button, default is 3 when refreshed 
            setattr(self, variable_name, var)  # saves it on self so save_survey can read it

            buttons_row = tk.Frame(group, bg=self.bg_colour)  # frame that holds the coloured buttons
            buttons_row.pack(pady=(6, 4))  # adds spacing around the buttons
            buttons = {}  # keeps references to all the buttons so we can change colours

            def select_value(value):
                var.set(value)  # updates the stored number
                for n, b in buttons.items():  # loops through each button
                    normal, selected = button_colours[n]  # gets colours for this number
                    if n == value:  # if this is the selected button
                        b.config(bg=selected, relief="sunken")  # show selected style
                    else:
                        b.config(bg=normal, relief="raised")  # show normal style

            for num in range(1, 6):  # makes buttons 1 to 5
                normal, selected = button_colours[num]  # this gets the colours previously listed
                btn = tk.Button(
                    buttons_row, text=str(num), width=5, height=2,  # sets size and number text
                    bg=normal, fg="white", font=("Arial", 12, "bold"),  # sets colours and font
                    command=lambda n=num: select_value(n)  # runs when the button is clicked
                )
                btn.grid(row=0, column=num-1, padx=8)  # places buttons in one row
                buttons[num] = btn  # stores the button reference

            desc = tk.Frame(group, bg=self.bg_colour)  # frame for the meaning text under buttons
            desc.pack(pady=(2, 0))  # places it under the buttons

            tk.Label(desc, text="1 Strongly Disagree", bg=self.bg_colour).grid(row=0, column=0, padx=10)  # label for button 1
            tk.Label(desc, text="2 Disagree", bg=self.bg_colour).grid(row=0, column=1, padx=10)  # label for button 2
            tk.Label(desc, text="3 Neither", bg=self.bg_colour).grid(row=0, column=2, padx=10)  # label for button 3
            tk.Label(desc, text="4 Agree", bg=self.bg_colour).grid(row=0, column=3, padx=10)  # label for button 4
            tk.Label(desc, text="5 Strongly Agree", bg=self.bg_colour).grid(row=0, column=4, padx=10)  # label for button 5

            select_value(3)  # sets the default selected colour to 3

       
        # LIKERT QUESTION 1 
        # -----------------------------
        build_likert(content, "Did you enjoy the sculpture?", "enjoyed_var")  # builds enjoyed buttons

       
        # LIKERT QUESTION 2 
        # -----------------------------
        build_likert(content, "Are you curious how it worked?", "curious_var")  # builds curious buttons

        
        # LIKERT QUESTION 3 
        # -----------------------------
        build_likert(content, "Do you want to learn more science?", "science_var")  # builds science buttons

       
        # SUBMIT BUTTON
        # -----------------------------
        submit_btn = ttk.Button(content, text="Submit Answers", command=self.save_survey)  # button that saves the survey
        submit_btn.pack(pady=20)  # places the button and adds spacing

    def save_survey(self):
       
        # 1. Get the name text
        # -------------------------------
        name = self.name_entry.get().strip()

        if name == "": # makes sure the name is entered in letters like a variable 
            messagebox.showerror("Error", "Name cannot be empty!")
            return

        # Extra validation: name should be at least 1 characters (helps data quality)
        if len(name) < 1:
            messagebox.showerror("Error", "Name must be at least 2 characters long!")
            return

        
        # 2. Gets the age and check its a valid number 
        # -------------------------------
        age_text = self.age_entry.get().strip()

        # Try to turn age into a number
        try:
            age = int(age_text)
            if age <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Age must be a positive number!")
            return

        # Extra validation: realistic age range check
        if age < 1 or age > 100:
            messagebox.showerror("Error", "Please enter an age between 1 and 100.")
            return

    
        # 3. Get the dropdown values 
        # -------------------------------
        sex = int(self.sex_var.get())
        ethnicity_choice = self.ethnicity_dropdown.get()[0]  # first character
        ethnicity = int(ethnicity_choice)
        disability = int(self.disability_var.get())


      
        # 4. Get the Likert values
        # -------------------------------
        enjoyed = self.enjoyed_var.get()
        curious = self.curious_var.get()
        more_science = self.science_var.get()

     
        # 5. Create a SurveyResponse object
        # -------------------------------
        response = SurveyResponse(
            name=name,
            age=age,
            sex=sex,
            ethnicity=ethnicity,
            disability=disability,
            enjoyed=enjoyed,
            curious=curious,
            more_science=more_science
       )

         
             # 6. Add it to the list of responses
            # -------------------------------
        self.responses.append(response)

     
        # Save response to CSV file
        # -------------------------------
        file_exists = os.path.isfile("survey_results.csv")

        with open("survey_results.csv", "a", newline="") as file:
            writer = csv.writer(file)

            # Write header only once
            if not file_exists:
                writer.writerow([
                    "Name", "Age", "Sex", "Ethnicity", "Disability",
                    "Enjoyed", "Curious", "More Science"
                ])

            writer.writerow([
                name, age, sex, ethnicity, disability,
                enjoyed, curious, more_science
            ])


       # 7. Show success message
       # -------------------------------
        messagebox.showinfo("Saved", "Thank you! Your response has been saved.")

    
       # 8. Clears the form for the next person to answer
       # -------------------------------
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.sex_var.set(1)
        self.ethnicity_dropdown.current(0)
        self.disability_var.set(0)
        self.enjoyed_var.set(3)
        self.curious_var.set(3)
        self.science_var.set(3)

        # Automatically refresh host table when you open host page 
        if hasattr(self, "responses_table"):
            self.update_stats()

    
    # Login Tab where Host types password
    # ---------------------------
    def create_login_tab(self):
        label = ttk.Label(self.tab_login, text="Host Login", font=("Arial", 20))
        label.pack(pady=20)
        self.password_entry = ttk.Entry(self.tab_login, show="*")  # this hides typed characters
        self.password_entry.pack()
        login_btn = ttk.Button(self.tab_login, text="Login", command=self.check_password)
        login_btn.pack(pady=10)

    def check_password(self):
        # Checks the entered password with previously set password and unlocks the Host tab if correct
        password = self.password_entry.get()

        if password == "Nigel":  # password for host
            messagebox.showinfo("Welcome", "Password correct!")

            # Enable Host tab and switch to it
            self.notebook.tab(self.tab_host, state="normal")
            self.notebook.select(self.tab_host)

            # Clear password box after successful login
            self.password_entry.delete(0, tk.END)

            # Populate table and stats immediately upon entering host page
            if hasattr(self, "responses_table"):
                self.update_stats()
        else:
            messagebox.showerror("Error", "Wrong password!")

    # Host Page which shows data + stats
    # ---------------------------
    def create_host_tab(self):
        label = ttk.Label(self.tab_host, text="Host Dashboard", font=("Arial", 20))
        label.pack(pady=20)

        
        # Host Search options and Filters 
        # -----------------------------
        filter_frame = ttk.Frame(self.tab_host)
        filter_frame.pack(fill="x", padx=10, pady=(0, 5))

        ttk.Label(filter_frame, text="Search name:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(filter_frame, textvariable=self.search_var, width=20)
        search_entry.grid(row=0, column=1, padx=5, pady=2, sticky="w")

        ttk.Label(filter_frame, text="Sex:").grid(row=0, column=2, padx=5, pady=2, sticky="w")
        self.filter_sex_var = tk.StringVar(value="All")
        self.filter_sex = ttk.Combobox(filter_frame, state="readonly",
                                       values=["All", "M", "F", "O"], width=6,
                                       textvariable=self.filter_sex_var)
        self.filter_sex.grid(row=0, column=3, padx=5, pady=2, sticky="w")

        ttk.Label(filter_frame, text="Disability:").grid(row=0, column=4, padx=5, pady=2, sticky="w")
        self.filter_dis_var = tk.StringVar(value="All")
        self.filter_dis = ttk.Combobox(filter_frame, state="readonly",
                                       values=["All", "Y", "N"], width=6,
                                       textvariable=self.filter_dis_var)
        self.filter_dis.grid(row=0, column=5, padx=5, pady=2, sticky="w")

        ttk.Button(filter_frame, text="Apply Filter", command=self.update_stats).grid(row=0, column=6, padx=10, pady=2)
        ttk.Button(filter_frame, text="Clear", command=self.clear_filters).grid(row=0, column=7, padx=5, pady=2)


        # This frame holds the table of responses
        table_frame = ttk.Frame(self.tab_host)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Create a table to display responses
        columns = ("name", "age", "sex", "ethnicity", "disability", "enjoyed", "curious", "more_science")
        self.responses_table = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)

        # Set table headings shown at the top of the Table
        self.responses_table.heading("name", text="Name")
        self.responses_table.heading("age", text="Age")
        self.responses_table.heading("sex", text="Sex (M/F/O)")
        self.responses_table.heading("ethnicity", text="Ethnicity")
        self.responses_table.heading("disability", text="Disability (Y/N)")
        self.responses_table.heading("enjoyed", text="Enjoyed (1-5)")
        self.responses_table.heading("curious", text="Curious (1-5)")
        self.responses_table.heading("more_science", text="More Science (1-5)")

        # Column widths (simple and readable)
        self.responses_table.column("name", width=140)
        self.responses_table.column("age", width=60, anchor="center")
        self.responses_table.column("sex", width=70, anchor="center")
        self.responses_table.column("ethnicity", width=110, anchor="center")
        self.responses_table.column("disability", width=110, anchor="center")
        self.responses_table.column("enjoyed", width=110, anchor="center")
        self.responses_table.column("curious", width=110, anchor="center")
        self.responses_table.column("more_science", width=140, anchor="center")

        # Add a scrollbar for the table
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.responses_table.yview)
        self.responses_table.configure(yscrollcommand=scrollbar.set)

        self.responses_table.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        # Stats area
        stats_frame = ttk.Frame(self.tab_host)
        stats_frame.pack(fill="x", padx=10, pady=10)
        self.avg_age_var = tk.StringVar(value="N/A")
        self.total_var = tk.StringVar(value="0")
        self.enjoy_agree_var = tk.StringVar(value="0")
        self.curious_agree_var = tk.StringVar(value="0")
        self.science_agree_var = tk.StringVar(value="0")
        self.enjoy_agree_pct_var = tk.StringVar(value="N/A")
        self.curious_agree_pct_var = tk.StringVar(value="N/A")
        self.science_agree_pct_var = tk.StringVar(value="N/A")
        self.ethnicity_counts_var = tk.StringVar(value="N/A")
        self.sex_counts_var = tk.StringVar(value="N/A")
        self.disability_counts_var = tk.StringVar(value="N/A")

        # This builds the stats labels
        ttk.Label(stats_frame, text="Total responses:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        ttk.Label(stats_frame, textvariable=self.total_var).grid(row=0, column=1, sticky="w", padx=5, pady=2)

        ttk.Label(stats_frame, text="Average age:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        ttk.Label(stats_frame, textvariable=self.avg_age_var).grid(row=1, column=1, sticky="w", padx=5, pady=2)

        ttk.Label(stats_frame, text="Enjoyed Agree/Strongly Agree:").grid(row=0, column=2, sticky="w", padx=15, pady=2)
        ttk.Label(stats_frame, textvariable=self.enjoy_agree_var).grid(row=0, column=3, sticky="w", padx=5, pady=2)
        ttk.Label(stats_frame, text="(%):").grid(row=0, column=4, sticky="w", padx=5, pady=2)
        ttk.Label(stats_frame, textvariable=self.enjoy_agree_pct_var).grid(row=0, column=5, sticky="w", padx=5, pady=2)

        ttk.Label(stats_frame, text="Curious Agree/Strongly Agree:").grid(row=1, column=2, sticky="w", padx=15, pady=2)
        ttk.Label(stats_frame, textvariable=self.curious_agree_var).grid(row=1, column=3, sticky="w", padx=5, pady=2)
        ttk.Label(stats_frame, text="(%):").grid(row=1, column=4, sticky="w", padx=5, pady=2)
        ttk.Label(stats_frame, textvariable=self.curious_agree_pct_var).grid(row=1, column=5, sticky="w", padx=5, pady=2)

        ttk.Label(stats_frame, text="More Science Agree/Strongly Agree:").grid(row=2, column=2, sticky="w", padx=15, pady=2)
        ttk.Label(stats_frame, textvariable=self.science_agree_var).grid(row=2, column=3, sticky="w", padx=5, pady=2)
        ttk.Label(stats_frame, text="(%):").grid(row=2, column=4, sticky="w", padx=5, pady=2)
        ttk.Label(stats_frame, textvariable=self.science_agree_pct_var).grid(row=2, column=5, sticky="w", padx=5, pady=2)

        ttk.Label(stats_frame, text="Sex counts (M/F/O):").grid(row=4, column=0, sticky="w", padx=5, pady=2)
        ttk.Label(stats_frame, textvariable=self.sex_counts_var).grid(row=4, column=1, sticky="w", padx=5, pady=2, columnspan=5)

        ttk.Label(stats_frame, text="Ethnicity counts:").grid(row=5, column=0, sticky="w", padx=5, pady=2)
        ttk.Label(stats_frame, textvariable=self.ethnicity_counts_var).grid(row=5, column=1, sticky="w", padx=5, pady=2, columnspan=5)

        ttk.Label(stats_frame, text="Disability counts (Y/N):").grid(row=6, column=0, sticky="w", padx=5, pady=2)
        ttk.Label(stats_frame, textvariable=self.disability_counts_var).grid(row=6, column=1, sticky="w", padx=5, pady=2, columnspan=5)

        
        # bar chart for Enjoyed (1-5)
        # -----------------------------
        chart_frame = ttk.Frame(self.tab_host)
        chart_frame.pack(fill="x", padx=10, pady=10)

                
        #bar chart for Enjoyed (1-5)
        # -----------------------------

        # Dropdown to choose what the bar chart shows
        selector_frame = ttk.Frame(chart_frame)
        selector_frame.pack(fill="x")

        ttk.Label(selector_frame, text="Bar chart shows:").pack(side="left", padx=(0, 8))

        self.chart_choice_var = tk.StringVar(value="Enjoyed")
        self.chart_choice_dropdown = ttk.Combobox(
            selector_frame,
            textvariable=self.chart_choice_var,
            state="readonly",
            values=["Enjoyed", "Curious", "More Science"],
            width=15
        )
        self.chart_choice_dropdown.pack(side="left")
        self.chart_choice_dropdown.bind("<<ComboboxSelected>>", lambda e: self.update_stats())

        # Chart heading 
        self.chart_title_label = ttk.Label(chart_frame, text="Enjoyed (1-5) Distribution:", font=("Arial", 11, "bold"))
        self.chart_title_label.pack(pady=(8, 4))  

        self.enjoyed_canvas = tk.Canvas(chart_frame, width=760, height=140, bg="white", highlightthickness=1, highlightbackground="gray")
        self.enjoyed_canvas.pack(pady=5)


        # Buttons section 
        buttons_frame = ttk.Frame(self.tab_host)
        buttons_frame.pack(pady=10)

        refresh_btn = ttk.Button(buttons_frame, text="Refresh Stats", command=self.update_stats)
        refresh_btn.grid(row=0, column=0, padx=10)

        logout_btn = ttk.Button(buttons_frame, text="Logout", command=self.logout_host)
        logout_btn.grid(row=0, column=1, padx=10)

        export_btn = ttk.Button(buttons_frame, text="Export Summary", command=self.export_summary)
        export_btn.grid(row=0, column=2, padx=10)

        # Populate table and stats when host page is created
        self.update_stats()


    def clear_filters(self):
        # Clears all host filters and refreshes the host dashboard
        self.search_var.set("")
        self.filter_sex_var.set("All")
        self.filter_dis_var.set("All")
        self.update_stats()


    def export_summary(self):
        # Exports a simple text summary file for the hosts
        filename = "survey_summary.txt"

        lines = []
        lines.append("Aeolus Sculpture Survey - Host Summary")
        lines.append("------------------------------------")
        lines.append(f"Total responses: {self.total_var.get()}")
        lines.append(f"Average age: {self.avg_age_var.get()}")
        lines.append("")
        lines.append(f"Enjoyed Agree/Strongly Agree: {self.enjoy_agree_var.get()} ({self.enjoy_agree_pct_var.get()})")
        lines.append(f"Curious Agree/Strongly Agree: {self.curious_agree_var.get()} ({self.curious_agree_pct_var.get()})")
        lines.append(f"More Science Agree/Strongly Agree: {self.science_agree_var.get()} ({self.science_agree_pct_var.get()})")
        lines.append("")
        lines.append(f"Sex counts (M/F/O): {self.sex_counts_var.get()}")
        lines.append(f"Ethnicity counts: {self.ethnicity_counts_var.get()}")
        lines.append(f"Disability counts (Y/N): {self.disability_counts_var.get()}")

        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        messagebox.showinfo("Exported", f"Saved summary to {filename}")


    def logout_host(self):
        # Logs the host out by disabling the Host tab and returning to the Survey tab
        self.notebook.tab(self.tab_host, state="disabled")
        self.notebook.select(self.tab_survey)
        self.password_entry.delete(0, tk.END)
        messagebox.showinfo("Logged out", "Host has been logged out.")


    def update_stats(self):
        # Rebuilds the dashboard, it clears the table, applys the filters, calculates the stats, then redraws the chart
        for row in self.responses_table.get_children():
            self.responses_table.delete(row)

        # Apply filters 
        search_text = self.search_var.get().strip().lower()
        sex_filter = self.filter_sex_var.get()
        dis_filter = self.filter_dis_var.get()

        filtered = []
        for r in self.responses:
            if search_text and search_text not in r.name.lower():
                continue

            sex_display = self.sex_display(r.sex)
            disability_display = self.disability_display(r.disability)

            if sex_filter != "All" and sex_display != sex_filter:
                continue
            if dis_filter != "All" and disability_display != dis_filter:
                continue

            filtered.append(r)

        # Add all responses to the table
        for r in filtered:
            sex_display = self.sex_display(r.sex)
            disability_display = self.disability_display(r.disability)
            ethnicity_display = self.ethnicity_display(r.ethnicity)

            self.responses_table.insert(
                "", "end",
                values=(
                    r.name,
                    r.age,
                    sex_display,
                    ethnicity_display,
                    disability_display,
                    r.enjoyed,
                    r.curious,
                    r.more_science
                )
            )

        # If no data, show defaults
        if len(filtered) == 0:
            self.total_var.set("0")
            self.avg_age_var.set("N/A")

            self.enjoy_agree_var.set("0")
            self.curious_agree_var.set("0")
            self.science_agree_var.set("0")

            self.enjoy_agree_pct_var.set("N/A")
            self.curious_agree_pct_var.set("N/A")
            self.science_agree_pct_var.set("N/A")

            self.sex_counts_var.set("N/A")
            self.ethnicity_counts_var.set("N/A")
            self.disability_counts_var.set("N/A")

            # Clear chart
            self.enjoyed_canvas.delete("all")
            return
        
        # Total responses
        total = len(filtered)
        self.total_var.set(str(total))

        # Average age + Std dev
        ages = [r.age for r in filtered]
        avg_age = sum(ages) / len(ages)
        self.avg_age_var.set(f"{avg_age:.1f}")

        # Agree/Strongly Agree counts (4 or 5)
        enjoy_agree = sum(1 for r in filtered if r.enjoyed in (4, 5))
        curious_agree = sum(1 for r in filtered if r.curious in (4, 5))
        science_agree = sum(1 for r in filtered if r.more_science in (4, 5))

        self.enjoy_agree_var.set(str(enjoy_agree))
        self.curious_agree_var.set(str(curious_agree))
        self.science_agree_var.set(str(science_agree))

        self.enjoy_agree_pct_var.set(f"{(enjoy_agree/total)*100:.1f}%")
        self.curious_agree_pct_var.set(f"{(curious_agree/total)*100:.1f}%")
        self.science_agree_pct_var.set(f"{(science_agree/total)*100:.1f}%")

        # Counts by sex / ethnicity / disability (used for quick at-a-glance demographics)
        sex_counts = {
            "M": sum(1 for r in filtered if r.sex == 1),
            "F": sum(1 for r in filtered if r.sex == 2),
            "O": sum(1 for r in filtered if r.sex == 3),
        }
        self.sex_counts_var.set(f"M={sex_counts['M']}  F={sex_counts['F']}  O={sex_counts['O']}")

        ethnicity_names = {1: "White", 2: "Black", 3: "Chinese", 4: "Asian", 5: "Other"}
        eth_counts_list = []
        for k in [1, 2, 3, 4, 5]:
            eth_counts_list.append(f"{ethnicity_names[k]}={sum(1 for r in filtered if r.ethnicity == k)}")
        self.ethnicity_counts_var.set("  ".join(eth_counts_list))

        disability_counts = {
            "Y": sum(1 for r in filtered if r.disability == 1),
            "N": sum(1 for r in filtered if r.disability == 0),
        }
        self.disability_counts_var.set(f"Y={disability_counts['Y']}  N={disability_counts['N']}")

       
        # Draws the speicifc bar chart you selected
        # -----------------------------
        
        chart_choice = self.chart_choice_var.get()

        if chart_choice == "Enjoyed":
            self.chart_title_label.config(text="Enjoyed (1-5) Distribution:")
            value_getter = lambda resp: resp.enjoyed
        elif chart_choice == "Curious":
            self.chart_title_label.config(text="Curious (1-5) Distribution:")
            value_getter = lambda resp: resp.curious
        else:
            self.chart_title_label.config(text="More Science (1-5) Distribution:")
            value_getter = lambda resp: resp.more_science

        counts = {i: 0 for i in range(1, 6)}
        for r in filtered:
            val = value_getter(r)
            if val in counts:
                counts[val] += 1

        # Clear canvas before re-drawing (prevents bars stacking on top of each other)
        self.enjoyed_canvas.delete("all")

        # Chart layout values
        left_margin = 40
        top_margin = 20
        bar_width = 90
        gap = 30
        max_height = 80

        max_count = max(counts.values()) if max(counts.values()) > 0 else 1

        for i in range(1, 6):
            x0 = left_margin + (i - 1) * (bar_width + gap)
            x1 = x0 + bar_width
            bar_height = int((counts[i] / max_count) * max_height)
            y1 = top_margin + max_height
            y0 = y1 - bar_height

            # Draws the bar
            self.enjoyed_canvas.create_rectangle(x0, y0, x1, y1, fill="#6FA8DC", outline="black")

            # Label under bar
            self.enjoyed_canvas.create_text((x0 + x1) / 2, y1 + 15, text=str(i))

            # Count above bar
            self.enjoyed_canvas.create_text((x0 + x1) / 2, y0 - 10, text=str(counts[i]))


# Start the program and keeps it open
if __name__ == "__main__":
    app = SurveyApp()
    app.mainloop()
    