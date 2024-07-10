import asyncio
from edge_tts import Communicate
import io

async def generate_speech_async(text: str, voice: str, speed: float, output_format: str):
    # 将速度转换为 Edge-TTS 可接受的格式
    if speed == 1.0:
        rate = "+0%"  # 默认速度
    else:
        # 将速度转换为百分比变化
        rate = f"{(speed - 1) * 100:+.0f}%"
    
    communicate = Communicate(text, voice, rate=rate)
    audio_stream = io.BytesIO()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_stream.write(chunk["data"])
    
    audio_stream.seek(0)
    return audio_stream

def get_voice(requested_voice: str, default_male: str, default_female: str):
    valid_voices = [
        "af-ZA-AdriNeural", "af-ZA-WillemNeural", "am-ET-AmehaNeural", "am-ET-MekdesNeural",
        "ar-AE-FatimaNeural", "ar-AE-HamdanNeural", "ar-BH-AliNeural", "ar-BH-LailaNeural",
        "ar-DZ-AminaNeural", "ar-DZ-IsmaelNeural", "ar-EG-SalmaNeural", "ar-EG-ShakirNeural",
        "ar-IQ-BasselNeural", "ar-IQ-RanaNeural", "ar-JO-SanaNeural", "ar-JO-TaimNeural",
        "ar-KW-FahedNeural", "ar-KW-NouraNeural", "ar-LB-LaylaNeural", "ar-LB-RamiNeural",
        "ar-LY-ImanNeural", "ar-LY-OmarNeural", "ar-MA-JamalNeural", "ar-MA-MounaNeural",
        "ar-OM-AbdullahNeural", "ar-OM-AyshaNeural", "ar-QA-AmalNeural", "ar-QA-MoazNeural",
        "ar-SA-HamedNeural", "ar-SA-ZariyahNeural", "ar-SY-AmanyNeural", "ar-SY-LaithNeural",
        "ar-TN-HediNeural", "ar-TN-ReemNeural", "ar-YE-MaryamNeural", "ar-YE-SalehNeural",
        "az-AZ-BabekNeural", "az-AZ-BanuNeural", "bg-BG-BorislavNeural", "bg-BG-KalinaNeural",
        "bn-BD-NabanitaNeural", "bn-BD-PradeepNeural", "bn-IN-BashkarNeural", "bn-IN-TanishaaNeural",
        "bs-BA-GoranNeural", "bs-BA-VesnaNeural", "ca-ES-EnricNeural", "ca-ES-JoanaNeural",
        "cs-CZ-AntoninNeural", "cs-CZ-VlastaNeural", "cy-GB-AledNeural", "cy-GB-NiaNeural",
        "da-DK-ChristelNeural", "da-DK-JeppeNeural", "de-AT-IngridNeural", "de-AT-JonasNeural",
        "de-CH-JanNeural", "de-CH-LeniNeural", "de-DE-AmalaNeural", "de-DE-ConradNeural",
        "de-DE-KatjaNeural", "de-DE-KillianNeural", "el-GR-AthinaNeural", "el-GR-NestorasNeural",
        "en-AU-NatashaNeural", "en-AU-WilliamNeural", "en-CA-ClaraNeural", "en-CA-LiamNeural",
        "en-GB-LibbyNeural", "en-GB-MaisieNeural", "en-GB-RyanNeural", "en-GB-SoniaNeural",
        "en-GB-ThomasNeural", "en-HK-SamNeural", "en-HK-YanNeural", "en-IE-ConnorNeural",
        "en-IE-EmilyNeural", "en-IN-NeerjaExpressiveNeural", "en-IN-NeerjaNeural", "en-IN-PrabhatNeural",
        "en-KE-AsiliaNeural", "en-KE-ChilembaNeural", "en-NG-AbeoNeural", "en-NG-EzinneNeural",
        "en-NZ-MitchellNeural", "en-NZ-MollyNeural", "en-PH-JamesNeural", "en-PH-RosaNeural",
        "en-SG-LunaNeural", "en-SG-WayneNeural", "en-TZ-ElimuNeural", "en-TZ-ImaniNeural",
        "en-US-AnaNeural", "en-US-AndrewNeural", "en-US-AriaNeural", "en-US-AvaNeural",
        "en-US-BrianNeural", "en-US-ChristopherNeural", "en-US-EmmaNeural", "en-US-EricNeural",
        "en-US-GuyNeural", "en-US-JennyNeural", "en-US-MichelleNeural", "en-US-RogerNeural",
        "en-US-SteffanNeural", "en-ZA-LeahNeural", "en-ZA-LukeNeural", "es-AR-ElenaNeural",
        "es-AR-TomasNeural", "es-BO-MarceloNeural", "es-BO-SofiaNeural", "es-CL-CatalinaNeural",
        "es-CL-LorenzoNeural", "es-CO-GonzaloNeural", "es-CO-SalomeNeural", "es-CR-JuanNeural",
        "es-CR-MariaNeural", "es-CU-BelkysNeural", "es-CU-ManuelNeural", "es-DO-EmilioNeural",
        "es-DO-RamonaNeural", "es-EC-AndreaNeural", "es-EC-LuisNeural", "es-ES-AlvaroNeural",
        "es-ES-ElviraNeural", "es-ES-XimenaNeural", "es-GQ-JavierNeural", "es-GQ-TeresaNeural",
        "es-GT-AndresNeural", "es-GT-MartaNeural", "es-HN-CarlosNeural", "es-HN-KarlaNeural",
        "es-MX-DaliaNeural", "es-MX-JorgeNeural", "es-NI-FedericoNeural", "es-NI-YolandaNeural",
        "es-PA-MargaritaNeural", "es-PA-RobertoNeural", "es-PE-AlexNeural", "es-PE-CamilaNeural",
        "es-PR-KarinaNeural", "es-PR-VictorNeural", "es-PY-MarioNeural", "es-PY-TaniaNeural",
        "es-SV-LorenaNeural", "es-SV-RodrigoNeural", "es-US-AlonsoNeural", "es-US-PalomaNeural",
        "es-UY-MateoNeural", "es-UY-ValentinaNeural", "es-VE-PaolaNeural", "es-VE-SebastianNeural",
        "et-EE-AnuNeural", "et-EE-KertNeural", "fa-IR-DilaraNeural", "fa-IR-FaridNeural",
        "fi-FI-HarriNeural", "fi-FI-NooraNeural", "fil-PH-AngeloNeural", "fil-PH-BlessicaNeural",
        "fr-BE-CharlineNeural", "fr-BE-GerardNeural", "fr-CA-AntoineNeural", "fr-CA-JeanNeural",
        "fr-CA-SylvieNeural", "fr-CA-ThierryNeural", "fr-CH-ArianeNeural", "fr-CH-FabriceNeural",
        "fr-FR-DeniseNeural", "fr-FR-EloiseNeural", "fr-FR-HenriNeural", "ga-IE-ColmNeural",
        "ga-IE-OrlaNeural", "gl-ES-RoiNeural", "gl-ES-SabelaNeural", "gu-IN-DhwaniNeural",
        "gu-IN-NiranjanNeural", "he-IL-AvriNeural", "he-IL-HilaNeural", "hi-IN-MadhurNeural",
        "hi-IN-SwaraNeural", "hr-HR-GabrijelaNeural", "hr-HR-SreckoNeural", "hu-HU-NoemiNeural",
        "hu-HU-TamasNeural", "id-ID-ArdiNeural", "id-ID-GadisNeural", "is-IS-GudrunNeural",
        "is-IS-GunnarNeural", "it-IT-DiegoNeural", "it-IT-ElsaNeural", "it-IT-GiuseppeNeural",
        "it-IT-IsabellaNeural", "ja-JP-KeitaNeural", "ja-JP-NanamiNeural", "jv-ID-DimasNeural",
        "jv-ID-SitiNeural", "ka-GE-EkaNeural", "ka-GE-GiorgiNeural", "kk-KZ-AigulNeural",
        "kk-KZ-DauletNeural", "km-KH-PisethNeural", "km-KH-SreymomNeural", "kn-IN-GaganNeural",
        "kn-IN-SapnaNeural", "ko-KR-HyunsuNeural", "ko-KR-InJoonNeural", "ko-KR-SunHiNeural",
        "lo-LA-ChanthavongNeural", "lo-LA-KeomanyNeural", "lt-LT-LeonasNeural", "lt-LT-OnaNeural",
        "lv-LV-EveritaNeural", "lv-LV-NilsNeural", "mk-MK-AleksandarNeural", "mk-MK-MarijaNeural",
        "ml-IN-MidhunNeural", "ml-IN-SobhanaNeural", "mn-MN-BataaNeural", "mn-MN-YesuiNeural",
        "mr-IN-AarohiNeural", "mr-IN-ManoharNeural", "ms-MY-OsmanNeural", "ms-MY-YasminNeural",
        "mt-MT-GraceNeural", "mt-MT-JosephNeural", "my-MM-NilarNeural", "my-MM-ThihaNeural",
        "nb-NO-FinnNeural", "nb-NO-PernilleNeural", "ne-NP-HemkalaNeural", "ne-NP-SagarNeural",
        "nl-BE-ArnaudNeural", "nl-BE-DenaNeural", "nl-NL-ColetteNeural", "nl-NL-FennaNeural",
        "nl-NL-MaartenNeural", "pl-PL-MarekNeural", "pl-PL-ZofiaNeural", "ps-AF-GulNawazNeural",
        "ps-AF-LatifaNeural", "pt-BR-AntonioNeural", "pt-BR-FranciscaNeural", "pt-BR-ThalitaNeural",
        "pt-PT-DuarteNeural", "pt-PT-RaquelNeural", "ro-RO-AlinaNeural", "ro-RO-EmilNeural",
        "ru-RU-DmitryNeural", "ru-RU-SvetlanaNeural", "si-LK-SameeraNeural", "si-LK-ThiliniNeural",
        "sk-SK-LukasNeural", "sk-SK-ViktoriaNeural", "sl-SI-PetraNeural", "sl-SI-RokNeural",
        "so-SO-MuuseNeural", "so-SO-UbaxNeural", "sq-AL-AnilaNeural", "sq-AL-IlirNeural",
        "sr-RS-NicholasNeural", "sr-RS-SophieNeural", "su-ID-JajangNeural", "su-ID-TutiNeural",
        "sv-SE-MattiasNeural", "sv-SE-SofieNeural", "sw-KE-RafikiNeural", "sw-KE-ZuriNeural",
        "sw-TZ-DaudiNeural", "sw-TZ-RehemaNeural", "ta-IN-PallaviNeural", "ta-IN-ValluvarNeural",
        "ta-LK-KumarNeural", "ta-LK-SaranyaNeural", "ta-MY-KaniNeural", "ta-MY-SuryaNeural",
        "ta-SG-AnbuNeural", "ta-SG-VenbaNeural", "te-IN-MohanNeural", "te-IN-ShrutiNeural",
        "th-TH-NiwatNeural", "th-TH-PremwadeeNeural", "tr-TR-AhmetNeural", "tr-TR-EmelNeural",
        "uk-UA-OstapNeural", "uk-UA-PolinaNeural", "ur-IN-GulNeural", "ur-IN-SalmanNeural",
        "ur-PK-AsadNeural", "ur-PK-UzmaNeural", "uz-UZ-MadinaNeural", "uz-UZ-SardorNeural",
        "vi-VN-HoaiMyNeural", "vi-VN-NamMinhNeural", "zh-CN-XiaoxiaoNeural", "zh-CN-XiaoyiNeural",
        "zh-CN-YunjianNeural", "zh-CN-YunxiNeural", "zh-CN-YunxiaNeural", "zh-CN-YunyangNeural",
        "zh-CN-liaoning-XiaobeiNeural", "zh-CN-shaanxi-XiaoniNeural", "zh-HK-HiuGaaiNeural",
        "zh-HK-HiuMaanNeural", "zh-HK-WanLungNeural", "zh-TW-HsiaoChenNeural", "zh-TW-HsiaoYuNeural",
        "zh-TW-YunJheNeural", "zu-ZA-ThandoNeural", "zu-ZA-ThembaNeural"
    ]
    if requested_voice.lower() == "male":
        return default_male
    elif requested_voice.lower() == "female":
        return default_female
    elif requested_voice in ["alloy", "echo", "fable", "onyx"]:
        # 这些是OpenAI的男声，我们用默认男声替代
        return default_male
    elif requested_voice in ["nova", "shimmer"]:
        # 这些是OpenAI的女声，我们用默认女声替代
        return default_female
    elif requested_voice in valid_voices:
        # 这些是Edge-tts的有效音色
        return requested_voice
    else:
        # 如果不在有效列表中，使用默认女声
        return default_female