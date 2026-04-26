# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager
# import time
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from datetime import datetime
# import sys
# import io
# import random

# # Fix Windows encoding issue with emojis
# if sys.platform == "win32":
#     sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# # Disable output buffering for real-time debug messages
# sys.stdout.reconfigure(line_buffering=True)

# class BookMyShowRealMonitor:
#     def __init__(self, email_from, email_password, email_to):
#         self.email_from = email_from
#         self.email_password = email_password
#         self.email_to = email_to
#         self.movie_name = "Mana Shankar Varraprasad"
#         self.theater_name = "ART Cinemas"
#         self.city = "hyderabad"
#         self.target_date = "15th Jan"
#         self.movie_url = "https://in.bookmyshow.com/movies/hyderabad/mana-shankara-vara-prasad-garu/buytickets/ET00457184/20260115"
#         self.last_status = None
#         self.driver = None
#         self.notification_sent = False  # Track if we already sent notification
        
#     def setup_driver(self):
#         """Setup Chrome driver with enhanced anti-detection"""
#         print("[SETUP] Setting up Chrome browser...", flush=True)
        
#         chrome_options = Options()
        
#         # Headless mode
#         chrome_options.add_argument("--headless=new")
        
#         # Anti-detection measures
#         chrome_options.add_argument("--no-sandbox")
#         chrome_options.add_argument("--disable-dev-shm-usage")
#         chrome_options.add_argument("--disable-blink-features=AutomationControlled")
#         chrome_options.add_argument("--disable-gpu")
#         chrome_options.add_argument("--window-size=1920,1080")
#         chrome_options.add_argument("--start-maximized")
        
#         # Random user agent
#         user_agents = [
#             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
#             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
#             "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
#         ]
#         chrome_options.add_argument(f"--user-agent={random.choice(user_agents)}")
        
#         # Additional stealth options
#         chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
#         chrome_options.add_experimental_option('useAutomationExtension', False)
#         chrome_options.add_argument("--disable-extensions")
#         chrome_options.add_argument("--disable-popup-blocking")
        
#         try:
#             service = Service(ChromeDriverManager().install())
#             self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
#             # Execute CDP commands to hide automation
#             self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
#                 "userAgent": random.choice(user_agents)
#             })
#             self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
#             print("[SETUP] ✓ Chrome browser ready!", flush=True)
#             return True
#         except Exception as e:
#             print(f"[ERROR] Failed to setup Chrome: {e}", flush=True)
#             return False
    
#     def close_driver(self):
#         """Close the browser"""
#         if self.driver:
#             try:
#                 self.driver.quit()
#                 print("[CLEANUP] Browser closed", flush=True)
#             except:
#                 pass
    
#     def send_email(self, subject, body):
#         """Send email notification"""
#         try:
#             print("\n[EMAIL] Sending notification...", flush=True)
            
#             msg = MIMEMultipart()
#             msg['From'] = self.email_from
#             msg['To'] = self.email_to
#             msg['Subject'] = subject
            
#             msg.attach(MIMEText(body, 'html'))
            
#             server = smtplib.SMTP('smtp.gmail.com', 587, timeout=30)
#             server.starttls()
#             server.login(self.email_from, self.email_password)
            
#             text = msg.as_string()
#             server.sendmail(self.email_from, self.email_to, text)
#             server.quit()
            
#             print(f"[EMAIL] ✓ Email sent at {datetime.now().strftime('%H:%M:%S')}", flush=True)
#             return True
#         except Exception as e:
#             print(f"[EMAIL] ✗ Failed: {e}", flush=True)
#             return False
    
#     def check_bookmyshow(self):
#         """Check BookMyShow for ART Cinemas ticket availability"""
#         try:
#             print(f"\n[BROWSER] Opening BookMyShow...", flush=True)
            
#             # Add random delay before loading
#             time.sleep(random.uniform(2, 4))
            
#             # Navigate to the movie page
#             self.driver.get(self.movie_url)
            
#             # Wait for page to load
#             print("[BROWSER] Loading page...", flush=True)
#             time.sleep(random.uniform(6, 10))
            
#             # Get page source
#             page_source = self.driver.page_source.lower()
#             page_length = len(page_source)
            
#             print(f"[BROWSER] Page loaded ({page_length} chars)", flush=True)
            
#             # Check if page has meaningful content
#             if page_length < 10000:
#                 print("[WARNING] Page seems too small - might be blocked", flush=True)
#                 return None
            
#             # Look for blocking indicators
#             blocking_keywords = ["access denied", "403", "blocked", "captcha"]
#             has_blocking = any(keyword in page_source for keyword in blocking_keywords)
            
#             # Look for valid content indicators
#             valid_keywords = ["bookmyshow", "movie", "cinema", "theater", "ticket"]
#             has_valid_content = any(keyword in page_source for keyword in valid_keywords)
            
