import tempfile
from pydub import AudioSegment
from pydub.utils import which

# ffmpeg 설정
AudioSegment.converter = which("ffmpeg")

# m4a → wav convert
def convert_m4a_to_wav(m4a_bytes):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".m4a") as temp_m4a:
        temp_m4a.write(m4a_bytes)
        temp_m4a_path = temp_m4a.name

    sound = AudioSegment.from_file(temp_m4a_path, format="m4a")
    temp_wav_path = temp_m4a_path.replace(".m4a", ".wav")
    sound.export(temp_wav_path, format="wav")
    return temp_wav_path
