# attendance_cli.py
# This is the command-line version of the attendance scraper.

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import getpass # For secure password entry

# --- Configuration ---
LOGIN_URL = "https://asiet.etlab.app/user/login"
# TODO: Make sure this path points to your local chromedriver.exe
DRIVER_PATH = r"C:\Users\adhit\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

# --- Attendance Calculation Functions ---
def calculate_current_percentage(attended, total):
    if total == 0: return 0.0
    return (attended / total) * 100

def classes_needed_for_target(attended, total, target_percentage):
    if calculate_current_percentage(attended, total) >= target_percentage: return 0
    classes_to_attend = 0
    while True:
        classes_to_attend += 1
        new_attended = attended + classes_to_attend
        new_total = total + classes_to_attend
        if calculate_current_percentage(new_attended, new_total) >= target_percentage:
            return classes_to_attend

def classes_to_bunk(attended, total, target_percentage):
    if calculate_current_percentage(attended, total) < target_percentage: return 0
    bunkable_classes = 0
    while True:
        new_total = total + bunkable_classes + 1
        if calculate_current_percentage(attended, new_total) < target_percentage:
            return bunkable_classes
        bunkable_classes += 1

# --- Web Scraping Function ---
def get_attendance_data(username, password):
    print("Starting the scraper...")
    service = Service(executable_path=DRIVER_PATH)
    # You can add options here if you want to run headless locally
    # options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # driver = webdriver.Chrome(service=service, options=options)
    driver = webdriver.Chrome(service=service)
    wait = WebDriverWait(driver, 20)
    scraped_data = {}

    try:
        print(f"Navigating to login page: {LOGIN_URL}")
        driver.get(LOGIN_URL)
        username_field = wait.until(EC.presence_of_element_located((By.ID, "LoginForm_username")))
        username_field.send_keys(username)
        print("Entered username.")
        password_field = driver.find_element(By.ID, "LoginForm_password")
        password_field.send_keys(password)
        print("Entered password.")
        login_button = driver.find_element(By.NAME, "yt0")
        login_button.click()
        print("Clicked login button.")
        
        wait.until(EC.presence_of_element_located((By.ID, "breadcrumb")))
        print("Successfully logged in. Navigating to attendance page...")
        attendance_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Attendance")))
        attendance_link.click()
        print("Clicked 'Attendance' link.")
        
        wait.until(EC.presence_of_element_located((By.ID, "itsthethetable")))
        print("Attendance table found. Parsing data...")
        time.sleep(2)

        page_html = driver.page_source
        soup = BeautifulSoup(page_html, 'html.parser')
        
        subject_attendance = {}
        attendance_table = soup.find('table', id='itsthetable')
        
        if attendance_table:
            period_cells = attendance_table.find_all('td', class_=['present', 'absent'])
            for cell in period_cells:
                link = cell.find('a')
                if link:
                    # This is the corrected logic to get only the subject name
                    subject_name = link.find(text=True, recursive=False).strip()
                    if subject_name: # Ensure the name is not empty
                        if subject_name not in subject_attendance:
                            subject_attendance[subject_name] = {'attended': 0, 'total': 0}
                        subject_attendance[subject_name]['total'] += 1
                        if 'present' in cell.get('class', []):
                            subject_attendance[subject_name]['attended'] += 1
            scraped_data = subject_attendance
            print("Successfully parsed all attendance data.")

    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        print("Closing the scraper.")
        driver.quit()
    
    return scraped_data

# --- Main Program Execution ---
def main():
    print("--- College Attendance Scraper (CLI Version) ---")
    user_username = input("Enter your college username: ")
    user_password = getpass.getpass("Enter your college password: ")

    while True:
        try:
            target_input = input("Enter your target attendance % (e.g., 75): ")
            TARGET_ATTENDANCE = float(target_input)
            break
        except ValueError:
            print("Invalid input. Please enter a number.")

    course_data = get_attendance_data(user_username, user_password)

    if not course_data:
        print("\nCould not retrieve attendance data. Please check scraper output for errors.")
        return

    print(f"\n--- Attendance Analysis (Target: {TARGET_ATTENDANCE}%) ---\n")
    for subject, data in course_data.items():
        attended_classes = data['attended']
        total_classes = data['total']
        current_perc = calculate_current_percentage(attended_classes, total_classes)
        
        print(f"Subject: {subject}")
        print(f"  - Current Status: {attended_classes} of {total_classes} classes attended.")
        print(f"  - Attendance: {current_perc:.2f}%")

        if current_perc < TARGET_ATTENDANCE:
            needed = classes_needed_for_target(attended_classes, total_classes, TARGET_ATTENDANCE)
            print(f"  - ⚠️ You are below the target!")
            print(f"  - You need to attend the next {needed} class(es) consecutively to reach {TARGET_ATTENDANCE}%.")
        else:
            bunks_available = classes_to_bunk(attended_classes, total_classes, TARGET_ATTENDANCE)
            print(f"  - ✅ You are meeting the target.")
            if bunks_available > 0:
                print(f"  - You can bunk the next {bunks_available} class(es) and stay above {TARGET_ATTENDANCE}%.")
            else:
                print(f"  - You cannot bunk any more classes without dropping below the target.")
        
        print("-" * 30)

if __name__ == "__main__":
    main()