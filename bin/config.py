from os import path

CONFIG = {
    "ENV": "TEST",
    "TEST_BASE_DIR": "C:\\Users\\conor.breen\\Development\\Youtube-Downloader\\",
}

CONFIG["BASE_DIR"] = CONFIG[CONFIG["ENV"] + "_BASE_DIR"]
CONFIG["ERROR_LOG"] = path.join(CONFIG["BASE_DIR"], "bin", "error.log")
CONFIG["DOWNLOAD_DIR"] = path.join(CONFIG["BASE_DIR"], "Videos")
