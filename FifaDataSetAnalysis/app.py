import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from prettytable import PrettyTable

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Analyzer")

        self.data = pd.DataFrame()  # Stores the loaded data

        # Button to upload a CSV file
        self.upload_button = tk.Button(self.root, text="Upload CSV", command=self.upload_csv)
        self.upload_button.pack()

        # Label and combobox for selecting a column to query
        tk.Label(self.root, text="Select a column to query:").pack()
        self.column_selector = ttk.Combobox(self.root)
        self.column_selector.pack()

        # Label and combobox for selecting a column for filtering
        tk.Label(self.root, text="Select a column for filter (Optional):").pack()
        self.filter_column_selector = ttk.Combobox(self.root)
        self.filter_column_selector.bind("<<ComboboxSelected>>", self.update_filter_values)
        self.filter_column_selector.pack()

        # Label and combobox for selecting a filter value
        tk.Label(self.root, text="Select a value for filter (Optional):").pack()
        self.filter_value_selector = ttk.Combobox(self.root)
        self.filter_value_selector.pack()

        # Label and combobox for selecting the first display column
        tk.Label(self.root, text="Select a column to display:").pack()
        self.column1Selector = ttk.Combobox(self.root)
        self.column1Selector.pack()

        # Label and combobox for selecting the second display column
        tk.Label(self.root, text="Select another column to display:").pack()
        self.column2Selector = ttk.Combobox(self.root)
        self.column2Selector.pack()

        # Label and combobox for selecting the top/bottom option
        tk.Label(self.root, text="Choose between top and bottom:").pack()
        self.top_bottom_selector = ttk.Combobox(self.root, values=['Top', 'Bottom', 'All', 'Random', 'Mid'])
        self.top_bottom_selector.pack()

        # Label and entry for specifying the number of records
        tk.Label(self.root, text="Enter the number of records:").pack()
        self.number_entry = tk.Entry(self.root)
        self.number_entry.pack()

        # Button to query the data based on the selected options
        self.query_button = tk.Button(self.root, text="Query Data", command=self.query_data)
        self.query_button.pack()

        # Text box to display the query results
        self.results_box = tk.Text(self.root)
        self.results_box.pack()

        # Checkboxes to enable/disable plotting
        self.plot_var_bar = tk.IntVar()
        self.plot_check_bar = tk.Checkbutton(self.root, text="Bar Graph", variable=self.plot_var_bar)
        self.plot_check_bar.pack(side="left")

        self.plot_var_hist = tk.IntVar()
        self.plot_check_hist = tk.Checkbutton(self.root, text="Histogram", variable=self.plot_var_hist)
        self.plot_check_hist.pack(side="left")

        self.plot_var_reg = tk.IntVar()
        self.plot_check_reg = tk.Checkbutton(self.root, text="Regression", variable=self.plot_var_reg)
        self.plot_check_reg.pack(side="left")

        # Add color selection
        tk.Label(self.root, text="Choose a color for the graph:").pack()
        self.color_selector = ttk.Combobox(self.root, values=['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black'])
        self.color_selector.pack()

        # Button to plot the data
        self.plot_button = tk.Button(self.root, text="Plot Data", command=self.plot_data)
        self.plot_button.pack()

        # Button to reset all selections and clear the results
        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset)
        self.reset_button.pack()

    def upload_csv(self):
        # Open a file dialog to select a CSV file
        filename = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if filename:
            # Read the selected CSV file into a pandas DataFrame
            self.data = pd.read_csv(filename)
            # Update the available column choices in the comboboxes
            columns_sorted = sorted(list(self.data.columns))
            self.column_selector['values'] = columns_sorted
            self.filter_column_selector['values'] = columns_sorted
            self.column1Selector['values'] = columns_sorted
            self.column2Selector['values'] = columns_sorted

    def update_filter_values(self, event):
        # Update the filter values based on the selected filter column
        column = self.filter_column_selector.get()
        if column:
            unique_values = sorted(pd.Series(self.data[column].unique()).dropna().astype(str).tolist())
            self.filter_value_selector['values'] = unique_values

    def query_data(self):
        # Retrieve the selected options for querying the data
        column = self.column_selector.get()
        filter_column = self.filter_column_selector.get()
        filter_value = self.filter_value_selector.get()
        displayColumn1 = self.column1Selector.get()
        displayColumn2 = self.column2Selector.get()
        top_bottom = self.top_bottom_selector.get()
        
        try:
            number = int(self.number_entry.get())
        except ValueError:
            if top_bottom not in ['All']:
                messagebox.showerror("Error", "Number of records must be an integer.")
                return

        if column and displayColumn1 and displayColumn2 and top_bottom:
            if filter_column and filter_value:
                filter_value_type_corrected = self.convert_to_correct_type(filter_column, filter_value)
                filtered_data = self.data[self.data[filter_column] == filter_value_type_corrected]
            else:
                filtered_data = self.data

            # Depending on the choice, select the data differently
            try:
                if top_bottom == 'Top':
                    result = filtered_data.nlargest(number, column)
                elif top_bottom == 'Bottom':
                    result = filtered_data.nsmallest(number, column)
                elif top_bottom == 'All':
                    result = filtered_data
                elif top_bottom == 'Random':
                    result = filtered_data.sample(number)
                elif top_bottom == 'Mid':
                    mid_index = len(filtered_data) // 2
                    lower = max(0, mid_index - number//2)
                    upper = min(len(filtered_data), mid_index + number//2 + number%2)
                    result = filtered_data.iloc[lower:upper]

                result = result[[displayColumn1, displayColumn2]]
            except:
                messagebox.showerror("Error", "Value/Key Error.")
                return

            # Create a PrettyTable object
            table = PrettyTable()

            # Add field names
            table.field_names = [displayColumn1, displayColumn2]

            # Add rows
            for index, row in result.iterrows():
                table.add_row([str(val) for val in row])

            # Display the table in the results box
            self.results_box.insert('end', str(table))
        #else:
        #    messagebox.showerror("Error", "All fields must be filled.")

    def convert_to_correct_type(self, column, value):
        if column:  # Check that a column was selected
            dtype = self.data[column].dtype

            # Convert the value to the correct type based on the column type
            if pd.api.types.is_integer_dtype(dtype):
                return int(value)
            elif pd.api.types.is_float_dtype(dtype):
                return float(value)
            elif pd.api.types.is_datetime64_any_dtype(dtype):
                return pd.to_datetime(value)
            else:
                return value  # Return the value as it is if the column type is object (string)
        else:
            return value  # If no column was selected, return the value as is

    def plot_data(self):
        column = self.column_selector.get()
        filter_column = self.filter_column_selector.get()
        filter_value = self.filter_value_selector.get()
        displayColumn1 = self.column1Selector.get()
        displayColumn2 = self.column2Selector.get()
        top_bottom = self.top_bottom_selector.get()
        color = self.color_selector.get()

        # Check if the number entered can be converted to int, otherwise show an error
        try:
            number = int(self.number_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Number of records must be an integer.")
            return

        # Check that all necessary selections have been made before trying to plot the data
        if not all((column, displayColumn1, displayColumn2, top_bottom, number)):
            messagebox.showerror("Error", "All necessary fields must be filled.")
            return

        # If a filter column has been selected, convert the filter value to the correct type
        if filter_column:
            filter_value_type_corrected = self.convert_to_correct_type(filter_column, filter_value)

            # Filter the data based on the selected filter column and value
            filtered_data = self.data[self.data[filter_column] == filter_value_type_corrected]
        else:
            filtered_data = self.data
        try:
            # Sort and select the data based on the selected option
            if top_bottom == 'Top':
                result = filtered_data.nlargest(number, column)
            elif top_bottom == 'Bottom':
                result = filtered_data.nsmallest(number, column)
            elif top_bottom == 'All':
                result = filtered_data
            elif top_bottom == 'Random':
                result = filtered_data.sample(n=number)
            elif top_bottom == 'Mid':
                mid_point = len(filtered_data) // 2
                result = filtered_data.sort_values(column).iloc[mid_point - number//2 : mid_point + number//2 + 1]
            else:
                messagebox.showerror("Error", "Invalid option.")
                return
            
            # Plot each type of graph selected
            if self.plot_var_bar.get():
                # Create a bar plot using seaborn
                plt.figure(figsize=(10,5))
                plot = sns.barplot(x=result[displayColumn1], y=result[displayColumn2], color=color)
                plot.set_xticklabels(plot.get_xticklabels(), rotation=45)
                if filter_column != '':
                    plt.title(f"{top_bottom} {number} {column} By {filter_value} {filter_column}")
                else:
                    plt.title(f"{top_bottom} {number} {column}")
                plt.show()

            if self.plot_var_hist.get():
                # Create a histogram using seaborn
                plt.figure(figsize=(10,5))
                sns.histplot(result[displayColumn1], kde=True, color=color)
                if filter_column == '':
                    plt.title(f"Histogram of {displayColumn1} of {top_bottom} {number} {column}")
                    plt.show()
                else:
                    plt.title(f"Histogram of {displayColumn1} of {top_bottom} {number} {column} By {filter_value} {filter_column}")
                    plt.show()

            if self.plot_var_reg.get():
                # Create a regression plot using seaborn
                plt.figure(figsize=(10,5))
                sns.regplot(x=displayColumn1, y=displayColumn2, data=result, color=color)
                if filter_column == '':
                    plt.title(f"Regression Plot of {displayColumn1} vs {displayColumn2} of {top_bottom} {number} {column}")
                    plt.show()
                else:
                    plt.title(f"Regression Plot of {displayColumn1} vs {displayColumn2} of {top_bottom} {number} {column} By {filter_value} {filter_column}")
                    plt.show()
        except:
            messagebox.showerror("Error", "Key/Value Error:\n\nEnsure that your columns and values actually exist, and that your datatypes are proper for the chart you are using.")

    def reset(self):
        # Reset all selections and clear the results
        self.column_selector.set('')
        self.filter_column_selector.set('')
        self.filter_value_selector.set('')
        self.column1Selector.set('')
        self.column2Selector.set('')
        self.top_bottom_selector.set('')
        self.number_entry.delete(0, 'end')
        self.results_box.delete('1.0', 'end')
        self.plot_var_bar.set(0)
        self.plot_var_hist.set(0)
        self.plot_var_reg.set(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
