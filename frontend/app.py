import streamlit as st
import requests

API_URL = "http://localhost:5000"

def login():
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        resp = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
        if resp.ok:
            data = resp.json()
            st.session_state['jwt'] = resp.json()['token']
            st.session_state['user_id'] = data.get('user_id')
            st.success("Logged in!")
        else:
            st.error("Login failed")

def register():
    st.header("Register")
    username = st.text_input("Username", key="reg_user")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password", key="reg_pwd")
    if st.button("Register"):
        resp = requests.post(f"{API_URL}/register", json={
            "username": username, "email": email, "password": password
        })
        if resp.ok:
            st.success("Registered! Please log in.")
        else:
            st.error(resp.json().get('error', 'Registration failed'))

def upload_post():
    st.header("New Post")
    image = st.file_uploader("Upload Image", type=['jpg', 'png'])
    caption = st.text_input("Caption")
    if st.button("Post") and image:
        files = {'image': image}
        data = {'caption': caption}
        headers = {'Authorization': st.session_state['jwt']}
        resp = requests.post(f"{API_URL}/upload_post", files=files, data=data, headers=headers)
        if resp.ok:
            st.success("Posted!")
        else:
            st.error("Failed to post")

def show_feed():
    st.header("Feed")
    headers = {'Authorization': st.session_state['jwt']}
    resp = requests.get(f"{API_URL}/feed", headers=headers)
    if resp.ok:
        for post in resp.json():
            st.image(API_URL + post['image_url'])
            st.write(f"{post['username']}: {post['caption']}")
            likes = get_likes(post['id'])
            st.write(f"Likes: {likes}")
            if st.button("Like/Unlike", key=f"like_{post['id']}"):
                like_post(post['id'])
            st.write("Comments:")
            comments = get_comments(post['id'])
            for c in comments:
                st.write(f"{c['username']}: {c['text']}")
            comment_text = st.text_input("Add a comment", key=f"comment_{post['id']}")
            if st.button("Post Comment", key=f"post_comment_{post['id']}"):
                add_comment(post['id'], comment_text)
    else:
        st.error("Failed to load feed")

def get_all_users():
    resp = requests.get(f"{API_URL}/users")  # You need to implement this endpoint
    if resp.ok:
        return resp.json().get('users', [])
    return []

def follow_user(target_id):
    headers = {'Authorization': st.session_state['jwt']}
    resp = requests.post(f"{API_URL}/follow", json={'user_id': target_id}, headers=headers)
    st.success(resp.json().get('message', ''))

def unfollow_user(target_id):
    headers = {'Authorization': st.session_state['jwt']}
    resp = requests.post(f"{API_URL}/unfollow", json={'user_id': target_id}, headers=headers)
    st.success(resp.json().get('message', ''))

def show_users():
    st.header("Users")
    users = get_all_users()
    my_id = st.session_state.get('user_id')  # You need to store this after login

    for user in users:
        if user['id'] == my_id:
            continue
        st.write(user['username'])
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"Follow {user['username']}", key=f"follow_{user['id']}"):
                follow_user(user['id'])
        with col2:
            if st.button(f"Unfollow {user['username']}", key=f"unfollow_{user['id']}"):
                unfollow_user(user['id'])

def like_post(post_id):
    headers = {'Authorization': st.session_state['jwt']}
    resp = requests.post(f"{API_URL}/like", json={'post_id': post_id}, headers=headers)
    if resp.ok:
        st.success(resp.json().get('message', ''))
    else:
        st.error(resp.json().get('error', 'Error'))

def add_comment(post_id, text):
    headers = {'Authorization': st.session_state['jwt']}
    resp = requests.post(f"{API_URL}/comment", json={'post_id': post_id, 'text': text}, headers=headers)
    if resp.ok:
        st.success(resp.json().get('message', ''))
    else:
        st.error(resp.json().get('error', 'Error'))

def get_likes(post_id):
    resp = requests.get(f"{API_URL}/likes/{post_id}")
    if resp.ok:
        return resp.json().get('likes', 0)
    return 0

def get_comments(post_id):
    resp = requests.get(f"{API_URL}/comments/{post_id}")
    if resp.ok:
        return resp.json()
    return []

def get_profile():
    headers = {'Authorization': st.session_state['jwt']}
    resp = requests.get(f"{API_URL}/profile", headers=headers)
    if resp.ok:
        return resp.json()
    return None

def delete_post(post_id):
    headers = {'Authorization': st.session_state['jwt']}
    resp = requests.delete(f"{API_URL}/delete_post/{post_id}", headers=headers)
    if resp.ok:
        st.success(resp.json().get('message', ''))
    else:
        st.error(resp.json().get('error', 'Error'))

def show_profile():
    st.header("My Profile")
    profile = get_profile()
    if profile:
        st.write(f"**Username:** {profile['username']}")
        st.write(f"**Email:** {profile['email']}")
        st.write(f"**Followers:** {profile['followers']}")
        st.write(f"**Following:** {profile['following']}")
        st.subheader("My Posts")
        for post in profile['posts']:
            st.image(API_URL + post['image_url'])
            st.write(post['caption'])
            st.write(f"Posted on: {post['created_at']}")
            if st.button("Delete Post", key=f"delete_{post['id']}"):
                delete_post(post['id'])
                st.experimental_rerun()  # Refresh profile after deletion
    else:
        st.error("Failed to load profile")

def main():
    st.title("Instagram Clone")
    if 'jwt' not in st.session_state:
        menu = st.sidebar.selectbox("Menu", ["Login", "Register"])
        if menu == "Login":
            login()
        else:
            register()
    else:
        menu = st.sidebar.selectbox("Menu", ["Feed", "New Post", "Discover Users", "Profile"])
        if menu == "Feed":
            show_feed()
        elif menu == "New Post":
            upload_post()
        elif menu == "Discover Users":
            show_users()
        elif menu == "Profile":
            show_profile()
        if st.sidebar.button("Logout"):
            del st.session_state['jwt']
            if 'user_id' in st.session_state:
                del st.session_state['user_id']

if __name__ == "__main__":
    main()