/**
 * AI Fitness Planner - Frontend Interactive Script
 * Demonstrates complete UI flows, micro-interactions, Chart.js integrations,
 * BMI calculations, workout tracking, and conversational AI mockup.
 */

document.addEventListener('DOMContentLoaded', function () {
  initMobileNavigation();
  initAssessmentInteractions();
  initGoalSelection();
  initBmiCalculator();
  initDashboardTrackers();
  initDietPlannerTabs();
  init30DayPlanModal();
  initWorkoutSessionModal();
  initChatbot();
  initProgressCharts();
  initProfileEdit();
});

/* ==========================================================================
   1. MOBILE NAVIGATION & SIDEBAR
   ========================================================================== */
function initMobileNavigation() {
  // Public navbar hamburger toggle
  const publicNavToggle = document.getElementById('publicNavToggle');
  const publicNavLinks = document.getElementById('publicNavLinks');
  if (publicNavToggle && publicNavLinks) {
    publicNavToggle.addEventListener('click', function () {
      publicNavLinks.classList.toggle('show-mobile');
    });
  }

  // App sidebar toggle on mobile/tablet
  const appSidebar = document.getElementById('appSidebar');
  const sidebarToggleBtn = document.getElementById('sidebarToggleBtn');
  const sidebarCloseBtn = document.getElementById('sidebarCloseBtn');

  if (sidebarToggleBtn && appSidebar) {
    sidebarToggleBtn.addEventListener('click', function () {
      appSidebar.classList.add('show');
    });
  }

  if (sidebarCloseBtn && appSidebar) {
    sidebarCloseBtn.addEventListener('click', function () {
      appSidebar.classList.remove('show');
    });
  }

  // Close sidebar on clicking outside in mobile view
  document.addEventListener('click', function (e) {
    if (appSidebar && appSidebar.classList.contains('show')) {
      if (!appSidebar.contains(e.target) && !sidebarToggleBtn.contains(e.target)) {
        appSidebar.classList.remove('show');
      }
    }
  });
}

/* ==========================================================================
   2. FITNESS ASSESSMENT PAGE INTERACTIONS
   ========================================================================== */
function initAssessmentInteractions() {
  const assessmentForm = document.getElementById('assessmentForm');
  if (!assessmentForm) return;

  // Single selectable cards (Activity Level, Fitness Level, Food, Workout)
  const selectCardGroups = document.querySelectorAll('.selectable-group');
  selectCardGroups.forEach(group => {
    const cards = group.querySelectorAll('.select-card');
    cards.forEach(card => {
      card.addEventListener('click', function () {
        cards.forEach(c => c.classList.remove('selected'));
        card.classList.add('selected');
        const input = card.querySelector('input[type="radio"]');
        if (input) input.checked = true;
      });
    });
  });

  // Handle Assessment Continue
  assessmentForm.addEventListener('submit', function (e) {
    e.preventDefault();
    const height = document.getElementById('inputHeight')?.value || 170;
    const weight = document.getElementById('inputWeight')?.value || 70;
    const targetWeight = document.getElementById('inputTargetWeight')?.value || 65;
    const name = document.getElementById('inputName')?.value || 'Alex';

    // Store in localStorage for complete cross-page simulation
    localStorage.setItem('userHeight', height);
    localStorage.setItem('userWeight', weight);
    localStorage.setItem('userTargetWeight', targetWeight);
    localStorage.setItem('userName', name);

    // Redirect to Goals page
    window.location.href = '/goals/';
  });
}

/* ==========================================================================
   3. FITNESS GOAL PAGE INTERACTIONS
   ========================================================================== */
function initGoalSelection() {
  const goalCards = document.querySelectorAll('.goal-selectable-card');
  const continueBtn = document.getElementById('goalContinueBtn');
  if (!goalCards.length) return;

  goalCards.forEach(card => {
    card.addEventListener('click', function () {
      goalCards.forEach(c => {
        c.classList.remove('selected');
        const btn = c.querySelector('.goal-select-btn');
        if (btn) btn.textContent = 'Select Goal';
      });

      card.classList.add('selected');
      const activeBtn = card.querySelector('.goal-select-btn');
      if (activeBtn) activeBtn.textContent = 'Selected ✓';

      const goalId = card.getAttribute('data-goal-id');
      localStorage.setItem('selectedGoal', goalId);

      if (continueBtn) {
        continueBtn.disabled = false;
        continueBtn.classList.remove('opacity-50');
      }
    });
  });

  if (continueBtn) {
    continueBtn.addEventListener('click', function () {
      const height = localStorage.getItem('userHeight') || 170;
      const weight = localStorage.getItem('userWeight') || 70;
      window.location.href = `/bmi-result/?height=${height}&weight=${weight}`;
    });
  }
}

