import os
import subprocess

from pymkv import MKVFile
from pymkv.MKVTrack import MKVTrack

from core.interfaces.command_interface import ICommand


class ExtractSubtitlesCommand(ICommand):
    def __init__(self, directory: str) -> None:
        self.directory: str = directory

    def execute(self) -> None:
        """
        Main method that executes the command.
        """
        mkv_files: list[str] = self._find_mkv_files()
        if not mkv_files:
            raise FileNotFoundError("No .mkv files found.")

        for file in mkv_files:
            print(file)
            self._process_mkv_file(file)

    def _find_mkv_files(self) -> list[str]:
        """
        Searches for MKVs in the directory and returns a list of paths.
        """
        mkv_files: list[str] = []
        for root, _, files in os.walk(self.directory):
            for file in files:
                if file.endswith(".mkv"):
                    mkv_files.append(os.path.join(root, file))
        return mkv_files

    def _process_mkv_file(self, file: str) -> None:
        """
        Processes an MKV file, lists the tracks, and extracts subtitles.
        """
        try:
            mkv: MKVFile = MKVFile(file)
            for track in mkv.tracks:
                if track.track_type == "subtitles":
                    self._extract_subtitle(file, track)
        except Exception as e:
            print(f"Error {file}: {e}")

    def _get_subtitle_type(self, format: str | None) -> str:
        if format == "SubRip/SRT":
            return ".srt"
        elif format == "SubStationAlpha":
            return ".ass"
        elif format == "HDMV PGS":
            return ".sup"
        else:
            raise ValueError(f"Unrecognized subtitle format '{format}'")

    def _extract_subtitle(self, file: str, track: MKVTrack) -> None:
        """
        Extracts a subtitle from an MKV file using mkvextract.
        """
        parent_directory: str = os.path.dirname(file)
        track_name: str = track.track_name if track.track_name else "Subtitle"
        sub_type: str = self._get_subtitle_type(track._track_codec)
        output_file_name: str = f"[{track.language}] {track_name}{sub_type}"
        output_file_path: str = os.path.join(
            parent_directory,
            output_file_name,
        )

        command: list[str] = [
            "mkvextract",
            "tracks",
            file,
            f"{track.track_id}:{output_file_path}",
        ]

        try:
            subprocess.run(command, check=True)
            print(f"Subtitle extracted to: {output_file_path}")
        except subprocess.CalledProcessError as e:
            print(f"Command error: [{file}] {e}")
