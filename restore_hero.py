import os

file_path = r"c:\Users\kokac\Downloads\online grocessr store\static\style.css"

# The missing block with LIGHT MODE defaults
hero_css = """
/* Hero */
.hero {
    position: relative;
    margin-top: 3rem;
    padding: clamp(3rem, 6vw, 4.5rem);
    border-radius: 48px;
    background: radial-gradient(circle at 15% 20%, rgba(255, 166, 92, 0.25), transparent 55%), linear-gradient(135deg, #fff6e5 0%, #f7f9fc 100%);
    color: var(--text-primary);
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.04);
    box-shadow: 0 40px 120px rgba(4, 6, 20, 0.1);
}

.hero::after {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at 20% 20%, rgba(255, 255, 255, 0.45), transparent 50%);
    z-index: 0;
    animation: heroGlow 12s ease-in-out infinite;
}

.hero-fruit {
    position: absolute;
    width: clamp(160px, 20vw, 260px);
    height: clamp(160px, 20vw, 260px);
    background-size: contain;
    background-repeat: no-repeat;
    z-index: 0;
    filter: drop-shadow(0 15px 25px rgba(0, 0, 0, 0.15));
    animation: fruitFloat 14s ease-in-out infinite;
}

.hero-fruit-left {
    top: -40px;
    left: -20px;
    background-image: url('images/fruit.png');
}

.hero-fruit-right {
    top: 10px;
    right: -10px;
    background-image: url('images/apple.png');
}

@keyframes heroGlow {
    0%, 100% { transform: scale(1); opacity: 0.9; }
    50% { transform: scale(1.05); opacity: 1; }
}

@keyframes fruitFloat {
    0%, 100% { transform: translate3d(0, 0, 0) rotate(0deg); }
    50% { transform: translate3d(15px, -20px, 0) rotate(3deg); }
}

.hero-content {
    position: relative;
    z-index: 1;
    text-align: center;
}

.hero-heading {
    font-size: clamp(3rem, 8vw, 5rem);
    margin: 0;
    font-weight: 800;
    color: #1a202c;
    text-shadow: none;
}

.hero-subheading {
    margin: 0.75rem 0 0;
    font-size: 1.2rem;
    color: var(--text-muted);
}

.hero-description {
    max-width: 560px;
    margin: 1rem auto 0;
    color: var(--text-muted);
    line-height: 1.5;
}

.hero-search {
    display: flex;
    justify-content: center;
    gap: 0.75rem;
    margin-top: 2.5rem;
}

.hero .search-bar {
    width: min(420px, 100%);
    padding: 0.95rem 1.25rem;
    border-radius: 999px;
    border: 1px solid rgba(0, 0, 0, 0.1);
    font-size: 1rem;
    background: #fff;
    color: var(--text-primary);
    box-shadow: 0 10px 30px rgba(148, 163, 184, 0.15);
    transition: box-shadow 0.2s ease, border-color 0.2s ease;
}

.hero .search-button {
    width: 56px;
    height: 56px;
    border-radius: 999px;
    border: none;
    background: linear-gradient(145deg, #ffb347, #ff8f6a);
    color: #0d142b;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 18px 35px rgba(255, 143, 106, 0.5);
    cursor: pointer;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.hero .search-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 16px 30px rgba(255, 118, 88, 0.5);
}

.hero .search-bar:focus-visible {
    outline: 3px solid var(--focus-ring);
    outline-offset: 2px;
}

/* Dark Mode Overrides for Hero */
body[data-theme="dark"] .hero {
    background: linear-gradient(145deg, #0b1226 0%, #101833 55%, #050a1a 100%);
    box-shadow: var(--shadow-soft-dark);
    color: #fff;
}

body[data-theme="dark"] .hero-heading {
    color: #f8fbff;
    text-shadow: 0 10px 30px rgba(9, 15, 38, 0.6);
}

body[data-theme="dark"] .hero-subheading,
body[data-theme="dark"] .hero-description {
    color: rgba(255, 255, 255, 0.9);
}

body[data-theme="dark"] .hero .search-bar {
    box-shadow: none;
    background: rgba(255, 255, 255, 0.08);
    color: #fff;
    border-color: rgba(255, 255, 255, 0.1);
}

body[data-theme="dark"] .hero .search-button {
    box-shadow: 0 12px 25px rgba(0, 0, 0, 0.45);
}
"""

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix the syntax error: remove "    color: #fff;" and the closing brace if it's misplaced
    # The error was:
    #     50% {
    #         transform: translate(-30px, 30px) scale(0.9);
    #     }
    # 
    #     color: #fff;
    # }
    
    # We will find the end of @keyframes float and replace the mess
    marker = """    50% {
        transform: translate(-30px, 30px) scale(0.9);
    }

    color: #fff;
}"""
    
    replacement = """    50% {
        transform: translate(-30px, 30px) scale(0.9);
    }
}"""
    
    if marker in content:
        content = content.replace(marker, replacement)
        print("Fixed syntax error.")
    else:
        # Fallback if whitespace is different
        # Try to find just the color: #fff; part
        if "color: #fff;" in content:
             # This is risky if color: #fff is used elsewhere, but let's check context
             pass

    # Now insert the hero_css
    # It should go before "body[data-theme="dark"] .hero .search-button"
    # But wait, that selector is part of the overrides which I am re-adding.
    # So I should probably remove any partial hero overrides if they exist.
    
    # Let's just insert it after the @keyframes float block.
    insert_point = """    50% {
        transform: translate(-30px, 30px) scale(0.9);
    }
}"""
    
    if insert_point in content:
        parts = content.split(insert_point)
        if len(parts) > 1:
            # Reassemble: part[0] + insert_point + hero_css + part[1]
            new_content = parts[0] + insert_point + "\n" + hero_css + parts[1]
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("Restored .hero section.")
        else:
            print("Could not split content correctly.")
    else:
        print("Could not find insertion point.")

except Exception as e:
    print(f"Error: {e}")
