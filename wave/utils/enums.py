from typing import Literal, TypedDict

from django.db.models import TextChoices


class CurrencyChoices(TextChoices):
    SAR = ("SAR", "SAR")
    USD = ("USD", "USD")
    # CAD = ("CAD", "CAD")
    # NGN = ("NGN", "NGN")


class PaymentPlans(TextChoices):
    FREE = ("FREE", "FREE")
    BASIC = ("BASIC", "BASIC")
    PREMIUM = ("PREMIUM", "PREMIUM")
    CUSTOM = ("CUSTOM", "CUSTOM")


class PaymentPlanDurationChoices(TextChoices):
    DEFAULT = ("DEFAULT", "DEFAULT")
    ONE_MONTH = ("ONE_MONTH", "ONE_MONTH")
    ONE_YEAR = ("ONE_YEAR", "ONE_YEAR")


class PaymentSubscriptionStatus(TextChoices):
    NONE = ("NONE", "NONE")
    ACTIVE = ("ACTIVE", "ACTIVE")
    EXPIRED = ("EXPIRED", "EXPIRED")


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
    ARABIC_SA = "ar-SA", "(Arabic) Saudi Arabia"
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
    ENGLISH_US = "en-US", "English"
    ENGLISH_GB = "en-GB", "English"
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


