# **Project Automatic Multimedia**

## 📌 Description

A CLI tool for the automated management of multimedia libraries. Its purpose is to facilitate the organization and metadata extraction of movies, series, anime, and manga, as well as automatically manage icons and covers.

## 🚀 Features

- **Automatic organization**: Generates and assigns icons and content folders.
- **Metadata management**: Extracts and edits metadata in MKV files.
- **Task automation**: CLI commands to process and organize multimedia libraries.
- **Compatibility**: Works with movies, series, anime, and manga.
- **Support for multiple formats**: JSON, SQLite databases, and multimedia files.

## 📂 Project Structure

```bash
project_automatic_multimedia/
│── cli.py              # Command Line Interface (CLI)
│── database.db         # SQLite database
│── movies.json         # Movie data
│── series.json         # Series data
│── requirements.txt    # Project dependencies
│── test.py             # Tests
│── core/               # Main project module
│ ├── commands/         # CLI command implementations
│ ├── interfaces/       # System interfaces
│ ├── manager/          # Command management
│ ├── observers/        # Observers (notifications, events)
│ ├── repositories/     # Data repositories
│ ├── settings/         # System configuration
│ └── utils/            # General utilities and functions
│── assets/             # Image resources and extensions
│── docs/               # Project documentation
```

## 📖 Installation

Make sure you have Python 3.11 installed, then run:

```bash
git clone https://github.com/tyronejosee/project_automatic_multimedia.git
cd project_automatic_multimedia
pip install -r requirements.txt
```

## 🛠 Usage

Run the following commands to manage your multimedia library:

```bash
python cli.py build_icons <media_type>
python cli.py generate_folders
python cli.py set_folder_icons <media_type>
python cli.py data_loader <media_type>
python cli.py copy_covers
python cli.py edit_mkv_metadata <media_type>
python cli.py extract_subtitles
```

## 📜 License

This project is licensed under the **Apache License 2.0**.

💡 **Contributions are welcome**: If you would like to improve this project, feel free to fork it and submit a pull request.  
📧 **Contact**: Open an issue in the repository if you need support.
