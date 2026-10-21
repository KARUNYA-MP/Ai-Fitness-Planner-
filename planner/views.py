import re
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def get_or_create_demo_user():
    """Helper to ensure the default demo user exists"""
    user, created = User.objects.get_or_create(
        username='alex',
        defaults={
            'email': 'alex.johnson@example.com',
            'first_name': 'Alex',
            'last_name': 'Johnson',
        }
    )
    if created or not user.has_usable_password():
        user.set_password('fitness123')
        user.first_name = 'Alex'
        user.last_name = 'Johnson'
        user.save()
    return user

def login_view(request):
    """User Login View - Accepts ANY username/email and password entered by the user"""
    next_url = request.GET.get('next') or request.POST.get('next') or 'dashboard'

    if request.user.is_authenticated:
        return redirect(next_url)

    if request.method == 'POST':
        login_identifier = (request.POST.get('username') or request.POST.get('email') or '').strip()
        password = request.POST.get('password', '').strip()

        # If empty, default to user
        if not login_identifier:
            login_identifier = 'User'
        if not password:
            password = 'password123'

        # Parse base name and email
        if '@' in login_identifier:
            email = login_identifier
            base_name = login_identifier.split('@')[0]
        else:
            base_name = login_identifier
            email = f"{base_name.lower()}@example.com"

        # Sanitize username for Django User model (alphanumeric, @/./+/-/_)
        clean_username = re.sub(r'[^\w.@+-]', '', base_name.lower()) or 'user'
        display_name = base_name.replace('.', ' ').replace('_', ' ').title()

        # Look for existing user by username or email
        user = User.objects.filter(username=clean_username).first()
        if not user and '@' in login_identifier:
            user = User.objects.filter(email__iexact=login_identifier).first()

        if not user:
            # Create the user on the fly so any entered credential works immediately
            user = User.objects.create_user(
                username=clean_username,
                email=email,
                password=password,
                first_name=display_name
            )
        else:
            # Update password so whatever password was typed works immediately
            user.set_password(password)
            if not user.first_name:
                user.first_name = display_name
            if '@' in login_identifier and not user.email:
                user.email = login_identifier
            user.save()

        # Authenticate and log in
        login(request, user)
        messages.success(request, f"Welcome, {user.first_name or user.username}! Successfully logged in.")
        return redirect(next_url)


    return render(request, 'login.html', {
        'page_title': 'Sign In',
        'active_page': 'login',
        'next': next_url,
    })


