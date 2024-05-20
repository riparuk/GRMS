# GRMS

GRMS is a FastAPI project for managing guest request.

## Project Structure

Here is the directory structure of this project:

## Requirements
tested on : 
- Python 3.12.3
- fastapi==0.111.0
- pydantic==2.7.1

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/riparuk/GRMS.git
    cd GRMS
    ```

2. Create and activate a virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1. Start the FastAPI server (for development):

    ```bash
    fastapi dev app/main.py
    ```

2. Open your browser and go to the interactive API documentation at:

    ```
    http://127.0.0.1:8000/docs
    ```

    or the alternative documentation at:

    ```
    http://127.0.0.1:8000/redoc
    ```

## Directory Explanation

- `app/main.py`: Main file to run the FastAPI application.
- `app/config.py`: Configuration file for the application.
- `app/db/`: Directory containing database logic like models, schemas, and CRUD operations.
- `app/routers/`: Directory containing router definitions for different endpoints.
- `requirements.txt`: File containing the list of required dependencies.

## Contribution

If you want to contribute to this project, please fork the repository and create a pull request. We appreciate your contributions!