class FromLanguages(TextChoices):
    AF_ZA = ("af-ZA", "Afrikaans (South Africa)")
    AM_ET = ("am-ET", "Amharic (Ethiopia)")
    AR_AE = ("ar-AE", "Arabic (United Arab Emirates)")
    AR_BH = ("ar-BH", "Arabic (Bahrain)")
    AR_DZ = ("ar-DZ", "Arabic (Algeria)")
    AR_EG = ("ar-EG", "Arabic (Egypt)")
    AR_IL = ("ar-IL", "Arabic (Israel)")
    AR_IQ = ("ar-IQ", "Arabic (Iraq)")
    AR_JO = ("ar-JO", "Arabic (Jordan)")
    AR_KW = ("ar-KW", "Arabic (Kuwait)")
    AR_LB = ("ar-LB", "Arabic (Lebanon)")
    AR_LY = ("ar-LY", "Arabic (Libya)")
    AR_MA = ("ar-MA", "Arabic (Morocco)")
    AR_OM = ("ar-OM", "Arabic (Oman)")
    AR_PS = ("ar-PS", "Arabic (Palestinian Authority)")
    AR_QA = ("ar-QA", "Arabic (Qatar)")
    AR_SA = ("ar-SA", "Arabic (Saudi Arabia)")
    AR_SY = ("ar-SY", "Arabic (Syria)")
    AR_TN = ("ar-TN", "Arabic (Tunisia)")
    AR_YE = ("ar-YE", "Arabic (Yemen)")
    AZ_AZ = ("az-AZ", "Azerbaijani (Latin, Azerbaijan)")
    BG_BG = ("bg-BG", "Bulgarian (Bulgaria)")
    BN_IN = ("bn-IN", "Bengali (India)")
    BS_BA = ("bs-BA", "Bosnian (Bosnia and Herzegovina)")
    CA_ES = ("ca-ES", "Catalan")
    CS_CZ = ("cs-CZ", "Czech (Czechia)")
    CY_GB = ("cy-GB", "Welsh (United Kingdom)")
    DA_DK = ("da-DK", "Danish (Denmark)")
    DE_AT = ("de-AT", "German (Austria)")
    DE_CH = ("de-CH", "German (Switzerland)")
    DE_DE = ("de-DE", "German (Germany)")
    EL_GR = ("el-GR", "Greek (Greece)")
    EN_AU = ("en-AU", "English (Australia)")
    EN_CA = ("en-CA", "English (Canada)")
    EN_GB = ("en-GB", "English (United Kingdom)")
    EN_GH = ("en-GH", "English (Ghana)")
    EN_HK = ("en-HK", "English (Hong Kong SAR)")
    EN_IE = ("en-IE", "English (Ireland)")
    EN_IN = ("en-IN", "English (India)")
    EN_KE = ("en-KE", "English (Kenya)")
    EN_NG = ("en-NG", "English (Nigeria)")
    EN_NZ = ("en-NZ", "English (New Zealand)")
    EN_PH = ("en-PH", "English (Philippines)")
    EN_SG = ("en-SG", "English (Singapore)")
    EN_TZ = ("en-TZ", "English (Tanzania)")
    EN_US = ("en-US", "English (United States)")
    EN_ZA = ("en-ZA", "English (South Africa)")
    ES_AR = ("es-AR", "Spanish (Argentina)")
    ES_BO = ("es-BO", "Spanish (Bolivia)")
    ES_CL = ("es-CL", "Spanish (Chile)")
    ES_CO = ("es-CO", "Spanish (Colombia)")
    ES_CR = ("es-CR", "Spanish (Costa Rica)")
    ES_CU = ("es-CU", "Spanish (Cuba)")
    ES_DO = ("es-DO", "Spanish (Dominican Republic)")
    ES_EC = ("es-EC", "Spanish (Ecuador)")
    ES_ES = ("es-ES", "Spanish (Spain)")
    ES_GQ = ("es-GQ", "Spanish (Equatorial Guinea)")
    ES_GT = ("es-GT", "Spanish (Guatemala)")
    ES_HN = ("es-HN", "Spanish (Honduras)")
    ES_MX = ("es-MX", "Spanish (Mexico)")
    ES_NI = ("es-NI", "Spanish (Nicaragua)")
    ES_PA = ("es-PA", "Spanish (Panama)")
    ES_PE = ("es-PE", "Spanish (Peru)")
    ES_PR = ("es-PR", "Spanish (Puerto Rico)")
    ES_PY = ("es-PY", "Spanish (Paraguay)")
    ES_SV = ("es-SV", "Spanish (El Salvador)")
    ES_US = ("es-US", "Spanish (United States)")
    ES_UY = ("es-UY", "Spanish (Uruguay)")
    ES_VE = ("es-VE", "Spanish (Venezuela)")
    ET_EE = ("et-EE", "Estonian (Estonia)")
    EU_ES = ("eu-ES", "Basque")
    FA_IR = ("fa-IR", "Persian (Iran)")
    FI_FI = ("fi-FI", "Finnish (Finland)")
    FIL_PH = ("fil-PH", "Filipino (Philippines)")
    FR_BE = ("fr-BE", "French (Belgium)")
    FR_CA = ("fr-CA", "French (Canada)")
    FR_CH = ("fr-CH", "French (Switzerland)")
    FR_FR = ("fr-FR", "French (France)")
    GA_IE = ("ga-IE", "Irish (Ireland)")
    GL_ES = ("gl-ES", "Galician")
    GU_IN = ("gu-IN", "Gujarati (India)")
    HE_IL = ("he-IL", "Hebrew (Israel)")
    HI_IN = ("hi-IN", "Hindi (India)")
    HR_HR = ("hr-HR", "Croatian (Croatia)")
    HU_HU = ("hu-HU", "Hungarian (Hungary)")
    HY_AM = ("hy-AM", "Armenian (Armenia)")
    ID_ID = ("id-ID", "Indonesian (Indonesia)")
    IS_IS = ("is-IS", "Icelandic (Iceland)")
    IT_CH = ("it-CH", "Italian (Switzerland)")
    IT_IT = ("it-IT", "Italian (Italy)")
    JA_JP = ("ja-JP", "Japanese (Japan)")
    JV_ID = ("jv-ID", "Javanese (Latin, Indonesia)")
    KA_GE = ("ka-GE", "Georgian (Georgia)")
    KK_KZ = ("kk-KZ", "Kazakh (Kazakhstan)")
    KM_KH = ("km-KH", "Khmer (Cambodia)")
    KN_IN = ("kn-IN", "Kannada (India)")
    KO_KR = ("ko-KR", "Korean (Korea)")
    LO_LA = ("lo-LA", "Lao (Laos)")
    LT_LT = ("lt-LT", "Lithuanian (Lithuania)")
    LV_LV = ("lv-LV", "Latvian (Latvia)")
    MK_MK = ("mk-MK", "Macedonian (North Macedonia)")
    ML_IN = ("ml-IN", "Malayalam (India)")
    MN_MN = ("mn-MN", "Mongolian (Mongolia)")
    MR_IN = ("mr-IN", "Marathi (India)")
    MS_MY = ("ms-MY", "Malay (Malaysia)")
    MT_MT = ("mt-MT", "Maltese (Malta)")
    MY_MM = ("my-MM", "Burmese (Myanmar)")
    NB_NO = ("nb-NO", "Norwegian Bokmål (Norway)")
    NE_NP = ("ne-NP", "Nepali (Nepal)")
    NL_BE = ("nl-BE", "Dutch (Belgium)")
    NL_NL = ("nl-NL", "Dutch (Netherlands)")
    PA_IN = ("pa-IN", "Punjabi (India)")
    PL_PL = ("pl-PL", "Polish (Poland)")
    PS_AF = ("ps-AF", "Pashto (Afghanistan)")
    PT_BR = ("pt-BR", "Portuguese (Brazil)")
    PT_PT = ("pt-PT", "Portuguese (Portugal)")
    RO_RO = ("ro-RO", "Romanian (Romania)")
    RU_RU = ("ru-RU", "Russian (Russia)")
    SI_LK = ("si-LK", "Sinhala (Sri Lanka)")
    SK_SK = ("sk-SK", "Slovak (Slovakia)")
    SL_SI = ("sl-SI", "Slovenian (Slovenia)")
    SO_SO = ("so-SO", "Somali (Somalia)")
    SQ_AL = ("sq-AL", "Albanian (Albania)")
    SR_RS = ("sr-RS", "Serbian (Cyrillic, Serbia)")
    SV_SE = ("sv-SE", "Swedish (Sweden)")
    SW_KE = ("sw-KE", "Swahili (Kenya)")
    SW_TZ = ("sw-TZ", "Swahili (Tanzania)")
    TA_IN = ("ta-IN", "Tamil (India)")
    TE_IN = ("te-IN", "Telugu (India)")
    TH_TH = ("th-TH", "Thai (Thailand)")
    TR_TR = ("tr-TR", "Turkish (Türkiye)")
    UK_UA = ("uk-UA", "Ukrainian (Ukraine)")
    UR_IN = ("ur-IN", "Urdu (India)")
    UZ_UZ = ("uz-UZ", "Uzbek (Latin, Uzbekistan)")
    VI_VN = ("vi-VN", "Vietnamese (Vietnam)")
    WUU_CN = ("wuu-CN", "Chinese (Wu, Simplified)")
    YUE_CN = ("yue-CN", "Chinese (Cantonese, Simplified)")
    ZH_CN = ("zh-CN", "Chinese (Mandarin, Simplified)")
    ZH_CN_SHANDONG = ("zh-CN-shandong", "Chinese (Jilu Mandarin, Simplified)")
    ZH_CN_SICHUAN = ("zh-CN-sichuan", "Chinese (Southwestern Mandarin, Simplified)")
    ZH_HK = ("zh-HK", "Chinese (Cantonese, Traditional)")
    ZH_TW = ("zh-TW", "Chinese (Taiwanese Mandarin, Traditional)")
    ZU_ZA = ("zu-ZA", "Zulu (South Africa)")
    OTHERS = ("ot", "Others")


