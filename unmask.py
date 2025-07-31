import requests
import os
import sys
import subprocess
import time
import random
from prompt_toolkit import prompt
from prompt_toolkit.completion import PathCompleter

try:
    from pystyle import Colors, Colorate, Center, Write, Box, System
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pystyle'])
    from pystyle import Colors, Colorate, Center, Write, Box, System

def check_and_install_packages(packages):
    Write.Print("\n" + "═" * 50 + "\n", Colors.red_to_blue, interval=0.01)
    Write.Print("   CHECKING REQUIREMENTS\n", Colors.red_to_blue, interval=0.02)
    Write.Print("═" * 50 + "\n", Colors.red_to_blue, interval=0.01)

    for package, version in packages.items():
        try:
            __import__(package)
            Write.Print(f"[✓] {package} is already installed\n", Colors.light_green, interval=0.01)
        except ImportError:
            Write.Print(f"[!] Installing {package}...\n", Colors.light_red, interval=0.02)
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', f"{package}=={version}"])
            Write.Print(f"[✓] {package} installed successfully\n", Colors.light_green, interval=0.01)

def get_file_path(prompt_text):
    completer = PathCompleter()
    colored_prompt = Colorate.Horizontal(Colors.red_to_blue, prompt_text)
    return prompt(colored_prompt, completer=completer).strip()

def clear_screen():
    System.Clear()

def loading_dots(text, duration=3):
    end_time = time.time() + duration
    dots = ""
    while time.time() < end_time:
        for i in range(4):
            dots = "." * i
            print(f"\r{Colorate.Horizontal(Colors.red_to_blue, f'{text}{dots}   ')}", end="", flush=True)
            time.sleep(0.3)
    print(f"\r{' ' * (len(text) + 10)}\r", end="")

def progress_bar(current, total, width=50):
    percent = int((current / total) * 100)
    filled = int((current / total) * width)
    bar = "█" * filled + "░" * (width - filled)
    progress_text = f"[{bar}] {percent}% ({current}/{total})"
    return Colorate.Horizontal(Colors.red_to_blue, progress_text)

def get_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:91.0) Gecko/20100101 Firefox/91.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
    ]
    return random.choice(user_agents)

