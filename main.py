from PyPDF2 import PdfReader


def pdf_to_text(path):
    reader = PdfReader(path)

    print("Press\n1: Full PDF\n2: Specific Page")
    users_input = input("Choose: ")

    if users_input == "1":
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    elif users_input == "2":
        page = input("Enter the page number: ")
        converted_page = reader.pages[int(page)]
        text = converted_page.extract_text()
        return text
    else:
        pdf_to_text(path)


def synthesize_text(text):
    """Synthesizes speech from the input string of text."""
    from google.cloud import texttospeech

    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Standard-C",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={"input": input_text,
                 "voice": voice,
                 "audio_config": audio_config}
    )

    # The response's audio_content is binary.
    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')


path = input("Enter the pdf path: ")
text = pdf_to_text(path)
# print(text)
synthesize_text(text)
