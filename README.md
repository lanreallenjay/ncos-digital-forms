# NCoS Forms & Books Catalogue

An AI-powered digital reference tool for cataloguing official forms and registers used in the Nigerian Correctional Service (NCoS). Built as part of the 3MTT Product Management capstone project, this app provides a searchable and smart interface to explore over 100 correctional administrative documents. This app was inspired by the reality that across our correctional centres, where we rely heavily on structured forms and official books to carry out key duties—from admitting inmates to processing rations and court orders. However, these resources are becoming less familiar to newer officers, many of whom don’t know what the forms are for or how to use them. This knowledge gap affects operational flow and professionalism.

*Note
The Forms and Books Titles used for the purpose of this showcase are obsolete as their names have changed by the NCoS Acts 2019 while some are not used any longer. The point of using them is to just showcase the solutions while while not going against the ethics of the service.


[Click Here to view the app](https://ncos-digital-forms-fvjvdpsikyhrtcfn5y3xpw.streamlit.app/#1-a-additional-information-of-superintendent)
---

## Project Overview

This Streamlit-based web app allows users to:

- Browse through a catalogue of forms and books by title or form number
- Use AI to generate helpful descriptions of each form on-demand
- Click on any form title to view the auto-generated description dynamically
- Experience a smooth, no-login interface for simplicity and accessibility

---

## Features

| Feature                             | Description                                                                 |
|------------------------------------|-----------------------------------------------------------------------------|
| Search Functionality            | Search by form title or number to quickly locate entries                    |
| AI Description Generator        | Uses OpenAI API to auto-generate form descriptions                         |
| Click-to-Reveal Descriptions   | Click on any form title to reveal the description (hover alternative not supported on Streamlit) |
| Lightweight Catalogue File      | Easy-to-update CSV file for seamless data management                        |
| Modular Codebase                | Built for future expansion (e.g., edit history, filtering by department)    |

---

## Tech Stack

- **Python 3.11+**
- **Streamlit**
- **Pandas**
- **OpenAI Python SDK (`openai` v1.x)**
- **Dotenv**
- **Git & GitHub**

---

## Project Structure

ncos-digital-forms/ ├── app.py                   # Main Streamlit app ├── forms_catalogue.csv      # Master file of forms & descriptions ├── .env                     # Stores your API key securely ├── requirements.txt         # Python dependencies └── README.md                # You're reading it

---

## ⚙️ Setup Instructions

1. **Clone this Repository**
   ```bash
   git clone https://github.com/lanreallenjay/ncos-digital-forms.git
   cd ncos-digital-forms

2. Create & Activate Virtual Environment

python -m venv venv
venv\Scripts\activate   # On Windows


3. Install Dependencies

pip install -r requirements.txt


4. Set up .env file Create a .env file in the root directory and paste your OpenAI API key:

OPENAI_API_KEY=your_openai_key_here


5. Run the App

streamlit run app.py




---

AI Integration

The app uses the OpenAI gpt-3.5-turbo model to generate descriptions of correctional forms. API responses are shown instantly when you click on a form title. Generated outputs are not stored permanently — ensuring minimal cost and a clean UX.


---

Future Improvements

[ ] Add admin role to approve or edit generated descriptions

[ ] Track edit history and contributor log

[ ] Export catalogue as PDF or Excel

[ ] Add category and department filters

[ ] Enable offline (static) export option

This is a practical, scalable, and easy-to-use solution built for internal government operations. It can be adapted to other ministries, agencies, or even local governments—anywhere structured documentation is key.


---

Project Credits

Developed by Anjorin Olanrewaju Olumuyiwa, Product Manager, Scrum Master & Public Relations Officer at the Nigerian Correctional Service (Oyo Command), as part of the 3MTT Nigeria Product Management program.

[Let’s connect on LinkedIn](https://www.linkedin.com/in/olanrewaju-anjorin-73719a29?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)


---

Acknowledgements

Streamlit

OpenAI

3MTT – 3 Million Technical Talent Initiative

Fellow learners, mentors, and instructors at the 3MTT Cohort 3



---

License

This project is licensed under the MIT License.


---

Feedback & Contributions

Pull requests, issues, and suggestions are welcome! Let’s work together to digitize public service workflows.

> “From analog records to AI-powered references — building for national transformation.”

Added detailed README with setup, AI features, and credits