class GitHubEmailExtractor:
    def __init__(self, username):
        self.username = username
        self.base_url = "https://api.github.com"
        self.headers = {"User-Agent": get_random_user_agent()}
        self.user_info = {}

    def user_exists(self):
        loading_dots("Checking user existence", 2)
        response = requests.get(f"{self.base_url}/users/{self.username}", headers=self.headers)

        if response.status_code == 200:
            user_data = response.json()
            self.user_info = {
                'name': user_data.get('name', 'N/A'),
                'id': user_data.get('id', 'N/A'),
                'bio': user_data.get('bio', 'No bio available'),
                'html_url': user_data.get('html_url', 'N/A'),
                'profile_pic': user_data.get('avatar_url', 'N/A'),
                'created_at': user_data.get('created_at', 'N/A'),
                'company': user_data.get('company', 'N/A'),
                'location': user_data.get('location', 'N/A'),
                'followers': user_data.get('followers', 'N/A'),
                'following': user_data.get('following', 'N/A'),
                'type': user_data.get('type', 'N/A'),
                'email': user_data.get('email', 'N/A'),
                'public_repos': user_data.get('public_repos', 'N/A')
            }
            Write.Print("[✓] User found successfully!\n", Colors.light_green, interval=0.02)
            return True
        elif response.status_code == 404:
            Write.Print("[✗] GitHub user does not exist\n", Colors.light_red, interval=0.03)
        elif response.status_code == 403:
            Write.Print("[✗] GitHub API rate limit reached\n", Colors.light_red, interval=0.03)
            sys.exit(1)
        else:
            Write.Print(f"[✗] Failed to retrieve user: {response.text}\n", Colors.light_red, interval=0.03)

        return False

    def get_repositories(self):
        loading_dots("Fetching repositories", 1)
        response = requests.get(f"{self.base_url}/users/{self.username}/repos", headers=self.headers)

        if response.status_code == 200:
            try:
                repos = response.json()
                Write.Print(f"[✓] Found {len(repos)} repositories\n", Colors.light_green, interval=0.02)
                return repos
            except ValueError:
                Write.Print("[✗] Unexpected response format\n", Colors.light_red, interval=0.03)
                return []
        else:
            Write.Print("[✗] Failed to retrieve repositories\n", Colors.light_red, interval=0.03)
            return []

    def get_commits(self, repo):
        response = requests.get(f"{self.base_url}/repos/{self.username}/{repo}/commits", headers=self.headers)
        if response.status_code == 200:
            try:
                return response.json()
            except ValueError:
                return []
        return []

    def get_public_events(self):
        loading_dots("Fetching public events", 1)
        response = requests.get(f"{self.base_url}/users/{self.username}/events/public", headers=self.headers)

        if response.status_code == 200:
            try:
                events = response.json()
                Write.Print(f"[✓] Found {len(events)} public events\n", Colors.light_green, interval=0.02)
                return events
            except ValueError:
                return []
        return []

    def collect_emails(self, include_hidden=False, user_specific=False):
        email_sources = {}
        repos = self.get_repositories()

        Write.Print("\nScanning repositories for emails...\n", Colors.red_to_blue, interval=0.02)

        processed_repos = 0
        total_repos = len([r for r in repos if not r.get("fork")])

        for repo in repos:
            if not repo.get("fork"):
                processed_repos += 1
                print(f"\r{progress_bar(processed_repos, total_repos)}", end="", flush=True)

                try:
                    commits = self.get_commits(repo.get('name', ''))
                    for commit in commits:
                        if commit:
                            email = commit.get('commit', {}).get('author', {}).get('email')
                            if email:
                                email_sources.setdefault(email, []).append(
                                    f"Repo: https://github.com/{self.username}/{repo['name']}, User: {commit.get('author', {}).get('login', 'unknown')}"
                                )
                except Exception:
                    continue

        print("\n")

        Write.Print("Scanning public events...\n", Colors.red_to_blue, interval=0.02)
        events = self.get_public_events()

        for event in events:
            if event.get('type') == 'PushEvent':
                try:
                    for commit in event.get('payload', {}).get('commits', []):
                        if commit:
                            email = commit.get('author', {}).get('email')
                            if email:
                                email_sources.setdefault(email, []).append(
                                    f"Public Commit, User: {event.get('actor', {}).get('login', 'unknown')}"
                                )
                except Exception:
                    continue

        if not include_hidden:
            email_sources = {email: sources for email, sources in email_sources.items() 
                           if not email.endswith('@users.noreply.github.com')}

        if user_specific:
            email_sources = {email: sources for email, sources in email_sources.items() 
                           if any(f"User: {self.username}" in source for source in sources)}

        return email_sources

def get_user_input(prompt_text, default_value):
    while True:
        colored_prompt = Colorate.Horizontal(Colors.red_to_blue, prompt_text)
        user_input = input(colored_prompt).strip().lower()
        if user_input in ['y', 'n', '']:
            return user_input if user_input else default_value
        else:
            Write.Print("Invalid input. Please enter 'y' or 'n'\n", Colors.light_red, interval=0.03)
            Write.Print("Press Enter to try again...\n", Colors.light_red, interval=0.02)
            input()
            clear_screen()
            banner()

def banner():
    banner_text = """
██╗   ██╗███╗   ██╗███╗   ███╗ █████╗ ███████╗██╗  ██╗
██║   ██║████╗  ██║████╗ ████║██╔══██╗██╔════╝██║ ██╔╝
██║   ██║██╔██╗ ██║██╔████╔██║███████║███████╗█████╔╝ 
██║   ██║██║╚██╗██║██║╚██╔╝██║██╔══██║╚════██║██╔═██╗ 
╚██████╔╝██║ ╚████║██║ ╚═╝ ██║██║  ██║███████║██║  ██╗
 ╚═════╝ ╚═╝  ╚═══╝╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
    """

    print(Center.XCenter(Colorate.Horizontal(Colors.red_to_blue, banner_text)))

    subtitle = "Unmasking GitHub's Hidden Insights, One Repo at a Time"
    print(Center.XCenter(Colorate.Horizontal(Colors.cyan_to_green, subtitle)))
    print()