/* ==========================================================================
   4. BMI RESULT PAGE INTERACTIONS & REAL-TIME CALCULATOR
   ========================================================================== */
function initBmiCalculator() {
  const bmiGaugePointer = document.getElementById('bmiGaugePointer');
  const bmiValueDisplay = document.getElementById('bmiValueDisplay');
  const bmiStatusBadge = document.getElementById('bmiStatusBadge');
  const bmiStatusDesc = document.getElementById('bmiStatusDesc');
  const liveHeightInput = document.getElementById('liveHeightInput');
  const liveWeightInput = document.getElementById('liveWeightInput');

  function calculateAndRenderBMI(height, weight) {
    if (!height || !weight || height <= 0) return;
    const hMeters = height / 100;
    const bmi = (weight / (hMeters * hMeters)).toFixed(1);

    if (bmiValueDisplay) bmiValueDisplay.textContent = bmi;

    let percentage = 0;
    let statusText = 'Normal Range';
    let badgeClass = 'badge-normal';
    let description = 'Your BMI is in the optimal healthy range. Excellent job maintaining a sound balance!';

    if (bmi < 18.5) {
      // 0 - 22% of gauge
      percentage = Math.max(5, (bmi / 18.5) * 22);
      statusText = 'Underweight';
      badgeClass = 'badge-warning';
      description = 'Your BMI indicates you are underweight. Consider a wholesome calorie surplus and resistance training.';
    } else if (bmi <= 24.9) {
      // 22% - 54% of gauge
      percentage = 22 + ((bmi - 18.5) / (24.9 - 18.5)) * 32;
      statusText = 'Normal Range';
      badgeClass = 'badge-normal';
      description = 'Your BMI is in the optimal healthy range. Excellent job maintaining a sound balance!';
    } else if (bmi <= 29.9) {
      // 54% - 78% of gauge
      percentage = 54 + ((bmi - 25.0) / (29.9 - 25.0)) * 24;
      statusText = 'Overweight';
      badgeClass = 'badge-warning';
      description = 'Your BMI is slightly elevated. A balanced workout routine and clean diet will yield great results.';
    } else {
      // 78% - 95% of gauge
      percentage = Math.min(95, 78 + ((bmi - 30) / 10) * 20);
      statusText = 'Obesity Range';
      badgeClass = 'badge-danger';
      description = 'Your BMI indicates obesity. We recommend a structured moderate cardio and calorie-deficit program.';
    }

    if (bmiGaugePointer) {
      bmiGaugePointer.style.left = `${percentage}%`;
    }

    if (bmiStatusBadge) {
      bmiStatusBadge.textContent = statusText;
      bmiStatusBadge.className = `bmi-badge-status ${badgeClass}`;
    }

    if (bmiStatusDesc) {
      bmiStatusDesc.textContent = description;
    }
  }

  if (liveHeightInput && liveWeightInput) {
    const update = () => calculateAndRenderBMI(parseFloat(liveHeightInput.value), parseFloat(liveWeightInput.value));
    liveHeightInput.addEventListener('input', update);
    liveWeightInput.addEventListener('input', update);
    update();
  } else if (bmiValueDisplay) {
    const initialBmi = parseFloat(bmiValueDisplay.textContent) || 24.2;
    // Map initial BMI to gauge
    let percentage = 42;
    if (initialBmi < 18.5) percentage = 12;
    else if (initialBmi <= 24.9) percentage = 22 + ((initialBmi - 18.5) / 6.4) * 32;
    else if (initialBmi <= 29.9) percentage = 54 + ((initialBmi - 25.0) / 4.9) * 24;
    else percentage = 85;

    if (bmiGaugePointer) {
      setTimeout(() => {
        bmiGaugePointer.style.left = `${percentage}%`;
      }, 300);
    }
  }
}

/* ==========================================================================
   5. DASHBOARD TRACKERS (Water Intake, Workout Checkboxes)
   ========================================================================== */
