import json 
from flask import Blueprint, render_template, redirect, url_for, session, request, current_app, flash
from app import db 
from app.forms import (
    ScaleQuestionForm, RadioQuestionForm, CheckboxQuestionForm, FinalSubmitForm,
    OPCOES_ESCALA_PRECONCEITO, OPCOES_VITIMA, OPCOES_AMBIENTE, OPCOES_AFETADO,
    OPCOES_FREQUENCIA, OPCOES_INTERVENCAO, OPCOES_SAUDE_PRECONCEITO, 
    OPCOES_REDES_SOCIAIS, OPCOES_PRIMEIRO_PASSO, OPCOES_IMPACTO_ESCALA
)

app = Blueprint('main', __name__)


PERGUNTAS_CONFIG = [
    # Q1: Escala
    {'pergunta': "Em que grau você considera que a gordofobia (preconceito contra pessoas gordas) está presente em sua sociedade?", 'form': ScaleQuestionForm, 'options': OPCOES_ESCALA_PRECONCEITO, 'key': 'q1'},
    # Q2: Rádio (Escolha Única)
    {'pergunta': "Você já foi vítima de comentários, piadas ou discriminação relacionados ao seu peso/corpo?", 'form': RadioQuestionForm, 'options': OPCOES_VITIMA, 'key': 'q2'},
    # Q3: CHECKBOX (Múltipla Escolha)
    {'pergunta': "Em qual destes ambientes você já percebeu ou sofreu manifestações de gordofobia? (Marque todas que se aplicam)", 'form': CheckboxQuestionForm, 'options': OPCOES_AMBIENTE, 'key': 'q3'},
    # Q4: CHECKBOX (Múltipla Escolha)
    {'pergunta': "Você acredita que o seu peso/corpo já afetou negativamente suas oportunidades em alguma das seguintes áreas? (Marque todas que se aplicam)", 'form': CheckboxQuestionForm, 'options': OPCOES_AFETADO, 'key': 'q4'},
    # Q5: Rádio (Frequência)
    {'pergunta': "Com que frequência você observa a mídia (filmes, séries, publicidade, redes sociais) retratando pessoas gordas de forma estereotipada (preguiçosa, desastrada, solitária)?", 'form': RadioQuestionForm, 'options': OPCOES_FREQUENCIA, 'key': 'q5'},
    # Q6: Rádio (Intervenção)
    {'pergunta': "Você já presenciou alguém sofrendo gordofobia e interveio em defesa dessa pessoa?", 'form': RadioQuestionForm, 'options': OPCOES_INTERVENCAO, 'key': 'q6'},
    # Q7: Rádio (Opinião)
    {'pergunta': "Você acredita que a gordofobia está diretamente ligada à saúde de uma pessoa, justificando o preconceito?", 'form': RadioQuestionForm, 'options': OPCOES_SAUDE_PRECONCEITO, 'key': 'q7'},
    # Q8: Rádio (Opinião - Redes Sociais)
    {'pergunta': "Em sua opinião, qual é o papel das redes sociais na disseminação ou no combate à gordofobia?", 'form': RadioQuestionForm, 'options': OPCOES_REDES_SOCIAIS, 'key': 'q8'},
    # Q9: Rádio (Opinião - Primeiro Passo)
    {'pergunta': "Qual seria o primeiro passo mais eficaz para reduzir a gordofobia na sociedade?", 'form': RadioQuestionForm, 'options': OPCOES_PRIMEIRO_PASSO, 'key': 'q9'},
    # Q10: Escala 0-5
    {'pergunta': "De 0 (nenhum impacto) a 5 (impacto extremo), qual é o nível de impacto que a gordofobia generalizada na sociedade tem sobre a saúde mental (autoestima, ansiedade, depressão) das pessoas gordas?", 'form': ScaleQuestionForm, 'options': OPCOES_IMPACTO_ESCALA, 'key': 'q10'},
]

NUM_PERGUNTAS = len(PERGUNTAS_CONFIG)


@app.route('/')
def index():
    
    session.pop('respostas_temporarias', None)
    return render_template('index.html')

