# Nucleic Acid Amplification Techniques Comparison Tool

## Overview

This is a bioinformatics application built with Streamlit that allows researchers and lab technicians to compare various nucleic acid amplification techniques such as PCR, qPCR, RPA, LAMP, and others. The application provides statistical analysis tools to evaluate diagnostic performance metrics including sensitivity, specificity, positive predictive value (PPV), negative predictive value (NPV), and Cohen's Kappa statistic with 95% confidence intervals. The goal is to help users select the most reliable amplification method based on statistical performance data.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web application framework for rapid prototyping and data science applications
- **Layout**: Wide layout with expandable sidebar navigation
- **Visualization**: Plotly Express and Plotly Graph Objects for interactive charts and statistical plots
- **Navigation**: Multi-page application structure with sidebar-based page selection

### Application Structure
- **Main Application**: `app.py` serves as the entry point with page routing and UI components
- **Data Layer**: Centralized data management in `data/amplification_data.py` containing default performance metrics for 8+ amplification techniques
- **Statistics Engine**: `utils/statistics.py` implements comprehensive diagnostic statistics calculations using Wilson confidence intervals and GraphPad-style methodologies
- **Page Components**: Modular page functions for overview, custom analysis, statistical testing, and documentation

### Statistical Analysis Components
- **Diagnostic Metrics Calculator**: Computes sensitivity, specificity, PPV, NPV, and accuracy with 95% confidence intervals
- **Confidence Interval Methods**: Wilson score intervals for more accurate small-sample statistics
- **Comparative Analysis**: Multi-technique comparison capabilities for research decision support
- **Cohen's Kappa Implementation**: Statistical agreement measurement for method validation

### Data Management
- **Default Dataset**: Pre-loaded performance data for major amplification techniques (PCR, qPCR, RPA, LAMP, NASBA, SDA, TMA, HDA)
- **Custom Data Support**: User input capabilities for experimental data analysis
- **Realistic Metrics**: Literature-based performance values with proper confusion matrix components (TP, FN, TN, FP)

## External Dependencies

### Core Libraries
- **Streamlit**: Web application framework for the user interface
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing and statistical calculations
- **Plotly**: Interactive visualization library for charts and graphs
- **SciPy**: Statistical functions and confidence interval calculations

### Statistical Computing
- **scipy.stats**: Statistical distributions and hypothesis testing
- **scipy.stats.chi2**: Chi-square distribution for confidence intervals
- **math**: Mathematical functions for statistical computations

### Data Processing
- **io**: Input/output operations for data handling
- **pandas DataFrame**: Structured data representation for amplification technique metrics

Note: The application currently operates with in-memory data and file-based storage. Future enhancements may include database integration for persistent data storage and user session management.