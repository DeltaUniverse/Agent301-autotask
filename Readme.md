# Agent301 Auto Complete Task

This Python script automates the process of claiming tasks. It reads authorization tokens from a file, extracts usernames, and uses those tokens to claim tasks asynchronously. The script is designed to run indefinitely with periodic pauses, making it ideal for long-term automation tasks.

## Features

- Asynchronous HTTP requests using `aiohttp` for efficient task handling.
- Randomized user-agent headers with `fake-useragent` to simulate different clients.
- Asynchronous file reading with `aiofiles` to handle large numbers of tokens.
- Comprehensive logging with `logging` module for easy monitoring and debugging.
- Graceful exit on user interruption (`Ctrl + C`).

## Requirements

- Python 3.7 or higher
- `aiohttp` library
- `aiofiles` library
- `fake-useragent` library

## Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/DeltaUniverse/Agent301-autotask.git
    cd Agent301-autotask
    ```

2. **Install Required Libraries:**

    Install the necessary Python libraries by running:

    ```bash
    pip install aiohttp aiofiles fake-useragent
    ```

3. **Prepare Your `query.txt` File:**

    Create a file named `query.txt` in the project directory. This file should contain the authorization tokens you want to use, one per line:

    ```
    token1
    token2
    ```

## Usage

1. **Run the Script:**

    Start the script by running:

    ```bash
    python main.py
    ```

2. **Monitor the Output:**

    The script logs all actions and errors. You can monitor the output directly in the terminal or check the `logger.log` file for a detailed log of all operations performed.

3. **Stopping the Script:**

    To stop the script, press `Ctrl + C` in the terminal where it's running. The script will handle the interruption gracefully and exit.

## Contributing

We welcome contributions! Feel free to fork the repository and submit pull requests. If you encounter any issues or have suggestions for improvements, please open an issue on the GitHub repository.

## Join Our Community

For updates, support, and more information, join our Telegram channels:

- [News and Announcements](https://t.me/deltaxnews)
- [Support Group](https://t.me/deltaxsupports)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
