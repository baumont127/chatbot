from html import entities
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from utils.luis_bot import get_lui_api, get_lui_entity, get_lui_score
from app_veille.models import Ressource, Type_ressource, User
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from utils.tfidf_pipeline import clean_text, gen_vector_T, cosine_sim, cosine_similarity_T
from django.db.models import Q
from utils.tfidf_pipeline import pipeline_tfidf
from django_q.tasks import AsyncTask



@login_required(login_url='login')
def chatbot(request):
    current_user = request.user
    name_current_user = User.objects.filter(id=current_user.id)
    id_user = current_user.id
    context = {'name_current_user': name_current_user}
    nb_ressource_user = Ressource.objects.filter(user=id_user).filter(ressource_id__name='Article').count()
    
    if nb_ressource_user != 0:
        
        a = AsyncTask('utils.tfidf_pipeline.pipeline_tfidf', id_user)
        a.run()

    return render(request, 'ChatBot/chatbot.html', context=context)

def get_bot_response(request):
    user_text = request.POST.get('msg')
    current_user = request.user
    id_user = current_user.id

    type_ressource = get_lui_api(user_text)
    nb_ressource_user = Ressource.objects.filter(user=id_user).filter(ressource_id__name='Article').count()
    if nb_ressource_user != 0:

        if type_ressource == "articles" and get_lui_score(user_text, type_ressource ) > 0.5:
            """ Get articles from the database """
            if get_lui_entity(user_text) != None:

                entities = get_lui_entity(user_text)
                str_entities = ' '.join(entities)

                X = cache.get('X')
                vocabulary = cache.get('vocabulary')
                vectorizer = cache.get('vectorizer')
                df = cache.get('df')
                df_result = cosine_similarity_T(X, 5, str_entities, vectorizer, vocabulary, df)
                id_ressource = [int(ressource) for ressource in df_result["id"]]
        
                objects = Ressource.objects.filter(pk__in=id_ressource).filter(user_id=id_user)
                objects = dict([(obj.id, obj) for obj in objects])
                sql_querry = [objects[id] for id in id_ressource]

                result = [{'titre': row.titre, 'lien': row.lien} for row in sql_querry]
            else:
                sql_querry = Ressource.objects.raw(f"SELECT rs.id, titre, lien FROM app_veille_ressource AS rs INNER JOIN app_veille_type_ressource AS tr ON rs.ressource_id = tr.id WHERE tr.name ='Article' AND user_id = {id_user}")
                result = [{'titre': 'Veuillez précisser votre demande', 'lien': ''}]

        elif type_ressource == "video" and get_lui_score(user_text, type_ressource ) > 0.5:
            """ Get videos from the database """
            if get_lui_entity(user_text) != None:
                
                entities = get_lui_entity(user_text)
                if len(entities) > 1:
                    sql_querry = Ressource.objects.raw(f"SELECT rs.id, titre, lien FROM app_veille_ressource AS rs INNER JOIN app_veille_type_ressource AS tr ON rs.ressource_id = tr.id WHERE (tr.name ='Video' AND rs.user_id = {id_user} AND (key_word LIKE '%{entities[0]}%' OR key_word LIKE '%{entities[1]}%')) OR (tr.name ='Video' AND rs.user_id = {id_user} AND (titre LIKE '%{entities[0]}%' OR titre LIKE '%{entities[1]}%'))")
                else:
                    sql_querry = Ressource.objects.raw(f"SELECT rs.id, titre, lien FROM app_veille_ressource AS rs INNER JOIN app_veille_type_ressource AS tr ON rs.ressource_id = tr.id WHERE (tr.name ='Video' AND user_id = {id_user} AND titre LIKE '%{entities[0]}%') OR (tr.name ='Video' AND user_id = {id_user} AND key_word LIKE '%{entities[0]}%')")
            else:
                sql_querry = Ressource.objects.raw(f"SELECT rs.id, titre, lien FROM app_veille_ressource AS rs INNER JOIN app_veille_type_ressource AS tr ON rs.ressource_id = tr.id WHERE tr.name ='Video' AND user_id = {id_user}")
            
            result = [{'titre': row.titre, 'lien': row.lien} for row in sql_querry]

        elif type_ressource == "video et articles avec sujet" and get_lui_score(user_text, type_ressource ) > 0.5:
            """ Get videos and articles from the database """
            if get_lui_entity(user_text) != None:
                entities = get_lui_entity(user_text)
                if len(entities) > 1:
                    sql_querry = Ressource.objects.raw(f"SELECT id, titre, lien FROM app_veille_ressource WHERE (titre LIKE '%{entities[0]}%' OR titre LIKE '%{entities[1]}%') OR (key_word LIKE '%{entities[0]}%' OR key_word LIKE '%{entities[1]}%')")
                else:
                    sql_querry = Ressource.objects.raw(f"SELECT id, titre, lien FROM app_veille_ressource WHERE (titre LIKE '%{entities[0]}%') OR (key_word LIKE '%{entities[0]}%')")
            else:
                sql_querry = Ressource.objects.raw(f"SELECT id, titre, lien FROM app_veille_ressource")

        
            result = [{'titre': row.titre, 'lien': row.lien} for row in sql_querry]
        else:

            result = [{'titre': "Je n'ai pas compris votre requêtes", 'lien': ""}]
    else:
        result = [{'titre': "Vous n'avez pas encore de ressource", 'lien': ""}]

    return JsonResponse({"operation_result": result})
