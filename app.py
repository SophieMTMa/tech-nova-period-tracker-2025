from flask import Flask, render_template, request, redirect, url_for, Response
from pymongo import MongoClient
import os
import csv

app = Flask(__name__)

# MongoDB setup
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URI)
db = client['period_tracker']

users = db['users']
logs = db['logs']

@app.route('/export_logs')
def export_logs():
    log_entries = list(logs.find().sort('date', -1))
    def generate():
        header = ['date', 'energy', 'mood', 'focus', 'notes']
        yield ','.join(header) + '\n'
        for log in log_entries:
            row = [str(log.get(col, '')) for col in header]
            yield ','.join(row) + '\n'
    return Response(generate(), mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=cycle_logs.csv"})
@app.route('/log', methods=['GET', 'POST'])
def log():
    recommendation = None
    recent_logs = list(logs.find().sort('date', -1).limit(5))
    # Analytics: calculate averages
    if recent_logs:
        avg_energy = round(sum(log['energy'] for log in recent_logs) / len(recent_logs), 2)
        avg_mood = round(sum(log['mood'] for log in recent_logs) / len(recent_logs), 2)
        avg_focus = round(sum(log['focus'] for log in recent_logs) / len(recent_logs), 2)
    else:
        avg_energy = avg_mood = avg_focus = None
    if request.method == 'POST':
        date = request.form['date']
        energy = int(request.form['energy'])
        mood = int(request.form['mood'])
        focus = int(request.form['focus'])
        notes = request.form.get('notes', '')
        log_entry = {
            'date': date,
            'energy': energy,
            'mood': mood,
            'focus': focus,
            'notes': notes
        }
        logs.insert_one(log_entry)
        # Simple focus hour recommendation logic
        if energy >= 4 and focus >= 4:
            recommendation = "Today is a great day for deep work and creative tasks. Schedule important work in the morning."
        elif energy >= 3:
            recommendation = "You have moderate energy. Focus on routine tasks and meetings."
        else:
            recommendation = "Low energy detected. Prioritize rest, self-care, and light tasks."
        recent_logs = list(logs.find().sort('date', -1).limit(5))
        if recent_logs:
            avg_energy = round(sum(log['energy'] for log in recent_logs) / len(recent_logs), 2)
            avg_mood = round(sum(log['mood'] for log in recent_logs) / len(recent_logs), 2)
            avg_focus = round(sum(log['focus'] for log in recent_logs) / len(recent_logs), 2)
        else:
            avg_energy = avg_mood = avg_focus = None
        return render_template('log.html', recommendation=recommendation, recent_logs=recent_logs, avg_energy=avg_energy, avg_mood=avg_mood, avg_focus=avg_focus)
    return render_template('log.html', recent_logs=recent_logs, avg_energy=avg_energy, avg_mood=avg_mood, avg_focus=avg_focus)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/track', methods=['GET', 'POST'])
def track():
    phase_info = None
    fitness = None
    nutrition = None
    recent_periods = list(users.find().sort('start_date', -1).limit(5))
    if request.method == 'POST':
        start_date = request.form['start_date']
        cycle_length = int(request.form['cycle_length'])
        user_data = {
            'start_date': start_date,
            'cycle_length': cycle_length
        }
        users.insert_one(user_data)

        # Calculate phase
        from datetime import datetime, timedelta
        today = datetime.today().date()
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        days_since = (today - start).days % cycle_length
        if days_since < 5:
            phase = 'Menstrual'
            phase_info = "You're in the Menstrual phase. Energy may be low, prioritize rest and gentle movement."
            fitness = "Recommended: Stretching, walking."
            nutrition = "Iron-rich foods (spinach, lentils, red meat) help replenish lost nutrients."
        elif days_since < 14:
            phase = 'Follicular'
            phase_info = "You're in the Follicular phase. Energy and focus rise, great for new projects."
            fitness = "Recommended: Strength training, HIIT."
            nutrition = "Complex carbs and protein (quinoa, eggs) support energy."
        elif days_since < 17:
            phase = 'Ovulation'
            phase_info = "You're in Ovulation. Peak energy and mood, ideal for social and high-intensity activities."
            fitness = "Recommended: Cardio, group workouts."
            nutrition = "Lighter, high-protein meals (chicken, tofu) are best."
        else:
            phase = 'Luteal'
            phase_info = "You're in the Luteal phase. Energy may dip, focus on self-care and winding down."
            fitness = "Recommended: Yoga, light cardio."
            nutrition = "Magnesium-rich foods (nuts, dark chocolate) help with PMS."

        # Predict next period using average cycle length
        recent_periods = list(users.find().sort('start_date', -1).limit(5))
        if recent_periods:
            avg_cycle = round(sum(int(p['cycle_length']) for p in recent_periods) / len(recent_periods))
            most_recent_start = datetime.strptime(recent_periods[0]['start_date'], '%Y-%m-%d').date()
            next_period_start = most_recent_start + timedelta(days=avg_cycle)
            period_prediction = f"Your next period is predicted to start on {next_period_start.strftime('%Y-%m-%d')} (avg cycle: {avg_cycle} days) and last 5-8 days."
        else:
            next_period_start = start + timedelta(days=cycle_length)
            period_prediction = f"Your next period is predicted to start on {next_period_start.strftime('%Y-%m-%d')} and last 5-8 days."

        return render_template('track.html', phase=phase, phase_info=phase_info, fitness=fitness, nutrition=nutrition, recent_periods=recent_periods, period_prediction=period_prediction)
    return render_template('track.html', recent_periods=recent_periods)


# Temporary route to clear all data for testing
@app.route('/reset-db')
def reset_db():
    users.delete_many({})
    logs.delete_many({})
    return "All data cleared. You can now test with fresh input. Remove this route after testing for security."

if __name__ == '__main__':
    app.run(debug=True)
