import requests

def analyze_profile(username):
    """GitHub user ki details nikalo"""
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url, timeout=10)

    # Agar user nahi mila (404)
    if response.status_code == 404:
        return None

    response.raise_for_status()
    return response.json()

# ---------- MAIN ----------
def main():
    print("👤 GITHUB PROFILE ANALYZER\n")
    username = input("GitHub username daalo: ")

    try:
        data = analyze_profile(username)

        if data is None:
            print(f"❌ User '{username}' nahi mila!")
            return

        # Formatted profile print karo
        print("\n" + "=" * 40)
        print(f"👤 {data['name'] or username}")
        print("=" * 40)
        print(f"   🆔 Username  : {data['login']}")
        print(f"   📝 Bio       : {data['bio'] or 'No bio'}")
        print(f"   👥 Followers : {data['followers']}")
        print(f"   ➡️  Following : {data['following']}")
        print(f"   📦 Repos     : {data['public_repos']}")
        print(f"   📅 Joined    : {data['created_at'][:10]}")
        print(f"   🔗 Profile   : {data['html_url']}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")

if __name__ == "__main__":
    main()