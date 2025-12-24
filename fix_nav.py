import os

file_path = r"c:\Users\kokac\Downloads\online grocessr store\static\style.css"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

start_marker = "nav.top-nav {"
end_marker = "}"

start_idx = content.find(start_marker)
if start_idx != -1:
    end_idx = content.find(end_marker, start_idx)
    if end_idx != -1:
        # Construct correct block
        correct_block = """nav.top-nav {
    background: rgba(8, 15, 35, 0.9);
    color: var(--text-primary);
    padding: 1.25rem 3rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-radius: 32px;
    margin: 1.5rem auto 0;
    max-width: 1200px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    box-shadow: 0 20px 60px rgba(4, 7, 20, 0.6);
    position: relative;
    z-index: 10;
    backdrop-filter: blur(16px);
    transition: background 0.3s ease, color 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
}"""
        
        # Replace
        new_content = content[:start_idx] + correct_block + content[end_idx+1:]
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Fixed nav.top-nav block")
    else:
        print("End marker not found")
else:
    print("Start marker not found")
