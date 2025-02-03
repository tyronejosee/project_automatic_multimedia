import os
import json
import logging
import subprocess

from pymkv import MKVFile
from pymkv.MKVTrack import MKVTrack

from core.interfaces.command_interface import ICommand
from core.utils.logging import setup_logging

setup_logging()


class ExtractMediaCommand(ICommand):
    def __init__(self, directory: str) -> None:
        self.directory: str = directory

    def execute(self) -> None:
        """
        Main method that executes the command.
        """
        file_paths: list[str] = self._list_files()
        if not file_paths:
            raise FileNotFoundError("No files found.")

        for file_path in file_paths:
            logging.info(f"Processing {file_path}...")
            self._process_mkv_file(file_path)
        logging.info("Task completed successfully. 🎉")

    def _list_files(self) -> list[str]:
        """
        Searches for MKVs in the directory and returns a list of paths.
        """
        file_paths: list[str] = []
        for root, _, archives in os.walk(self.directory):
            for archive in archives:
                if archive.endswith(".mkv"):
                    file_paths.append(os.path.join(root, archive))
        return file_paths

    def _process_mkv_file(self, file_path: str) -> None:
        """
        Processes file, lists the tracks, extracts subtitles and audios.
        """
        file: MKVFile = MKVFile(file_path)
        for track in file.tracks:
            S_LANGUAGES: set[str] = {"spa", "lat"}
            A_LANGUAGES: set[str] = {"spa", "lat", "jpn"}
            A_EXCLUDED_CODECS: set[str] = {"AAC"}

            match (
                track.track_type,
                track.language,
                track._track_codec,
            ):
                case (
                    "subtitles",
                    lang,
                    _,
                ) if lang in S_LANGUAGES:
                    self._extract_subtitle(file_path, track)

                case (
                    "audio",
                    lang,
                    codec,
                ) if lang in A_LANGUAGES and codec not in A_EXCLUDED_CODECS:
                    self._extract_audio(file_path, track)

    def _get_subtitle_extension(self, codec: str) -> str:
        extensions: dict[str, str] = {
            "SubRip/SRT": ".srt",
            "SubStationAlpha": ".ass",
            "Advanced SubStationAlpha": ".ssa",
            "HDMV PGS": ".sup",
            "VobSub": ".sub",
            "MicroDVD": ".sub",
            "DVD Subtitle": ".sub",
            "BluRay SUP": ".sup",
            "TTML": ".ttml",
            "WebVTT": ".vtt",
        }
        return extensions.get(codec, "")

    def _get_audio_extension(self, codec: str) -> str:
        extensions: dict[str, str] = {
            "AAC": ".aac",
            "MP3": ".mp3",
            "AC-3": ".ac3",
            "E-AC-3": ".eac3",
            "TrueHD": ".thd",
            "DTS": ".dts",
            "DTS-HD": ".dts",
            "DTS-HD MA": ".dtsma",
            "FLAC": ".flac",
            "PCM": ".wav",
            "ALAC": ".m4a",
        }
        return extensions.get(codec, "")

    def _get_track_delays(self, file_path: str, track_id: int) -> int:
        """
        Gets the delays from an file using MediaInfo.
        """
        command: list[str] = ["mediainfo", "--Output=JSON", file_path]

        try:
            result: subprocess.CompletedProcess[str] = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True,
            )
            mediainfo_data: dict = json.loads(result.stdout)
            tracks: list[dict] = mediainfo_data["media"]["track"]

            for track in tracks:
                if (
                    track["@type"] == "Audio"
                    and int(track["StreamOrder"]) == track_id
                ):
                    delay: int = 0
                    if "Delay" in track:
                        delay_str: str = track["Delay"]
                        delay = (
                            int(float(delay_str) * 1000) if delay_str else 0
                        )
            return delay
        except subprocess.CalledProcessError as e:
            logging.error(f"Error getting track delays for {file_path}: {e}")
            return 0

    def _extract_audio(self, file: str, track: MKVTrack) -> None:
        """
        Extracts an audio track from a file.
        """
        parent_directory: str = os.path.dirname(file)
        audio_type: str = self._get_audio_extension(str(track._track_codec))
        delay: int = self._get_track_delays(file, track.track_id or 0)

        file_name: str = (
            f"[{track.language}] [{track.track_id}] "
            f"{track.track_name or ''} DELAY {delay}ms{audio_type}"
        )
        output_path: str = os.path.join(
            parent_directory,
            file_name,
        )
        track_id: int = track.track_id or 0

        self._run_mkvextract(file, track_id, output_path)
        logging.info(f"Audio extracted to: {output_path}")

    def _extract_subtitle(self, file: str, track: MKVTrack) -> None:
        """
        Extracts a subtitle track from a file.
        """
        parent_directory: str = os.path.dirname(file)
        sub_type: str = self._get_subtitle_extension(str(track._track_codec))
        file_name: str = (
            f"[{track.language}] [{track.track_id}] "
            f"{track.track_name or ''}{sub_type}"
        )
        output_path: str = os.path.join(
            parent_directory,
            file_name,
        )
        track_id: int = track.track_id or 0

        self._run_mkvextract(file, track_id, output_path)
        logging.info(f"Subtitle extracted to: {output_path}")

    def _run_mkvextract(
        self,
        file: str,
        track_id: int,
        output_path: str,
    ) -> None:
        """
        Runs the mkvextract command to extract the specified track.
        """
        command: list[str] = [
            "mkvextract",
            "tracks",
            file,
            f"{track_id}:{output_path}",
        ]

        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"{file}: {e}")