class ToLanguages(TextChoices):
    AFRIKAANS = "af", "Afrikaans"
    ALBANIAN = "sq", "Albanian"
    AMHARIC = "am", "Amharic"
    ARABIC = "ar", "Arabic"
    ARMENIAN = "hy", "Armenian"
    ASSAMESE = "as", "Assamese"
    AZERBAIJANI = "az", "Azerbaijani"
    BANGLA = "bn", "Bangla"
    BOSNIAN_LATIN = "bs", "Bosnian (Latin)"
    BULGARIAN = "bg", "Bulgarian"
    CANTONESE_TRADITIONAL = "yue", "Cantonese (Traditional)"
    CATALAN = "ca", "Catalan"
    CHINESE_LITERARY = "lzh", "Chinese (Literary)"
    CHINESE_SIMPLIFIED = "zh-Hans", "Chinese Simplified"
    CHINESE_TRADITIONAL = "zh-Hant", "Chinese Traditional"
    CROATIAN = "hr", "Croatian"
    CZECH = "cs", "Czech"
    DANISH = "da", "Danish"
    DARI = "prs", "Dari"
    DUTCH = "nl", "Dutch"
    ENGLISH = "en", "English"
    ESTONIAN = "et", "Estonian"
    FIJIAN = "fj", "Fijian"
    FILIPINO = "fil", "Filipino"
    FINNISH = "fi", "Finnish"
    FRENCH = "fr", "French"
    FRENCH_CANADA = "fr-ca", "French (Canada)"
    GERMAN = "de", "German"
    GREEK = "el", "Greek"
    GUJARATI = "gu", "Gujarati"
    HAITIAN_CREOLE = "ht", "Haitian Creole"
    HEBREW = "he", "Hebrew"
    HINDI = "hi", "Hindi"
    HMONG_DAW = "mww", "Hmong Daw"
    HUNGARIAN = "hu", "Hungarian"
    ICELANDIC = "is", "Icelandic"
    INDONESIAN = "id", "Indonesian"
    INUKTITUT = "iu", "Inuktitut"
    IRISH = "ga", "Irish"
    ITALIAN = "it", "Italian"
    JAPANESE = "ja", "Japanese"
    KANNADA = "kn", "Kannada"
    KAZAKH = "kk", "Kazakh"
    KHMER = "km", "Khmer"
    KLINGON = "tlh-Latn", "Klingon"
    KLINGON_PLQAD = "tlh-Piqd", "Klingon (plqaD)"
    KOREAN = "ko", "Korean"
    KURDISH_CENTRAL = "ku", "Kurdish (Central)"
    KURDISH_NORTHERN = "kmr", "Kurdish (Northern)"
    LAO = "lo", "Lao"
    LATVIAN = "lv", "Latvian"
    LITHUANIAN = "lt", "Lithuanian"
    MALAGASY = "mg", "Malagasy"
    MALAY = "ms", "Malay"
    MALAYALAM = "ml", "Malayalam"
    MALTESE = "mt", "Maltese"
    MAORI = "mi", "Maori"
    MARATHI = "mr", "Marathi"
    MYANMAR = "my", "Myanmar"
    NEPALI = "ne", "Nepali"
    NORWEGIAN = "nb", "Norwegian"
    ODIA = "or", "Odia"
    PASHTO = "ps", "Pashto"
    PERSIAN = "fa", "Persian"
    POLISH = "pl", "Polish"
    PORTUGUESE_BRAZIL = "pt", "Portuguese (Brazil)"
    PORTUGUESE_PORTUGAL = "pt-pt", "Portuguese (Portugal)"
    PUNJABI = "pa", "Punjabi"
    QUERETARO_OTOMI = "otq", "Queretaro Otomi"
    ROMANIAN = "ro", "Romanian"
    RUSSIAN = "ru", "Russian"
    SAMOAN = "sm", "Samoan"
    SERBIAN_CYRILLIC = "sr-Cyrl", "Serbian (Cyrillic)"
    SERBIAN_LATIN = "sr-Latn", "Serbian (Latin)"
    SLOVAK = "sk", "Slovak"
    SLOVENIAN = "sl", "Slovenian"
    SPANISH = "es", "Spanish"
    SWAHILI = "sw", "Swahili"
    SWEDISH = "sv", "Swedish"
    TAHITIAN = "ty", "Tahitian"
    TAMIL = "ta", "Tamil"
    TELUGU = "te", "Telugu"
    THAI = "th", "Thai"
    TIGRINYA = "ti", "Tigrinya"
    TONGAN = "to", "Tongan"
    TURKISH = "tr", "Turkish"
    UKRAINIAN = "uk", "Ukrainian"
    URDU = "ur", "Urdu"
    VIETNAMESE = "vi", "Vietnamese"
    WELSH = "cy", "Welsh"
    YUCATEC_MAYA = "yua", "Yucatec Maya"
    OTHERS = ("ot", "Others")