#             if has_blocking and not has_valid_content:
#                 print("[WARNING] Page appears blocked - will retry next cycle", flush=True)
#                 return None
            
#             print("[CHECK] Searching for ART Cinemas...", flush=True)
            
#             # Check for ART Cinemas - be flexible with search
#             art_found = False
#             art_keywords = [
#                 "art cinema",
#                 "artcinema", 
#                 "vanasthalipuram",
#                 "art_cinema",
#                 "a.r.t cinema"
#             ]
            
#             for keyword in art_keywords:
#                 if keyword in page_source:
#                     print(f"[CHECK] ✓ Found: '{keyword}'", flush=True)
#                     art_found = True
#                     break
            
#             if not art_found:
#                 print("[CHECK] ⏳ ART Cinemas not listed yet for Jan 15th", flush=True)
#                 return False
            
#             # ART Cinemas found! Now check if tickets are bookable
#             print("[CHECK] ✓ ART Cinemas found! Checking ticket availability...", flush=True)
            
#             # Look for booking indicators
#             booking_indicators = [
#                 "book",
#                 "available",
#                 "select seats",
#                 "show times",
#                 "showtimes",
#                 "₹",
#                 "rs.",
#                 "buy tickets",
#                 "add to cart"
#             ]
            
#             found_booking = []
#             for indicator in booking_indicators:
#                 if indicator in page_source:
#                     found_booking.append(indicator)
            
#             if found_booking:
#                 print(f"[CHECK] 🎉 TICKETS AVAILABLE! Indicators: {found_booking}", flush=True)
#                 return True
#             else:
#                 print("[CHECK] ⏳ ART Cinemas listed but booking not open yet", flush=True)
#                 return False
                
#         except Exception as e:
#             print(f"[ERROR] Check failed: {type(e).__name__} - {e}", flush=True)
#             return None
    
#     def run_check(self):
#         """Run a single check cycle"""
#         print(f"\n{'='*60}", flush=True)
#         print(f"🔍 Check started: {datetime.now().strftime('%H:%M:%S')}", flush=True)
#         print(f"{'='*60}", flush=True)
        
#         # Setup browser
#         if not self.setup_driver():
#             print("[ERROR] Browser setup failed - will retry next cycle", flush=True)
#             return
        
#         try:
#             # Check BookMyShow
#             status = self.check_bookmyshow()
            
#             # If tickets became available AND we haven't sent notification yet
#             if status is True and not self.notification_sent:
#                 print("\n" + "🎊"*30, flush=True)
#                 print("🎉🎉🎉 TICKETS ARE NOW AVAILABLE! 🎉🎉🎉", flush=True)
#                 print("🎊"*30 + "\n", flush=True)
                
#                 subject = "🎟️ TICKETS AVAILABLE NOW! - ART Cinemas Jan 15th"
#                 body = f"""
#                 <html>
#                     <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f5f5f5;">
#                         <div style="background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
#                             <h1 style="color: #e74c3c; margin-top: 0; font-size: 32px;">🎉 TICKETS AVAILABLE!</h1>
                            
#                             <div style="background-color: #d4edda; padding: 20px; border-radius: 5px; border-left: 4px solid #28a745; margin: 20px 0;">
#                                 <h2 style="margin-top: 0; color: #155724;">📋 Booking Details:</h2>
#                                 <p style="margin: 10px 0; font-size: 18px;"><strong>🎬 Movie:</strong> Mana Shankar Varraprasad Garu</p>
#                                 <p style="margin: 10px 0; font-size: 18px;"><strong>🎭 Theater:</strong> ART Cinemas, Vanasthalipuram</p>
#                                 <p style="margin: 10px 0; font-size: 18px;"><strong>📅 Date:</strong> January 15th, 2026</p>
#                                 <p style="margin: 10px 0; font-size: 18px;"><strong>📍 Location:</strong> Hyderabad</p>
#                             </div>
                            
#                             <div style="background-color: #fff3cd; padding: 15px; border-radius: 5px; margin: 20px 0;">
#                                 <p style="margin: 0; color: #856404; font-size: 16px;">
#                                     ⚡ <strong>ACT FAST!</strong> Tickets might sell out quickly!
#                                 </p>
#                             </div>
                            
#                             <div style="text-align: center; margin: 30px 0;">
#                                 <a href="{self.movie_url}" 
#                                    style="background-color: #e74c3c; color: white; padding: 20px 50px; 
#                                           text-decoration: none; border-radius: 5px; font-size: 22px; 
#                                           font-weight: bold; display: inline-block; box-shadow: 0 4px 6px rgba(0,0,0,0.2);">
#                                     🎟️ BOOK NOW
#                                 </a>
#                             </div>
                            