def create_box_simple(title, content):
    """Create a simple box display"""
    width = 78

    # Box content
    box_content = f"""
╔{'═' * width}╗
║{title.center(width)}║
╠{'═' * width}╣
"""
    for line in content:
        if len(line) > width - 4:
            line = line[:width - 7] + "..."
        box_content += f"║ {line:<{width-2}} ║\n"

    box_content += f"╚{'═' * width}╝"

    return Colorate.Horizontal(Colors.red_to_blue, box_content)

def display_user_info(extractor, username):
    Write.Print("\n" + "═" * 50 + "\n", Colors.red_to_blue, interval=0.01)
    Write.Print("   USER INFORMATION\n", Colors.red_to_blue, interval=0.02)
    Write.Print("═" * 50 + "\n", Colors.red_to_blue, interval=0.01)

    info_lines = [
        f"Username        : {username}",
        f"Name            : {extractor.user_info['name']}",
        f"Profile URL     : {extractor.user_info['html_url']}",
        f"Bio             : {extractor.user_info['bio'][:60]}{'...' if len(extractor.user_info['bio']) > 60 else ''}",
        f"Email           : {extractor.user_info['email']}",
        f"Company         : {extractor.user_info['company']}",
        f"Location        : {extractor.user_info['location']}",
        f"Account Type    : {extractor.user_info['type']}",
        f"Followers       : {extractor.user_info.get('followers', 'N/A')}",
        f"Following       : {extractor.user_info.get('following', 'N/A')}",
        f"Public Repos    : {extractor.user_info.get('public_repos', 'N/A')}",
        f"User ID         : {extractor.user_info['id']}",
        f"Created         : {extractor.user_info['created_at']}"
    ]

    print(create_box_simple("USER PROFILE", info_lines))

def display_emails(emails):
    if not emails:
        Write.Print("\n[✗] No emails were found\n", Colors.light_red, interval=0.03)
        return 0

    email_count = len(emails)
    Write.Print(f"\n[✓] Found {email_count} email address(es):\n", Colors.light_green, interval=0.03)

    for i, (email, sources) in enumerate(emails.items(), 1):
        # Email header
        email_header = f"Email #{i}: {email}"
        Write.Print(f"\n{email_header}\n", Colors.red_to_blue, interval=0.01)
        Write.Print("─" * len(email_header) + "\n", Colors.red_to_blue, interval=0.01)

        # Sources
        for j, source in enumerate(sources, 1):
            source_text = f"  {j}. {source}"
            Write.Print(f"{source_text}\n", Colors.cyan_to_blue, interval=0.005)

        time.sleep(0.1)

    return email_count

