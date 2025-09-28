
# Flow State: Comprehensive Period Tracker & Wellness Recommender

## Inspiration
Women naturally experience different energy levels throughout their menstrual cycle, where lifestyle choices—workouts, nutrition, and focus—can be optimized for each phase. We wanted to build a website that empowers women to thrive, no matter where they are in their cycle.


## Features & Frameworks
**Flow State** offers a unique blend of wellness tracking and actionable recommendations:

### 1. Cycle Phase Tracking
- **Frameworks:** Python (Flask), MongoDB
- **How:** Users input their last period start date and average cycle length. Flask processes this data, stores it in MongoDB, and calculates the current phase (Menstrual, Follicular, Ovulation, Luteal) using date math. The app displays phase-specific advice and predictions for the next period using average cycle length ($\text{avg cycle length} = \frac{\sum_{i=1}^n \text{cycle}_i}{n}$).

### 2. Fitness & Nutrition Recommendations
- **Frameworks:** Python (Flask), HTML/CSS
- **How:** Flask dynamically renders recommendations for workouts and nutrition based on the user's current cycle phase. These are shown on the tracking page, with tips tailored to each phase.

### 3. Daily Log & Analytics
- **Frameworks:** Python (Flask), MongoDB, Chart.js, HTML/CSS
- **How:** Users log daily mood, energy, focus, and notes. Flask saves logs to MongoDB, computes averages, and passes data to Chart.js for interactive visualizations. Analytics are shown for the last 5 logs, helping users spot trends and optimize routines.

### 4. Cycle History Visualization
- **Frameworks:** Python (Flask), MongoDB, Chart.js
- **How:** The app displays a table and chart of recent periods, visualizing cycle length fluctuations and trends. Data is fetched from MongoDB and rendered with Chart.js for clarity.

### 5. CSV Export
- **Frameworks:** Python (Flask)
- **How:** Users can export their logs and period history as CSV files for personal use or further analysis. Flask generates CSV responses from MongoDB data.

### 6. User Interface
- **Frameworks:** HTML, CSS, Figma (design)
- **How:** The UI is wireframed in Figma, then implemented with HTML and CSS for a clean, responsive experience. Buttons, forms, and navigation are designed for ease of use.

---

## How to Run & Replicate Flow State
Follow these steps to set up Flow State on your own machine:

### Prerequisites
- Python 3.10+
- pip
- MongoDB (local or cloud)

### 1. Clone the Repository
```bash
git clone https://github.com/SophieMTMa/tech-nova-period-tracker-2025.git
cd tech-nova-period-tracker-2025
```

### 2. Install Dependencies
```bash
pip install flask pymongo
```

### 3. Start MongoDB
If local, run:
```bash
mongod --dbpath ./dbdata
```
Or use your preferred MongoDB setup.

### 4. Run the Flask App
```bash
python app.py
```
Visit `http://localhost:5000` in your browser.

### 5. Test Features
- Track your cycle, log daily stats, view analytics, and export data.

---
**Tip:** If you encounter `ServerSelectionTimeoutError`, ensure MongoDB is running and accessible at the URI in `app.py`.

## How We Built It
- **Design:** Wireframed in Figma for a user-friendly, modern interface
- **Frontend:** HTML, CSS for responsive layouts and clean visuals
- **Backend:** Python (Flask) for server logic and routing
- **Database:** MongoDB to store user cycles, logs, and analytics
- **Visualization:** Chart.js for interactive graphs

## Challenges We Ran Into
We had many ideas, but limited time and simultaneous workshops meant we couldn't implement every feature we envisioned. Our main challenge was prioritizing core functionalities and ensuring a robust, testable MVP. Technical hurdles included:
- Setting up MongoDB in a containerized dev environment
- Debugging pymongo connection errors (e.g., `ServerSelectionTimeoutError`)
- Managing port conflicts and process lifecycles

## Accomplishments That We're Proud Of
We are proud to have built a website that:
1. Tracks menstrual cycles and predicts next periods using average cycle length ($\text{avg cycle length} = \frac{\sum_{i=1}^n \text{cycle}_i}{n}$)
2. Provides actionable recommendations for fitness and nutrition based on cycle phase
3. Offers daily logging and analytics for mood, energy, and focus, visualized with interactive charts

## What We Learned
- How to integrate Flask with MongoDB and handle real-world database errors
- The importance of user experience in health tech
- How to design recommendations based on biological cycles and data
- The value of rapid prototyping and iterative testing

## What's Next for Flow State
- Add personalized notifications and reminders
- Integrate more granular analytics (e.g., symptom tracking, hormonal trends)
- Expand recommendations to include mindfulness and productivity tips
- Mobile app version for on-the-go tracking

---
Flow State is more than a tracker—it's a wellness companion for every phase of life.