#                             <p style="color: #666; font-size: 12px; margin-top: 30px; text-align: center;">
#                                 Detected at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
#                                 Click the button above or copy this link:<br>
#                                 <a href="{self.movie_url}" style="color: #007bff;">{self.movie_url}</a>
#                             </p>
#                         </div>
#                     </body>
#                 </html>
#                 """
                
#                 if self.send_email(subject, body):
#                     self.notification_sent = True
#                     print("\n✅ NOTIFICATION SENT SUCCESSFULLY!", flush=True)
#                     print("✅ Check your email and phone!", flush=True)
            
#             elif status is False:
#                 print("[RESULT] No tickets available yet - will check again", flush=True)
#             elif status is None:
#                 print("[RESULT] Check inconclusive - will retry", flush=True)
            
#             self.last_status = status
            
#         finally:
#             self.close_driver()
    
#     def start_monitoring(self, check_interval_minutes=15):
#         """Start continuous monitoring"""
#         print("\n" + "="*60, flush=True)
#         print("🎬 BookMyShow Real-Time Monitor", flush=True)
#         print("="*60, flush=True)
#         print(f"📧 Email: {self.email_to}", flush=True)
#         print(f"🎥 Movie: {self.movie_name}", flush=True)
#         print(f"🎭 Theater: {self.theater_name}", flush=True)
#         print(f"📅 Date: January 15th, 2026", flush=True)
#         print(f"⏱️  Interval: Every {check_interval_minutes} minutes", flush=True)
#         print("="*60, flush=True)
#         print("\n💡 Monitor running in background", flush=True)
#         print("💡 Press Ctrl+C to stop\n", flush=True)
        
#         # Send startup confirmation
#         startup_subject = "✅ Monitor Started - Watching for Tickets"
#         startup_body = f"""
#         <html>
#             <body style="font-family: Arial, sans-serif; padding: 20px;">
#                 <div style="background-color: #d1ecf1; padding: 20px; border-radius: 5px; border-left: 4px solid #0c5460;">
#                     <h2 style="margin-top: 0; color: #0c5460;">🤖 Monitor Active!</h2>
#                     <p>Your ticket monitor is now running and checking BookMyShow every {check_interval_minutes} minutes.</p>
#                     <h3>Watching for:</h3>
#                     <ul>
#                         <li><strong>Movie:</strong> {self.movie_name}</li>
#                         <li><strong>Theater:</strong> {self.theater_name}</li>
#                         <li><strong>Date:</strong> January 15th, 2026</li>
#                     </ul>
#                     <p style="margin-top: 20px;">
#                         You'll receive an <strong>instant notification</strong> when tickets become available!
#                     </p>
#                     <p style="color: #666; font-size: 12px;">
#                         Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
#                     </p>
#                 </div>
#             </body>
#         </html>
#         """
#         self.send_email(startup_subject, startup_body)
        
#         try:
#             check_count = 0
#             while True:
#                 check_count += 1
#                 print(f"\n📊 Check #{check_count}", flush=True)
                
#                 self.run_check()
                
#                 # If we've sent notification, we can stop monitoring
#                 if self.notification_sent:
#                     print("\n" + "="*60, flush=True)
#                     print("✅ Notification sent! Mission accomplished!", flush=True)
#                     print("="*60, flush=True)
#                     print("\nYou can:", flush=True)
#                     print("  - Press Ctrl+C to stop monitoring", flush=True)
#                     print("  - Or let it continue checking", flush=True)
                
#                 next_check_time = datetime.fromtimestamp(time.time() + check_interval_minutes*60)
#                 print(f"\n⏳ Next check at: {next_check_time.strftime('%H:%M:%S')}", flush=True)
                
#                 time.sleep(check_interval_minutes * 60)
                
#         except KeyboardInterrupt:
#             print("\n\n" + "="*60, flush=True)
#             print("👋 Monitor stopped by user", flush=True)
#             print(f"Total checks: {check_count}", flush=True)
#             if self.notification_sent:
#                 print("✅ Notification was sent successfully!", flush=True)
#             print("="*60 + "\n", flush=True)


# # ============================================
# # CONFIGURATION
# # ============================================

# if __name__ == "__main__":
#     print("\n🚀 Starting BookMyShow Real-Time Monitor...\n", flush=True)
    
#     # Gmail credentials
#     EMAIL_FROM = "sathviknarayana49@gmail.com"
#     EMAIL_PASSWORD = "ubxzqtnptksgsyqz"
#     EMAIL_TO = "sathviknarayana49@gmail.com"
    
#     # Create monitor
#     monitor = BookMyShowRealMonitor(EMAIL_FROM, EMAIL_PASSWORD, EMAIL_TO)
    
#     # Start monitoring
#     # Check every 15 minutes (you can change: 5, 10, 15, 30)
#     monitor.start_monitoring(check_interval_minutes=15)