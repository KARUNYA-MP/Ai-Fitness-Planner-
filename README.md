# AI Fitness Planner - Frontend Web Application

A modern, responsive, and aesthetic frontend UI for an **AI Fitness Planner** web application built using **Python Django**, **Django Templates**, **HTML5**, **CSS3**, and **JavaScript** (with Chart.js and Font Awesome 6).

---

## 🌟 Key Highlights & Features

- **Clean Green & White Design Aesthetic**: Styled with an emerald green primary palette (`#10b981`), crisp white cards, light background (`#f8fafc`), soft shadows, and modern typography (*Plus Jakarta Sans*).
- **Responsive Layout**:
  - **Public Pages**: Modern sticky header with brand logo, smooth navigation links, and footer.
  - **Dashboard & App Pages**: Desktop fixed sidebar with active indicators; responsive collapsible drawer with hamburger toggle on tablet and mobile.
- **Dynamic Frontend Interactions**:
  - Multi-step onboarding flow (*Personal Details* → *Fitness Goal* → *BMI & Plan*).
  - Interactive BMI gauge with live height and weight calibration sliders.
  - Interactive water hydration tracker (`+ Log Glass` and `-` with animated progress).
  - Interactive checklist on today's workout with real-time percentage completion calculation.
  - Workout session timer modal with Play/Pause and countdown demo.
  - Interactive daily meal tabs (*Breakfast*, *Lunch*, *Evening Snack*, *Dinner*) with macro nutrients and healthy food tips.
  - Clickable 30-Day calendar with visual states (*Completed*, *Today's Workout*, *Upcoming*, *Rest Day*) and a day-detail modal.
  - Professional analytics with **Chart.js** line chart for weekly weight progress and bar chart for daily steps, plus a modal to log new weight data points.
  - 24/7 conversational **AI Fitness Assistant** chatbot with quick prompt suggestions, realistic typing simulation, and contextual dummy answers.
  - User profile with biometrics, milestone badges, and an interactive edit profile modal.

---

## 📁 Project Structure

```text
d:/New folder/
│
├── ai_fitness_planner/        # Django Project configuration
│   ├── __init__.py
│   ├── settings.py            # Registered planner app, templates, and static dir
│   ├── urls.py                # URL routes for all 11 pages
│   ├── wsgi.py
│   └── asgi.py
│
├── planner/                   # Django Planner App
│   ├── views.py               # View controllers rendering sample/dummy context
│   └── ...
│
├── templates/                 # Django Templates
│   ├── base.html              # Master layout (public navbar + dashboard sidebar)
│   ├── home.html              # 1. Landing Page (Hero, Features, How It Works)
│   ├── assessment.html        # 4. Fitness Assessment Form & Stepper
│   ├── goals.html             # 5. Fitness Goal Selectable Cards
│   ├── bmi_result.html        # 6. BMI Result Card & Horizontal Indicator Gauge
│   ├── dashboard.html         # 7-9. Main Dashboard, Workout Checklist & Diet
│   ├── workout.html           # 11. Workout Planner & Exercise Cards
│   ├── diet.html              # 12. Diet Planner & Meal Tabs
│   ├── plan_30days.html       # 10. 30-Day Fitness Journey Calendar
│   ├── progress.html          # 13. Progress Tracking & Chart.js Analytics
│   ├── chatbot.html           # 14. AI Fitness Assistant Chatbot
│   └── profile.html           # 15. User Profile & Milestones
│
├── static/
│   ├── css/
│   │   └── style.css          # Comprehensive design system & responsive CSS
│   └── js/
│       └── script.js          # Client-side reactivity, chart config & chatbot
│
├── manage.py
└── README.md
```

---

## 🚀 How to Run Locally

1. **Open Terminal / Command Prompt** in this directory:
   ```bash
   cd "d:/New folder"
   ```

2. **Verify Python & Django**:
   ```bash
   python --version
   python manage.py check
   ```

3. **Start the Django Development Server**:
   ```bash
   python manage.py runserver 127.0.0.1:8000
   ```

4. **Authentication & Pages Access**:
   - All core fitness tools, dashboard, workout, diet, and progress tracking are protected. Users must log in before continuing to the next process.
   - **Sign In / Registration**: [http://127.0.0.1:8000/login/](http://127.0.0.1:8000/login/)
   - **Quick Demo Credentials**:
     - Username: `alex`
     - Password: `fitness123`
     *(Or simply click the green "1-Click Demo Login" button on the login screen)*
   - **Landing Page**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   - **Dashboard**: [http://127.0.0.1:8000/dashboard/](http://127.0.0.1:8000/dashboard/)
   - **Fitness Assessment**: [http://127.0.0.1:8000/assessment/](http://127.0.0.1:8000/assessment/)
   - **Workout Planner**: [http://127.0.0.1:8000/workout/](http://127.0.0.1:8000/workout/)
   - **Diet Planner**: [http://127.0.0.1:8000/diet/](http://127.0.0.1:8000/diet/)
   - **30-Day Plan**: [http://127.0.0.1:8000/plan-30days/](http://127.0.0.1:8000/plan-30days/)
   - **Progress Tracking**: [http://127.0.0.1:8000/progress/](http://127.0.0.1:8000/progress/)
   - **AI Chatbot**: [http://127.0.0.1:8000/chatbot/](http://127.0.0.1:8000/chatbot/)
   - **Profile**: [http://127.0.0.1:8000/profile/](http://127.0.0.1:8000/profile/)

---

## 🎨 Design Philosophy
- **Aesthetic**: Premium, minimalist, health-inspired green & white theme.
- **Accessibility**: High-contrast text, clear visual cues, semantic tags, and responsive typography.
- **Interactivity**: Instant feedback on buttons, toggles, form fields, and charts without reloading pages.
