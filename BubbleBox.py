class Coordinates:
    def __init__(self, x1 : int ,y1:int, x2:int, y2 : int ):
        self.x1 =x1
        self.x2=x2
        self.y1 = y1
        self.y2 = y2


class BubbleBox:
    def __init__(self,box,shape:str, start_line:int, coordinates:Coordinates= [],text = "",translated_text = ""):
        self.start_line = start_line
        self.coordinates = coordinates
        self.box = box
        self.text = text
        self.translated_text = translated_text
        self.shape = shape

