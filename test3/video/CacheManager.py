import pymysql
from video.VideoModel import *

tablename = 'Video'
class CacheManager:
    def __init__(self):
        self.db = pymysql.connect("localhost","root","root","test" )

        cursor = self.db.cursor()
        sql = """CREATE TABLE IF NOT EXISTS %s (
         NAME  CHAR(200) NOT NULL COLLATE utf8_unicode_ci,
         IMAGEURL  CHAR(200) COLLATE utf8_unicode_ci,
         VIDEOURL  CHAR(200) COLLATE utf8_unicode_ci,
         DOWNLOADURL  CHAR(200) COLLATE utf8_unicode_ci)""" % tablename
        cursor.execute(sql)

    def insertVideo(self, video):
        cursor = self.db.cursor()
        exsit = self.selectByName(video.name)
        if exsit == False:
            sql = "INSERT INTO %s(NAME, \
            IMAGEURL, VIDEOURL) \
            VALUES ('%s', '%s',  '%s')" % \
              (tablename, video.name, video.imgUrl, video.videoUrl)
            try:
                cursor.execute(sql)
                self.db.commit()
            except:
                self.db.rollback()

    def insertAll(self, videos):
        for video in videos:
            self.insertVideo(video)

    def cleanCache(self):
        cursor = self.db.cursor()
        sql1 = 'DELETE FROM %s' % tablename
        sql2 = ' truncate table %s' % tablename
        try:
            cursor.execute(sql1)
            cursor.execute(sql2)
            self.db.commit()
        except:
            self.db.rollback()


    def deleteVideo(self, video):
        cursor = self.db.cursor()
        sql1 = 'DELETE FROM %s WHERE NAME = %s' % (tablename, video.name)
        sql2 = ' truncate table %s' % tablename
        try:
            cursor.execute(sql1)
            cursor.execute(sql2)
            self.db.commit()
        except:
            self.db.rollback()

    def selectByName(self, name):
        cursor = self.db.cursor()
        sql = "SELECT COUNT(NAME) FROM %s where NAME = '%s'" % (tablename, name)
        try:
            cursor.execute(sql)
            results = cursor.fetchone()
            if results[0] == 0:
                return False


        except:
            print('Error: unable to fecth data')
            return None

    def selectAllData(self):
        cursor = self.db.cursor()
        sql = 'SELECT * FROM %s' % tablename
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            videos = []
            for row in results:
                video = Video(row[0], row[1], row[2], row[3])
                videos.append(video)
            return videos

        except:
            print('Error: unable to fecth data')
            return None

    def updateVideoDownLoadUrl(self, video, downloaderUrl):
        cursor = self.db.cursor()
        sql = "UPDATE %s SET DOWNLOADURL = '%s' WHERE NAME = '%s'" % (tablename, downloaderUrl, video.name)
        try:
            cursor.execute(sql)
            self.db.commit()
        except:
            print('Error: unable to fecth data')
            self.db.rollback()
            return None
