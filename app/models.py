from app import db 
from sqlalchemy import func

class RespostaFormulario(db.Model):
    __tablename__ = 'respostas_formulario'
    id = db.Column(db.Integer, primary_key=True)
    
    resp_q1 = db.Column(db.String(5), nullable=False) 
    resp_q2 = db.Column(db.String(50), nullable=False)
    resp_q3 = db.Column(db.Text, nullable=False) 
    resp_q4 = db.Column(db.Text, nullable=False)
    resp_q5 = db.Column(db.String(50), nullable=False)
    resp_q6 = db.Column(db.String(50), nullable=False)
    resp_q7 = db.Column(db.String(50), nullable=False)
    resp_q8 = db.Column(db.String(50), nullable=False)
    resp_q9 = db.Column(db.Text, nullable=False)
    resp_q10 = db.Column(db.String(5), nullable=False)
    
    data_envio = db.Column(db.DateTime, default=func.now())

    def __repr__(self):
        return f'<RespostaFormulario {self.id}>'