function initDashboardTrackers() {
  // Water Tracker
  let waterCount = 5;
  const targetWater = 8;
  const waterCountDisplay = document.getElementById('waterCountDisplay');
  const waterProgressBar = document.getElementById('waterProgressBar');
  const btnAddWater = document.getElementById('btnAddWater');
  const btnSubWater = document.getElementById('btnSubWater');

  function updateWaterUI() {
    if (waterCountDisplay) waterCountDisplay.textContent = `${waterCount} / ${targetWater} glasses`;
    if (waterProgressBar) {
      const pct = Math.min(100, Math.round((waterCount / targetWater) * 100));
      waterProgressBar.style.width = `${pct}%`;
    }
  }

  if (btnAddWater) {
    btnAddWater.addEventListener('click', function () {
      if (waterCount < 16) {
        waterCount++;
        updateWaterUI();
      }
    });
  }

  if (btnSubWater) {
    btnSubWater.addEventListener('click', function () {
      if (waterCount > 0) {
        waterCount--;
        updateWaterUI();
      }
    });
  }

  // Workout Checklist Progress on Dashboard
  const workoutCheckboxes = document.querySelectorAll('.dashboard-workout-check');
  const workoutProgressPct = document.getElementById('workoutProgressPct');
  const workoutProgressBar = document.getElementById('workoutProgressBar');

  function updateWorkoutProgress() {
    if (!workoutCheckboxes.length) return;
    let completed = 0;
    workoutCheckboxes.forEach(cb => {
      const parentItem = cb.closest('.workout-item');
      if (cb.checked) {
        completed++;
        if (parentItem) parentItem.classList.add('completed');
      } else {
        if (parentItem) parentItem.classList.remove('completed');
      }
    });

    const pct = Math.round((completed / workoutCheckboxes.length) * 100);
    if (workoutProgressPct) workoutProgressPct.textContent = `${pct}%`;
    if (workoutProgressBar) workoutProgressBar.style.width = `${pct}%`;
  }

  workoutCheckboxes.forEach(cb => {
    cb.addEventListener('change', updateWorkoutProgress);
  });
}

/* ==========================================================================
   6. DIET PLANNER TABS
   ========================================================================== */
function initDietPlannerTabs() {
  const tabs = document.querySelectorAll('.diet-tab-btn');
  const mealSections = document.querySelectorAll('.meal-detail-section');
  if (!tabs.length || !mealSections.length) return;

  tabs.forEach(tab => {
    tab.addEventListener('click', function () {
      tabs.forEach(t => t.classList.remove('active'));
      mealSections.forEach(s => s.style.display = 'none');

      tab.classList.add('active');
      const targetId = tab.getAttribute('data-target');
      const targetSection = document.getElementById(targetId);
      if (targetSection) {
        targetSection.style.display = 'block';
      }
    });
  });
}

/* ==========================================================================
   7. 30-DAY FITNESS PLAN MODAL
   ========================================================================== */
function init30DayPlanModal() {
  const dayCards = document.querySelectorAll('.day-card');
  const modalOverlay = document.getElementById('dayDetailModal');
  const modalTitle = document.getElementById('modalDayTitle');
  const modalFocus = document.getElementById('modalDayFocus');
  const modalDuration = document.getElementById('modalDayDuration');
  const modalCalories = document.getElementById('modalDayCalories');
  const modalStatus = document.getElementById('modalDayStatus');
  const modalClose = document.getElementById('modalDayClose');
  const modalMarkDone = document.getElementById('modalDayMarkDone');

  let activeCard = null;

  if (!dayCards.length || !modalOverlay) return;

  dayCards.forEach(card => {
    card.addEventListener('click', function () {
      activeCard = card;
      const dayNum = card.getAttribute('data-day');
      const title = card.getAttribute('data-title');
      const duration = card.getAttribute('data-duration') || '30 mins';
      const cals = card.getAttribute('data-cals') || '250 kcal';
      const status = card.getAttribute('data-status');

      if (modalTitle) modalTitle.textContent = `Day ${dayNum}: ${title}`;
      if (modalFocus) modalFocus.textContent = title;
      if (modalDuration) modalDuration.textContent = duration;
      if (modalCalories) modalCalories.textContent = cals;
      if (modalStatus) {
        modalStatus.textContent = status ? status.toUpperCase() : 'UPCOMING';
      }

      modalOverlay.classList.add('active');
    });
  });

  if (modalClose) {
    modalClose.addEventListener('click', function () {
      modalOverlay.classList.remove('active');
    });
  }

  if (modalOverlay) {
    modalOverlay.addEventListener('click', function (e) {
      if (e.target === modalOverlay) {
        modalOverlay.classList.remove('active');
      }
    });
  }

  if (modalMarkDone && modalOverlay) {
    modalMarkDone.addEventListener('click', function () {
      if (activeCard) {
        activeCard.classList.remove('upcoming', 'today');
        activeCard.classList.add('completed');
        const iconSpan = activeCard.querySelector('.day-status-pill');
        if (iconSpan) {
          iconSpan.className = 'day-status-pill status-check';
          iconSpan.innerHTML = '<i class="fa-solid fa-check"></i>';
        }
      }
      modalOverlay.classList.remove('active');
    });
  }
}

