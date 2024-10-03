import json
import base64
from email import message_from_bytes
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import logging

from openai import OpenAI
from insuradmin_backend.settings import OPENAI_API_KEY
from utils.decorators import ajax_required
from utils.mixins import FormErrors
from .forms import InputForm
from insuradmin_backend.settings import SENDGRID_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)
logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class InsuranceAssistantEmailView(generic.View):

    def post(self, request, *args, **kwargs):
        data = {'result': 'Error', 'message': "Something went wrong, please try again", "redirect": False, "data": None}
        try:
            # Log the incoming request
            logger.info("Received request: %s", request.body)

            # Ensure that the request body is in JSON format
            try:
                request_json = json.loads(request.body)
                logger.info("Parsed JSON: %s", request_json)
            except json.JSONDecodeError:
                data['message'] = "Invalid JSON payload"
                logger.error("Invalid JSON payload: %s", request.body)
                return JsonResponse(data, status=400)

            raw_email_base64 = request_json.get('raw_email')
            if not raw_email_base64:
                data['message'] = "No raw email provided"
                logger.error("No raw email provided")
                return JsonResponse(data, status=400)

            # Decode the base64 encoded email
            raw_email = base64.b64decode(raw_email_base64)
            email_message = message_from_bytes(raw_email)
            logger.info("Email message: %s", email_message)

            email_subject = email_message.get('subject', '')
            email_from = email_message.get('from', '')
            email_body = ""

            if email_message.is_multipart():
                for part in email_message.walk():
                    if part.get_content_type() == "text/plain":
                        email_body = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8')
                        break
            else:
                email_body = email_message.get_payload(decode=True).decode(email_message.get_content_charset() or 'utf-8')

            # Log the email body
            logger.info("Email body to process with GPT: %s", email_body)

            # Process the email with GPT model
            processed_text = self.process_with_gpt(email_body)

            # Log the GPT response
            logger.info("Processed text from GPT: %s", processed_text)

            # Send the processed information as a response email
            self.send_email(email_from, f'Re: {email_subject}', processed_text)

            data.update({
                'result': "Success",
                'message': "The email has been processed and a response has been sent",
                'data': processed_text
            })
        except Exception as e:
            logger.error("Error processing request: %s", str(e))
            data['message'] = f'Error: {str(e)}'
            return JsonResponse(data, status=500)

        return JsonResponse(data)

    def process_with_gpt(self, email_body):
        try:
            # prompt = (
            #     "You are an assistant tasked with drafting professional email responses. "
            #     "Generate a polite, professional email based on the following input: \n\n"
            #     f"{email_body}\n\n"
            #     "Make sure the email is in HTML format."
            # )
            ################ EMAIL OUTPUT 4SCRIPTS ############################
            # prompt = (
            #     "Du bist ein professioneller Versicherungsassistent. "
            #     "Antworte in der Sprache des Benutzers und löse sein Problem basierend auf den folgenden Eingaben: \n\n"
            #     f"{email_body}\n\n"
            # )
            ################ EMAIL OUTPUT 4SCRIPTS ############################
            prompt = (
                "Du bist ein professioneller Versicherungsassistent. "
                "Antworte in der Sprache des Benutzers und löse sein Versicherungsproblem"
            )
            logger.info("Sending to GPT-4: %s", prompt)
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500
            )
            gpt_response = response.choices[0].message.content.strip()
            logger.info("Received from GPT-4: %s", gpt_response)
            return gpt_response
        except Exception as e:
            logger.error("Error in GPT processing: %s", str(e))
            return "Error in processing the email with GPT-4."

    def send_email(self, to_email, subject, content):
        try:
            message = Mail(
                from_email='service@duewiger.com',
                to_emails='kd@duewiger.com',
                subject=subject,
                html_content=content
            )
            sg = SendGridAPIClient(api_key=SENDGRID_API_KEY)
            response = sg.send(message)
            logger.info(f"Email sent successfully: {response.status_code}")
        except Exception as e:
            logger.error("Error sending email: %s", str(e))

class InsuranceAssistantView(generic.FormView):
    template_name = "assistant/assistant.html"
    form_class = InputForm
    success_url = "/"

    def generate_prompt(self, user_input):
        return (
            ##### EMAIL 4SCRIPTS #####
            # "You are a personal insurance assistant for customers of insurances and insurance or finance brokers. "
            # "Use the user's message to summarize what their intention is and try your best to create an professional email in relation to this keyword, which will be forwarded to the insurance or broker of the customer."
            # f"User input: {user_input}"
            ##### EMAIL 4SCRIPTS #####
            "Du bist ein professioneller Versicherungsassistent. "
            "Antworte in der Sprache des Benutzers und löse sein Versicherungsproblem"
            f"User input: {user_input}"
        )

    @method_decorator(ajax_required)
    def post(self, request, *args, **kwargs):
        data = {'result': 'Error', 'message': "Something went wrong, please try again", "redirect": False, "data": None}
        form = InputForm(request.POST)
        if form.is_valid():
            user_input = form.cleaned_data.get("input")
            prompt = self.generate_prompt(user_input)

            try:
                response = client.chat.completions.create(
                    model="gpt-4-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.6,
                )
                data.update({
                    'result': "Success",
                    'message': "The insurance assistant has generated a response",
                    'data': response.choices[0].message.content.strip()
                })
            except Exception as e:
                data['message'] = f'Error: {str(e)}'
                return JsonResponse(data, status=500)

            return JsonResponse(data)

        else:
            data["message"] = FormErrors(form)
            return JsonResponse(data, status=400)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assistant_messages'] = []
        return context


  
    
