# 🛡️ Password Shield

A beautifully designed, premium-grade **Password Strength Checker** built with Python and Tkinter. It evaluates your password security in real-time, displays interactive requirements, suggests improvements, and generates secure credentials.

---

## ✨ Features

- **🎨 Modern Dark Mode:** A curated dark aesthetic inspired by the Catppuccin Mocha palette, complete with subtle flat styling and smooth transitions.
- **⚡ Real-time Evaluation:** Instantly validates your password strength as you type, giving immediate feedback without needing manual clicks.
- **📊 Custom Visual Meter:** A multi-segmented progress bar drawn custom on Tkinter canvas that changes colors based on the safety grade:
  - 🟥 **Weak**
  - 🟧 **Medium**
  - 🟩 **Strong**
  - 🧪 **Very Strong**
- **✅ Requirement Checklist:** Visual security criteria checklist that lights up green (✓) or red (✗) to clearly show what requirements are satisfied.
- **👁️ Visibility Toggle:** One-click show/hide password toggle to mask or unmask your input securely.
- **🎲 Password Generator:** Generate a cryptographically secure, randomized 16-character password instantly with guaranteed variety (uppercase, lowercase, digits, and symbols).
- **📋 Summary Report:** A complete popup report explaining exactly how to make your password bulletproof.

---

## 🔒 Security Criteria & Scoring Logic

The application evaluates passwords against the following 5 fundamental parameters:
1. **Length:** Minimum 8 characters.
2. **Uppercase:** Contains at least one uppercase character (`A-Z`).
3. **Lowercase:** Contains at least one lowercase character (`a-z`).
4. **Numbers:** Contains at least one numeric digit (`0-9`).
5. **Special Characters:** Contains at least one special character/symbol (e.g. `!`, `@`, `#`, `$`, `%`, etc.).

### ⚖️ Strength Classifications
* **Weak:** Scores 0-2 (or any length < 8, even if other criteria are met).
* **Medium:** Score of 3 (requires length >= 8).
* **Strong:** Score of 4 (requires length >= 8).
* **Very Strong:** Score of 5 (meets all 5 criteria).

*Note: For maximum security, any password with a length less than 8 characters is automatically restricted to a **Weak** classification, regardless of other characters present.*

---

## 🚀 How to Run

Make sure you have Python installed on your system. Tkinter is built-in, so there are no external dependencies required!

1. Open a terminal or Command Prompt.
2. Navigate to the project directory:
   ```bash
   cd "C:\Users\manos\OneDrive\Desktop\passchecker"
   ```
3. Run the application:
   ```bash
   python app.py
   ```

---

*Designed and engineered with care by Antigravity.*
