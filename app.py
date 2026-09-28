"""
app.py - Aplicação Web Principal em Flask para o Portal Aion 2 Guides.
Portal de guias, tutoriais e banco de dados para o lançamento global de Aion 2.
Todas as descrições e interfaces em pt-BR com nomenclaturas do jogo em INGLÊS.
"""

from flask import Flask, render_template, abort, jsonify, request
import os
from database import init_db
from models import ClassModel, NewsModel, SystemModel, EventModel

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)
app.config['SECRET_KEY'] = 'aion2-global-secret-key-2026'

# Inicialização automática do banco de dados na subida da aplicação
with app.app_context():
    try:
        init_db()
    except Exception as e:
        # Em ambientes serverless somente-leitura (como Vercel),
        # o banco SQLite empacotado já está inicializado e pode ser lido normalmente.
        pass

@app.context_processor
def inject_global_data():
    """Injeta dados globais em todos os templates (como a lista de classes para o menu dropdown)."""
    all_classes = ClassModel.get_all()
    return {
        'nav_classes': all_classes,
        'app_name': 'Aion 2 Guides Global',
        'level_cap': 45
    }

# 1. Rota: Página Inicial ( / )
@app.route('/')
def index():
    classes = ClassModel.get_all()
    events = EventModel.get_active()
    return render_template('index.html', classes=classes, events=events)

# 2. Rota: Guia de Iniciantes ( /beginner-guide )
@app.route('/beginner-guide')
def beginner_guide():
    return render_template('beginner_guide.html')

# 3. Rota: Diretório de Classes ( /classes )
@app.route('/classes')
def classes_list():
    classes = ClassModel.get_all()
    return render_template('classes.html', classes=classes)

# 3b. Rota: Detalhe de Classe Individual ( /classes/<slug> )
@app.route('/classes/<slug>')
def class_detail(slug):
    class_data = ClassModel.get_by_slug(slug)
    if not class_data:
        abort(404)
    
    # Obter lista de outras classes para sugestão no rodapé da página
    all_classes = ClassModel.get_all()
    other_classes = [c for c in all_classes if c['slug'] != slug]
    
    return render_template('class_detail.html', cls=class_data, other_classes=other_classes)

# 4. Rota: Sistemas de Progressão ( /progression )
@app.route('/progression')
def progression():
    stigmas_system = SystemModel.get_by_key('stigmas')
    daevanion_system = SystemModel.get_by_key('daevanion')
    classes = ClassModel.get_all()
    return render_template('progression.html', stigmas=stigmas_system, daevanion=daevanion_system, classes=classes)

# 5. Rota: Guia de Equipamentos ( /gearing )
@app.route('/gearing')
def gearing():
    enhancement_system = SystemModel.get_by_key('enhancement')
    inheritance_system = SystemModel.get_by_key('inheritance')
    soul_binding_system = SystemModel.get_by_key('soul_binding')
    gems_system = SystemModel.get_by_key('manastones_godstones')
    return render_template('gearing.html', 
                           enhancement=enhancement_system,
                           inheritance=inheritance_system,
                           soul_binding=soul_binding_system,
                           gems=gems_system)

# 6. Rota: Ferramentas ( /ferramentas e /tools )
@app.route('/ferramentas')
@app.route('/tools')
def tools():
    return render_template('tools.html')

# 7. Rota: Planejador de Builds ( /planner e /planejador )
@app.route('/planner')
@app.route('/planejador')
def planner():
    classes = ClassModel.get_all()
    return render_template('planner.html', classes=classes)

# 8. Rota: Tracker de Tarefas Diárias e Semanais ( /tracker e /tarefas )
@app.route('/tracker')
@app.route('/tarefas')
def tracker():
    classes = ClassModel.get_all()
    return render_template('tracker.html', classes=classes)

# 9. Rota: Mapa Interativo de Atreia ( /mapa e /map )
@app.route('/mapa')
@app.route('/map')
def interactive_map():
    return render_template('map.html')


# Rotas de API Úteis (para busca rápida e simuladores dinâmicos)
@app.route('/api/classes')
def api_classes():
    classes = ClassModel.get_all()
    return jsonify(classes)

@app.route('/api/classes/<slug>')
def api_class_detail(slug):
    class_data = ClassModel.get_by_slug(slug)
    if not class_data:
        return jsonify({'error': 'Classe não encontrada'}), 404
    return jsonify(class_data)

