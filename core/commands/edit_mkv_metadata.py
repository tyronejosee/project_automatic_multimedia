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
        file_paths: list[str] = self._list_files(self.directory)
        if not file_paths:
            logging.error("No supported files were found.")
            return

        for file_path in file_paths:
            self._process_mkv(file_path)

    def _list_files(self, directory: str) -> list[str]:
        """
        Traverse a folder and return the file paths.
        """
        file_paths: list = []
        for root, _, archives in os.walk(directory):
            for archive in archives:
                if archive.endswith(".mkv"):
                    file_paths.append(os.path.join(root, archive))
        return file_paths

    def _process_mkv(self, file_path: str) -> None:
        """
        Process the file, clean it, add subtitles, and modify metadata.
        """
        file = MKVFile(file_path)
        file.title = self._generate_title(file_path)
        subtitles, audios = self._find_media(file_path)
        if self._verify_file(file, file_path, subtitles):
            return

        self._clean_metadata(file)
        self._remove_media(file, subtitles, audios)
        self._rename_tracks(file)
        self._process_media(file, subtitles, audios)

        output_file: str = os.path.splitext(file_path)[0] + " (1).mkv"
        file.mux(output_file)
        logging.info(f"Created {output_file}")

    def _verify_file(self, file: MKVFile, file_path: str, subtitles) -> bool:
        """
        Check if there are any audio tracks that are not AAC.
        """
        if not subtitles:
            logging.warning(
                f"Ignored {file_path} No subtitles found.",
            )
            return True

        seen_languages = set()

        for track in file.tracks:
            if track.track_type == "audio":
                if track.language in seen_languages:
                    logging.warning(
                        f"Ignored {file_path} Duplicate audio language"
                        f"{{track.language}}."
                    )
                    return True
                seen_languages.add(track.language)

            match (self.param, track.track_type, track._track_codec):
                # case ("series", "audio", codec) if codec != "AAC":
                #     logging.warning(
                #         f"Ignored {file_path} ({track._track_codec})",
                #     )
                #     return True

                case ("movies", "audio", codec) if codec != "AC-3":
                    logging.warning(
                        f"Ignored {file_path} ({track._track_codec})",
                    )
                    return True

                case _:
                    pass
        return False

    def _remove_media(
        self, file: MKVFile, subtitles: list[dict], audios: list[dict]
    ) -> None:
        """
        Remove media tracks from a file.
        """
        if subtitles:
            sub_tracks: list[int] = [
                track.track_id
                for track in file.tracks
                if track.track_type == "subtitles"
            ]
            for track_id in sorted(sub_tracks, reverse=True):
                try:
                    file.remove_track(track_id)
                except IndexError:
                    logging.error(
                        f"{track_id} does not exist or has already been deleted.",
                    )
        if audios:
            aud_tracks: list[int] = [
                track.track_id
                for track in file.tracks
                if track.track_type == "audio"
            ]
            for track_id in sorted(aud_tracks, reverse=True):
                try:
                    file.remove_track(track_id)
                except IndexError:
                    logging.error(
                        f"{track_id} does not exist or has already been deleted.",
                    )

    def _clean_metadata(self, file: MKVFile) -> None:
        """
        Remove chapters, attachments, and global tags from a file.
        """
        file.no_attachments()
        file.no_chapters()
        file.no_global_tags()

    def _find_media(self, file_path: str) -> tuple[list[dict], list[dict]]:
        """
        Pending.
        """
        folder: str = os.path.dirname(file_path)
        subtitles: list = []
        audios: list = []
        for archive in os.listdir(folder):
            if archive.endswith(".srt"):
                if archive == "spa.srt":
                    subtitles.append(
                        {
                            "path": os.path.join(folder, archive),
                            "language": "spa",
                            "track_name": "Español",
                            "is_default": False,
                        }
                    )
                elif archive == "forced.srt":
                    subtitles.append(
                        {
                            "path": os.path.join(folder, archive),
                            "language": "spa",
                            "track_name": "Forced",
                            "is_default": True,
                        }
                    )
            elif archive.endswith(".aac"):
                if archive == "jpn.aac":
                    audios.append(
                        {
                            "path": os.path.join(folder, archive),
                            "language": "jpn",
                            "track_name": "日本語",
                            "is_default": True,
                        }
                    )
        return subtitles, audios

    def _process_media(
        self,
        file: MKVFile,
        subtitles: list[dict],
        audios: list[dict],
    ) -> None:
        for subtitle in subtitles:
            if subtitle["track_name"] == "Español" and not any(
                s["track_name"] == "Forced" for s in subtitles
            ):
                subtitle["is_default"] = True

            match (self.param, subtitle["track_name"]):
                case "series", "Español":
                    self._add_new_track(
                        file,
                        subtitle["path"],
                        subtitle["language"],
                        subtitle["track_name"],
                        subtitle["is_default"],
                    )

                case "series", "Forced":
                    self._add_new_track(
                        file,
                        subtitle["path"],
                        subtitle["language"],
                        subtitle["track_name"],
                        subtitle["is_default"],
                    )

                case "movies", "Español":
                    self._add_new_track(
                        file,
                        subtitle["path"],
                        subtitle["language"],
                        subtitle["track_name"],
                        subtitle["is_default"],
                    )

                case "movies", "Forced":
                    self._add_new_track(
                        file,
                        subtitle["path"],
                        subtitle["language"],
                        subtitle["track_name"],
                        subtitle["is_default"],
                    )
        for audio in audios:
            match (self.param, audio["track_name"]):
                case "series", "日本語":
                    self._add_new_track(
                        file,
                        audio["path"],
                        audio["language"],
                        audio["track_name"],
                        audio["is_default"],
                    )

    def _add_new_track(
        self,
        file: MKVFile,
        media_path: str,
        language: str,
        track_name: str,
        default_track: bool,
    ) -> None:
        """
        Add a new track to the file.
        """
        new_track = MKVTrack(media_path)
        new_track.language = language
        new_track.track_name = track_name
        new_track.default_track = default_track
        file.add_track(new_track)

    def _rename_tracks(self, file: MKVFile) -> None:
        """
        Rename audio and video tracks based on their language and type,
        considering whether the content is 'series' or 'movies'.
        """
        has_spanish_audio: bool = any(
            track.track_type == "audio" and track.language == "spa"
            for track in file.tracks
        )

        for track in file.tracks:
            match (self.param, track.track_type, track.language):
                case ("series", "video", "und"):
                    track.language = "jpn"
                    track.track_name = "日本語"
                    track.default_track = True

                case ("series", "video", "jpn"):
                    track.language = "jpn"
                    track.track_name = "日本語"
                    track.default_track = True

                case ("series", "video", "eng"):
                    track.track_name = "English"
                    track.default_track = True

                case ("series", "audio", "jpn"):
                    track.track_name = "日本語"
                    if not has_spanish_audio:
                        track.default_track = True
                    else:
                        track.default_track = False

                case ("series", "audio", "spa"):
                    track.track_name = "Español"
                    track.default_track = True

                case ("movies", "video", "und"):
                    track.language = "eng"
                    track.track_name = "English"
                    track.default_track = True

                case ("movies", "video", "jpn"):
                    track.track_name = "日本語"
                    if not has_spanish_audio:
                        track.default_track = True
                    track.default_track = False

                case ("movies", "audio", "spa"):
                    track.track_name = "Español"
                    track.default_track = True

                case _:
                    pass

    def _generate_title(self, file_path: str) -> str:
        """
        Generate title for the file based on folder name and episode number.
        """
        folder: str = os.path.basename(os.path.dirname(file_path))
        folder_without_year: str = re.sub(r" \(\d{4}\)", "", folder)
        title: str = re.sub(r"_ ", ": ", folder_without_year)

        if self.param == "series":
            episode: list[str] = re.findall(r"- (\d{2,4})", file_path)
            title: str = f"{title} - {episode[0]}"
        elif self.param == "movies":
            title: str = f"{title}"

        return title
