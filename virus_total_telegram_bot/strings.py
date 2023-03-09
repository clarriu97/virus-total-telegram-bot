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
    }
}
