from celery import shared_task
import graphene
from vidhya.models import Course, Language
# from .gqMutations import TranslateTextMutation
from django.db.models import Q
import requests
from django.conf import settings
from google.cloud import translate_v2 as translate
from django.conf import settings


@shared_task(name='tasks.updateTranslation')
def updateTranslation(**kwargs):
    # Detect language type
    # If language type is detected then check the variation by comparing it with translate column and default values
    # Handle with  resource name for dynamic purpose like authorization.py
    if(settings.ENV_CELERY_TASK):
        qs = Course.objects.filter(~Q(translate__isnull=True) | ~Q(translate='')).distinct().order_by('id')
        for input in qs:        
            translate_object={}
            courseins = {'title':input.title,'blurb':input.blurb,'description':input.description}
            translate_object = TranslateTextMutation.translate_data(None, courseins)
            input.translate=translate_object
            input.save()
    
class TranslationInput(graphene.InputObjectType):
    text = graphene.String(required=True)
    target_language = graphene.String(required=True)

class TranslateTextMutation(graphene.Mutation):
    class Arguments:
        translation_input = TranslationInput(required=True)

    translated_text = graphene.String()

    def mutate(translation_input,**kwargs):
        target_language = translation_input['target_language']
        translate_instance = {}
        for index,item in  enumerate(translation_input['object'], start=1):
            google_translation_endpoint =  settings.ENV_TRANSLATION_ENDPOINT + settings.ENV_TRANSLATION_KEY
            google_translation_detect_endpoint = 'https://translation.googleapis.com/language/translate/v2/detect?key=' + settings.ENV_TRANSLATION_KEY
            try:
                headers = {
                'Content-Type': 'application/json',
                }
                translateDetectParam = {
                    'q': translation_input['object'][item],
                }
                response = requests.post(google_translation_detect_endpoint, data=translateDetectParam)
                if response.status_code == 200:
                    # Parsing JSON response
                    result = response.json()     
                    # Output the detected language
                    if 'language' in result['data']['detections'][0][0]:
                        language_code = result['data']['detections'][0][0]['language']
                        data = {
                        'q': translation_input['object'][item],
                        'target': language_code,
                        'format': 'text'
                        }
                        response = requests.post(google_translation_endpoint, headers=headers, json=data)
                        translation_result = response.json()
                        if response.status_code == 200:
                            translated_text = translation_result['data']['translations'][0]['translatedText']
                            translate_instance.update({item:translated_text})
                            if(index==len(translation_input['object'])):
                                return translate_instance
                        else:
                            return None
                    else:
                        print('Language detection failed.')
                else:
                    print(f'Error during translation: {response.status_code} - {response.text}')
            
                
            except requests.exceptions.RequestException as e:
                print(f"Error during translation: {e}")
                return None

    def translate_data(self,input=None):
        targetLanguages = []
        languages=Language.objects.filter(active=True).values_list('short_code', flat=True)
        for name in languages:
            targetLanguages.append(name)
        tranlate_object={}

        for language in targetLanguages:
            translation_input = {
                'object': input,
                'target_language': language
            }
            translation_result = TranslateTextMutation.mutate(translation_input) 
            # Extract the translated text from the result
            if translation_result is not None:
                translated_text = translation_result
                tranlate_object.update({language:translation_result})
            else:
                translated_text = translation_result
                tranlate_object.update({language:translation_result})
        return tranlate_object