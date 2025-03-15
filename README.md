# Starter Code for Deepseek-R1 via AWS Bedrock

This repository provides starter code to run the Deepseek-R1 model using AWS Bedrock. It serves as a basic template to help you get up and running quickly with AWS Bedrock inferencing using Deepseek-R1. You can extend and customize this codebase according to your project's requirements.

## Features

- **Starter Implementation:**  
  A minimal setup for interacting with AWS Bedrock's Deepseek-R1 model.

- **Non-Streaming Query:**  
  Perform a single API call to fetch a complete response along with its reasoning text.

- **Streaming Query:**  
  Process and display streaming tokens in real-time, separating reasoning tokens from the final response.

- **Configuration Management:**  
  Environment variables are managed via a `.env` file using the `python-dotenv` package.

- **Modular Design:**  
  The project is organized into clearly separated modules for AWS interaction, configuration management, and client logic.

## Prerequisites

- Python 3 installed on your system.
- A properly configured IAM account for AWS Bedrock:
  - Set up an IAM user in AWS with the permissions required to access AWS Bedrock.
  - Ensure that the IAM user has the necessary policies attached allowing access to the relevant AWS services.
- Valid AWS credentials and relevant service details.
- Model access in AWS Bedrock must be available in the region you choose. Verify that your selected AWS region supports the Deepseek-R1 model.

## Repository Structure

```
.
├── .env.example          # Example environment configuration file.
├── .gitignore            # Git ignore file.
├── main.py               # Main entry point for command-line interactions.
├── README.md             # This file.
├── requirements.txt      # List of required Python packages.
├── streamlit_app.py      # Streamlit application for web-based interactions.
└── app
    ├── __init__.py       # Initializes the app package.
    ├── aws_client.py     # Module to manage AWS client interactions.
    ├── bedrock_client.py # Module for AWS Bedrock DeepSeek communication.
    └── config.py         # Configuration management for the application.
```

## Setup

1. **Clone the Repository**

   Clone this repository to your local machine.

2. **Configure Environment**

   Follow these steps to obtain your AWS environment variables from the AWS Console:

   - **Step 1:** Log in to your [AWS Management Console](https://aws.amazon.com/console/).
   - **Step 2:** Navigate to the **IAM** (Identity and Access Management) service.
   - **Step 3:** Create a new IAM user (or use an existing one) with appropriate permissions for AWS Bedrock.
   - **Step 4:** After creating the user, go to the **Security credentials** tab to generate an **Access key** and **Secret access key**.
   - **Step 5:** Note down or download these keys along with your AWS region details.
   - **Step 6:** To verify model access for Deepseek-R1, perform the following:
     - Navigate to **AWS Bedrock** in your AWS Console.
     - Click on **Foundation Models** and then select **Model Catalog**.
     - Locate the **Deepseek-R1** model in the catalog.
     - In the box where "serverless" is mentioned, click the three-dot button and select **Modify Access**.
     - This will take you to the **Model Access** page. Click **Available to request** for Deepseek-R1.
     - Follow the on-screen instructions to complete the request. Click on **Next** followed by **Submit**.
   - **Step 7:** Copy the provided details into a file:
     
     Copy the `.env.example` file to `.env` and update it as follows. **Note:** The `AWS_SERVICE_NAME` should remain set to `bedrock-runtime`:
     
     ```
     AWS_SERVICE_NAME=bedrock-runtime
     AWS_REGION_NAME=your_aws_region
     AWS_ACCESS_KEY_ID=your_access_key_id
     AWS_SECRET_ACCESS_KEY=your_secret_access_key
     ```

3. **Install Dependencies**

   It is recommended to create a virtual environment before installing the required packages:
   
   - Create and activate a virtual environment:
     
     On macOS/Linux:
     ```
     python3 -m venv venv
     source venv/bin/activate
     ```
     
     On Windows:
     ```
     python -m venv venv
     venv\Scripts\activate
     ```
   
   - Install the required Python packages:
   
     ```
     pip install -r requirements.txt
     ```

## Running the Application

### Command-line Interface

Run the main entry point to launch the application via the command line:

```bash
python main.py
```

### Streamlit Web Interface

Launch the Streamlit web interface for an interactive experience:

```bash
streamlit run streamlit_app.py
```

## Project Structure

- **main.py**  
  The entry point of the application. It handles configuration loading, client initialization, and execution of inferencing queries.

- **app/config.py**  
  Loads environment variables from the `.env` file and supplies the configuration.

- **app/aws_client.py**  
  Sets up a universal boto3 client for AWS Bedrock using the provided configuration.

- **app/bedrock_client.py**  
  Contains the `BedrockClientDeepseek` class which:
  - Structures the conversation.
  - Issues both non-streaming and streaming queries.
  - Distinguishes between reasoning tokens and final response tokens.

## Notes

- **Starter Code:**  
  This is a foundational template intended for learning and initial experimentation with AWS Bedrock and Deepseek-R1. Adapt and expand the code as needed for production use.

- **Troubleshooting:**  
  - Ensure your `.env` file contains correct AWS credentials.
  - Verify that all dependencies are installed properly.

## Contributing

Contributions are welcome. Feel free to open issues or submit pull requests with improvements and bug fixes.
