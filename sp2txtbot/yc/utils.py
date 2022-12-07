from pydub import AudioSegment


def convert_ogg_to_mp3(ogg_file: str, mp3_file: str) -> str:
    """
    Преобразует аудиофайл в формате .ogg в .mp3

    :param str ogg_file: Путь до аудиофайла в формате .ogg
    :param str mp3_file: Путь до аудиофайла в формате .mp3
    """
    sound = AudioSegment.from_ogg(ogg_file)
    sound.export(mp3_file, format="mp3")
    return mp3_file


def convert_mp4_to_mp3(mp4_file: str, mp3_file: str) -> str:
    """
    Преобразует аудиофайл в формате .mp4 в .mp3

    :param str mp4_file: Путь до аудиофайла в формате .mp4
    :param str mp3_file: Путь до аудиофайла в формате .mp3
    """
    sound = AudioSegment.from_file(mp4_file)
    sound.export(mp3_file, format="mp3")
    return mp3_file
