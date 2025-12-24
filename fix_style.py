import os

file_path = r"c:\Users\kokac\Downloads\online grocessr store\static\style.css"

header = """:root {
    color-scheme: light;
    /* Light Mode Colors */
    --bg-gradient: radial-gradient(circle at 20% 20%, #fdfbfb 0%, #ebedee 100%); /* Soft Cloud */
    --bg-gradient-dark: radial-gradient(circle at 10% 10%, #23294b 0%, #101326 50%, #04050c 100%);
    --surface: #ffffff;
    --surface-muted: rgba(0, 0, 0, 0.05);
    --surface-dark: rgba(10, 14, 32, 0.75);
    --text-primary: #1a202c; /* Dark Gray for Light Mode */
    --text-muted: #718096; /* Medium Gray */
    --text-inverse: #f4f6ff; /* Light Text for Dark Mode */
    --accent: #ffb347;
    --accent-strong: #ff8f6a;
    --accent-secondary: #15a364;
    --focus-ring: rgba(21, 163, 100, 0.4);
    --card-gradient: linear-gradient(135deg, #ffffff 0%, #f7f9fc 100%); /* Light Card */
    --card-gradient-dark: linear-gradient(180deg, rgba(19, 24, 44, 0.95), rgba(11, 14, 26, 0.95));
    --shadow-soft: 0 20px 40px rgba(148, 163, 184, 0.15); /* Soft Light Shadow */
    --shadow-soft-dark: 0 25px 50px rgba(0, 0, 0, 0.55);

    /* Glass Variables (Light Mode Default) */
    --glass-bg: rgba(255, 255, 255, 0.7);
    --glass-border: rgba(255, 255, 255, 0.6);
    --glass-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
    --glass-blur: blur(12px);
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin: 0;
    padding: 0;
    background: var(--bg-gradient);
    background-attachment: fixed;
    color: var(--text-primary);
    position: relative;
    overflow-x: hidden;
    min-height: 100vh;
    transition: background 0.4s ease, color 0.3s ease;
}

body[data-theme="dark"] {
    color-scheme: dark;
    background: var(--bg-gradient-dark);
    color: var(--text-inverse);
}

body[data-theme="dark"]::before {
    background: radial-gradient(circle, rgba(255, 177, 177, 0.4) 0%, transparent 70%);
}

body[data-theme="dark"]::after {
    background: radial-gradient(circle, rgba(255, 217, 61, 0.35) 0%, transparent 70%);
}

/* Floating decorative elements */
body::before,
body::after {
    content: '';
    position: fixed;
    border-radius: 50%;
    opacity: 0.3;
    z-index: 0;
    animation: float 20s ease-in-out infinite;
}

body::before {
    width: 420px;
    height: 420px;
    background: radial-gradient(circle, rgba(73, 142, 255, 0.15) 0%, transparent 70%);
    top: -180px;
    left: -180px;
    animation-delay: 0s;
}

body::after {
    width: 520px;
    height: 520px;
    background: radial-gradient(circle, rgba(255, 140, 101, 0.15) 0%, transparent 70%);
    bottom: -250px;
    right: -220px;
    animation-delay: 5s;
}

@keyframes float {
    0%,
    100% {
        transform: translate(0, 0) scale(1);
    }

    25% {
        transform: translate(50px, -50px) scale(1.1);
    }

    50% {
        transform: translate(-30px, 30px) scale(0.9);
    }

    75% {
        transform: translate(40px, 20px) scale(1.05);
    }
}

nav.top-nav {
    background: rgba(8, 15, 35, 0.9);
    color: var(--text-primary);
    padding: 1.25rem 3rem;
"""

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Dedent the content (remove 8 spaces from each line)
    lines = content.splitlines()
    dedented_lines = []
    for line in lines:
        if line.startswith("        "):
            dedented_lines.append(line[8:])
        else:
            dedented_lines.append(line)
    
    dedented_content = "\n".join(dedented_lines)

    # Combine header and dedented content
    # Note: The dedented content starts with 'display: flex;', so we just append it to the header which ends with 'nav.top-nav {'
    full_content = header + dedented_content

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(full_content)
    
    print("Successfully restored style.css")

except Exception as e:
    print(f"Error: {e}")
