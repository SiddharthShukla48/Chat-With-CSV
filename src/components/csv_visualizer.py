import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

class CsvVisualizer:
    def __init__(self, data=None):
        self.data = data

    def load_csv(self, file_path):
        self.data = pd.read_csv(file_path)

    def get_data_summary(self):
        if self.data is not None:
            return {
                "shape": self.data.shape,
                "columns": list(self.data.columns),
                "dtypes": self.data.dtypes.to_dict(),
                "missing_values": self.data.isnull().sum().to_dict(),
                "sample": self.data.head(5).to_dict()
            }
        return None

    def render_csv(self):
        if self.data is not None:
            st.write("### CSV Data Preview")
            st.dataframe(self.data)
            
            st.write("### Data Summary")
            st.write(f"Rows: {self.data.shape[0]}, Columns: {self.data.shape[1]}")
            
            # Show column info
            st.write("### Column Information")
            for col in self.data.columns:
                st.write(f"**{col}**: {self.data[col].dtype}")
                
            # Visualization options
            st.write("### Visualizations")
            viz_type = st.selectbox(
                "Select visualization type", 
                ["Bar Chart", "Line Chart", "Histogram", "Scatter Plot"]
            )
            
            if viz_type == "Bar Chart":
                self.render_bar_chart()
            elif viz_type == "Line Chart":
                self.render_line_chart()
            elif viz_type == "Histogram":
                self.render_histogram()
            elif viz_type == "Scatter Plot":
                self.render_scatter_plot()
        else:
            st.write("No CSV data loaded.")

    def render_bar_chart(self):
        if self.data is not None:
            numeric_cols = self.data.select_dtypes(include=['int64', 'float64']).columns.tolist()
            categorical_cols = self.data.select_dtypes(include=['object']).columns.tolist()
            
            if numeric_cols and categorical_cols:
                x_axis = st.selectbox("Select X-axis (categorical)", categorical_cols)
                y_axis = st.selectbox("Select Y-axis (numeric)", numeric_cols)
                
                # Create and display bar chart
                fig, ax = plt.subplots(figsize=(10, 6))
                self.data.groupby(x_axis)[y_axis].mean().plot(kind='bar', ax=ax)
                plt.title(f"Average {y_axis} by {x_axis}")
                plt.xlabel(x_axis)
                plt.ylabel(f"Average {y_axis}")
                plt.xticks(rotation=45)
                st.pyplot(fig)

    def render_line_chart(self):
        if self.data is not None:
            numeric_cols = self.data.select_dtypes(include=['int64', 'float64']).columns.tolist()
            
            if len(numeric_cols) >= 2:
                x_axis = st.selectbox("Select X-axis", numeric_cols)
                y_axis = st.selectbox("Select Y-axis", [col for col in numeric_cols if col != x_axis])
                
                # Create and display line chart
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.plot(self.data[x_axis], self.data[y_axis])
                plt.title(f"{y_axis} vs {x_axis}")
                plt.xlabel(x_axis)
                plt.ylabel(y_axis)
                st.pyplot(fig)

    def render_histogram(self):
        if self.data is not None:
            numeric_cols = self.data.select_dtypes(include=['int64', 'float64']).columns.tolist()
            
            if numeric_cols:
                column = st.selectbox("Select column for histogram", numeric_cols)
                bins = st.slider("Number of bins", 5, 100, 20)
                
                # Create and display histogram
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.hist(self.data[column], bins=bins)
                plt.title(f"Histogram of {column}")
                plt.xlabel(column)
                plt.ylabel("Frequency")
                st.pyplot(fig)

    def render_scatter_plot(self):
        if self.data is not None:
            numeric_cols = self.data.select_dtypes(include=['int64', 'float64']).columns.tolist()
            
            if len(numeric_cols) >= 2:
                x_axis = st.selectbox("Select X-axis", numeric_cols)
                y_axis = st.selectbox("Select Y-axis", [col for col in numeric_cols if col != x_axis])
                
                # Create and display scatter plot
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.scatter(self.data[x_axis], self.data[y_axis])
                plt.title(f"{y_axis} vs {x_axis}")
                plt.xlabel(x_axis)
                plt.ylabel(y_axis)
                st.pyplot(fig)