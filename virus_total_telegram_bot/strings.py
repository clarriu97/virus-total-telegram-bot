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
        "is_url": {
            ENGLISH: "🔎 I am analyzing the URL you sent me...",
            SPANISH: "🔎 Estoy analizando la URL que me enviaste...",
        },
        "is_not_url": {
            ENGLISH:
                "It seems that the text you sent me is not a URL. Please send me a valid URL or a file.",
            SPANISH:
                "Parece que el texto que me enviaste no es una URL. Por favor, envíame una URL válida."
        },
    }
}
