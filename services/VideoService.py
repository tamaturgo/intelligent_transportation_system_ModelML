import cv2
import os
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask import send_file
Base = declarative_base()


class Video(Base):
    __tablename__ = 'videos'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    data = Column(String)
    duracao = Column(Integer)


class VideoService:
    def __init__(self):
        self.engine = create_engine('sqlite:///its.db')
        Base.metadata.create_all(self.engine)
        session = sessionmaker(bind=self.engine)
        self.session = session()

    def save_video(self, nome, video):
        with open('videos/' + nome, 'wb') as f:
            f.write(video.read())
        video = Video(nome=nome, data=text('datetime("now")'))
        self.session.add(video)
        self.session.commit()
        return video.id

    def get_last_video(self):
        last = self.session.query(Video).order_by(Video.id.desc()).first()

        if last:
            video_file_path = 'videos/' + last.nome
            return send_file(video_file_path)
        else:
            return "Video não encontrado", 404

    def get_videos_at_folder(self):
        videos = []
        for file in os.listdir('videos/'):
            videos.append(
                file
            )
        return videos

    def video_to_opencv(self, video):
        cap = cv2.VideoCapture(video)
        while (cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                cv2.imshow('Frame', frame)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            else:
                break
        cap.release()
        cv2.destroyAllWindows()

    def video_to_frames(self, video):
        cap = cv2.VideoCapture(video)
        frames = []
        while (cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                frames.append(frame)
            else:
                break
        cap.release()
        return frames
