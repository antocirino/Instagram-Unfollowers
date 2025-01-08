# Instagram Unfollowers
Instagram Unfollower is a tool that helps you identify users who do not follow you back on Instagram. This tool is designed to help you manage your Instagram followers more effectively.

![Instagram Unfollowers Screenshot](screenshot.png)

## Features
- Identify users who do not follow you back
- Simple and easy-to-use interface
- Guided procedure
- No authentication required

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/antocirino/Instagram-Unfollowers/
    ```
2. Navigate to the project directory:
    ```bash
    cd Instagram-Unfollowers
    ```

## Usage
1. Run the tool:
    ```bash
    python3 instagram-unfollowers.py [-h] [-d] [-v] [-q] [-e]
    ```
2. Follow the on-screen instructions

### Optional arguments:
- `-h`, `--help`     Show the help message and exit
- `-v`, `--version`  Show program's version number and exit
- `-d`, `--debug`    Enable debug mode
- `-q`, `--quick`    Skip the guided procedure (the zip file must already be in the Data folder)
- `-e`, `--export`   Export the results to a text file in the Data folder

### Example
To follow the guided procedure and export the results:
```bash
python3 instagram-unfollowers.py -e
```
To automatically export the results and to skip the guided procedures (the zip file must already be in the Data folder):
```bash
python3 instagram-unfollowers.py -q -e
```


## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

