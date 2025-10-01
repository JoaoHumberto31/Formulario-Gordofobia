from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField, SelectMultipleField, widgets
from wtforms.validators import DataRequired

OPCOES_ESCALA_PRECONCEITO = [
    ('muito_baixo', 'Nível muito baixo'),
    ('baixo', 'Nível baixo'),
    ('moderado', 'Nível moderado'),
    ('alto', 'Nível alto'),
    ('muito_alto', 'Nível muito alto')
]

OPCOES_VITIMA = [
    ('sim_frequentemente', 'Sim, frequentemente'),
    ('sim_algumas_vezes', 'Sim, algumas vezes'),
    ('raramente', 'Raramente'),
    ('nao', 'Não'),
    ('prefiro_nao_responder', 'Prefiro não responder')
]

OPCOES_AMBIENTE = [
    ('familiar', 'Ambiente familiar'),
    ('escolar', 'Ambiente escolar/acadêmico'),
    ('trabalho', 'Ambiente de trabalho'),
    ('saude', 'Serviços de saúde (consultas médicas, exames, etc.)'),
    ('transporte', 'Transporte público'),
    ('midias_sociais', 'Mídias sociais / Internet'),
    ('lojas', 'Lojas de roupas/comércio'),
    ('nunca_percebi', 'Nunca percebi/sofri')
]

OPCOES_AFETADO = [
    ('emprego', 'Emprego/Carreira'),
    ('relacionamentos', 'Relacionamentos amorosos'),
    ('social', 'Vida social/Amizades'),
    ('roupas', 'Acesso a roupas adequadas'),
    ('saude_qualidade', 'Acesso à saúde de qualidade (tratamento respeitoso)'),
    ('nao_afetou', 'Não afetou negativamente')
]

OPCOES_FREQUENCIA = [
    ('muito_frequentemente', 'Muito frequentemente'),
    ('frequentemente', 'Frequentemente'),
    ('as_vezes', 'Às vezes'),
    ('raramente', 'Raramente'),
    ('nunca', 'Nunca')
]

OPCOES_INTERVENCAO = [
    ('sim_sempre', 'Sim, sempre'),
    ('sim_algumas_vezes', 'Sim, algumas vezes'),
    ('nao_medo', 'Não, por medo/insegurança'),
    ('nao_gostaria', 'Não, mas gostaria de ter intervindo'),
    ('nunca_presenciei', 'Nunca presenciei')
]

OPCOES_SAUDE_PRECONCEITO = [
    ('justificado', 'Sim, o preconceito é justificado pela saúde.'),
    ('parcialmente', 'Parcialmente, mas o preconceito ainda é inaceitável.'),
    ('nao_justifica', 'Não, a saúde é privada e não justifica o preconceito.'),
    ('nao_sei_opinar', 'Não sei opinar.')
]

OPCOES_REDES_SOCIAIS = [
    ('disseminam', 'Principalmente disseminam o preconceito.'),
    ('combatem', 'Principalmente ajudam a combater o preconceito.'),
    ('neutro', 'Têm um impacto neutro.'),
    ('misto', 'Têm um papel misto (disseminam e combatem).')
]

OPCOES_PRIMEIRO_PASSO = [
    ('representatividade', 'Mais representatividade gorda positiva na mídia.'),
    ('legislacao', 'Legislação mais rigorosa contra a discriminação baseada no peso.'),
    ('campanhas', 'Campanhas de conscientização e educação nas escolas.'),
    ('saude_tamanhos', 'Foco em discussões sobre "saúde em todos os tamanhos".')
]

OPCOES_IMPACTO_ESCALA = [
    ('0', '0'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5')
]


class ScaleQuestionForm(FlaskForm):
    resposta = RadioField(
        'Sua Resposta:', 
        choices=OPCOES_ESCALA_PRECONCEITO, 
        validators=[DataRequired('Você deve selecionar uma opção.')],
        coerce=str 
    )
    submit = SubmitField('Próxima Pergunta')

class RadioQuestionForm(FlaskForm):
    resposta = RadioField(
        'Sua Resposta:', 
        choices=[], 
        validators=[DataRequired('Você deve selecionar uma opção.')],
        coerce=str 
    )
    submit = SubmitField('Próxima Pergunta')

class CheckboxQuestionForm(FlaskForm):
    
    resposta = SelectMultipleField(
        'Selecione as opções que se aplicam:', 
        choices=[],
        option_widget=widgets.CheckboxInput(), 
        widget=widgets.ListWidget(html_tag='ul'), 
    )
    submit = SubmitField('Próxima Pergunta')


class FinalSubmitForm(FlaskForm):
    
    submit = SubmitField('Finalizar e Salvar Respostas no Banco de Dados')