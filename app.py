from flask import Flask, render_template_string, request, jsonify
from flask_cors import CORS
import threading
import time
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import sys
import io

# Fix encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

app = Flask(__name__)
CORS(app)

# Store active monitors
active_monitors = {}

# Your Gmail credentials for sending notifications
SENDER_EMAIL = "sathviknarayana49@gmail.com"
SENDER_PASSWORD = "ubxzqtnptksgsyqz"

class TicketMonitor:
    def __init__(self, user_email, city, movie_name, date, theater_name, monitor_id):
        self.user_email = user_email
        self.city = city
        self.movie_name = movie_name
        self.date = date
        self.theater_name = theater_name
        self.monitor_id = monitor_id
        self.is_running = True
        self.notification_sent = False
        
    def setup_driver(self):
        """Setup Chrome driver"""
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            return driver
        except:
            return None
    
    def send_notification(self, subject, body):
        """Send email notification"""
        try:
            msg = MIMEMultipart()
            msg['From'] = SENDER_EMAIL
            msg['To'] = self.user_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'html'))
            
            server = smtplib.SMTP('smtp.gmail.com', 587, timeout=30)
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            
            text = msg.as_string()
            server.sendmail(SENDER_EMAIL, self.user_email, text)
            server.quit()
            
            print(f"[{self.monitor_id}] Notification sent to {self.user_email}")
            return True
        except Exception as e:
            print(f"[{self.monitor_id}] Email failed: {e}")
            return False
    
    def check_tickets(self):
        """Check for ticket availability"""
        driver = self.setup_driver()
        if not driver:
            return None
        
        try:
            # Build BookMyShow URL
            search_url = f"https://in.bookmyshow.com/{self.city}/movies"
            driver.get(search_url)
            time.sleep(5)
            
            page_source = driver.page_source.lower()
            
            # Check if movie exists
            movie_check = self.movie_name.lower().replace(" ", "")
            if movie_check in page_source:
                # Check for theater if specified
                if self.theater_name and self.theater_name != "Any theater":
                    theater_check = self.theater_name.lower()
                    if theater_check not in page_source:
                        return False
                
                # Check for booking indicators
                booking_indicators = ["book", "available", "buy tickets", "₹"]
                if any(ind in page_source for ind in booking_indicators):
                    return True
            
            return False
            
        except Exception as e:
            print(f"[{self.monitor_id}] Error: {e}")
            return None
        finally:
            driver.quit()
    
    def start_monitoring(self):
        """Start the monitoring loop"""
        print(f"[{self.monitor_id}] Started monitoring for {self.user_email}")
        
        # Send startup confirmation
        startup_subject = "✅ Monitoring Started - BookMyShow Notifier"
        startup_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <div style="background-color: #d1ecf1; padding: 20px; border-radius: 10px;">
                    <h2 style="color: #0c5460;">🎬 Monitoring Started!</h2>
                    <p>We're now watching for tickets with these details:</p>
                    <ul>
                        <li><strong>Movie:</strong> {self.movie_name}</li>
                        <li><strong>City:</strong> {self.city.title()}</li>
                        <li><strong>Date:</strong> {self.date}</li>
                        <li><strong>Theater:</strong> {self.theater_name}</li>
                    </ul>
                    <p style="margin-top: 20px;">
                        You'll receive an email notification as soon as tickets are available!
                    </p>
                    <p style="font-size: 12px; color: #666;">
                        Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                    </p>
                </div>
            </body>
        </html>
        """
        self.send_notification(startup_subject, startup_body)
        
        check_count = 0
        while self.is_running:
            check_count += 1
            print(f"[{self.monitor_id}] Check #{check_count}")
            
            result = self.check_tickets()
            
            if result and not self.notification_sent:
                # Tickets found!
                print(f"[{self.monitor_id}] TICKETS FOUND!")
                
                ticket_subject = "🎟️ TICKETS AVAILABLE NOW! - BookMyShow"
                ticket_body = f"""
                <html>
                    <body style="font-family: Arial, sans-serif; padding: 20px;">
                        <div style="background-color: white; padding: 30px; border-radius: 10px;">
                            <h1 style="color: #e74c3c;">🎉 TICKETS AVAILABLE!</h1>
                            
                            <div style="background-color: #d4edda; padding: 20px; border-radius: 10px; margin: 20px 0;">
                                <h3 style="color: #155724;">Booking Details:</h3>
                                <p><strong>🎬 Movie:</strong> {self.movie_name}</p>
                                <p><strong>📍 City:</strong> {self.city.title()}</p>
                                <p><strong>📅 Date:</strong> {self.date}</p>
                                <p><strong>🎭 Theater:</strong> {self.theater_name}</p>
                            </div>
                            
                            <div style="text-align: center; margin: 30px 0;">
                                <a href="https://in.bookmyshow.com/{self.city}/movies" 
                                   style="background-color: #e74c3c; color: white; padding: 15px 40px; 
                                          text-decoration: none; border-radius: 5px; font-size: 18px; 
                                          font-weight: bold; display: inline-block;">
                                    🎟️ BOOK NOW
                                </a>
                            </div>
                            
                            <p style="color: #666; font-size: 12px; text-align: center;">
                                Detected at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                            </p>
                        </div>
                    </body>
                </html>
                """
                
                if self.send_notification(ticket_subject, ticket_body):
                    self.notification_sent = True
                    print(f"[{self.monitor_id}] Notification sent successfully!")
                    # Stop monitoring after notification
                    self.is_running = False
                    break
            
            # Wait 15 minutes before next check
            if self.is_running:
                time.sleep(15 * 60)
        
        print(f"[{self.monitor_id}] Monitoring stopped")

# Read the HTML file
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BookMyShow Ticket Notifier</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 500px;
            width: 100%;
            padding: 40px;
        }
        .header { text-align: center; margin-bottom: 30px; }
        .header h1 { color: #333; font-size: 28px; margin-bottom: 10px; }
        .header .icon { font-size: 50px; margin-bottom: 10px; }
        .header p { color: #666; font-size: 14px; }
        .form-group { margin-bottom: 20px; }
        .form-group label {
            display: block;
            color: #333;
            font-weight: 600;
            margin-bottom: 8px;
            font-size: 14px;
        }
        .required { color: #e74c3c; }
        .optional { color: #95a5a6; font-weight: 400; font-size: 12px; }
        .form-group input, .city-select {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 14px;
            transition: all 0.3s;
        }
        .form-group input:focus, .city-select:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        .submit-btn {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .submit-btn:hover { transform: translateY(-2px); }
        .info-box {
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            font-size: 13px;
        }
        .success-message {
            background: #d4edda;
            border-left: 4px solid #28a745;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            display: none;
        }
        .example-text { font-size: 12px; color: #95a5a6; margin-top: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="icon">🎬</div>
            <h1>BookMyShow Notifier</h1>
            <p>Get instant notifications when tickets are available!</p>
        </div>
        <div class="info-box">
            <strong>📧 How it works:</strong><br>
            Enter your details and we'll notify you via email when tickets are available!
        </div>
        <form id="notifierForm">
            <div class="form-group">
                <label>Email Address <span class="required">*</span></label>
                <input type="email" id="email" placeholder="your.email@gmail.com" required>
            </div>
            <div class="form-group">
                <label>City <span class="required">*</span></label>
                <select class="city-select" id="city" required>
                    <option value="">Select city</option>
                    <option value="hyderabad">Hyderabad</option>
                    <option value="bangalore">Bangalore</option>
                    <option value="mumbai">Mumbai</option>
                    <option value="delhi-ncr">Delhi-NCR</option>
                    <option value="chennai">Chennai</option>
                    <option value="pune">Pune</option>
                </select>
            </div>
            <div class="form-group">
                <label>Movie Name <span class="required">*</span></label>
                <input type="text" id="movieName" placeholder="Enter movie name" required>
            </div>
            <div class="form-group">
                <label>Date <span class="optional">(Optional)</span></label>
                <input type="date" id="date">
            </div>
            <div class="form-group">
                <label>Theater <span class="optional">(Optional)</span></label>
                <input type="text" id="theaterName" placeholder="Enter theater name">
            </div>
            <button type="submit" class="submit-btn">🔔 Start Monitoring</button>
        </form>
        <div class="success-message" id="successMessage">
            <h3>✅ Monitoring Started!</h3>
            <p>Check your email for confirmation!</p>
        </div>
    </div>
    <script>
        document.getElementById('notifierForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const data = {
                email: document.getElementById('email').value,
                city: document.getElementById('city').value,
                movieName: document.getElementById('movieName').value,
                date: document.getElementById('date').value || 'Any date',
                theaterName: document.getElementById('theaterName').value || 'Any theater'
            };
            
            try {
                const response = await fetch('/api/start-monitoring', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                
                if (response.ok) {
                    document.getElementById('successMessage').style.display = 'block';
                    document.getElementById('notifierForm').reset();
                }
            } catch (error) {
                alert('Error starting monitoring. Please try again.');
            }
        });
        
        const today = new Date().toISOString().split('T')[0];
        document.getElementById('date').setAttribute('min', today);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/start-monitoring', methods=['POST'])
def start_monitoring():
    data = request.json
    
    # Generate unique monitor ID
    monitor_id = f"monitor_{len(active_monitors) + 1}_{int(time.time())}"
    
    # Create monitor instance
    monitor = TicketMonitor(
        user_email=data['email'],
        city=data['city'],
        movie_name=data['movieName'],
        date=data['date'],
        theater_name=data['theaterName'],
        monitor_id=monitor_id
    )
    
    # Start monitoring in background thread
    thread = threading.Thread(target=monitor.start_monitoring, daemon=True)
    thread.start()
    
    # Store active monitor
    active_monitors[monitor_id] = {
        'monitor': monitor,
        'thread': thread,
        'started_at': datetime.now()
    }
    
    return jsonify({
        'success': True,
        'monitor_id': monitor_id,
        'message': 'Monitoring started successfully!'
    })

@app.route('/api/active-monitors')
def get_active_monitors():
    monitors_info = []
    for monitor_id, info in active_monitors.items():
        monitors_info.append({
            'id': monitor_id,
            'email': info['monitor'].user_email,
            'movie': info['monitor'].movie_name,
            'started_at': info['started_at'].strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify(monitors_info)

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🎬 BookMyShow Notifier Server")
    print("="*60)
    print("Server starting on: http://127.0.0.1:5000")
    print("Open this URL in your browser!")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)