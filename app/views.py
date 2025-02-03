from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.urls import reverse
from .models import UserFormTemplate, FormResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Import for form analysis feature
import pandas as pd
from io import BytesIO
import base64
import matplotlib.pyplot as plt

# Imports for Environment Variable
import os
from dotenv import load_dotenv
load_dotenv() 

# Setup GEMINI API
import google.generativeai as genai
# Prompt which is passed to the LLM
pr = """you are being used in a automatic form generation web application so don't response with any additional text (e.g., explanations or formatting artifacts). directly respons in json format. Generate a set of questions for a form in JSON format with the accurate html tags. Each question should have: - A type (e.g., "text", "slider", "multiple-choice", "single-choice", "dropdown-list"). - A text field for the question. - Additional fields depending on the type, such as min, max for sliders, or choices for multiple-choice, single-choice and dropdown-list questions. Example output: { "questions": [ { "type": "slider", "text": "Rate your satisfaction on a scale of 1-10.", "min": 1, "max": 10 }, { "type": "text", "text": "What is your name?" }, { "type": "multiple-choice", "text": "Choose your favorite fruit:", "choices": ["Apple", "Banana", "Cherry"] } ] } Now, generate JSON for the following input: \n"""
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

unnamed_form_counter = 0


class home(View):
    def get(self, request):
        return render(request, "index.html")

    def post(self, request):
        
        # Retrieving the form data from the POST request
        print("Inside Post")
        form_description = request.POST.get('form_description')
        goal_objective = request.POST.get('goal_objective')
        target_audience = request.POST.get('target_audience')
        tone_style = request.POST.get('tone_style')
        num_questions = request.POST.get('num_questions')
        question_preferences = request.POST.get('question_preferences')

        # Validation of form inputs
        errors = []

        if not form_description:
            errors.append("Form description is required.")
        if not goal_objective:
            errors.append("Goal/objective is required.")
        if not target_audience:
            errors.append("Target audience is required.")
        if not tone_style:
            errors.append("Preferred tone/style is required.")
        if not num_questions:
            errors.append("Number of questions is required.")
        if not question_preferences:
            errors.append("Question preferences are required.")
        
        # If there are any validation errors, return them in the response
        if errors:
            message = "Please fix the following errors:\n" + "\n".join(errors)
            return render(request, "index.html", {"message": message})

        # If no validation errors, continue
        print("Stage 1: Clear")

        prompt = (f"""{pr}"""
            f"Generate a form with the following details:\n\n"
            f"Form Description: {form_description}\n"
            f"Goal/Objective: {goal_objective}\n"
            f"Target Audience: {target_audience}\n"
            f"Preferred Tone/Style: {tone_style}\n"
            f"Number of Questions: {num_questions}\n"
            f"Question Preferences: {question_preferences}\n"
            f"Provide a list of {num_questions} form questions with their types (e.g., text, checkbox, radio)."
        )
      

        try:
            response = model.generate_content(prompt)

            # Ensuring that only 'json' part is extracted  
            start_index = response.text.find('{') 
            end_index = response.text.rfind('}')

            if start_index != -1 and end_index != -1:
                json_string = response.text[start_index:end_index + 1] 
                    
            else:
                message = "Error Occured with start and end index"
                return render(request, "index.html", {"message": message})
            
            form_data = json.loads(json_string)
            for question in form_data['questions']:
                print(question)

            return render(request, "dynamic_form.html", {"form_data": form_data, "flag": True})

        except Exception as e:
            print(f"Error generating form: {e}")
            message = "Error Occured while generating the form"
            return render(request, "index.html", {"message": message})


