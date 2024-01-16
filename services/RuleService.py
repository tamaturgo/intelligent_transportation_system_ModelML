from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Regra(Base):
    __tablename__ = 'regras'
    id = Column(Integer, primary_key=True)
    tipo = Column(String)
    valor = Column(Integer)
    aux_valor = Column(Integer)

class Rel_Poligonos_regras (Base):
    __tablename__ = 'rel_poligonos_regras'
    poligono_id = Column(Integer, primary_key=True)
    regra_id = Column(Integer, primary_key=True)

class RuleService:
    def __init__(self):
        self.engine = create_engine('sqlite:///its.db')
        Base.metadata.create_all(self.engine)
        session = sessionmaker(bind=self.engine)
        self.session = session()

    def add_rule(self, rule_type, value, aux_valor=None):
        rule = Regra( tipo=rule_type, valor=value, aux_valor=aux_valor)
        self.session.add(rule)
        self.session.commit()
    
    def get_all_rules(self):
        rules = self.session.query(Regra).all()
        rules_retur = []
        for rule in rules:
            rules_retur.append({'id': rule.id, 'tipo': rule.tipo, 'valor': rule.valor, 'aux_valor': rule.aux_valor})

        return rules_retur
    
    def remove_rule_cascade(self, id):
        self.session.query(Regra).filter(Regra.id == id).delete()
        self.session.commit()
    
    def associate_rule(self, rule_id, area_id):
        rel = Rel_Poligonos_regras(poligono_id=area_id, regra_id=rule_id)
        self.session.add(rel)
        self.session.commit()

    def desassociate_rule(self, rule_id, area_id):
        self.session.query(Rel_Poligonos_regras).filter(Rel_Poligonos_regras.poligono_id == area_id, Rel_Poligonos_regras.regra_id == rule_id).delete()
        self.session.commit()
        