/* ==========================================================================
   8. WORKOUT SESSION DEMO MODAL
   ========================================================================== */
function initWorkoutSessionModal() {
  const startWorkoutBtns = document.querySelectorAll('.btn-start-workout');
  const workoutModal = document.getElementById('workoutSessionModal');
  const timerDisplay = document.getElementById('workoutTimerDisplay');
  const pausePlayBtn = document.getElementById('workoutTimerPausePlay');
  const closeBtn = document.getElementById('workoutModalClose');

  if (!workoutModal) return;

  let timerInterval = null;
  let secondsElapsed = 0;
  let isRunning = false;

  function formatTime(secs) {
    const mins = Math.floor(secs / 60);
    const s = secs % 60;
    return `${mins < 10 ? '0' : ''}${mins}:${s < 10 ? '0' : ''}${s}`;
  }

  function startTimer() {
    isRunning = true;
    if (pausePlayBtn) pausePlayBtn.innerHTML = '<i class="fa-solid fa-pause"></i> Pause';
    timerInterval = setInterval(() => {
      secondsElapsed++;
      if (timerDisplay) timerDisplay.textContent = formatTime(secondsElapsed);
    }, 1000);
  }

  function pauseTimer() {
    isRunning = false;
    clearInterval(timerInterval);
    if (pausePlayBtn) pausePlayBtn.innerHTML = '<i class="fa-solid fa-play"></i> Resume';
  }

  startWorkoutBtns.forEach(btn => {
    btn.addEventListener('click', function () {
      secondsElapsed = 0;
      if (timerDisplay) timerDisplay.textContent = '00:00';
      workoutModal.classList.add('active');
      startTimer();
    });
  });

  if (pausePlayBtn) {
    pausePlayBtn.addEventListener('click', function () {
      if (isRunning) pauseTimer();
      else startTimer();
    });
  }

  if (closeBtn) {
    closeBtn.addEventListener('click', function () {
      pauseTimer();
      workoutModal.classList.remove('active');
    });
  }
}

/* ==========================================================================
   9. AI FITNESS ASSISTANT CHATBOT
   ========================================================================== */
