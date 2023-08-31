from TextModel import TextModel
class BaloonText:
    def __init__(self, border_box: TextModel,text_models = list(),text = "", translatedText:str = ""):
        self.border_box = border_box
        self.text_models = text_models
        self.text = text
        self.translatedText = translatedText