# Handels the edit for the form generated using HTMX
class add_field(View):
    def get(self, request):
        return render(request,"partials/add_field_form.html", {"flag": False})

    def post(self, request):
        # Get form data from the POST request
        field_label = request.POST.get('field_label')
        field_type = request.POST.get('field_type')

        # Print the result in the terminal( for testting purpose )
        # print(f"Field Label: {field_label}")
        # print(f"Field Type: {field_type}")


        # Construct JSON based on selected option by user as well as gemini generated. 

        #1)Range
        if field_type == "range":
            min_value = request.POST.get('min_value')
            max_value = request.POST.get('max_value')
            print(min_value, max_value)

            json_data = {
                "questions": [
                    {
                        "type": "slider",
                        "text": field_label,
                        "min": int(min_value),
                        "max": int(max_value),
                        "labels": {
                            "1": "Very Dissatisfied",
                            "2": "Dissatisfied",
                            "3": "Neutral",
                            "4": "Satisfied",
                            "5": "Very Satisfied"
                        }
                    }
                ]
            }

        #2)Radio Button
        elif field_type == "radio":
            options = request.POST.get('options')
            options_list = options.split(',') if options else []
            print(options_list)

            json_data = {
                "questions": [
                    {
                        "type": "single-choice",
                        "text": field_label,
                        "choices": options_list
                    }
                ]
            }

        #3) Checkbox
        elif field_type == "checkbox":
            options = request.POST.get('options')
            options_list = options.split(',') if options else []
            print(options_list)

            json_data = {
                "questions": [
                    {
                        "type": "multiple-choice",
                        "text": field_label,
                        "labels": options_list
                    }
                ]
            }

        #4) text
        elif field_type == "text":
            json_data = {
                "questions": [
                    {
                        "type": "text",
                        "text": field_label
                    }
                ]
            }

        #5) Textbox
        elif field_type == "textbox":
            json_data = {
                "questions": [
                    {
                        "type": "textbox",
                        "text": field_label
                    }
                ]
            }

        else:
            return HttpResponse("Invalid field type", status=400)

        return render(request, "partials/partial_df.html", {"form_data": json_data, "flag": True})

# Remove the added field
def remove_form(request):
    return render(request, "partials/partial_df.html", {"flag": True})

# add suboptions
class GetSuboptions(View):
    def get(self, request):
        field_type = request.GET.get('field_type')

        if field_type == 'range':
            type = "range"
            # Return fields for min_value and max_value
            return render(request, 'partials/options_suboptions.html', {"type": type})
        
        elif field_type == 'radio':
            # Return fields for options input
            type = "radio"
            return render(request, 'partials/options_suboptions.html', {"type": type})
        
        elif field_type == 'checkbox':
            # Return fields for options input
            type = "checkbox"
            return render(request, 'partials/options_suboptions.html', {"type": type})
        
        elif field_type == 'textbox':
            type = "textbox"
            # Return fields for options input
            return render(request, 'partials/options_suboptions.html', {"type": type})
        
        elif field_type == 'text':
            type = "text"
            # Return fields for options input
            return render(request, 'partials/options_suboptions.html', {"type": type})



@csrf_exempt #No csrf verification required
def save_form_data(request):
    global unnamed_form_counter

    if request.method == "GET":
        try:
            # Get the logged-in user and retrive all the saved forms created by user
            user = request.user
            user_forms = UserFormTemplate.objects.filter(user=user).order_by("-created_at")
            context = {
                "user_forms": user_forms,
            }

            # print(context)
            # print(context['user_forms']) for testing purpose
            return render(request, "myforms.html", {"forms_list": context['user_forms']})
        
        except Exception as e:
            print(e)
            return render(request, "myforms.html")
        
    if request.method == "POST":
        try:
            unnamed_form_counter += 1
            data = json.loads(request.body)
            html_code = data.get("html_code")
            css_files = data.get("css_files")
            form_name = data.get("form_name", f"Form {unnamed_form_counter}")
            # print(html_code) #Testing Purpose

            # Save form data associated with the logged-in user
            user = request.user
            form_template = UserFormTemplate.objects.create(
                user=user,
                name=form_name,
                html_code=html_code,
                css_files=','.join(css_files),
            )
            return JsonResponse({"status": "success", "message": "Form created successfully!"})
        
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    


def view_form(request, form_id):
    if request.method == "GET":
        try:
            form = get_object_or_404(UserFormTemplate, id=form_id, user=request.user)
            return render(request, "user_form.html", {"html_code":form.html_code, "form_id": form_id, "form_css": form.css_files})
        except Exception as e:
            return render(request, "user_form.html", {"error": str(e)})
        
        
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            html_code = data.get("html_code")
            css_files = data.get("css_files")
            form_name = data.get("form_name", f"Form {unnamed_form_counter}")

            # Save form data associated with the logged-in user
            user = request.user

            if form_id:
                # Update the form if it exists for the given id and user
                form_template, created = UserFormTemplate.objects.update_or_create(
                    id=form_id,
                    user=user,
                    defaults={
                        "name": form_name,
                        "html_code": html_code,
                        "css_files": ','.join(css_files),
                    }
                )
            else:
                # Create a new form if no id is provided
                form_template = UserFormTemplate.objects.create(
                    user=user,
                    name=form_name,
                    html_code=html_code,
                    css_files=','.join(css_files),
                )
                created = True

            message = "Form created successfully!" if created else "Form updated successfully!"
            return JsonResponse({"status": "success", "message": message})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})