function initChatbot() {
  const chatMessagesArea = document.getElementById('chatMessagesArea');
  const chatInput = document.getElementById('chatInput');
  const chatSendBtn = document.getElementById('chatSendBtn');
  const suggestionChips = document.querySelectorAll('.suggestion-chip');

  if (!chatMessagesArea || !chatInput || !chatSendBtn) return;

  function appendMessage(sender, text) {
    const now = new Date();
    const timeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    const row = document.createElement('div');
    row.className = `message-row ${sender === 'user' ? 'user-row' : 'ai-row'}`;

    const avatar = document.createElement('div');
    avatar.className = `message-avatar ${sender === 'user' ? 'user-avatar' : 'ai-avatar'}`;
    avatar.innerHTML = sender === 'user' ? '<i class="fa-solid fa-user"></i>' : '<i class="fa-solid fa-robot"></i>';

    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    bubble.innerHTML = text.replace(/\n/g, '<br>');

    const time = document.createElement('div');
    time.className = 'message-time';
    time.textContent = timeStr;
    bubble.appendChild(time);

    row.appendChild(avatar);
    row.appendChild(bubble);

    chatMessagesArea.appendChild(row);
    chatMessagesArea.scrollTop = chatMessagesArea.scrollHeight;
  }

  function generateAIResponse(userText) {
    const text = userText.toLowerCase();

    // Show typing indicator
    const typingRow = document.createElement('div');
    typingRow.className = 'message-row ai-row';
    typingRow.id = 'aiTypingIndicator';
    typingRow.innerHTML = `
      <div class="message-avatar ai-avatar"><i class="fa-solid fa-robot"></i></div>
      <div class="message-bubble" style="color: #64748b; font-style: italic;">
        AI is typing<span class="typing-dots">...</span>
      </div>
    `;
    chatMessagesArea.appendChild(typingRow);
    chatMessagesArea.scrollTop = chatMessagesArea.scrollHeight;

    setTimeout(() => {
      const typingEl = document.getElementById('aiTypingIndicator');
      if (typingEl) typingEl.remove();

      let reply = "I'm here to help you hit your fitness goals! You can ask me about beginner workouts, high-protein meal options, BMI evaluation, or staying motivated.";

      if (text.includes('workout') || text.includes('exercise')) {
        reply = "Here is a quick high-energy bodyweight circuit:\n• 15 Bodyweight Squats\n• 10 Push-ups\n• 15 Glute Bridges\n• 20 Jumping Jacks\n• 30s Forearm Plank\n\nPerform 3 rounds with 60 seconds rest in between. Focus on crisp form!";
      } else if (text.includes('protein') || text.includes('diet') || text.includes('meal') || text.includes('breakfast')) {
        reply = "For high-protein clean nutrition, try:\n• Breakfast: Rolled oats with chia seeds, scoop of protein/almonds, and sliced banana.\n• Lunch: Grilled paneer/tofu or chicken breast with brown rice & steamed broccoli.\n• Snack: Greek yogurt with roasted walnuts.\n• Target: 1.6g - 2.0g protein per kg of bodyweight.";
      } else if (text.includes('water') || text.includes('hydrate')) {
        reply = "Hydration is essential for metabolic rate and muscle recovery! We recommend drinking at least 2.5 to 3 Liters (8 to 10 glasses) of water daily. Try having 1 glass right after waking up.";
      } else if (text.includes('weight loss') || text.includes('lose weight')) {
        reply = "Sustainable fat loss formula:\n1. Maintain a modest 300-500 kcal daily deficit.\n2. Prioritize 10,000 daily steps for steady NEAT (activity).\n3. Lift weights 3-4x weekly to protect lean muscle tissue.\n4. Sleep 7-8 hours for hormone balance.";
      } else if (text.includes('sore') || text.includes('pain') || text.includes('recovery')) {
        reply = "Delayed Onset Muscle Soreness (DOMS) is common. To recover quickly:\n• Light dynamic walking or swimming\n• Adequate hydration + electrolyte intake\n• 10 mins of gentle stretching or foam rolling\n• High protein intake for tissue rebuilding.";
      }

      appendMessage('ai', reply);
    }, 700);
  }

  function handleSend() {
    const text = chatInput.value.trim();
    if (!text) return;
    appendMessage('user', text);
    chatInput.value = '';
    generateAIResponse(text);
  }

  chatSendBtn.addEventListener('click', handleSend);
  chatInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
      handleSend();
    }
  });

  suggestionChips.forEach(chip => {
    chip.addEventListener('click', function () {
      const prompt = chip.getAttribute('data-prompt') || chip.textContent.trim();
      chatInput.value = prompt;
      handleSend();
    });
  });
}

/* ==========================================================================
   10. PROGRESS TRACKING (Chart.js Visualization)
   ========================================================================== */
