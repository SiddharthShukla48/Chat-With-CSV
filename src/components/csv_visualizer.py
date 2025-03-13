import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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
            st.dataframe(self.data, use_container_width=True)
            
            st.write("### Data Summary")
            st.write(f"Rows: {self.data.shape[0]}, Columns: {self.data.shape[1]}")
            
            # Column info in an expander
            with st.expander("Column Information", expanded=False):
                for col in self.data.columns:
                    st.write(f"**{col}**: {self.data[col].dtype}")
                    
            # Visualization options with tabs
            st.markdown('<h3 class="subheader">Visualizations</h3>', unsafe_allow_html=True)
            
            # Create tabs for different visualization types
            viz_tabs = st.tabs(["📊 Bar Chart", "📈 Line Chart", "📉 Histogram", "🔍 Scatter Plot", "🔥 Heatmap", "💡 Insights"])
            
            with viz_tabs[0]:
                self.render_bar_chart()
            with viz_tabs[1]:
                self.render_line_chart()
            with viz_tabs[2]:
                self.render_histogram()
            with viz_tabs[3]:
                self.render_scatter_plot()
            with viz_tabs[4]:
                self.render_heatmap()
            with viz_tabs[5]:
                self.render_data_insights()
        else:
            st.info("Upload a CSV file to visualize it here.")

    def render_bar_chart(self):
        if self.data is not None:
            numeric_cols = self.data.select_dtypes(include=['int64', 'float64']).columns.tolist()
            categorical_cols = self.data.select_dtypes(include=['object']).columns.tolist()
            
            if numeric_cols and categorical_cols:
                x_axis = st.selectbox("Select X-axis (categorical)", categorical_cols, key="bar_x_axis")
                y_axis = st.selectbox("Select Y-axis (numeric)", numeric_cols, key="bar_y_axis")
                
                try:
                    # Create and display bar chart
                    fig, ax = plt.subplots(figsize=(10, 6))
                    self.data.groupby(x_axis)[y_axis].mean().plot(kind='bar', ax=ax)
                    plt.title(f"Average {y_axis} by {x_axis}")
                    plt.xlabel(x_axis)
                    plt.ylabel(f"Average {y_axis}")
                    plt.xticks(rotation=45)
                    st.pyplot(fig)
                except Exception as e:
                    st.error(f"Error creating bar chart: {str(e)}")

    def render_line_chart(self):
        if self.data is not None:
            numeric_cols = self.data.select_dtypes(include=['int64', 'float64']).columns.tolist()
            
            if len(numeric_cols) >= 2:
                x_axis = st.selectbox("Select X-axis", numeric_cols, key="line_x_axis")
                y_axis = st.selectbox("Select Y-axis", [col for col in numeric_cols if col != x_axis], key="line_y_axis")
                
                try:
                    # Sort data by x_axis for better line chart
                    sorted_data = self.data.sort_values(by=x_axis)
                    
                    # Create and display line chart
                    fig, ax = plt.subplots(figsize=(10, 6))
                    ax.plot(sorted_data[x_axis], sorted_data[y_axis])
                    plt.title(f"{y_axis} vs {x_axis}")
                    plt.xlabel(x_axis)
                    plt.ylabel(y_axis)
                    plt.grid(True, linestyle='--', alpha=0.7)
                    st.pyplot(fig)
                except Exception as e:
                    st.error(f"Error creating line chart: {str(e)}")
            else:
                st.warning("Need at least 2 numeric columns for a line chart.")

    def render_histogram(self):
        if self.data is not None:
            numeric_cols = self.data.select_dtypes(include=['int64', 'float64']).columns.tolist()
            
            if numeric_cols:
                column = st.selectbox("Select column for histogram", numeric_cols, key="hist_column")
                bins = st.slider("Number of bins", 5, 100, 20, key="hist_bins")
                
                try:
                    # Create and display histogram
                    fig, ax = plt.subplots(figsize=(10, 6))
                    ax.hist(self.data[column].dropna(), bins=bins)
                    plt.title(f"Histogram of {column}")
                    plt.xlabel(column)
                    plt.ylabel("Frequency")
                    st.pyplot(fig)
                except Exception as e:
                    st.error(f"Error creating histogram: {str(e)}")
            else:
                st.warning("Need numeric columns for a histogram.")

    def render_scatter_plot(self):
        if self.data is not None:
            numeric_cols = self.data.select_dtypes(include=['int64', 'float64']).columns.tolist()
            
            if len(numeric_cols) >= 2:
                x_axis = st.selectbox("Select X-axis", numeric_cols, key="scatter_x_axis")
                y_axis = st.selectbox("Select Y-axis", [col for col in numeric_cols if col != x_axis], key="scatter_y_axis")
                
                try:
                    # Create and display scatter plot
                    fig, ax = plt.subplots(figsize=(10, 6))
                    ax.scatter(self.data[x_axis], self.data[y_axis], alpha=0.6)
                    plt.title(f"{y_axis} vs {x_axis}")
                    plt.xlabel(x_axis)
                    plt.ylabel(y_axis)
                    plt.grid(True, linestyle='--', alpha=0.3)
                    st.pyplot(fig)
                except Exception as e:
                    st.error(f"Error creating scatter plot: {str(e)}")
            else:
                st.warning("Need at least 2 numeric columns for a scatter plot.")
    
    def render_heatmap(self):
        if self.data is not None:
            numeric_cols = self.data.select_dtypes(include=['int64', 'float64']).columns.tolist()
            
            if len(numeric_cols) >= 2:
                selected_cols = st.multiselect(
                    "Select columns for correlation heatmap", 
                    numeric_cols, 
                    default=numeric_cols[:min(5, len(numeric_cols))],
                    key="heatmap_columns"
                )
                
                if selected_cols and len(selected_cols) >= 2:
                    try:
                        fig, ax = plt.subplots(figsize=(10, 8))
                        correlation = self.data[selected_cols].corr()
                        sns.heatmap(correlation, annot=True, cmap='coolwarm', ax=ax, fmt=".2f")
                        plt.title("Correlation Heatmap")
                        st.pyplot(fig)
                    except Exception as e:
                        st.error(f"Error creating heatmap: {str(e)}")
                else:
                    st.warning("Please select at least 2 numeric columns for the heatmap.")
            else:
                st.warning("Not enough numeric columns for a correlation heatmap.")
    
    def render_data_insights(self):
        if self.data is not None:
            st.write("## Automated Data Insights")
            
            insights = []
            
            try:
                # Check for missing values
                missing = self.data.isnull().sum()
                missing_cols = missing[missing > 0]
                if not missing_cols.empty:
                    insights.append(f"Found missing values in {len(missing_cols)} columns: {', '.join(missing_cols.index)}")
                
                # Find columns with high correlation
                numeric_cols = self.data.select_dtypes(include=['int64', 'float64']).columns
                if len(numeric_cols) >= 2:
                    corr = self.data[numeric_cols].corr().abs()
                    upper = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
                    high_corr = [(numeric_cols[i], numeric_cols[j], c) for i, j, c in 
                                zip(*np.where(upper > 0.8), upper[upper > 0.8])]
                    
                    for i, j, c in high_corr[:3]:  # Show top 3 correlations
                        insights.append(f"Strong correlation ({c:.2f}) between {i} and {j}")
                
                # Detect outliers in numeric columns
                for col in numeric_cols[:3]:  # Check first 3 numeric columns
                    if self.data[col].count() > 0:  # Check if column has non-NA values
                        q1 = self.data[col].quantile(0.25)
                        q3 = self.data[col].quantile(0.75)
                        iqr = q3 - q1
                        outliers = self.data[(self.data[col] < q1 - 1.5 * iqr) | (self.data[col] > q3 + 1.5 * iqr)]
                        if len(outliers) > 0:
                            insights.append(f"Found {len(outliers)} potential outliers in column {col}")
            except Exception as e:
                insights.append(f"Error generating insights: {str(e)}")
            
            if insights:
                for i, insight in enumerate(insights, 1):
                    st.info(f"{i}. {insight}")
            else:
                st.write("No significant insights found in this dataset.")