from django.db.models import TextChoices


class CurrencyChoices(TextChoices):
    SAR = ("SAR", "SAR")
    USD = ("USD", "USD")
    CAD = ("CAD", "CAD")
    NGN = ("NGN", "NGN")


class PaymentPlans(TextChoices):
    BASIC = ("BASIC", "BASIC")
    PRO = ("PRO", "PRO")
    PREMIUM = ("PREMIUM", "PREMIUM")


class FreeModeChoices(TextChoices):
    ACTIVE = ("ACTIVE", "ACTIVE")
    EXPIRED = ("EXPIRED", "EXPIRED")
    NOT_USED = ("NOT_USED", "NOT_USED")


class PaymentStatus(TextChoices):
    INITIATED = ("initiated", "initiated")
    PAID = ("paid", "paid")
    REFUNDED = ("refunded", "refunded")
    VOIDED = ("voided", "voided")


class TaskLiterals(TextChoices):
    TRANSLATE = ("translate", "translate")
    TRANSCRIBE = ("transcribe", "transcribe")


class LanguageChoices(TextChoices):
    AFRIKAANS = "af", "Afrikaans"
    ARABIC = "ar", "Arabic"
    ARMENIAN = "hy", "Armenian"
    AZERBAIJANI = "az", "Azerbaijani"
    BELARUSIAN = "be", "Belarusian"
    BOSNIAN = "bs", "Bosnian"
    BULGARIAN = "bg", "Bulgarian"
    CATALAN = "ca", "Catalan"
    CHINESE = "zh", "Chinese"
    CROATIAN = "hr", "Croatian"
    CZECH = "cs", "Czech"
    DANISH = "da", "Danish"
    DUTCH = "nl", "Dutch"
    ENGLISH = "en", "English"
    ESTONIAN = "et", "Estonian"
    FINNISH = "fi", "Finnish"
    FRENCH = "fr", "French"
    GALICIAN = "gl", "Galician"
    GERMAN = "de", "German"
    GREEK = "el", "Greek"
    HEBREW = "he", "Hebrew"
    HINDI = "hi", "Hindi"
    HUNGARIAN = "hu", "Hungarian"
    ICELANDIC = "is", "Icelandic"
    INDONESIAN = "id", "Indonesian"
    ITALIAN = "it", "Italian"
    JAPANESE = "ja", "Japanese"
    KANNADA = "kn", "Kannada"
    KAZAKH = "kk", "Kazakh"
    KOREAN = "ko", "Korean"
    LATVIAN = "lv", "Latvian"
    LITHUANIAN = "lt", "Lithuanian"
    MACEDONIAN = "mk", "Macedonian"
    MALAY = "ms", "Malay"
    MARATHI = "mr", "Marathi"
    MAORI = "mi", "Maori"
    NEPALI = "ne", "Nepali"
    NORWEGIAN = "no", "Norwegian"
    PERSIAN = "fa", "Persian"
    POLISH = "pl", "Polish"
    PORTUGUESE = "pt", "Portuguese"
    ROMANIAN = "ro", "Romanian"
    RUSSIAN = "ru", "Russian"
    SERBIAN = "sr", "Serbian"
    SLOVAK = "sk", "Slovak"
    SLOVENIAN = "sl", "Slovenian"
    SPANISH = "es", "Spanish"
    SWAHILI = "sw", "Swahili"
    SWEDISH = "sv", "Swedish"
    TAGALOG = "tl", "Tagalog"
    TAMIL = "ta", "Tamil"
    THAI = "th", "Thai"
    TURKISH = "tr", "Turkish"
    UKRAINIAN = "uk", "Ukrainian"
    URDU = "ur", "Urdu"
    VIETNAMESE = "vi", "Vietnamese"
    WELSH = "cy", "Welsh"
    OTHERS = "ot", "Others"
