# Project Profit Pulse

A comprehensive financial analytics dashboard for project performance monitoring, providing visual insights into margins, costs, and regional comparisons.

## Features

- **Executive Dashboard**: Visual summary of key performance metrics across regions
- **AI-Powered Executive Summary**: Automated analysis of financial data with actionable insights
- **Project Details**: Interactive exploration of individual project performance
- **Negative Margin Analysis**: In-depth investigation of underperforming projects
- **Data Visualization**: Interactive charts showing margins, costs, variances by region

## Quick Start

### Local Development

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the app:
   ```
   streamlit run app.py
   ```

### Private Deployment (No GitHub or Paid Services Required)

The app includes built-in password protection and secure tunnel sharing via ngrok:

#### Option 1: One-Step Private Deployment

Run the included shell script to start everything automatically:
```
./run_private_app.sh
```

This will:
1. Start the Streamlit app locally
2. Create a secure ngrok tunnel with a public URL
3. Display the URL and password to share with others

#### Option 2: Manual Private Deployment

1. Start the Streamlit app:
   ```
   streamlit run app.py
   ```

2. In a separate terminal, create a secure tunnel:
   ```
   python setup_ngrok.py
   ```

3. Share the provided URL and the default password (`projectpulse123`) with specific people

#### Changing the Password

1. Edit `.streamlit/secrets.toml` to change the default password
2. Restart the application

### Data Requirements

The application expects two CSV files in the `attached_assets` folder:
- `Summary.csv`: Aggregated metrics by region
- `Projects.csv`: Detailed project-level data

## Deployment Options

### Streamlit Cloud

For a more permanent solution, you can use Streamlit Cloud:
1. Fork this repository to your GitHub account
2. Sign up for [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repo and deploy
4. Add your password to the Streamlit Cloud secrets

### Docker

Build and run as a Docker container:
```
docker build -t project-profit-pulse .
docker run -p 8501:8501 project-profit-pulse
```

## Troubleshooting

If you encounter data formatting issues:
- Ensure your CSV files have properly formatted numeric columns
- Check for missing required columns in your data files
- Review data types (the app handles automatic conversion of percentages and currency values)

## License

For internal use only. 