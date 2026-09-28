"""
test_app.py - Testes de integridade das rotas, templates e banco de dados.
"""

import unittest
from app import app
from models import ClassModel

class Aion2WebTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Level 45', response.data)
        self.assertIn(b'Gladiator', response.data)
        self.assertIn('Eventos Ativos In-Game'.encode('utf-8'), response.data)

    def test_beginner_guide(self):
        response = self.app.get('/beginner-guide')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Main Story', response.data)
        self.assertIn(b'Regional Quests', response.data)
        self.assertIn(b'Sealed Dungeons', response.data)
        self.assertIn(b'Strongholds', response.data)

    def test_classes_directory(self):
        response = self.app.get('/classes')
        self.assertEqual(response.status_code, 200)
        classes = ["Gladiator", "Templar", "Assassin", "Ranger", "Sorcerer", "Elementalist", "Cleric", "Chanter"]
        for c in classes:
            self.assertIn(c.encode('utf-8'), response.data)

    def test_all_individual_classes(self):
        classes = ["gladiator", "templar", "assassin", "ranger", "sorcerer", "elementalist", "cleric", "chanter"]
        for slug in classes:
            response = self.app.get(f'/classes/{slug}')
            self.assertEqual(response.status_code, 200, f"Falha ao carregar a classe {slug}")
            self.assertIn(b'Stigmas', response.data)
            self.assertIn(b'Daevanion', response.data)
            # Verifica se a seção de vídeo está presente no template
            self.assertIn('Demonstração em Vídeo'.encode('utf-8'), response.data)

    def test_class_video_api(self):
        # 1. Testar que todas as 8 classes possuem vídeo ativo e configurado
        classes = ["gladiator", "templar", "assassin", "ranger", "sorcerer", "elementalist", "cleric", "chanter"]
        for slug in classes:
            resp = self.app.get(f'/api/classes/{slug}/video')
            self.assertEqual(resp.status_code, 200)
            data = resp.get_json()
            self.assertEqual(data['slug'], slug)
            self.assertIsNotNone(data.get('video_url'), f"Classe {slug} sem video_url")
            self.assertIsNotNone(data.get('video_embed_url'), f"Classe {slug} sem video_embed_url")
            self.assertIsNotNone(data.get('video_credits'), f"Classe {slug} sem video_credits")
            
            # Checar que o HTML da classe renderiza o embed correspondente
            page_resp = self.app.get(f'/classes/{slug}')
            self.assertEqual(page_resp.status_code, 200)
            self.assertIn(data['video_embed_url'].encode('utf-8'), page_resp.data)
            self.assertIn(data['video_credits'].encode('utf-8'), page_resp.data)

        # 2. Testar POST para atualizar vídeo e depois restaurar
        original_sorc = self.app.get('/api/classes/sorcerer/video').get_json()
        test_payload = {
            'video_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'video_title': 'Guia Sorcerer Teste',
            'video_credits': 'Aion2 Community',
            'video_author_url': 'https://youtube.com/@aion2community'
        }
        post_resp = self.app.post('/api/classes/sorcerer/video', json=test_payload)
        self.assertEqual(post_resp.status_code, 200)
        post_data = post_resp.get_json()
        self.assertTrue(post_data['success'])
        self.assertEqual(post_data['class']['video_title'], 'Guia Sorcerer Teste')
        self.assertIn('embed/dQw4w9WgXcQ', post_data['class']['video_embed_url'])
        
        # Restaurar Sorcerer original
        self.app.post('/api/classes/sorcerer/video', json={
            'video_url': original_sorc['video_url'],
            'video_title': original_sorc['video_title'],
            'video_credits': original_sorc['video_credits'],
            'video_author_url': original_sorc['video_author_url']
        })

    def test_class_macros(self):
        classes = ["gladiator", "templar", "assassin", "ranger", "sorcerer", "elementalist", "cleric", "chanter"]
        for slug in classes:
            response = self.app.get(f'/classes/{slug}')
            self.assertEqual(response.status_code, 200)
            self.assertIn('Macros da Comunidade'.encode('utf-8'), response.data)
            self.assertIn(b'/Skill', response.data)
            self.assertIn(b'/Delay', response.data)
            self.assertIn('.txt'.encode('utf-8'), response.data)

    def test_class_macros_api_and_download(self):
        # 1. API JSON de macros
        response = self.app.get('/api/classes/gladiator/macros')
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(json_data['slug'], 'gladiator')
        self.assertTrue(len(json_data['macros']) >= 3)
        self.assertEqual(json_data['macros'][0]['id'], 'macro-gladiator-boss')
        self.assertIn('/Skill', json_data['macros'][0]['commands_raw'])

        # 2. Download do arquivo .txt
        dl_resp = self.app.get('/api/classes/gladiator/macros/macro-gladiator-boss/download')
        self.assertEqual(dl_resp.status_code, 200)
        self.assertIn('text/plain', dl_resp.headers.get('Content-Type', ''))
        self.assertIn('attachment', dl_resp.headers.get('Content-Disposition', ''))
        self.assertIn(b'/Skill Armor Murder', dl_resp.data)

    def test_progression_page(self):
        response = self.app.get('/progression')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Stigmas', response.data)
        self.assertIn(b'Daevanion Boards', response.data)
        self.assertIn(b'Monoliths', response.data)

    def test_gearing_page(self):
        response = self.app.get('/gearing')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Enhancement', response.data)
        self.assertIn(b'Enhancement Stones', response.data)
        self.assertIn(b'Manastones', response.data)
        self.assertIn(b'Godstones', response.data)
        self.assertIn(b'Soul Binding', response.data)
        self.assertIn(b'Inheritance', response.data)

    def test_enhancement_api_simulation(self):
        response = self.app.post('/api/enhancement-simulate', json={'current_level': 5})
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertTrue(json_data['success'])
        self.assertEqual(json_data['new_level'], 6)

    def test_tools_page(self):
        response = self.app.get('/ferramentas')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Ferramentas'.encode('utf-8'), response.data)
        self.assertIn('Tarefas'.encode('utf-8'), response.data)

        response_alias = self.app.get('/tools')
        self.assertEqual(response_alias.status_code, 200)

    def test_planner_page(self):
        for route in ['/planner', '/planejador']:
            response = self.app.get(route)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Planejador de Builds'.encode('utf-8'), response.data)
            self.assertIn(b'Daevanion Planner', response.data)
            self.assertIn(b'Daevanion Board', response.data)
            self.assertIn(b'Stigmas', response.data)

    def test_tracker_page(self):
        for route in ['/tracker', '/tarefas']:
            response = self.app.get(route)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Tarefas'.encode('utf-8'), response.data)
            self.assertIn(b'Main', response.data)
            self.assertIn(b'Alts', response.data)
            self.assertIn(b'Thiago Soares Ferreira', response.data)

    def test_map_page(self):
        for route in ['/mapa', '/map']:
            response = self.app.get(route)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Mapa'.encode('utf-8'), response.data)
            self.assertIn(b'QuestLog.gg', response.data)
            self.assertIn(b'Atreia', response.data)

    def test_404_page(self):

        response = self.app.get('/rota-inexistente')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'404', response.data)

if __name__ == '__main__':
    unittest.main()