@app.route('/pergunta/<int:num_pergunta>', methods=['GET', 'POST'])
def pergunta(num_pergunta):
    if not 1 <= num_pergunta <= NUM_PERGUNTAS:
        flash('Número de pergunta inválido.', 'error')
        return redirect(url_for('main.index'))

    config = PERGUNTAS_CONFIG[num_pergunta - 1]
    FormClass = config['form']
    key = config['key']

    form = FormClass()
    
    if hasattr(form.resposta, 'choices'):
        form.resposta.choices = config['options']
    
    pergunta_atual = config['pergunta']
    form.resposta.label.text = pergunta_atual

    if 'respostas_temporarias' not in session:
        session['respostas_temporarias'] = {}

    if form.validate_on_submit():
        
        resposta_data = form.resposta.data
        
        if isinstance(resposta_data, list):
            session['respostas_temporarias'][key] = json.dumps(resposta_data)
        else:
            session['respostas_temporarias'][key] = str(resposta_data)
            
        session.modified = True
        
        if num_pergunta < NUM_PERGUNTAS:
            return redirect(url_for('main.pergunta', num_pergunta=num_pergunta + 1))
        else:
            return redirect(url_for('main.revisao_e_envio'))

    if key in session.get('respostas_temporarias', {}):
        saved_data = session['respostas_temporarias'][key]
        
        if FormClass == CheckboxQuestionForm:
            try:
                form.resposta.data = json.loads(saved_data)
            except json.JSONDecodeError:
                 form.resposta.data = [] 
        else:
            form.resposta.data = saved_data


    return render_template(
        'pergunta_base.html', 
        form=form, 
        num_pergunta=num_pergunta,
        total_perguntas=NUM_PERGUNTAS,
        pergunta=pergunta_atual
    )

@app.route('/revisao', methods=['GET', 'POST'])
def revisao_e_envio():
    from app.models import RespostaFormulario 
    
    respostas_salvas = session.get('respostas_temporarias')

    if not respostas_salvas or len(respostas_salvas) != NUM_PERGUNTAS:
        flash('O formulário não está completo. Por favor, comece novamente.', 'warning')
        return redirect(url_for('main.pergunta', num_pergunta=1))

    form = FinalSubmitForm()

    if form.validate_on_submit():
        data_to_save = {}
        for config in PERGUNTAS_CONFIG:
            key = config['key']
            db_col_name = f'resp_{key}' # ex: 'resp_q1', 'resp_q2'
            data_to_save[db_col_name] = respostas_salvas.get(key)
        
        try:
            nova_resposta = RespostaFormulario(**data_to_save)
            
            with current_app.app_context():
                db.session.add(nova_resposta)
                db.session.commit()
            
            session.pop('respostas_temporarias', None)
            flash('Respostas salvas com sucesso!', 'success')
            return redirect(url_for('main.sucesso'))

        except Exception as e:
            current_app.logger.error(f"Erro ao salvar no DB: {e}")
            flash('Ocorreu um erro interno ao salvar as respostas. Tente novamente.', 'error')
            return redirect(url_for('main.revisao_e_envio'))

    respostas_formatadas = []
    for i, config in enumerate(PERGUNTAS_CONFIG):
        key = config['key']
        valor = respostas_salvas.get(key, 'Não respondido')
        
        if config['form'] == CheckboxQuestionForm:
            try:
                lista_valores = json.loads(valor)
                opcoes_map = {v: l for v, l in config['options']}
                exibicao = [opcoes_map.get(v, v) for v in lista_valores]
                valor = "<ul>" + "".join([f"<li>{item}</li>" for item in exibicao]) + "</ul>"
            except (json.JSONDecodeError, TypeError):
                valor = "Erro na resposta (Checkbox)"
        
        elif config['form'] != CheckboxQuestionForm:
            opcoes_map = {v: l for v, l in config['options']}
            valor = opcoes_map.get(valor, valor)
        
        respostas_formatadas.append({
            'num': i + 1,
            'pergunta': config['pergunta'],
            'resposta': valor
        })
        
    return render_template('revisao.html', respostas=respostas_formatadas, form=form, perguntas=PERGUNTAS_CONFIG)

@app.route('/voltar/<int:num_pergunta>')
def voltar(num_pergunta):
    if 1 < num_pergunta <= NUM_PERGUNTAS:
        return redirect(url_for('main.pergunta', num_pergunta=num_pergunta - 1))
    return redirect(url_for('main.index'))

@app.route('/sucesso')
def sucesso():
    return render_template('sucesso.html')