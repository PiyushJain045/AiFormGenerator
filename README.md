- [Video Demo](https://youtu.be/t-1YEd-Y4sE) 
- [Ai Form Generator](http://16.171.33.245:8000/)  | Note: not optimized for mobile
# AI Form Generator 🤖📝  

Welcome to **AI Form Generator**, where Wall-E, the lovable robot, guides you through the magical world of form creation! 🚀  

Powered by **Gemini 1.5 Flash**, this web app transforms simple inputs into dynamic, customizable forms, perfect for surveys, feedback, or even quirky pizza polls. With a **3D Wall-E model** keeping you entertained, form-building becomes fun, interactive, and engaging.  

Users can **generate, edit, save, and analyze responses**—all while enjoying seamless authentication with Django’s `allauth`.  

Who said forms had to be boring? Let’s build **smarter, more exciting forms** together! 🎉 

---

## Features
- **AI-Powered Form Generation**: Input your form requirements, and the AI generates a form in seconds.
- **Dynamic Form Customization**: Add or remove fields dynamically using HTMX.
- **Form Saving & Sharing**: Save your forms and share them with others via a unique link.
- **Response Analysis**: View total responses and visualize data with bar graphs.
- **Wall-E Guidance**: A 3D model of Wall-E guides you through the process, making form creation interactive and fun.
- **User Authentication**: Secure user authentication and form management using Django's `allauth`.
- **Design Template Selection**: Choose from a variety of pre-made designs to customize the appearance of your form with just a click.

--- 

## Tech Stack
- **Frontend**: Webflow, HTML, CSS, JavaScript, HTMX
- **Backend**: Django (Python)
- **3D Model Integration**: Spline (Credits to [VictorGG](https://app.spline.design/community/file/9246a5ca-7437-4bc7-9f6e-58b84d4e932f))
- **AI Model**: Gemini 1.5 Flash (via Google's Generative AI API)
- **Database**: SQLite (default for Django, can be swapped for PostgreSQL/MySQL)
- **Authentication**: Django Allauth
- **Data Visualization**: Matplotlib, Pandas

---

### How My AI Form Builder Helps the Community

- **Empowers Non-Technical Users**: AI-driven form generation enables anyone, regardless of technical skill, to create professional forms easily, benefiting small businesses, educators, and non-profits.
- **Streamlines Data Collection**: The dynamic form-building process simplifies gathering and analyzing data, helping organizations collect insights and make informed decisions efficiently.
- **Facilitates Collaboration**: Sharing forms via unique links encourages collaboration, allowing community members to easily provide feedback and contribute.
  
---

### Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/PiyushJain045/AiForm-Generator.git
   cd AiForm-Generator

2. **Setup a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt

4. ** Add Your Gemini API key in .env file **:
   ```bash
   GEMINI_API_KEY="Add your gemini-1.5-flash API key"

5. **Run Migrations**:
   ```bash
   python manage.py makemigration
   python manage.py migrate

6. **Start the Development Server**:
   ```bash
   python manage.py runserver

**And voilà! Your setup is complete.** 🎉  

**Thanks for checking out this repo!** 🙌  