# Logic to share form link
def share_form(request, unique_id):
        if request.method == "GET":
        # Generate the full URL for the unique_id
            base_url = request.build_absolute_uri(reverse("fill-form", args=[unique_id]))
            return render(request, "share_form.html", {"shareable_link": base_url})



## Logic for others to fill the form
@csrf_exempt 
def fill_form(request, unique_id):
    form_template = get_object_or_404(UserFormTemplate, unique_id=unique_id)
    
    if request.method == "POST":
        # Handle form submission from a randommperson.

        # print("INSIDE POST") testing purpose
        # print(unique_id) Testing Purpose
        response_data = dict(request.POST)
        # print(response_data)
        response_data.pop("csrfmiddlewaretoken", None) 
        FormResponse.objects.create(
            form_template= form_template,
            user=request.user if request.user.is_authenticated else None,
            response_data=response_data,
        )
        user=request.user if request.user.is_authenticated else None
        print(user)
        return render(request, "form_saved_succ.html", {"unique_id": unique_id, "user": user})
    
    
    
    # Fetch the form template using the unique_id
    form_template = get_object_or_404(UserFormTemplate, unique_id=unique_id)
    html_code = form_template.html_code
    css_path = form_template.css_files
    print("CSS FILES:", css_path)

    start_remove = '<div class="add-field">'

    start_index = html_code.find(start_remove)
    # print("Start Index", start_index) #Testing purpose

    if start_index != -1:
        sliced_html_code = html_code[:start_index] 

    sliced_html_code = sliced_html_code.replace('/User-Forms', f'/fill-form/{unique_id}/')

    # print(sliced_html_code)
    return render(request, "fill_form.html", {"form_template": sliced_html_code, "unique_id": unique_id, "css_path":css_path})


# Handels the form analysis feautre.
def analysis(request, unique_id):
        if request.method == "GET":
        # Fetch the form and responses
            try:
                form = get_object_or_404(UserFormTemplate, unique_id=unique_id)
                responses = FormResponse.objects.filter(form_template=form)

                # 1) Total Users
                total_users = responses.count()

                # Convert responses to a DataFrame
                data = [response.response_data for response in responses]
                df = pd.DataFrame(data)

                # 2) Radio graph. Only Radio graph for now.
                if "same-radio" in df.columns:
                    same_radio_counts = df["same-radio"].explode().value_counts()
                else:
                    same_radio_counts = pd.Series([])

                # Generate a graph using Matplotlib
                plt.figure(figsize=(6, 4))
                same_radio_counts.plot(kind="bar", color="skyblue", alpha=0.7)
                plt.title("Responses to 'same-radio'")
                plt.xlabel("Choices")
                plt.ylabel("Count")
                plt.xticks(rotation=45)
                plt.tight_layout()

                # Save the graph to a BytesIO buffer
                buffer = BytesIO()
                plt.savefig(buffer, format="png")
                buffer.seek(0)
                graph_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
                buffer.close()
                plt.close()
            except TypeError as e:
                print(f"Error generating plot: {e}")
                graph_image = None

                # Pass the graph to the template
                return render(
                    request, 
                    "form_analysis.html", 
                    {"unique_id": unique_id, "graph_image": graph_image, "total_users": total_users, 
                     "error_message": None if graph_image else "No response submitted to your form yet 🥺"
                     }
                )
        
# Designs for form. Coming Soon...
def templates_view(request, slug):
    if request.method == "GET":
        print("Inside************")
        print("SLUG:",slug)
        return render(request, 'designs.html', {"slug": slug})

    if request.method == "POST":
        slug = request.POST.get("slug")
        print(slug)
        return render(request, "view_design.html", {"slug": slug})

def dynamic_form_view(request):
    # Get selected design from GET request (default to 'dynamic_form.css' if none is selected)
    selected_design = request.GET.get("selected_design", "dynamic_form")
    slug = request.GET.get("slug")
    print(slug)
    # Construct the correct CSS file path
    css_path = f"/static/css/designs/{selected_design}.css" if selected_design != "dynamic_form" else "css/dynamic_form.css"
    print(css_path)

    try:
        form = get_object_or_404(UserFormTemplate, id=slug, user=request.user)
        return render(request, "user_form.html", {"html_code":form.html_code, "form_id": slug, "form_css": css_path})
    except Exception as e:
        return render(request, "user_form.html", {"error": str(e)})

def demo_design(request):
    if request.method == "GET":
        return render(request, "demo_design.html")

    if request.method == "POST":
        selected_design = request.POST.get("selected_design", "dynamic_form")

        print(selected_design)
        return render(request, "view_design.html", {"selected_design":selected_design})