class CountryEnum(TextChoices):
    AF = ("https://flagcdn.com/w320/af.png", "+93")
    AX = ("https://flagcdn.com/w320/ax.png", "+358")
    AL = ("https://flagcdn.com/w320/al.png", "+355")
    DZ = ("https://flagcdn.com/w320/dz.png", "+213")
    AS = ("https://flagcdn.com/w320/as.png", "+1-684")
    AD = ("https://flagcdn.com/w320/ad.png", "+376")
    AO = ("https://flagcdn.com/w320/ao.png", "+244")
    AI = ("https://flagcdn.com/w320/ai.png", "+1-264")
    # AQ = ('https://flagcdn.com/w320/aq.png', None)
    AG = ("https://flagcdn.com/w320/ag.png", "+1-268")
    AR = ("https://flagcdn.com/w320/ar.png", "+54")
    AM = ("https://flagcdn.com/w320/am.png", "+374")
    AW = ("https://flagcdn.com/w320/aw.png", "+297")
    AU = ("https://flagcdn.com/w320/au.png", "+61")
    AT = ("https://flagcdn.com/w320/at.png", "+43")
    AZ = ("https://flagcdn.com/w320/az.png", "+994")
    BS = ("https://flagcdn.com/w320/bs.png", "+1-242")
    BH = ("https://flagcdn.com/w320/bh.png", "+973")
    BD = ("https://flagcdn.com/w320/bd.png", "+880")
    BB = ("https://flagcdn.com/w320/bb.png", "+1-246")
    BY = ("https://flagcdn.com/w320/by.png", "+375")
    BE = ("https://flagcdn.com/w320/be.png", "+32")
    BZ = ("https://flagcdn.com/w320/bz.png", "+501")
    BJ = ("https://flagcdn.com/w320/bj.png", "+229")
    BM = ("https://flagcdn.com/w320/bm.png", "+1-441")
    BT = ("https://flagcdn.com/w320/bt.png", "+975")
    BO = ("https://flagcdn.com/w320/bo.png", "+591")
    BA = ("https://flagcdn.com/w320/ba.png", "+387")
    BW = ("https://flagcdn.com/w320/bw.png", "+267")
    # BV = ('https://flagcdn.com/w320/bv.png', None)
    BR = ("https://flagcdn.com/w320/br.png", "+55")
    IO = ("https://flagcdn.com/w320/io.png", "+246")
    BN = ("https://flagcdn.com/w320/bn.png", "+673")
    BG = ("https://flagcdn.com/w320/bg.png", "+359")
    BF = ("https://flagcdn.com/w320/bf.png", "+226")
    BI = ("https://flagcdn.com/w320/bi.png", "+257")
    CV = ("https://flagcdn.com/w320/cv.png", "+238")
    KH = ("https://flagcdn.com/w320/kh.png", "+855")
    CM = ("https://flagcdn.com/w320/cm.png", "+237")
    CA = ("https://flagcdn.com/w320/ca.png", "+1")
    KY = ("https://flagcdn.com/w320/ky.png", "+1-345")
    CF = ("https://flagcdn.com/w320/cf.png", "+236")
    TD = ("https://flagcdn.com/w320/td.png", "+235")
    CL = ("https://flagcdn.com/w320/cn.png", "+86")
    CX = ("https://flagcdn.com/w320/cx.png", "+61")
    CC = ("https://flagcdn.com/w320/cc.png", "+61")
    CO = ("https://flagcdn.com/w320/co.png", "+57")
    KM = ("https://flagcdn.com/w320/km.png", "+269")
    CG = ("https://flagcdn.com/w320/cg.png", "+242")
    CD = ("https://flagcdn.com/w320/cd.png", "+243")
    CK = ("https://flagcdn.com/w320/ck.png", "+682")
    CR = ("https://flagcdn.com/w320/cr.png", "+506")
    HR = ("https://flagcdn.com/w320/hr.png", "+385")
    CU = ("https://flagcdn.com/w320/cu.png", "+53")
    CY = ("https://flagcdn.com/w320/cy.png", "+357")
    CZ = ("https://flagcdn.com/w320/cz.png", "+420")
    DK = ("https://flagcdn.com/w320/dk.png", "+45")
    DJ = ("https://flagcdn.com/w320/dj.png", "+253")
    DM = ("https://flagcdn.com/w320/dm.png", "+1-767")
    DO = ("https://flagcdn.com/w320/do.png", "+1-809")
    EC = ("https://flagcdn.com/w320/ec.png", "+593")
    EG = ("https://flagcdn.com/w320/eg.png", "+20")
    SV = ("https://flagcdn.com/w320/sv.png", "+503")
    GQ = ("https://flagcdn.com/w320/gq.png", "+240")
    ER = ("https://flagcdn.com/w320/er.png", "+291")
    EE = ("https://flagcdn.com/w320/ee.png", "+372")
    ET = ("https://flagcdn.com/w320/et.png", "+251")
    FK = ("https://flagcdn.com/w320/fk.png", "+500")
    FO = ("https://flagcdn.com/w320/fo.png", "+298")
    FJ = ("https://flagcdn.com/w320/fj.png", "+679")
    FI = ("https://flagcdn.com/w320/fi.png", "+358")
    FR = ("https://flagcdn.com/w320/fr.png", "+33")
    GF = ("https://flagcdn.com/w320/gf.png", "+594")
    PF = ("https://flagcdn.com/w320/pf.png", "+689")
    # TF = ('https://flagcdn.com/w320/tf.png', None)
    GA = ("https://flagcdn.com/w320/ga.png", "+241")
    GM = ("https://flagcdn.com/w320/gm.png", "+220")
    GE = ("https://flagcdn.com/w320/ge.png", "+995")
    DE = ("https://flagcdn.com/w320/de.png", "+49")
    GH = ("https://flagcdn.com/w320/gh.png", "+233")
    GI = ("https://flagcdn.com/w320/gi.png", "+350")
    GR = ("https://flagcdn.com/w320/gr.png", "+30")
    GL = ("https://flagcdn.com/w320/gl.png", "+299")
    GD = ("https://flagcdn.com/w320/gd.png", "+1-473")
    GP = ("https://flagcdn.com/w320/gp.png", "+590")
    GU = ("https://flagcdn.com/w320/gu.png", "+1-671")
    GT = ("https://flagcdn.com/w320/gt.png", "+502")
    GG = ("https://flagcdn.com/w320/gg.png", "+44")
    GN = ("https://flagcdn.com/w320/gn.png", "+224")
    GW = ("https://flagcdn.com/w320/gw.png", "+245")
    GY = ("https://flagcdn.com/w320/gy.png", "+592")
    HT = ("https://flagcdn.com/w320/ht.png", "+509")
    # HM = (None, 'https://flagcdn.com/w320/hm.png')
    VA = ("https://flagcdn.com/w320/va.png", "+379")
    HN = ("https://flagcdn.com/w320/hn.png", "+504")
    HK = ("https://flagcdn.com/w320/hk.png", "+852")
    HU = ("https://flagcdn.com/w320/hu.png", "+36")
    IS = ("https://flagcdn.com/w320/is.png", "+354")
    IN = ("https://flagcdn.com/w320/in.png", "+91")
    ID = ("https://flagcdn.com/w320/id.png", "+62")
    IR = ("https://flagcdn.com/w320/ir.png", "+98")
    IQ = ("https://flagcdn.com/w320/iq.png", "+964")
    IE = ("https://flagcdn.com/w320/ie.png", "+353")
    IM = ("https://flagcdn.com/w320/im.png", "+44")
    IL = ("https://flagcdn.com/w320/il.png", "+972")
    IT = ("https://flagcdn.com/w320/it.png", "+39")
    JM = ("https://flagcdn.com/w320/jm.png", "+1-876")
    JP = ("https://flagcdn.com/w320/jp.png", "+81")
    JE = ("https://flagcdn.com/w320/je.png", "+44")
    JO = ("https://flagcdn.com/w320/jo.png", "+962")
    KZ = ("https://flagcdn.com/w320/kz.png", "+7")
    KE = ("https://flagcdn.com/w320/ke.png", "+254")
    KI = ("https://flagcdn.com/w320/ki.png", "+686")
    KP = ("https://flagcdn.com/w320/kp.png", "+850")
    KR = ("https://flagcdn.com/w320/kr.png", "+82")
    KW = ("https://flagcdn.com/w320/kw.png", "+965")
    KG = ("https://flagcdn.com/w320/kg.png", "+996")
    LA = ("https://flagcdn.com/w320/la.png", "+856")
    LV = ("https://flagcdn.com/w320/lv.png", "+371")
    LB = ("https://flagcdn.com/w320/lb.png", "+961")
    LS = ("https://flagcdn.com/w320/ls.png", "+266")
    LR = ("https://flagcdn.com/w320/lr.png", "+231")
    LY = ("https://flagcdn.com/w320/ly.png", "+218")
    LI = ("https://flagcdn.com/w320/li.png", "+423")
    LT = ("https://flagcdn.com/w320/lt.png", "+370")
    LU = ("https://flagcdn.com/w320/lu.png", "+352")
    MO = ("https://flagcdn.com/w320/mo.png", "+853")
    MK = ("https://flagcdn.com/w320/mk.png", "+389")
    MG = ("https://flagcdn.com/w320/mg.png", "+261")
    MW = ("https://flagcdn.com/w320/mw.png", "+265")
    MY = ("https://flagcdn.com/w320/my.png", "+60")
    MV = ("https://flagcdn.com/w320/mv.png", "+960")
    ML = ("https://flagcdn.com/w320/ml.png", "+223")
    MT = ("https://flagcdn.com/w320/mt.png", "+356")
    MH = ("https://flagcdn.com/w320/mh.png", "+692")
    MQ = ("https://flagcdn.com/w320/mq.png", "+596")
    MR = ("https://flagcdn.com/w320/mr.png", "+222")
    MU = ("https://flagcdn.com/w320/mu.png", "+230")
    YT = ("https://flagcdn.com/w320/yt.png", "+262")
    MX = ("https://flagcdn.com/w320/mx.png", "+52")
    FM = ("https://flagcdn.com/w320/fm.png", "+691")
    MD = ("https://flagcdn.com/w320/md.png", "+373")
    MC = ("https://flagcdn.com/w320/mc.png", "+377")
    MN = ("https://flagcdn.com/w320/mn.png", "+976")
    ME = ("https://flagcdn.com/w320/me.png", "+382")
    MS = ("https://flagcdn.com/w320/ms.png", "+1-664")
    MA = ("https://flagcdn.com/w320/ma.png", "+212")
    MZ = ("https://flagcdn.com/w320/mz.png", "+258")
    MM = ("https://flagcdn.com/w320/mm.png", "+95")
    NA = ("https://flagcdn.com/w320/na.png", "+264")
    NR = ("https://flagcdn.com/w320/nr.png", "+674")
    NP = ("https://flagcdn.com/w320/np.png", "+977")
    NL = ("https://flagcdn.com/w320/nl.png", "+31")
    NC = ("https://flagcdn.com/w320/nc.png", "+687")
    NZ = ("https://flagcdn.com/w320/nz.png", "+64")
    NI = ("https://flagcdn.com/w320/ni.png", "+505")
    NE = ("https://flagcdn.com/w320/ne.png", "+227")
    NG = ("https://flagcdn.com/w320/ng.png", "+234")
    NU = ("https://flagcdn.com/w320/nu.png", "+683")
    NF = ("https://flagcdn.com/w320/nf.png", "+672")
    MP = ("https://flagcdn.com/w320/mp.png", "+1-670")
    NO = ("https://flagcdn.com/w320/no.png", "+47")
    OM = ("https://flagcdn.com/w320/om.png", "+968")
    PK = ("https://flagcdn.com/w320/pk.png", "+92")
    PW = ("https://flagcdn.com/w320/pw.png", "+680")
    PS = ("https://flagcdn.com/w320/ps.png", "+970")
    PA = ("https://flagcdn.com/w320/pa.png", "+507")
    PG = ("https://flagcdn.com/w320/pg.png", "+675")
    PY = ("https://flagcdn.com/w320/py.png", "+595")
    PE = ("https://flagcdn.com/w320/pe.png", "+51")
    PH = ("https://flagcdn.com/w320/ph.png", "+63")
    # PN = (None, 'https://flagcdn.com/w320/pn.png')
    PL = ("https://flagcdn.com/w320/pl.png", "+48")
    PT = ("https://flagcdn.com/w320/pt.png", "+351")
    PR = ("https://flagcdn.com/w320/pr.png", "+1-787")
    QA = ("https://flagcdn.com/w320/qa.png", "+974")
    RE = ("https://flagcdn.com/w320/re.png", "+262")
    RO = ("https://flagcdn.com/w320/ro.png", "+40")
    RU = ("https://flagcdn.com/w320/ru.png", "+7")
    RW = ("https://flagcdn.com/w320/rw.png", "+250")
    BL = ("https://flagcdn.com/w320/bl.png", "+590")
    SH = ("https://flagcdn.com/w320/sh.png", "+290")
    KN = ("https://flagcdn.com/w320/kn.png", "+1-869")
    LC = ("https://flagcdn.com/w320/lc.png", "+1-758")
    MF = ("https://flagcdn.com/w320/mf.png", "+590")
    PM = ("https://flagcdn.com/w320/pm.png", "+508")
    VC = ("https://flagcdn.com/w320/vc.png", "+1-784")
    WS = ("https://flagcdn.com/w320/ws.png", "+685")
    SM = ("https://flagcdn.com/w320/sm.png", "+378")
    ST = ("https://flagcdn.com/w320/st.png", "+239")
    SA = ("https://flagcdn.com/w320/sa.png", "+966")
    SN = ("https://flagcdn.com/w320/sn.png", "+221")
    RS = ("https://flagcdn.com/w320/rs.png", "+381")
    SC = ("https://flagcdn.com/w320/sc.png", "+248")
    SL = ("https://flagcdn.com/w320/sl.png", "+232")
    SG = ("https://flagcdn.com/w320/sg.png", "+65")
    SX = ("https://flagcdn.com/w320/sx.png", "+1-721")
    SK = ("https://flagcdn.com/w320/sk.png", "+421")
    SI = ("https://flagcdn.com/w320/si.png", "+386")
    SB = ("https://flagcdn.com/w320/sb.png", "+677")
    SO = ("https://flagcdn.com/w320/so.png", "+252")
    ZA = ("https://flagcdn.com/w320/za.png", "+27")
    # GS = (None, 'https://flagcdn.com/w320/gs.png')
    SS = ("https://flagcdn.com/w320/ss.png", "+211")
    ES = ("https://flagcdn.com/w320/es.png", "+34")
    LK = ("https://flagcdn.com/w320/lk.png", "+94")
    SD = ("https://flagcdn.com/w320/sd.png", "+249")
    SR = ("https://flagcdn.com/w320/sr.png", "+597")
    SJ = ("https://flagcdn.com/w320/sj.png", "+47")
    SZ = ("https://flagcdn.com/w320/sz.png", "+268")
    SE = ("https://flagcdn.com/w320/se.png", "+46")
    CH = ("https://flagcdn.com/w320/ch.png", "+41")
    SY = ("https://flagcdn.com/w320/sy.png", "+963")
    TW = ("https://flagcdn.com/w320/tw.png", "+886")
    TJ = ("https://flagcdn.com/w320/tj.png", "+992")
    TZ = ("https://flagcdn.com/w320/tz.png", "+255")
    TH = ("https://flagcdn.com/w320/th.png", "+66")
    TL = ("https://flagcdn.com/w320/tl.png", "+670")
    TG = ("https://flagcdn.com/w320/tg.png", "+228")
    TK = ("https://flagcdn.com/w320/tk.png", "+690")
    TO = ("https://flagcdn.com/w320/to.png", "+676")
    TT = ("https://flagcdn.com/w320/tt.png", "+1-868")
    TN = ("https://flagcdn.com/w320/tn.png", "+216")
    TR = ("https://flagcdn.com/w320/tr.png", "+90")
    TM = ("https://flagcdn.com/w320/tm.png", "+993")
    TC = ("https://flagcdn.com/w320/tc.png", "+1-649")
    TV = ("https://flagcdn.com/w320/tv.png", "+688")
    UG = ("https://flagcdn.com/w320/ug.png", "+256")
    UA = ("https://flagcdn.com/w320/ua.png", "+380")
    AE = ("https://flagcdn.com/w320/ae.png", "+971")
    GB = ("https://flagcdn.com/w320/gb.png", "+44")
    US = ("https://flagcdn.com/w320/us.png", "+1")
    # UM = (None, 'https://flagcdn.com/w320/um.png')
    UY = ("https://flagcdn.com/w320/uy.png", "+598")
    UZ = ("https://flagcdn.com/w320/uz.png", "+998")
    VU = ("https://flagcdn.com/w320/vu.png", "+678")
    VE = ("https://flagcdn.com/w320/ve.png", "+58")
    VN = ("https://flagcdn.com/w320/vn.png", "+84")
    VG = ("https://flagcdn.com/w320/vg.png", "+1-284")
    VI = ("https://flagcdn.com/w320/vi.png", "+1-340")
    WF = ("https://flagcdn.com/w320/wf.png", "+681")
    EH = ("https://flagcdn.com/w320/eh.png", "+212")
    YE = ("https://flagcdn.com/w320/ye.png", "+967")
    ZM = ("https://flagcdn.com/w320/zm.png", "+260")
    ZW = ("https://flagcdn.com/w320/zw.png", "+263")


