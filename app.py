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
        self.column_selector = ttk.Combobox(self.root, state="readonly")
        self.column_selector.pack()

        # Label and combobox for selecting a column for filtering
        tk.Label(self.root, text="Select a column for filter (Optional):").pack()
        self.filter_column_selector = ttk.Combobox(self.root, state="readonly")
        self.filter_column_selector.bind("<<ComboboxSelected>>", self.update_filter_values)
        self.filter_column_selector.pack()

        # Label and combobox for selecting a filter value
        tk.Label(self.root, text="Select a value for filter (Optional):").pack()
        self.filter_value_selector = ttk.Combobox(self.root, state="readonly")
        self.filter_value_selector.pack()

        # Label and combobox for selecting the first display column
        tk.Label(self.root, text="Select a column to display:").pack()
        self.column1Selector = ttk.Combobox(self.root, state="readonly")
        self.column1Selector.pack()

        # Label and combobox for selecting the second display column
        tk.Label(self.root, text="Select another column to display:").pack()
        self.column2Selector = ttk.Combobox(self.root, state="readonly")
        self.column2Selector.pack()

        # Label and combobox for selecting the top/bottom option
        tk.Label(self.root, text="Choose between top and bottom:").pack()
        self.top_bottom_selector = ttk.Combobox(self.root, state="readonly", values=['Top', 'Bottom'])
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

        # Checkbox to enable/disable plotting
        self.plot_var = tk.IntVar()
        self.plot_check = tk.Checkbutton(self.root, text="Plot Data", variable=self.plot_var)
        self.plot_check.pack()

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
            self.column_selector['values'] = list(self.data.columns)
            self.filter_column_selector['values'] = list(self.data.columns)
            self.column1Selector['values'] = list(self.data.columns)
            self.column2Selector['values'] = list(self.data.columns)

    def update_filter_values(self, event):
        # Update the filter values based on the selected filter column
        column = self.filter_column_selector.get()
        if column:
            unique_values = pd.Series(self.data[column].unique())
            self.filter_value_selector['values'] = list(unique_values.dropna())

    def query_data(self):
        # Retrieve the selected options for querying the data
        column = self.column_selector.get()
        print(column.isnumeric())
        filter_column = self.filter_column_selector.get()
        filter_value = self.filter_value_selector.get()
        displayColumn1 = self.column1Selector.get()
        displayColumn2 = self.column2Selector.get()
        top_bottom = self.top_bottom_selector.get()
        number = int(self.number_entry.get())

        if column and displayColumn1 and displayColumn2 and top_bottom and number:
            if filter_column and filter_value:
                # Filter the data based on the selected filter column and value
                filtered_data = self.data[self.data[filter_column] == filter_value]
            else:
                filtered_data = self.data
            if top_bottom == 'Top' and column.isnumeric() == True:
                # Get the top N records based on the selected column
                result = filtered_data.nlargest(number, column)
            elif top_bottom =='Bottom' and column.isnumeric() == True:
                # Get the bottom N records based on the selected column
                result = filtered_data.nsmallest(number, column)
            elif top_bottom == 'Top' and column.isnumeric() == False:
                # Get the top N records based on the selected column
                result = filtered_data.sort_values(column).tail(number)
            elif top_bottom =='Bottom' and column.isnumeric() == False:
                # Get the bottom N records based on the selected column
                result = filtered_data.sort_values(column).head(number)
            result = result[[displayColumn1, displayColumn2]]
            

            # Create a PrettyTable object
            table = PrettyTable()

            # Add field names
            table.field_names = [displayColumn1, displayColumn2]

            # Add rows
            for index, row in result.iterrows():
                table.add_row(row)

            # Display the table in the results box
            self.results_box.insert('end', str(table))
        else:
            messagebox.showerror("Error", "All fields must be filled.")

    def plot_data(self):
        if self.plot_var.get() == 1:
            sns.set_style("darkgrid")
            column = self.column_selector.get()
            filter_column = self.filter_column_selector.get()
            filter_value = self.filter_value_selector.get()
            displayColumn1 = self.column1Selector.get()
            displayColumn2 = self.column2Selector.get()
            top_bottom = self.top_bottom_selector.get()
            number = int(self.number_entry.get())

            if column and displayColumn1 and displayColumn2 and top_bottom and number:
                if filter_column and filter_value:
                    filtered_data = self.data[self.data[filter_column] == filter_value]
                else:
                    filtered_data = self.data
                if top_bottom == 'Top':
                    result = filtered_data.nlargest(number, column)
                else:
                    result = filtered_data.nsmallest(number, column)

                # Create a bar plot using seaborn
                plt.figure(figsize=(10,5))
                plot = sns.barplot(x=result[displayColumn1], y=result[displayColumn2], palette='Greens_d')
                plot.set_xticklabels(plot.get_xticklabels(), rotation=45)
                if filter_column != '':
                    plt.title(f"By {filter_value} {filter_column}")
                plt.show()
            else:
                messagebox.showerror("Error", "All fields must be filled.")

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
        self.plot_var.set(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
