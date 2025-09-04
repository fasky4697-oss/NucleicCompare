import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
from utils.statistics import StatisticsCalculator
from data.amplification_data import get_default_data

# Page configuration
st.set_page_config(
    page_title="Nucleic Acid Amplification Techniques Comparison",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize statistics calculator
stats_calc = StatisticsCalculator()

def main():
    st.title("🧬 Nucleic Acid Amplification Techniques Statistical Comparison")
    st.markdown("---")
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Select Analysis Type",
        ["Overview & Comparison", "Custom Data Analysis", "Statistical Testing", "About"]
    )
    
    if page == "Overview & Comparison":
        show_overview_page()
    elif page == "Custom Data Analysis":
        show_custom_analysis_page()
    elif page == "Statistical Testing":
        show_statistical_testing_page()
    else:
        show_about_page()

def show_overview_page():
    st.header("📊 Amplification Techniques Overview")
    
    # Load default data
    default_data = get_default_data()
    df = pd.DataFrame(default_data)
    
    # Display data table
    st.subheader("Performance Metrics Summary")
    st.dataframe(df, use_container_width=True)
    
    # Technique selection for comparison
    st.subheader("🔍 Technique Comparison")
    selected_techniques = st.multiselect(
        "Select techniques to compare:",
        df['Technique'].tolist(),
        default=df['Technique'].tolist()[:3]
    )
    
    if len(selected_techniques) >= 2:
        # Filter data for selected techniques
        filtered_df = df[df['Technique'].isin(selected_techniques)]
        
        # Create comparison charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Sensitivity vs Specificity scatter plot
            fig_scatter = px.scatter(
                filtered_df,
                x='Specificity (%)',
                y='Sensitivity (%)',
                color='Technique',
                size='Accuracy (%)',
                hover_data=['PPV (%)', 'NPV (%)'],
                title="Sensitivity vs Specificity"
            )
            fig_scatter.update_layout(height=400)
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        with col2:
            # Bar chart comparing all metrics
            metrics = ['Sensitivity (%)', 'Specificity (%)', 'PPV (%)', 'NPV (%)', 'Accuracy (%)']
            fig_bar = go.Figure()
            
            for technique in selected_techniques:
                technique_data = filtered_df[filtered_df['Technique'] == technique].iloc[0]
                fig_bar.add_trace(go.Bar(
                    name=technique,
                    x=metrics,
                    y=[technique_data[metric] for metric in metrics]
                ))
            
            fig_bar.update_layout(
                title="Performance Metrics Comparison",
                xaxis_title="Metrics",
                yaxis_title="Percentage (%)",
                barmode='group',
                height=400
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Detailed comparison table
        st.subheader("📋 Detailed Comparison")
        comparison_df = filtered_df[['Technique', 'Sensitivity (%)', 'Specificity (%)', 
                                   'PPV (%)', 'NPV (%)', 'Accuracy (%)']]
        st.dataframe(comparison_df, use_container_width=True)
        
        # Export functionality
        csv_buffer = io.StringIO()
        comparison_df.to_csv(csv_buffer, index=False)
        st.download_button(
            label="📥 Download Comparison Data (CSV)",
            data=csv_buffer.getvalue(),
            file_name="amplification_comparison.csv",
            mime="text/csv"
        )

def show_custom_analysis_page():
    st.header("🔬 Custom Data Analysis")
    st.markdown("Input your experimental data for statistical analysis")
    
    # Input method selection
    input_method = st.radio(
        "Choose input method:",
        ["Manual Entry", "Upload CSV File"]
    )
    
    if input_method == "Manual Entry":
        show_manual_entry()
    else:
        show_file_upload()

def show_manual_entry():
    st.subheader("📝 Manual Data Entry")
    
    # Create form for data input
    with st.form("manual_data_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            technique_name = st.text_input("Technique Name", value="Custom Technique")
            true_positives = st.number_input("True Positives (TP)", min_value=0, value=85)
            false_negatives = st.number_input("False Negatives (FN)", min_value=0, value=15)
        
        with col2:
            st.write("")  # Spacing
            true_negatives = st.number_input("True Negatives (TN)", min_value=0, value=90)
            false_positives = st.number_input("False Positives (FP)", min_value=0, value=10)
        
        submitted = st.form_submit_button("Calculate Statistics")
        
        if submitted:
            # Calculate statistics
            results = stats_calc.calculate_diagnostic_stats(
                true_positives, false_negatives, true_negatives, false_positives
            )
            
            # Display results
            display_custom_results(technique_name, results, 
                                 true_positives, false_negatives, true_negatives, false_positives)

def show_file_upload():
    st.subheader("📁 Upload CSV File")
    st.markdown("Upload a CSV file with columns: TP, FN, TN, FP, Technique (optional)")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.write("Uploaded data preview:")
            st.dataframe(df.head())
            
            # Validate required columns
            required_cols = ['TP', 'FN', 'TN', 'FP']
            if all(col in df.columns for col in required_cols):
                # Process each row
                results_list = []
                for idx, row in df.iterrows():
                    technique_name = row.get('Technique', f'Technique_{int(idx)+1}')
                    results = stats_calc.calculate_diagnostic_stats(
                        int(row['TP']), int(row['FN']), int(row['TN']), int(row['FP'])
                    )
                    results['Technique'] = technique_name
                    results_list.append(results)
                
                # Display results
                results_df = pd.DataFrame(results_list)
                st.subheader("📊 Calculated Results")
                st.dataframe(results_df, use_container_width=True)
                
                # Export results
                csv_buffer = io.StringIO()
                results_df.to_csv(csv_buffer, index=False)
                st.download_button(
                    label="📥 Download Results (CSV)",
                    data=csv_buffer.getvalue(),
                    file_name="custom_analysis_results.csv",
                    mime="text/csv"
                )
            else:
                st.error(f"Missing required columns. Expected: {required_cols}")
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

def display_custom_results(technique_name, results, tp, fn, tn, fp):
    st.subheader(f"📊 Results for {technique_name}")
    
    # Display confusion matrix
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.write("**Confusion Matrix**")
        confusion_data = [
            ["", "Predicted Positive", "Predicted Negative"],
            ["Actual Positive", tp, fn],
            ["Actual Negative", fp, tn]
        ]
        st.table(confusion_data)
    
    with col2:
        # Display calculated metrics
        st.write("**Diagnostic Performance**")
        metrics_df = pd.DataFrame([
            ["Sensitivity", f"{results['sensitivity']:.2f}%", f"({results['sensitivity_ci'][0]:.2f}% - {results['sensitivity_ci'][1]:.2f}%)"],
            ["Specificity", f"{results['specificity']:.2f}%", f"({results['specificity_ci'][0]:.2f}% - {results['specificity_ci'][1]:.2f}%)"],
            ["PPV", f"{results['ppv']:.2f}%", f"({results['ppv_ci'][0]:.2f}% - {results['ppv_ci'][1]:.2f}%)"],
            ["NPV", f"{results['npv']:.2f}%", f"({results['npv_ci'][0]:.2f}% - {results['npv_ci'][1]:.2f}%)"],
            ["Accuracy", f"{results['accuracy']:.2f}%", f"({results['accuracy_ci'][0]:.2f}% - {results['accuracy_ci'][1]:.2f}%)"]
        ], columns=["Metric", "Value", "95% CI"])
        st.dataframe(metrics_df, use_container_width=True)

def show_statistical_testing_page():
    st.header("📈 Statistical Testing")
    st.markdown("Perform Cohen's Kappa analysis and statistical comparisons")
    
    # Load default data for comparison
    default_data = get_default_data()
    df = pd.DataFrame(default_data)
    
    # Technique selection for Kappa analysis
    st.subheader("🎯 Cohen's Kappa Analysis")
    st.markdown("Compare agreement between two techniques")
    
    col1, col2 = st.columns(2)
    with col1:
        technique1 = st.selectbox("Select first technique:", df['Technique'].tolist())
    with col2:
        technique2 = st.selectbox("Select second technique:", df['Technique'].tolist())
    
    if technique1 != technique2:
        # Get data for both techniques
        tech1_data = df[df['Technique'] == technique1].iloc[0]
        tech2_data = df[df['Technique'] == technique2].iloc[0]
        
        # Calculate Kappa (simplified demonstration)
        kappa_result = stats_calc.calculate_cohens_kappa(tech1_data, tech2_data)
        
        st.subheader("📊 Cohen's Kappa Results")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Kappa Value", f"{kappa_result['kappa']:.4f}")
        with col2:
            st.metric("95% CI Lower", f"{kappa_result['ci_lower']:.4f}")
        with col3:
            st.metric("95% CI Upper", f"{kappa_result['ci_upper']:.4f}")
        
        # Interpretation
        interpretation = stats_calc.interpret_kappa(kappa_result['kappa'])
        st.info(f"**Interpretation:** {interpretation}")
        
        # Additional statistical tests
        st.subheader("📋 Additional Comparisons")
        
        # McNemar's test simulation
        mcnemar_result = stats_calc.mcnemar_test_simulation(tech1_data, tech2_data)
        st.write(f"**McNemar's Test p-value:** {mcnemar_result['p_value']:.4f}")
        if mcnemar_result['p_value'] < 0.05:
            st.warning("Significant difference detected between techniques (p < 0.05)")
        else:
            st.success("No significant difference detected between techniques (p ≥ 0.05)")

def show_about_page():
    st.header("ℹ️ About This Application")
    
    st.markdown("""
    ## 🧬 Nucleic Acid Amplification Techniques Comparison Tool
    
    This application provides comprehensive statistical analysis for comparing various nucleic acid amplification techniques including:
    
    - **PCR** (Polymerase Chain Reaction)
    - **qPCR** (Quantitative PCR)
    - **RPA** (Recombinase Polymerase Amplification)
    - **LAMP** (Loop-mediated Isothermal Amplification)
    - **NASBA** (Nucleic Acid Sequence-Based Amplification)
    - **SDA** (Strand Displacement Amplification)
    - **TMA** (Transcription-Mediated Amplification)
    - **HDA** (Helicase-Dependent Amplification)
    
    ### 📊 Statistical Capabilities
    
    - **Diagnostic Performance Metrics**: Sensitivity, Specificity, PPV, NPV, Accuracy
    - **Confidence Intervals**: 95% CI calculations for all metrics
    - **Cohen's Kappa**: Inter-rater reliability analysis
    - **Statistical Testing**: McNemar's test for paired comparisons
    - **Data Visualization**: Interactive charts and comparisons
    
    ### 🔬 Use Cases
    
    - Laboratory method validation
    - Technique selection for specific applications
    - Research publication support
    - Quality control analysis
    - Performance benchmarking
    
    ### 📚 References
    
    - MedCalc statistical methods
    - GraphPad statistical analysis
    - Cohen's Kappa interpretation guidelines
    - Diagnostic test accuracy standards
    
    ### 👥 Target Users
    
    - Bioinformatics researchers
    - Laboratory technicians
    - Clinical diagnostics professionals
    - Academic researchers
    - Quality assurance specialists
    """)

if __name__ == "__main__":
    main()
