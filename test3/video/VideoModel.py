class Video:
    def __init__(self, name, imgUrl, videoUrl, downUrl = None):
        self.name = name
        self.imgUrl = imgUrl
        self.videoUrl = videoUrl
        self.downUrl = downUrl


class Title:
    def __init__(self, name, requestUrl):
        self.name = name
        self.requestUrl = requestUrl