function initProgressCharts() {
  const weightChartCanvas = document.getElementById('weightProgressChart');
  const activityChartCanvas = document.getElementById('activityBarChart');

  if (typeof Chart === 'undefined') return;

  // 1. Line Chart: Weight Progress
  if (weightChartCanvas) {
    const ctx = weightChartCanvas.getContext('2d');
    const gradient = ctx.createLinearGradient(0, 0, 0, 300);
    gradient.addColorStop(0, 'rgba(16, 185, 129, 0.25)');
    gradient.addColorStop(1, 'rgba(16, 185, 129, 0.0)');

    window.weightChartInstance = new Chart(ctx, {
      type: 'line',
      data: {
        labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
        datasets: [{
          label: 'Weight (kg)',
          data: [70.0, 69.5, 68.8, 68.0],
          borderColor: '#10b981',
          borderWidth: 3,
          backgroundColor: gradient,
          fill: true,
          tension: 0.35,
          pointBackgroundColor: '#ffffff',
          pointBorderColor: '#10b981',
          pointBorderWidth: 3,
          pointRadius: 6,
          pointHoverRadius: 8
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: '#0f172a',
            padding: 10,
            titleFont: { size: 13, weight: 'bold' },
            bodyFont: { size: 12 },
            cornerRadius: 8,
            displayColors: false,
            callbacks: {
              label: (context) => `Weight: ${context.parsed.y} kg`
            }
          }
        },
        scales: {
          y: {
            min: 64,
            max: 72,
            grid: { color: '#f1f5f9' },
            ticks: {
              stepSize: 1,
              callback: (val) => `${val} kg`,
              font: { family: 'Plus Jakarta Sans', size: 11 },
              color: '#64748b'
            }
          },
          x: {
            grid: { display: false },
            ticks: {
              font: { family: 'Plus Jakarta Sans', size: 11 },
              color: '#64748b'
            }
          }
        }
      }
    });
  }

  // 2. Bar Chart: Weekly Activity Steps
  if (activityChartCanvas) {
    const actCtx = activityChartCanvas.getContext('2d');
    new Chart(actCtx, {
      type: 'bar',
      data: {
        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        datasets: [{
          label: 'Steps',
          data: [7200, 8400, 6900, 9100, 6240, 10500, 8100],
          backgroundColor: '#38bdf8',
          borderRadius: 8,
          hoverBackgroundColor: '#0284c7',
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false }
        },
        scales: {
          y: {
            grid: { color: '#f1f5f9' },
            ticks: {
              stepSize: 3000,
              font: { family: 'Plus Jakarta Sans', size: 11 },
              color: '#64748b'
            }
          },
          x: {
            grid: { display: false },
            ticks: {
              font: { family: 'Plus Jakarta Sans', size: 11 },
              color: '#64748b'
            }
          }
        }
      }
    });
  }

  // Weight Logging simulation
  const logWeightBtn = document.getElementById('btnLogWeight');
  const logWeightModal = document.getElementById('logWeightModal');
  const logWeightClose = document.getElementById('logWeightClose');
  const logWeightForm = document.getElementById('logWeightForm');

  if (logWeightBtn && logWeightModal) {
    logWeightBtn.addEventListener('click', () => logWeightModal.classList.add('active'));
  }
  if (logWeightClose && logWeightModal) {
    logWeightClose.addEventListener('click', () => logWeightModal.classList.remove('active'));
  }
  if (logWeightForm) {
    logWeightForm.addEventListener('submit', function (e) {
      e.preventDefault();
      const newWeight = parseFloat(document.getElementById('inputNewWeight')?.value || 67.5);
      if (window.weightChartInstance) {
        window.weightChartInstance.data.labels.push('Week 5');
        window.weightChartInstance.data.datasets[0].data.push(newWeight);
        window.weightChartInstance.update();
      }
      logWeightModal.classList.remove('active');
    });
  }
}

/* ==========================================================================
   11. PROFILE EDIT MODAL INTERACTION
   ========================================================================== */
function initProfileEdit() {
  const btnEditProfile = document.getElementById('btnEditProfile');
  const profileEditModal = document.getElementById('profileEditModal');
  const profileEditClose = document.getElementById('profileEditClose');
  const profileEditForm = document.getElementById('profileEditForm');

  if (!btnEditProfile || !profileEditModal) return;

  btnEditProfile.addEventListener('click', () => {
    profileEditModal.classList.add('active');
  });

  if (profileEditClose) {
    profileEditClose.addEventListener('click', () => {
      profileEditModal.classList.remove('active');
    });
  }

  if (profileEditForm) {
    profileEditForm.addEventListener('submit', function (e) {
      e.preventDefault();
      const name = document.getElementById('profileEditName')?.value;
      const age = document.getElementById('profileEditAge')?.value;
      const weight = document.getElementById('profileEditWeight')?.value;
      const targetWeight = document.getElementById('profileEditTargetWeight')?.value;

      if (name) {
        const nameDisplay = document.getElementById('profileNameDisplay');
        if (nameDisplay) nameDisplay.textContent = name;
      }
      if (age) {
        const ageDisplay = document.getElementById('profileAgeDisplay');
        if (ageDisplay) ageDisplay.textContent = age;
      }
      if (weight) {
        const weightDisplay = document.getElementById('profileWeightDisplay');
        if (weightDisplay) weightDisplay.textContent = `${weight} kg`;
      }
      if (targetWeight) {
        const targetDisplay = document.getElementById('profileTargetDisplay');
        if (targetDisplay) targetDisplay.textContent = `${targetWeight} kg`;
      }

      profileEditModal.classList.remove('active');
    });
  }
}
