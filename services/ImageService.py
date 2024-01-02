import base64
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from CONST import areas_file
from flask import jsonify, send_file
Base = declarative_base()
import cv2

class Image(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    data = Column(String)


class ImageService:
    def __init__(self):
        self.engine = create_engine('sqlite:///its.db')
        Base.metadata.create_all(self.engine)
        session = sessionmaker(bind=self.engine)
        self.session = session()

    def save_image(self, image):

        nome = image.filename

        with open('images/' + nome, 'wb') as f:
            f.write(image.read())
        image = Image(nome=nome, data=text('datetime("now")'))
        self.session.add(image)
        self.session.commit()
        print("Imagem salva com sucesso!")
        return image.id
    
    def get_last_image(self):
        last = self.session.query(Image).order_by(Image.id.desc()).first()      
        
        if last:
            image_file_path = 'images/' + last.nome
            
            # Lê o arquivo de imagem.
            image = cv2.imread(image_file_path)
            # redimensiona a imagem.
            image = cv2.resize(image, (640, 360))
            
            # Codifica a imagem em base64.
            retval, buffer = cv2.imencode('.jpg', image)
            # Converte o buffer para base64.
            encoded_string = base64.b64encode(buffer)
            

            # Retorna o arquivo em base64.
            return jsonify({'image': encoded_string.decode('utf-8')})
            
        else:
              return "Imagem não encontrada", 404