#     # def check_for_scripts(self, user_input):
#     #     # Definierte Schlüsselwörter und zugeordnete Skripte
#     #     scripts = {
#     #         "cancellation": "cancellation.py",
#     #         "termination": "cancellation.py",
#     #         "change bankdaten": "change_bankdaten.py",
#     #         # Füge hier weitere Schlüsselwörter und Skripte hinzu
#     #     }

#     #     for keyword, script in scripts.items():
#     #         if keyword in user_input.lower():
#     #             return script
#     #     return None

# # "When asked a question, try your best to transform the user input into a professional email message which "
# # "will be forwarded to the insurance or broker of the customer. "
# # "Use the user's message to summarize what their intention is. And ask the user whether he would like to carry out the action behind the respective keyword"
#     def generate_prompt(self, user_input):
#         # script = self.check_for_scripts(user_input)
#         # if script:
#         #     # Hier kannst du die spezifische Logik zum Ausführen des Skripts einfügen
#         #     # Beispiel: `exec(open(script).read())`
#         #     return f"Running specific script for keyword detected: {script}"
#         # else:
#         #     return (
#         #         "You are a personal insurance assistant for customers of insurances and insurance or finance brokers. "
#         #         "Use the user's message to summarize what their intention is. And ask the user whether he would like to carry out the action behind the respective keyword. "
#         #         f"User input: {user_input}"
#         #     )
#         return (
#             "You are a personal insurance assistant for customers of insurances and insurance or finance brokers. "
#             "Use the user's message to summarize what their intention is and try your best to create an professional email in relation to this keyword, which will be forwarded to the insurance or broker of the customer."
#             f"User input: {user_input}"
#         )

#     @method_decorator(ajax_required)
#     def post(self, request, *args, **kwargs):
#         data = {'result': 'Error', 'message': "Something went wrong, please try again", "redirect": False, "data": None}
#         form = InputForm(request.POST)
#         if form.is_valid():
#             user_input = form.cleaned_data.get("input")
#             prompt = self.generate_prompt(user_input)

#             try:
#                 response = client.chat.completions.create(
#                     model="gpt-4-turbo",
#                     messages=[{"role": "user", "content": prompt}],
#                     temperature=0.6,
#                 )
#                 data.update({
#                     'result': "Success",
#                     'message': "The insurance assistant has generated a response",
#                     'data': response.choices[0].message.content.strip()
#                 })
#             except Exception as e:
#                 data['message'] = f'Error: {str(e)}'
#                 return JsonResponse(data, status=500)

#             return JsonResponse(data)

#         else:
#             data["message"] = FormErrors(form)
#             return JsonResponse(data, status=400)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['assistant_messages'] = []
#         return context

# from django.views import generic
# from django.utils.decorators import method_decorator
# from django.http import JsonResponse

# from utils.decorators import ajax_required
# from utils.mixins import FormErrors

# from openai import OpenAI

# from insuradmin_backend.settings import OPENAI_API_KEY
# from .forms import InputForm


# # Insurance Assistent API
# client = OpenAI(api_key=OPENAI_API_KEY)

# class InsuranceAssistantView(generic.FormView):
#     template_name = "assistant/assistant.html"
#     form_class = InputForm
#     success_url = "/"
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
        
#         try:
#             # Create the Assistant
#             assistant = client.beta.assistants.create(
#                 instructions="You are a personal insurance assistant for customers of insurances and insurance or finance brokers. When asked a question, try your best to transform the user input into a professional email message which will be forwarded to the insurance or broker of the customer.",
#                 name="Insurance Assistant",
#                 model="gpt-4-turbo",
#             )
            
#             # Create the Thread
#             thread = client.beta.threads.create()
            
#             # Add the message to the thread
#             message = client.beta.threads.messages.create(
#                 thread_id=thread.id,
#                 role="user",
#                 content="Initial message or user input",
#             )
            
#             # Run the Assistant
#             run = client.beta.threads.runs.create(
#                 thread_id=thread.id,
#                 assistant_id=assistant.id,
#             )
            
#             # Retrieve the Assistant's Response
#             run = client.beta.threads.runs.retrieve(
#                 thread_id=thread.id,
#                 run_id=run.id,
#             )
            
#             # Get all messages from the thread
#             messages = client.beta.threads.messages.list(
#                 thread_id=thread.id
#             )
            
#             # Store messages in context as a list of dictionaries
#             context['assistant_messages'] = [
#                 {"role": message.role, "content": message.content[0].text.value}
#                 for message in reversed(messages.data)
#             ]
        
#         except Exception as e:
#             context['assistant_messages'] = [{'role': 'error', 'content': f'Error: {str(e)}'}]
        
#         return context