def register_view(request):
    """User Registration View"""
    next_url = request.GET.get('next') or request.POST.get('next') or 'assessment'
    if request.user.is_authenticated:
        return redirect(next_url)

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not username or not password:
            messages.error(request, "Username and password are required.")
        elif password != confirm_password:
            messages.error(request, "Passwords do not match.")
        elif len(password) < 6:
            messages.error(request, "Password should be at least 6 characters long.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, f"Username '{username}' already exists. Please choose a different one.")
        else:
            names = full_name.split(' ', 1)
            first_name = names[0] if names else ''
            last_name = names[1] if len(names) > 1 else ''

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            login(request, user)
            messages.success(request, f"Account created! Welcome, {user.first_name or user.username}. Let's get started.")
            return redirect(next_url)

    return render(request, 'login.html', {
        'page_title': 'Create Account | FitAI',
        'active_page': 'login',
        'initial_tab': 'register',
        'next': next_url,
    })

def logout_view(request):
    """User Logout View"""
    logout(request)
    messages.info(request, "You have been logged out. Please sign in to access your workout and diet routines.")
    return redirect('login')

def home(request):
    """Landing Page"""
    return render(request, 'home.html', {
        'page_title': 'Your Personal AI Fitness Planner',
        'active_page': 'home'
    })

@login_required
def assessment(request):
    """Fitness Assessment Page"""
    return render(request, 'assessment.html', {
        'page_title': "Let's Build Your Fitness Plan",
        'active_page': 'assessment'
    })


@login_required
def goals(request):
    """Fitness Goal Page"""
    goals_list = [
        {
            'id': 'weight_loss',
            'title': 'Weight Loss',
            'icon': '🔥',
            'tagline': 'Burn calories & get lean',
            'description': 'Lose excess weight, reduce body fat percentage, and improve overall cardio-metabolic fitness.',
            'recommended_for': 'High body fat %, Calorie deficit preference',
            'popular': True,
        },
        {
            'id': 'weight_gain',
            'title': 'Weight Gain',
            'icon': '💪',
            'tagline': 'Hypertrophy & healthy bulk',
            'description': 'Build healthy body mass, lean muscle tissue, and foundational functional strength with progressive overload.',
            'recommended_for': 'Lean individuals, Muscle building',
            'popular': False,
        },
        {
            'id': 'weight_maintenance',
            'title': 'Weight Maintenance',
            'icon': '⚖️',
            'tagline': 'Balance & athletic vitality',
            'description': 'Maintain your current weight, tone muscles, boost daily energy, and establish sustainable lifelong habits.',
            'recommended_for': 'Balanced BMI, Healthy lifestyle',
            'popular': False,
        },
        {
            'id': 'improve_fitness',
            'title': 'Improve Fitness',
            'icon': '🏃',
            'tagline': 'Endurance, stamina & agility',
            'description': 'Improve stamina, cardiovascular capacity, core stability, flexibility, and overall athletic fitness.',
            'recommended_for': 'Runners, Active sports, General stamina',
            'popular': False,
        },
        {
            'id': 'build_strength',
            'title': 'Build Strength',
            'icon': '🏋️',
            'tagline': 'Power & compound lifting',
            'description': 'Develop peak mechanical strength, bone density, and tendon power through structured progressive workouts.',
            'recommended_for': 'Strength training, Powerlifting focus',
            'popular': False,
        }
    ]
    return render(request, 'goals.html', {
        'page_title': 'Select Your Fitness Goal',
        'active_page': 'goals',
        'goals': goals_list
    })

@login_required
def bmi_result(request):
    """BMI Result Page"""
    # Sample dummy data that can also be dynamically adjusted via query params or JS
    height = float(request.GET.get('height', 170))
    weight = float(request.GET.get('weight', 70))
    bmi = round(weight / ((height / 100) ** 2), 1) if height > 0 else 24.2
    
    status = "Normal Weight"
    status_desc = "You have a healthy body weight. Maintain your balanced nutrition and regular physical activity."
    badge_color = "success"
    
    if bmi < 18.5:
        status = "Underweight"
        status_desc = "Your BMI suggests you are underweight. Consider a calorie surplus and strength training."
        badge_color = "warning"
    elif 18.5 <= bmi <= 24.9:
        status = "Normal Range"
        status_desc = "Your BMI is in the optimal healthy range. Excellent job maintaining a sound balance!"
        badge_color = "success"
    elif 25.0 <= bmi <= 29.9:
        status = "Overweight"
        status_desc = "Your BMI is slightly elevated. A balanced workout routine and clean diet will yield great results."
        badge_color = "warning"
    else:
        status = "Obesity Range"
        status_desc = "Your BMI indicates obesity. We recommend a structured moderate cardio and calorie-deficit program."
        badge_color = "danger"

    return render(request, 'bmi_result.html', {
        'page_title': 'Your BMI Assessment',
        'active_page': 'bmi_result',
        'height': int(height),
        'weight': int(weight),
        'bmi': bmi,
        'status': status,
        'status_desc': status_desc,
        'badge_color': badge_color,
    })

@login_required
def dashboard(request):
    """Main Fitness Dashboard"""
    user_display_name = request.user.get_full_name() or request.user.username.capitalize() or 'Alex Johnson'
    first_name = request.user.first_name or request.user.username.capitalize() or 'Alex'
    import datetime
    current_hour = datetime.datetime.now().hour
    if 5 <= current_hour < 12:
        time_greeting = "Good Morning"
    elif 12 <= current_hour < 17:
        time_greeting = "Good Afternoon"
    else:
        time_greeting = "Good Evening"

    dummy_stats = {
        'user_name': user_display_name,
        'greeting': f'{time_greeting}, {first_name} 👋',
        'subtitle': "Let's make today a healthier day.",
        'current_weight': 70,
        'target_weight': 65,
        'bmi': 24.2,
        'goal_progress': 65,
        'today_workout_progress': 70,
        'water_intake_current': 5,
        'water_intake_target': 8,
        'daily_steps': 6240,
        'daily_steps_target': 10000,
        'active_calories': 480,
    }
    
    today_workout = {
        'title': 'Full Body Beginner Workout',
        'duration': '30 Mins',
        'intensity': 'Moderate',
        'calories': '260 kcal',
        'exercises': [
            {'name': 'Warm-up', 'details': 'Light mobility & stretching', 'duration': '5 min', 'done': True},
            {'name': 'Squats', 'details': 'Bodyweight squats', 'duration': '3 × 15 reps', 'done': True},
            {'name': 'Push-ups', 'details': 'Knee or standard push-ups', 'duration': '3 × 10 reps', 'done': True},
            {'name': 'Lunges', 'details': 'Alternating forward lunges', 'duration': '3 × 10 reps', 'done': False},
            {'name': 'Plank', 'details': 'Forearm isometric hold', 'duration': '3 × 30 sec', 'done': False},
            {'name': 'Cool Down', 'details': 'Full body dynamic stretches', 'duration': '5 min', 'done': False},
        ]
    }
    
    meals = [
        {
            'type': 'Breakfast',
            'food': 'Oats + Fruits & Almonds',
            'time': '08:30 AM',
            'calories': 350,
            'icon': 'fa-bowl-rice',
            'tag': 'High Fiber',
            'protein': '14g'
        },
        {
            'type': 'Lunch',
            'food': 'Brown Rice + Vegetables + Yellow Dal',
            'time': '01:15 PM',
            'calories': 550,
            'icon': 'fa-utensils',
            'tag': 'Balanced Energy',
            'protein': '22g'
        },
        {
            'type': 'Evening Snack',
            'food': 'Fresh Seasonal Fruits + Roasted Nuts',
            'time': '05:00 PM',
            'calories': 180,
            'icon': 'fa-apple-whole',
            'tag': 'Antioxidants',
            'protein': '6g'
        },
        {
            'type': 'Dinner',
            'food': 'Whole Wheat Chapati + Mixed Veggies + Grilled Paneer/Tofu',
            'time': '08:00 PM',
            'calories': 480,
            'icon': 'fa-plate-wheat',
            'tag': 'Lean Protein',
            'protein': '26g'
        },
    ]
    
    return render(request, 'dashboard.html', {
        'page_title': 'Fitness Dashboard',
        'active_page': 'dashboard',
        'stats': dummy_stats,
        'workout': today_workout,
        'meals': meals
    })

@login_required
def workout(request):
    """Workout Planner Page"""
    exercises = [
        {
            'id': 'ex1',
            'name': 'Jumping Jacks',
            'category': 'Cardio / Warm-up',
            'icon': 'fa-person-running',
            'sets': '3',
            'reps': '30 reps',
            'duration': '45 sec',
            'rest': '30 sec',
            'difficulty': 'Beginner',
            'tip': 'Land softly on the balls of your feet and keep your core braced.',
            'badge': 'Warm-Up'
        },
        {
            'id': 'ex2',
            'name': 'Bodyweight Squats',
            'category': 'Lower Body / Quads & Glutes',
            'icon': 'fa-person',
            'sets': '3',
            'reps': '15 reps',
            'duration': '60 sec',
            'rest': '45 sec',
            'difficulty': 'Beginner',
            'tip': 'Keep your chest tall, knees aligned with toes, and drive through your heels.',
            'badge': 'Strength'
        },
        {
            'id': 'ex3',
            'name': 'Push-ups',
            'category': 'Upper Body / Chest & Triceps',
            'icon': 'fa-dumbbell',
            'sets': '3',
            'reps': '10 reps',
            'duration': '45 sec',
            'rest': '60 sec',
            'difficulty': 'Beginner',
            'tip': 'Maintain a neutral spine and lower chest to 2 inches from the floor.',
            'badge': 'Strength'
        },
        {
            'id': 'ex4',
            'name': 'Walking Lunges',
            'category': 'Lower Body / Hamstrings & Core',
            'icon': 'fa-shoe-prints',
            'sets': '3',
            'reps': '10 / leg',
            'duration': '60 sec',
            'rest': '45 sec',
            'difficulty': 'Beginner',
            'tip': 'Ensure front knee does not extend past toes and back knee hovers above floor.',
            'badge': 'Balance'
        },
        {
            'id': 'ex5',
            'name': 'Forearm Plank',
            'category': 'Core / Transverse Abdominis',
            'icon': 'fa-stopwatch-20',
            'sets': '3',
            'reps': 'Hold',
            'duration': '30 sec',
            'rest': '45 sec',
            'difficulty': 'Beginner',
            'tip': 'Squeeze glutes and abs tight; do not let hips dip or hike upward.',
            'badge': 'Core'
        },
        {
            'id': 'ex6',
            'name': 'Mountain Climbers',
            'category': 'Cardio & Core',
            'icon': 'fa-fire-flame-curved',
            'sets': '3',
            'reps': '20 reps',
            'duration': '40 sec',
            'rest': '30 sec',
            'difficulty': 'Intermediate',
            'tip': 'Drive knees dynamically toward chest while keeping shoulders stacked over wrists.',
            'badge': 'Cardio'
        }
    ]
    return render(request, 'workout.html', {
        'page_title': 'Workout Planner',
        'active_page': 'workout',
        'workout_title': 'Full Body Beginner Blast',
        'difficulty': 'Beginner',
        'duration': '30 Minutes',
        'calories': '240 - 280 kcal',
        'exercises': exercises
    })

@login_required
def diet(request):
    """Diet Planner Page"""
    meals = {
        'breakfast': {
            'title': 'Energizing Morning Bowl',
            'food': 'Rolled Oats + Banana + Chia Seeds + Almond Milk + Honey',
            'calories': 380,
            'protein': 15,
            'carbs': 58,
            'fats': 9,
            'tip': 'Complex carbs provide steady glucose release without mid-morning energy crashes.',
            'prep_time': '10 mins'
        },
        'lunch': {
            'title': 'Wholesome Power Plate',
            'food': 'Steamed Brown Rice + Steamed Broccoli & Carrots + Spiced Yellow Moong Dal',
            'calories': 560,
            'protein': 24,
            'carbs': 84,
            'fats': 12,
            'tip': 'Combining whole grains with legumes provides a complete amino acid profile for tissue repair.',
            'prep_time': '25 mins'
        },
        'snack': {
            'title': 'Mid-day Vitality Boost',
            'food': 'Apple Slices with 1 Tbsp Almond Butter + Handful Roasted Walnuts',
            'calories': 195,
            'protein': 6,
            'carbs': 22,
            'fats': 11,
            'tip': 'Rich in Omega-3 fatty acids and polyphenols to keep focus sharp and inflammation low.',
            'prep_time': '5 mins'
        },
        'dinner': {
            'title': 'Light & Nourishing Dinner',
            'food': '2 Whole Wheat Chapatis + Stir-fried Spinach & Cottage Cheese (Paneer / Tofu)',
            'calories': 470,
            'protein': 28,
            'carbs': 52,
            'fats': 14,
            'tip': 'Eating a protein-rich, lower-sodium dinner 2 hours before bed supports nighttime cellular repair.',
            'prep_time': '20 mins'
        }
    }
    
    weekly_overview = [
        {'day': 'Monday', 'focus': 'Clean Detox & High Fiber', 'cals': '1,600 kcal', 'macros': 'P: 75g | C: 215g | F: 46g'},
        {'day': 'Tuesday', 'focus': 'Lean Protein & Energy', 'cals': '1,650 kcal', 'macros': 'P: 80g | C: 210g | F: 48g'},
        {'day': 'Wednesday', 'focus': 'Balanced Whole Grains', 'cals': '1,620 kcal', 'macros': 'P: 74g | C: 220g | F: 44g'},
        {'day': 'Thursday', 'focus': 'Metabolic Boost Greens', 'cals': '1,590 kcal', 'macros': 'P: 78g | C: 205g | F: 45g'},
        {'day': 'Friday', 'focus': 'Antioxidants & Superfoods', 'cals': '1,640 kcal', 'macros': 'P: 76g | C: 218g | F: 47g'},
        {'day': 'Saturday', 'focus': 'Active Recovery Feast', 'cals': '1,700 kcal', 'macros': 'P: 85g | C: 230g | F: 50g'},
        {'day': 'Sunday', 'focus': 'Mindful Reset & Hydration', 'cals': '1,550 kcal', 'macros': 'P: 72g | C: 195g | F: 42g'},
    ]
    
    return render(request, 'diet.html', {
        'page_title': 'Diet Planner',
        'active_page': 'diet',
        'meals': meals,
        'weekly_overview': weekly_overview,
        'daily_target_calories': 1605,
        'consumed_calories': 1135
    })

@login_required
def plan_30days(request):
    """30-Day Fitness Plan Page"""
    weeks = [
        {
            'week_number': 1,
            'title': 'Week 1: Foundation & Mobility',
            'description': 'Awaken core muscle groups and establish consistent movement patterns.',
            'days': [
                {'day': 1, 'title': 'Full Body Awakening', 'type': 'workout', 'status': 'completed', 'duration': '30m', 'cals': '240 kcal'},
                {'day': 2, 'title': 'Low-Impact Cardio', 'type': 'cardio', 'status': 'completed', 'duration': '25m', 'cals': '210 kcal'},
                {'day': 3, 'title': 'Upper & Core Strength', 'type': 'strength', 'status': 'completed', 'duration': '30m', 'cals': '250 kcal'},
                {'day': 4, 'title': 'Active Rest & Walk', 'type': 'rest', 'status': 'completed', 'duration': '20m', 'cals': '80 kcal'},
                {'day': 5, 'title': 'Lower Body & Glutes', 'type': 'workout', 'status': 'today', 'duration': '35m', 'cals': '270 kcal'},
                {'day': 6, 'title': 'Brisk Cardio & Core', 'type': 'cardio', 'status': 'upcoming', 'duration': '30m', 'cals': '230 kcal'},
                {'day': 7, 'title': 'Full Recovery & Yoga', 'type': 'rest', 'status': 'rest', 'duration': '15m', 'cals': '50 kcal'},
            ]
        },
        {
            'week_number': 2,
            'title': 'Week 2: Strength Progression',
            'description': 'Gradually increase repetition capacity and improve posture stability.',
            'days': [
                {'day': 8, 'title': 'Full Body Blast', 'type': 'workout', 'status': 'upcoming', 'duration': '32m', 'cals': '260 kcal'},
                {'day': 9, 'title': 'Cardio Intervals', 'type': 'cardio', 'status': 'upcoming', 'duration': '28m', 'cals': '240 kcal'},
                {'day': 10, 'title': 'Strength & Form', 'type': 'strength', 'status': 'upcoming', 'duration': '35m', 'cals': '280 kcal'},
                {'day': 11, 'title': 'Rest & Foam Rolling', 'type': 'rest', 'status': 'rest', 'duration': '20m', 'cals': '70 kcal'},
                {'day': 12, 'title': 'Core & Calisthenics', 'type': 'workout', 'status': 'upcoming', 'duration': '30m', 'cals': '240 kcal'},
                {'day': 13, 'title': 'HIIT Cardio Burst', 'type': 'cardio', 'status': 'upcoming', 'duration': '25m', 'cals': '260 kcal'},
                {'day': 14, 'title': 'Complete Rest Day', 'type': 'rest', 'status': 'rest', 'duration': '0m', 'cals': '0 kcal'},
            ]
        },
        {
            'week_number': 3,
            'title': 'Week 3: Endurance & Stamina',
            'description': 'Elevate cardiovascular endurance and shorten transition times between sets.',
            'days': [
                {'day': 15, 'title': 'Full Body Functional', 'type': 'workout', 'status': 'upcoming', 'duration': '35m', 'cals': '290 kcal'},
                {'day': 16, 'title': 'Speed & Agility Cardio', 'type': 'cardio', 'status': 'upcoming', 'duration': '30m', 'cals': '270 kcal'},
                {'day': 17, 'title': 'Compound Strength', 'type': 'strength', 'status': 'upcoming', 'duration': '35m', 'cals': '300 kcal'},
                {'day': 18, 'title': 'Mindful Rest Day', 'type': 'rest', 'status': 'rest', 'duration': '15m', 'cals': '60 kcal'},
                {'day': 19, 'title': 'Dynamic Core Sculpt', 'type': 'workout', 'status': 'upcoming', 'duration': '30m', 'cals': '250 kcal'},
                {'day': 20, 'title': 'Endurance Cardio Run', 'type': 'cardio', 'status': 'upcoming', 'duration': '35m', 'cals': '310 kcal'},
                {'day': 21, 'title': 'Deep Stretch & Rest', 'type': 'rest', 'status': 'rest', 'duration': '20m', 'cals': '70 kcal'},
            ]
        },
        {
            'week_number': 4,
            'title': 'Week 4: Peak Transformation',
            'description': 'Consolidate monthly athletic gains, boost metabolic rate, and test fitness milestones.',
            'days': [
                {'day': 22, 'title': 'Full Body Power', 'type': 'workout', 'status': 'upcoming', 'duration': '35m', 'cals': '310 kcal'},
                {'day': 23, 'title': 'Tabata Cardio Burn', 'type': 'cardio', 'status': 'upcoming', 'duration': '30m', 'cals': '290 kcal'},
                {'day': 24, 'title': 'Total Muscle Tone', 'type': 'strength', 'status': 'upcoming', 'duration': '38m', 'cals': '320 kcal'},
                {'day': 25, 'title': 'Active Rest & Stroll', 'type': 'rest', 'status': 'rest', 'duration': '20m', 'cals': '80 kcal'},
                {'day': 26, 'title': 'HIIT Full Blast', 'type': 'workout', 'status': 'upcoming', 'duration': '32m', 'cals': '300 kcal'},
                {'day': 27, 'title': 'Milestone Fitness Test', 'type': 'cardio', 'status': 'upcoming', 'duration': '30m', 'cals': '280 kcal'},
                {'day': 28, 'title': 'Active Recovery & Walk', 'type': 'rest', 'status': 'rest', 'duration': '25m', 'cals': '90 kcal'},
                {'day': 29, 'title': 'Celebration Circuit', 'type': 'workout', 'status': 'upcoming', 'duration': '35m', 'cals': '310 kcal'},
                {'day': 30, 'title': 'Victory Rest & Review', 'type': 'rest', 'status': 'rest', 'duration': '15m', 'cals': '60 kcal'},
            ]
        }
    ]
    return render(request, 'plan_30days.html', {
        'page_title': 'Your 30-Day Fitness Journey',
        'active_page': 'plan_30days',
        'weeks': weeks,
        'completed_days': 4,
        'total_days': 30,
        'completion_pct': 13
    })

@login_required
def progress(request):
    """Progress Tracking Page"""
    weight_logs = [
        {'week': 'Week 1', 'weight': 70.0, 'date': '01 Sep', 'change': '0.0 kg'},
        {'week': 'Week 2', 'weight': 69.5, 'date': '08 Sep', 'change': '-0.5 kg'},
        {'week': 'Week 3', 'weight': 68.8, 'date': '15 Sep', 'change': '-0.7 kg'},
        {'week': 'Week 4', 'weight': 68.0, 'date': '22 Sep', 'change': '-0.8 kg'},
    ]
    
    analytics = {
        'initial_weight': 70.0,
        'current_weight': 68.0,
        'target_weight': 65.0,
        'total_loss': 2.0,
        'goal_remaining': 3.0,
        'goal_progress_pct': 40,
        'workout_completion_rate': 82,
        'workouts_completed': 18,
        'workouts_total': 22,
        'total_calories_burned': 5420,
        'avg_daily_steps': 7480,
    }
    
    return render(request, 'progress.html', {
        'page_title': 'Progress Tracking',
        'active_page': 'progress',
        'weight_logs': weight_logs,
        'analytics': analytics
    })

@login_required
def chatbot(request):
    """AI Fitness Assistant Page"""
    example_messages = [
        {
            'sender': 'ai',
            'text': "Hello Alex! 👋 I'm your AI Fitness Assistant. I can help guide your workouts, customize meal choices, advise on recovery, or answer any fitness questions. How can I help you today?",
            'time': '10:00 AM'
        },
        {
            'sender': 'user',
            'text': "Give me a beginner workout.",
            'time': '10:02 AM'
        },
        {
            'sender': 'ai',
            'text': "Here is a simple beginner workout:\n• 10 Bodyweight Squats\n• 10 Push-ups (knee or standard)\n• 20 Jumping Jacks\n• 30-Second Forearm Plank\n\nPerform 3 rounds with 60 seconds rest between rounds. Don't forget a 5-minute warm-up and to stay hydrated! 💧",
            'time': '10:02 AM'
        }
    ]
    return render(request, 'chatbot.html', {
        'page_title': 'AI Fitness Assistant',
        'active_page': 'chatbot',
        'messages': example_messages
    })

@login_required
def profile(request):
    """User Profile Page"""
    user_display_name = request.user.get_full_name() or request.user.username.capitalize() or 'Alex Johnson'
    user_email = request.user.email or f"{request.user.username}@example.com"
    user_data = {
        'name': user_display_name,
        'email': user_email,
        'member_since': 'August 2026',
        'membership_plan': 'AI Fitness Pro (Active)',
        'age': 28,
        'gender': 'Male',
        'height': '170 cm',
        'current_weight': '70 kg',
        'target_weight': '65 kg',
        'fitness_goal': 'Weight Loss & Muscle Tone',
        'activity_level': 'Moderately Active',
        'fitness_level': 'Beginner / Intermediate',
        'food_preference': 'Vegetarian',
        'workout_preference': 'Home & Bodyweight',
        'daily_calorie_goal': '1,650 kcal',
        'daily_water_goal': '8 glasses (2.5L)',
        'completed_workouts': 24,
        'current_streak': '7 Days 🔥'
    }
    return render(request, 'profile.html', {
        'page_title': 'User Profile',
        'active_page': 'profile',
        'profile': user_data
    })
