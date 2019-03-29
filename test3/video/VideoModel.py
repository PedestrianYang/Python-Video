class Video:
    def __init__(self, name, imgUrl, downUrl):
        self.name = name
        self.imgUrl = imgUrl
        self.downUrl = downUrl


class Title:
    def __init__(self, name, requestUrl):
        self.name = name
        self.requestUrl = requestUrl