import threading
from queue import Queue
from typing import Any, Optional

import dashscope
from dashscope.audio.tts_v2 import *
from dashscope.audio.tts import SpeechSynthesizer as LegacySpeechSynthesizer
from core.model_runtime.errors.validate import CredentialsValidateFailedError
from core.model_runtime.model_providers.__base.tts_model import TTSModel
from core.model_runtime.model_providers.tongyi._common import _CommonTongyi

class TongyiText2SpeechModel(_CommonTongyi, TTSModel):
    """
    Model class for Tongyi Speech-to-Text model.
    """

    def _invoke(self, model: str, tenant_id: str, credentials: dict, content_text: str, voice: str, user: Optional[str] = None) -> Any:
        """
        Invoke text-to-speech model.
        
        :param model: Model name
        :param tenant_id: User tenant ID
        :param credentials: Model credentials
        :param content_text: Text content to be converted
        :param voice: Voice model
        :param user: Unique user ID (optional)
        :return: Audio file generated from text
        """
        voice = voice or self._get_model_default_voice(model, credentials)
        return self._tts_invoke_streaming(model, credentials, content_text, voice)

    def validate_credentials(self, model: str, credentials: dict, user: Optional[str] = None) -> None:
        """
        Validate the provided credentials.

        :param model: Model name
        :param credentials: Model credentials
        :param user: Unique user ID (optional)
        :raises CredentialsValidateFailedError: If validation fails
        """
        try:
            self._tts_invoke_streaming(
                model=model,
                credentials=credentials,
                content_text="Hello Dify!",
                voice=self._get_model_default_voice(model, credentials),
            )
        except Exception as ex:
            raise CredentialsValidateFailedError(str(ex))

    def _tts_invoke_streaming(self, model: str, credentials: dict, content_text: str, voice: str) -> Any:
        """
        Perform text-to-speech conversion with streaming.

        :param model: Model name
        :param credentials: Model credentials
        :param content_text: Text content to be converted
        :param voice: Voice model
        :return: Generator yielding audio data
        """
        word_limit = self._get_model_word_limit(model, credentials)

        def invoke_remote(content, m, v, api_key, cb, audio_format, limit):
            sentences = [content] if len(content) < limit else self._split_text_into_sentences(content, limit)
            for sentence in sentences:
                dashscope.api_key = api_key
                if m == "cosyvoice-v1":
                    SpeechSynthesizer(model=m, voice=v, callback=cb, format=audio_format).call(text=sentence.strip())
                else:
                    LegacySpeechSynthesizer.call(
                        model=v,
                        sample_rate=16000,
                        api_key=api_key,
                        text=sentence.strip(),
                        callback=cb,
                        format=audio_format,
                        word_timestamp_enabled=True,
                        phoneme_timestamp_enabled=True,
                    )

        audio_queue = Queue()
        callback = Callback(queue=audio_queue) if model == "cosyvoice-v1" else Callback_(queue=audio_queue)
        audio_format = AudioFormat.MP3_16000HZ_MONO_128KBPS if model == "cosyvoice-v1" else 'mp3'

        threading.Thread(
            target=invoke_remote,
            args=(content_text, model, voice, credentials.get("dashscope_api_key"), callback, audio_format, word_limit),
        ).start()

        while True:
            audio = audio_queue.get()
            if audio is None:
                break
            yield audio

class Callback(ResultCallback):
    """
    Callback class for handling speech synthesis events.
    """

    def __init__(self, queue: Queue):
        self._queue = queue

    def on_open(self):
        print("Connection opened.")

    def on_complete(self):
        print("Speech synthesis complete.")
        self._queue.put(None)
        self._queue.task_done()

    def on_error(self, message: str):
        print(f"Error occurred: {message}")
        self._queue.put(None)
        self._queue.task_done()

    def on_close(self):
        print("Connection closed.")
        self._queue.put(None)
        self._queue.task_done()

    def on_event(self, message: str):
        print(f"Event received: {message}")

    def on_data(self, data: bytes):
        if data:
            print(f"Received audio data: {len(data)} bytes.")
            self._queue.put(data)

class Callback_(dashscope.audio.tts.ResultCallback):
    def __init__(self, queue: Queue):
        self._queue = queue

    def on_open(self):
        pass

    def on_complete(self):
        self._queue.put(None)
        self._queue.task_done()

    def on_error(self, response: Any):
        self._queue.put(None)
        self._queue.task_done()

    def on_close(self):
        self._queue.put(None)
        self._queue.task_done()

    def on_event(self, result: dashscope.audio.tts.SpeechSynthesisResult):
        audio_frame = result.get_audio_frame()
        if audio_frame:
            self._queue.put(audio_frame)
