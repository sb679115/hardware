from flask import Flask, request, render_template
import hashlib

app = Flask(__name__)

# Simulated EEPROM memory
EEPROM = {
    0x01: "Password: 1234",  # Stored password
    0x02: b"\x8f\x14\x92",  # Encrypted key (dummy data)
    0x09: "STURSEC{HARDWARE_HACK_COMPLETE}",  # Hidden flag
}

# Simulated tamper detection logic
tamper_detected = False

def tamper_check(input_text):
    if "override" in input_text:
        global tamper_detected
        tamper_detected = True
        return "Tamper Detected! System Locked!"
    return None

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    global tamper_detected
    input_text = request.form.get('text', '')

    # Check for tampering
    tamper_message = tamper_check(input_text)
    if tamper_message:
        return render_template("index.html", response=tamper_message)

    # Simulate authentication bypass
    if input_text == EEPROM[0x01]:  # Check password
        return render_template("index.html", response="Authentication Successful!")

    # Simulate hardware exploitation to extract flag
    if "read_memory" in input_text:
        try:
            address = int(input_text.split(":")[1], 16)
            if address in EEPROM:
                return render_template(
                    "index.html", response=f"Memory [{hex(address)}]: {EEPROM[address]}"
                )
            else:
                return render_template("index.html", response="Invalid Memory Address!")
        except Exception:
            return render_template("index.html", response="Error reading memory!")

    return render_template("index.html", response="Access Denied!")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004)