def main():
    clear_screen()

    # Check packages
    required_packages = {
        'requests': '2.28.1',
        'prompt_toolkit': '3.0.36',
        'pystyle': '2.9'
    }

    check_and_install_packages(required_packages)
    loading_dots("Initializing UNMASK", 2)
    clear_screen()

    while True:
        banner()
        username = get_file_path("[?] Enter GitHub username: ")
        if not username:
            Write.Print("\nUsername cannot be empty\n", Colors.light_red, interval=0.03)
            Write.Print("Press Enter to try again...\n", Colors.light_red, interval=0.02)
            input()
            clear_screen()
            continue
        else:
            break

    extractor = GitHubEmailExtractor(username)
    if not extractor.user_exists():
        return

    clear_screen()
    banner()

    # Configuration menu
    config_content = [
        "Choose your scanning preferences:",
        "",
        "1. Quick Scan    - Default settings, faster results",
        "2. Advanced Scan - Customizable options for detailed analysis",
        ""
    ]

    print(create_box_simple("SCAN CONFIGURATION", config_content))

    scan_choice = input(Colorate.Horizontal(Colors.red_to_blue, "\n[?] Choose scan type (1/2, press Enter for 1): ")).strip()

    if scan_choice == '2':
        Write.Print("\nAdvanced Configuration:\n", Colors.red_to_blue, interval=0.03)
        include_hidden = get_user_input("[?] Include hidden emails (@users.noreply.github.com)? (y/n, press Enter for y): ", 'y')
        user_specific = get_user_input("[?] Filter emails by user activity? (y/n, press Enter for n): ", 'n')
    else:
        include_hidden = 'y'
        user_specific = 'n'
        Write.Print("\nUsing Quick Scan settings...\n", Colors.light_green, interval=0.03)

    include_hidden = include_hidden == 'y'
    user_specific = user_specific == 'y'

    loading_dots("Preparing scan environment", 2)
    clear_screen()

    Write.Print("Starting GitHub analysis...\n", Colors.red_to_blue, interval=0.03)

    display_user_info(extractor, username)

    start_time = time.time()
    emails = extractor.collect_emails(include_hidden, user_specific)
    email_count = display_emails(emails)

    # Results summary
    elapsed_time = round(time.time() - start_time, 2)

    Write.Print("\n" + "═" * 50 + "\n", Colors.red_to_blue, interval=0.01)
    Write.Print("   SCAN SUMMARY\n", Colors.red_to_blue, interval=0.02)
    Write.Print("═" * 50 + "\n", Colors.red_to_blue, interval=0.01)

    summary_lines = [
        f"Status          : COMPLETED ✓",
        f"Emails Found    : {email_count}",
        f"Time Taken      : {elapsed_time} seconds",
        f"Target User     : {username}",
        f"Hidden Emails   : {'Included' if include_hidden else 'Excluded'}",
        f"User Filter     : {'Applied' if user_specific else 'Not Applied'}"
    ]

    print(create_box_simple("RESULTS", summary_lines))

    # Save results option
    save_prompt = Colorate.Horizontal(Colors.red_to_blue, "\n[?] Save results to file? (y/n, press Enter for n): ")
    save = input(save_prompt).lower()

    if save == 'y':
        filename_prompt = Colorate.Horizontal(Colors.red_to_blue, "[?] Enter filename (press Enter for 'results.txt'): ")
        filename = input(filename_prompt).strip()
        if not filename:
            filename = 'results.txt'

        loading_dots("Saving results", 2)

        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("GITHUB EMAIL EXTRACTION RESULTS\n")
            f.write("=" * 80 + "\n\n")

            f.write("USER INFORMATION:\n")
            f.write("-" * 40 + "\n")
            for line in summary_lines:
                f.write(f"{line}\n")
            f.write(f"\nProfile URL: {extractor.user_info['html_url']}\n")
            f.write(f"Bio: {extractor.user_info['bio']}\n")
            f.write(f"Company: {extractor.user_info['company']}\n")
            f.write(f"Location: {extractor.user_info['location']}\n")
            f.write(f"User ID: {extractor.user_info['id']}\n")
            f.write(f"Created: {extractor.user_info['created_at']}\n\n")

            f.write("EXTRACTED EMAILS:\n")
            f.write("-" * 40 + "\n")
            for i, (email, sources) in enumerate(emails.items(), 1):
                f.write(f"\nEmail #{i}: {email}\n")
                f.write("Sources:\n")
                for j, source in enumerate(sources, 1):
                    f.write(f"  {j}. {source}\n")

        Write.Print(f"[✓] Results saved to {filename}\n", Colors.light_green, interval=0.02)

    Write.Print("\nThank you for using UNMASK! Stay curious, stay ethical.\n", Colors.red_to_blue, interval=0.02)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        Write.Print("\n\n[!] Program terminated by user. Goodbye!\n", Colors.light_red, interval=0.03)
        sys.exit(0)
    except Exception as e:
        Write.Print(f"\n[!] An unexpected error occurred: {e}\n", Colors.light_red, interval=0.03)
        sys.exit(1)