@app.route('/api/classes/<slug>/video', methods=['GET', 'POST'])
def api_class_video(slug):
    """Obtém ou atualiza os metadados e URL do vídeo de uma classe."""
    class_data = ClassModel.get_by_slug(slug)
    if not class_data:
        return jsonify({'error': 'Classe não encontrada'}), 404
        
    if request.method == 'POST':
        data = request.get_json() or {}
        video_url = data.get('video_url')
        video_title = data.get('video_title')
        video_credits = data.get('video_credits')
        video_author_url = data.get('video_author_url')
        ClassModel.update_video(slug, video_url, video_title, video_credits, video_author_url)
        updated_data = ClassModel.get_by_slug(slug)
        return jsonify({
            'success': True,
            'message': f'Vídeo da classe {class_data["name"]} atualizado com sucesso!',
            'class': {
                'slug': slug,
                'video_url': updated_data.get('video_url'),
                'video_embed_url': updated_data.get('video_embed_url'),
                'video_title': updated_data.get('video_title'),
                'video_credits': updated_data.get('video_credits'),
                'video_author_url': updated_data.get('video_author_url')
            }
        })
        
    return jsonify({
        'slug': slug,
        'name': class_data['name'],
        'video_url': class_data.get('video_url'),
        'video_embed_url': class_data.get('video_embed_url'),
        'video_title': class_data.get('video_title'),
        'video_credits': class_data.get('video_credits'),
        'video_author_url': class_data.get('video_author_url')
    })

@app.route('/api/classes/<slug>/macros')
def api_class_macros(slug):
    """Retorna os macros comunitários recomendados para a classe."""
    class_data = ClassModel.get_by_slug(slug)
    if not class_data:
        return jsonify({'error': 'Classe não encontrada'}), 404
    macros = class_data.get('macros', [])
    return jsonify({
        'slug': slug,
        'name': class_data['name'],
        'macros': macros
    })

@app.route('/api/classes/<slug>/macros/<macro_id>/download')
def api_download_macro(slug, macro_id):
    """Permite download direto do arquivo .txt do macro."""
    from flask import Response
    class_data = ClassModel.get_by_slug(slug)
    if not class_data:
        return jsonify({'error': 'Classe não encontrada'}), 404
    macros = class_data.get('macros', [])
    macro = next((m for m in macros if m['id'] == macro_id), None)
    if not macro:
        return jsonify({'error': 'Macro não encontrado'}), 404
    filename = macro.get('filename', f"{macro_id}.txt")
    content = macro.get('commands_raw', '')
    return Response(
        content,
        mimetype="text/plain; charset=utf-8",
        headers={"Content-Disposition": f"attachment;filename={filename}"}
    )

@app.route('/api/enhancement-simulate', methods=['POST'])

def api_enhancement_simulate():
    """Simulador matemático de taxas de sucesso do sistema de Enhancement."""
    import random
    data = request.get_json() or {}
    current_level = int(data.get('current_level', 0))
    
    # Regras Oficiais:
    # 0 -> 10: 100% de sucesso
    # 10 -> 11: 70%
    # 11 -> 12: 50%
    # 12 -> 13: 35%
    # 13 -> 14: 20%
    # 14 -> 15: 10%
    rates = {
        0: 100, 1: 100, 2: 100, 3: 100, 4: 100,
        5: 100, 6: 100, 7: 100, 8: 100, 9: 100,
        10: 70, 11: 50, 12: 35, 13: 20, 14: 10
    }
    
    if current_level >= 15:
        return jsonify({
            'success': False,
            'message': 'Nível máximo de Enhancement (+15) já alcançado!',
            'new_level': 15,
            'rate': 0
        })

    rate = rates.get(current_level, 5)
    roll = random.uniform(0, 100)
    success = roll <= rate
    
    kina_cost = (current_level + 1) * 25000
    
    if success:
        new_level = current_level + 1
        msg = f"Sucesso! O equipamento foi aprimorado para +{new_level}!"
    else:
        # Se falhar acima de +10, há chance de regredir 1 nível
        downgrade = current_level > 10
        new_level = max(10, current_level - 1) if downgrade else current_level
        msg = f"Falha no aprimoramento! Nível atual: +{new_level}."
        
    return jsonify({
        'success': success,
        'new_level': new_level,
        'rate': rate,
        'roll': round(roll, 2),
        'kina_spent': kina_cost,
        'message': msg
    })

# Tratamento amigável de erro 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    # Permite rodar com `python app.py` diretamente
    print("Iniciando Aion 2 Guides Web Server...")
    print("Acesse em: http://127.0.0.1:5000")
    app.run(debug=True, host='127.0.0.1', port=5000)
