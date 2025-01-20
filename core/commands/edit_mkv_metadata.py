import os
import re
import logging

from pymkv import MKVFile, MKVTrack

from core.interfaces.command_interface import ICommand
from core.utils.logging import setup_logging

setup_logging()


class EditMkvMetadataCommand(ICommand):
    def __init__(self, param: str, directory: str) -> None:
        self.param: str = param
        self.directory: str = directory

    def execute(self) -> None:
        """
        Main method that executes the command.
        """
        files: list[str] = self._list_files(self.directory)
        if not files:
            logging.error("No supported files were found.")
            return

        for file in files:
            self._process_mkv(file, self.param)

    def _list_files(self, directory) -> list[str]:
        """
        Traverse a folder and return the file paths.
        """
        mkv_files: list = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".mkv"):
                    mkv_files.append(os.path.join(root, file))
        return mkv_files

    def _process_mkv(self, input_file, param) -> None:
        """
        Process the file, clean it, add subtitles, and modify metadata.
        """
        file = MKVFile(input_file)
        # if self._verify_audio_tracks(mkv, param, input_file):
        #     return
        self._remove_subtitles(file)
        self._clean_mkv_metadata(file)
        subtitles: list[dict] = self._find_subtitles(input_file)
        default_subtitle = None

        for subtitle in subtitles:
            if subtitle["type"] == "Forced":
                default_subtitle = subtitle
                break
        if not default_subtitle:
            for subtitle in subtitles:
                if subtitle["type"] == "Español":
                    default_subtitle = subtitle
                    break

        for subtitle in subtitles:
            if subtitle["type"] == "Español":
                self._add_subtitle_track(file, subtitle["path"], "Español")
            elif subtitle["type"] == "Forced":
                self._add_subtitle_track(
                    file,
                    subtitle["path"],
                    "Español (Forced)",
                )

        if default_subtitle:
            for track in file.tracks:
                if (
                    track.track_type == "subtitles"
                    and track.file_path == default_subtitle["path"]
                ):
                    track.default_track = True
                elif track.track_type == "subtitles":
                    track.default_track = False

        self._rename_tracks(file)
        title: str = self._generate_title(input_file)
        file.title = title
        output_file: str = os.path.splitext(input_file)[0] + " (1).mkv"
        file.mux(output_file)
        print(f"Created {output_file}")

    def _verify_audio_tracks(self, file, param, input_file) -> bool:
        """
        Check if there are any audio tracks that are not AAC.
        """
        for track in file.tracks:
            if (
                param == "series"
                and track.track_type == "audio"
                and track._track_codec != "AAC"
            ):
                logging.warning(
                    f"Ignored {input_file} ({track._track_codec})",
                )
                return True
        return False

    def _remove_subtitles(self, file) -> None:
        """
        Remove all subtitle tracks from a file.
        """
        sub_tracks: list[int] = [
            track.track_id for track in file.tracks if track.track_type == "subtitles"
        ]
        for track_id in sorted(sub_tracks, reverse=True):
            try:
                file.remove_track(track_id)
            except IndexError:
                logging.error(
                    f"{track_id} does not exist or has already been deleted.",
                )

    def _clean_mkv_metadata(self, file) -> None:
        """
        Remove chapters, attachments, and global tags from a file.
        """
        file.no_attachments()
        file.no_chapters()
        file.no_global_tags()

    def _find_subtitles(self, file) -> list[dict]:
        """
        Search for .srt files in the same folder as the MKV file.
        Return a list of found subtitles with their type and path.
        """
        directory: str = os.path.dirname(file)
        subtitles: list = []
        for archive in os.listdir(directory):
            if archive.endswith(".srt"):
                if archive == "spa.srt":
                    subtitles.append(
                        {
                            "type": "Español",
                            "path": os.path.join(directory, archive),
                        }
                    )
                elif archive == "forced.srt":
                    subtitles.append(
                        {
                            "type": "Forced",
                            "path": os.path.join(directory, archive),
                        }
                    )
        return subtitles

    def _add_subtitle_track(
        self,
        file,
        subtitle_path,
        track_name,
        language="spa",
    ) -> None:
        """
        Add a subtitle track to the file.
        """
        new_subtitle = MKVTrack(subtitle_path)
        new_subtitle.language = language
        new_subtitle.track_name = track_name
        new_subtitle.default_track = False
        file.add_track(new_subtitle)

    def _rename_tracks(self, file) -> None:
        """
        Rename audio and video tracks based on their language and type.
        """
        for track in file.tracks:
            if track.track_type == "video" and track.language == "und":
                track.language = "jpn"
                track.default_track = True
                track.track_name = "日本語"
            elif track.track_type == "video" and track.language == "eng":
                track.default_track = True
                track.track_name = "English"
            elif track.track_type == "video" and track.language == "jpn":
                track.default_track = True
                track.track_name = "日本語"
            elif track.track_type == "audio" and track.language == "jpn":
                track.track_name = "日本語"
            elif track.track_type == "audio" and track.language == "spa":
                track.track_name = "Español"

    def _generate_title(self, file_path) -> str:
        folder: str = os.path.basename(os.path.dirname(file_path))
        folder_year: str = re.sub(r" \(\d{4}\)", "", folder)
        folder_year: str = re.sub(r"_ ", ": ", folder_year)
        episode: list[str] = re.findall(r"- \d{2,4}", file_path)
        title: str = f"{folder_year} {episode[0]}"
        return title
