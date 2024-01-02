from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Poligono(Base):
    __tablename__ = 'poligonos'
    id = Column(Integer, primary_key=True)
    pontos = Column(String)

class Regra(Base):
    __tablename__ = 'regras'
    id = Column(Integer, primary_key=True)
    poligono_id = Column(Integer)
    tipo = Column(String)
    valor = Column(Integer)

class AreaService:
    def __init__(self):
        self.engine = create_engine('sqlite:///its.db')
        Base.metadata.create_all(self.engine)
        session = sessionmaker(bind=self.engine)
        self.session = session()

    def add_area(self, polygon):
        pontos_str = ';'.join(
            [f"{ponto['x']},{ponto['y']}" for ponto in polygon])
        print(pontos_str)
        poligono = Poligono(pontos=pontos_str)
        self.session.add(poligono)
        self.session.commit()

    def get_all_areas(self):
        areas = self.session.query(Poligono).all()
        areas_retur = []
        for area in areas:
            pontos = area.pontos.split(';')
            pontos = [{'x': int(ponto.split(',')[0]), 'y': int(
                ponto.split(',')[1])} for ponto in pontos]
            areas_retur.append({'id': area.id, 'points': pontos})

        return areas_retur

    def get_area_info(self, id):
        area = self.session.query(Poligono).filter(Poligono.id == id).first()
        rules = self.session.query(Regra).filter(Regra.poligono_id == id).all()
        rules_retur = []
        for rule in rules:
            rules_retur.append({'id': rule.id, 'type': rule.tipo, 'value': rule.valor})

        pontos = area.pontos.split(';')
        pontos = [{'x': int(ponto.split(',')[0]), 'y': int(
            ponto.split(',')[1])} for ponto in pontos]
        return {'id': area.id, 'points': pontos, 'rules': rules_retur}
    
    def delete_area(self, id):
        area = self.session.query(Poligono).filter(Poligono.id == id).first()
        self.session.delete(area)
        self.session.commit()
        return {'msg': 'area deleted!'}