CountryName = [
    ("AF", "Afghanistan"),
    ("AX", "Åland Islands"),
    ("AL", "Albania"),
    ("DZ", "Algeria"),
    ("AS", "American Samoa"),
    ("AD", "Andorra"),
    ("AO", "Angola"),
    ("AI", "Anguilla"),
    ("AQ", "Antarctica"),
    ("AG", "Antigua and Barbuda"),
    ("AR", "Argentina"),
    ("AM", "Armenia"),
    ("AW", "Aruba"),
    ("AU", "Australia"),
    ("AT", "Austria"),
    ("AZ", "Azerbaijan"),
    ("BS", "Bahamas"),
    ("BH", "Bahrain"),
    ("BD", "Bangladesh"),
    ("BB", "Barbados"),
    ("BY", "Belarus"),
    ("BE", "Belgium"),
    ("BZ", "Belize"),
    ("BJ", "Benin"),
    ("BM", "Bermuda"),
    (
        "BT",
        "Bhutan",
    ),
    (
        "BO",
        "Bolivia",
    ),
    ("BA", "Bosnia and Herzegovina"),
    (
        "BW",
        "Botswana",
    ),
    (
        "BV",
        "Bouvet Island",
    ),
    (
        "BR",
        "Brazil",
    ),
    (
        "IO",
        "British Indian Ocean Territory",
    ),
    (
        "BN",
        "Brunei Darussalam",
    ),
    (
        "BG",
        "Bulgaria",
    ),
    (
        "BF",
        "Burkina Faso",
    ),
    (
        "BI",
        "Burundi",
    ),
    (
        "CV",
        "Cabo Verde",
    ),
    (
        "KH",
        "Cambodia",
    ),
    (
        "CM",
        "Cameroon",
    ),
    (
        "CA",
        "Canada",
    ),
    (
        "KY",
        "Cayman Islands",
    ),
    (
        "CF",
        "Central African Republic",
    ),
    (
        "TD",
        "Chad",
    ),
    (
        "CL",
        "Chile",
    ),
    (
        "CN",
        "China",
    ),
    (
        "CX",
        "Christmas Island",
    ),
    (
        "CC",
        "Cocos (Keeling) Islands",
    ),
    ("CO", "Colombia"),
    ("KM", "Comoros"),
    ("CG", "Congo"),
    (
        "CD",
        "Congo, Democratic Republic",
    ),
    (
        "CK",
        "Cook Islands",
    ),
    (
        "CR",
        "Costa Rica",
    ),
    ("HR", "Croatia"),
    ("CU", "Cuba"),
    ("CY", "Cyprus"),
    ("CZ", "Czech Republic"),
    ("DK", "Denmark"),
    ("DJ", "Djibouti"),
    ("DM", "Dominica"),
    ("DO", "Dominican Republic"),
    ("EC", "Ecuador"),
    ("EG", "Egypt"),
    ("SV", "El Salvador"),
    ("GQ", "Equatorial Guinea"),
    ("ER", "Eritrea"),
    ("EE", "Estonia"),
    ("ET", "Ethiopia"),
    ("FK", "Falkland Islands (Malvinas)"),
    ("FO", "Faroe Islands"),
    ("FJ", "Fiji"),
    ("FI", "Finland"),
    ("FR", "France"),
    ("GF", "French Guiana"),
    ("PF", "French Polynesia"),
    ("TF", "French Southern Territories"),
    ("GA", "Gabon"),
    ("GM", "Gambia"),
    ("GE", "Georgia"),
    ("DE", "Germany"),
    ("GH", "Ghana"),
    ("GI", "Gibraltar"),
    ("GR", "Greece"),
    ("GL", "Greenland"),
    ("GD", "Grenada"),
    ("GP", "Guadeloupe"),
    ("GU", "Guam"),
    ("GT", "Guatemala"),
    ("GG", "Guernsey"),
    ("GN", "Guinea"),
    ("GW", "Guinea-Bissau"),
    ("GY", "Guyana"),
    ("HT", "Haiti"),
    ("HM", "Heard Island and McDonald Islands"),
    ("VA", "Holy See (Vatican City State)"),
    ("HN", "Honduras"),
    ("HK", "Hong Kong"),
    ("HU", "Hungary"),
    ("IS", "Iceland"),
    ("IN", "India"),
    ("ID", "Indonesia"),
    ("IR", "Iran, Islamic Republic"),
    ("IQ", "Iraq"),
    ("IE", "Ireland"),
    ("IM", "Isle of Man"),
    ("IL", "Israel"),
    ("IT", "Italy"),
    ("JM", "Jamaica"),
    ("JP", "Japan"),
    ("JE", "Jersey"),
    ("JO", "Jordan"),
    ("KZ", "Kazakhstan"),
    ("KE", "Kenya"),
    ("KI", "Kiribati"),
    ("KP", "Korea, Democratic People's Republic"),
    ("KR", "Korea, Republic"),
    ("KW", "Kuwait", "+965"),
    ("KG", "Kyrgyzstan"),
    ("LA", "Lao People's Democratic Republic"),
    ("LV", "Latvia"),
    ("LB", "Lebanon"),
    ("LS", "Lesotho"),
    ("LR", "Liberia"),
    ("LY", "Libya"),
    ("LI", "Liechtenstein"),
    ("LT", "Lithuania"),
    ("LU", "Luxembourg"),
    ("MO", "Macao"),
    ("MK", "Macedonia, the former Yugoslav Republic"),
    ("MG", "Madagascar"),
    ("MW", "Malawi"),
    ("MY", "Malaysia"),
    ("MV", "Maldives"),
    ("ML", "Mali"),
    ("MT", "Malta"),
    ("MH", "Marshall Islands"),
    ("MQ", "Martinique"),
    ("MR", "Mauritania"),
    ("MU", "Mauritius"),
    ("YT", "Mayotte"),
    ("MX", "Mexico"),
    ("FM", "Micronesia, Federated States"),
    ("MD", "Moldova"),
    ("MC", "Monaco"),
    ("MN", "Mongolia"),
    ("ME", "Montenegro"),
    ("MS", "Montserrat"),
    ("MA", "Morocco"),
    ("MZ", "Mozambique"),
    ("MM", "Myanmar"),
    ("NA", "Namibia"),
    ("NR", "Nauru"),
    ("NP", "Nepal"),
    ("NL", "Netherlands"),
    ("NC", "New Caledonia"),
    ("NZ", "New Zealand"),
    ("NI", "Nicaragua"),
    ("NE", "Niger"),
    ("NG", "Nigeria"),
    ("NU", "Niue"),
    ("NF", "Norfolk Island"),
    ("MP", "Northern Mariana Islands"),
    ("NO", "Norway"),
    ("OM", "Oman"),
    ("PK", "Pakistan"),
    ("PW", "Palau"),
    ("PS", "Palestine, State of"),
    ("PA", "Panama"),
    ("PG", "Papua New Guinea"),
    ("PY", "Paraguay"),
    ("PE", "Peru"),
    ("PH", "Philippines"),
    ("PN", "Pitcairn"),
    ("PL", "Poland"),
    ("PT", "Portugal"),
    ("PR", "Puerto Rico"),
    ("QA", "Qatar"),
    ("RE", "Réunion"),
    ("RO", "Romania"),
    ("RU", "Russian Federation"),
    ("RW", "Rwanda"),
    ("BL", "Saint Barthélemy"),
    ("SH", "Saint Helena, Ascension and Tristan da Cunha"),
    ("KN", "Saint Kitts and Nevis"),
    ("LC", "Saint Lucia"),
    ("MF", "Saint Martin (French part)"),
    ("PM", "Saint Pierre and Miquelon"),
    ("VC", "Saint Vincent and the Grenadines"),
    ("WS", "Samoa"),
    ("SM", "San Marino"),
    ("ST", "Sao Tome and Principe"),
    ("SA", "Saudi Arabia"),
    ("SN", "Senegal"),
    ("RS", "Serbia"),
    ("SC", "Seychelles"),
    ("SL", "Sierra Leone"),
    ("SG", "Singapore"),
    ("SX", "Sint Maarten (Dutch part)"),
    ("SK", "Slovakia"),
    ("SI", "Slovenia"),
    ("SB", "Solomon Islands"),
    ("SO", "Somalia"),
    ("ZA", "South Africa"),
    ("GS", "South Georgia and the South Sandwich Islands"),
    ("SS", "South Sudan"),
    ("ES", "Spain"),
    ("LK", "Sri Lanka"),
    ("SD", "Sudan"),
    ("SR", "Suriname"),
    ("SJ", "Svalbard and Jan Mayen"),
    ("SZ", "Swaziland"),
    ("SE", "Sweden"),
    ("CH", "Switzerland"),
    ("SY", "Syrian Arab Republic"),
    ("TW", "Taiwan, Province of China"),
    ("TJ", "Tajikistan"),
    ("TZ", "Tanzania, United Republic"),
    ("TH", "Thailand"),
    ("TL", "Timor-Leste"),
    ("TG", "Togo"),
    ("TK", "Tokelau"),
    ("TO", "Tonga"),
    ("TT", "Trinidad and Tobago"),
    ("TN", "Tunisia"),
    ("TR", "Turkey"),
    ("TM", "Turkmenistan"),
    ("TC", "Turks and Caicos Islands"),
    ("TV", "Tuvalu"),
    ("UG", "Uganda"),
    ("UA", "Ukraine"),
    ("AE", "United Arab Emirates"),
    ("GB", "United Kingdom"),
    ("US", "United States"),
    ("UM", "United States Minor Outlying Islands"),
    ("UY", "Uruguay"),
    ("UZ", "Uzbekistan"),
    ("VU", "Vanuatu"),
    ("VE", "Venezuela"),
    ("VN", "Viet Nam"),
    ("VG", "Virgin Islands, British"),
    ("VI", "Virgin Islands, U.S."),
    ("WF", "Wallis and Futuna"),
    ("EH", "Western Sahara"),
    ("YE", "Yemen"),
    ("ZM", "Zambia"),
    ("ZW", "Zimbabwe"),
]


class CardSourceType(TypedDict):
    type: Literal["applepay", "creditcard"]
    name: str
    number: str
    cvc: str
    month: Literal["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    year: str


class PaymentPriviledges(TextChoices):
    CAN_DOWNLOAD = ("CAN_DOWNLOAD", "User can download video to watch offline")
    CAN_CREATE_SUBTILES = ("CAN_CREATE_SUBTILES", "User can add subtitles to video")
