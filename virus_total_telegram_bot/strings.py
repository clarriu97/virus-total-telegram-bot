"""Strings used as the text of the Bot"""
# pylint: disable=anomalous-backslash-in-string

ENGLISH = 'en'
SPANISH = 'es'

dialogs = {
    "start": {
        ENGLISH:
            "💻 Hi there! Welcome to Virus Total 🔍, I am an unofficial Telegram bot that uses the "
            "VirusTotal API (https://virustotal.com) to perform security analysis on URLs and files. "
            "I can help you check the safety and integrity of your files and URLs. You can send me a "
            "URL or a file (up to 30 megabytes) and I will give you the results of the analysis. 😊",
        SPANISH:
            "💻 Hola! Bienvenido a Virus Total 🔍, soy un bot no oficial de Telegram que usa la "
            "API de VirusTotal (https://virustotal.com) para realizar análisis de seguridad en "
            "URLs y archivos. Puedo ayudarte a verificar la seguridad e integridad de tus archivos "
            "y URLs. Puedes enviarme una URL o un archivo (hasta 30 megabytes) y te daré los "
            "resultados del análisis. 😊",
    },
    "text_received": {
        "analyzing": {
            ENGLISH: "🔎 I am analyzing the URL you sent me, give me one second...",
            SPANISH: "🔎 Estoy analizando la URL que me enviaste, dame un segundo...",
        },
        "error": {
            ENGLISH:
                "🚨 It seems that the URL you sent me is not valid. Please, send me a valid URL.",
            SPANISH:
                "🚨 Parece que la URL que me enviaste no es válida. Por favor, envíame una URL válida.",
        },
        "results": {
            ENGLISH: "📊 Here are the results of the analysis for the domain %s:",
            SPANISH: "📊 Aquí están los resultados del análisis para el dominio %s:",
        },
    },
    "file_received": {
        "analyzing": {
            ENGLISH: "🔎 File received! Starting the analysis, I will send you back the results, it might take a few minutes.",
            SPANISH: "🔎 Archivo recibido! Comenzando el análisis, te enviaré los resultados, puede tardar unos minutos.",
        },
        "error": {
            ENGLISH:
                "🚨 It seems that the file you sent me is not valid. Please, try anotherone.",
            SPANISH:
                "🚨 Parece que el archivo que me enviaste no es válido. Por favor, intenta con otro.",
        },
        "too_big": {
            ENGLISH: "🚨 The file you sent me is too big. Please, send me a file smaller than %s megabytes.",
            SPANISH: "🚨 El archivo que me enviaste es demasiado grande. Por favor, envíame un archivo de menos de %s megabytes.",
        },
        "results": {
            ENGLISH: "📊 Here are the results of the analysis for the file %s:",
            SPANISH: "📊 Aquí están los resultados del análisis para el archivo %s:",
        },
    },
}
