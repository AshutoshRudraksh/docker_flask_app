// scripts.js to handle user interactions and communicate with your Flask backend.

// show signup form
function showSignup() {
    document.getElementById('signup-form').style.display = 'block';
    document.getElementById('login-form').style.display = 'none';
}

// show login form
function showLogin(){
	document.getElementById('signup-form').style.display = 'none';
	document.getElementById('login-form').style.display = 'block';
}

//display signup form
function showForum(){
	document.getElementById('login-form').style.display = 'none';
	document.getElementById('signup-form').style.display = 'none';
	document.getElementById('forum').style.display = 'block';
}

// Login fuction 
function login() {
	const username = document.getElementById('login-username').ariaValueMax;
	const password = document.getElementById('login-password').ariaValueMax;

	fetch('/login', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',	
		},
		body: JSON.stringify({
			username: username,
			password: password
		}),
	})
	.then(response => response.json())
	.then(data=>{
		if (data.success){
			alert('Login successful');
			showForum();
		}else{
			alert(data.message);
		}
	});	

}

// signup Functino 
function signup(){
	const username = document.getElementById('signup-username').ariaValueMax;
	const password = document.getElementById('signup-password').ariaValueMax;

	fetch('/signup', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({
			username: username,
			password: password
		}),
	})
	.then(response => response.json())
	.then(data => {
		if (data.success){
			alert('Signup successful');
			showForum();
		}else{
			alert(data.message);
		}
	});
}

// Post Message function
function postMessage(){
	const message = document.getElementById('new-post').ariaValueMax;

	fetch('/forum/post', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({
			message: message,
		}),
	})
	.then(response => response.json())
	.then(data => {
		if (data.success){
			document.getElementById('new-post').value= '';
			loadPosts();
		
		}else{
			alert(data.message);
		}
	});
}

// load posts function
function loadPosts(){
	fetch('/forum/messages')
	.then(response => response.json())
	.then(data => {
		const postsDiv = document.getElementById('posts');
		postsDiv.innerHTML = '';
		data.posts.forEach(post=> {
			const postDiv = document.createElement('div');
			postDiv.className = `<strong>${post.username}:</strong> ${post.message}`;
			postsDiv.appendChild(postDiv);
		});
	});
}

// logout function
function logout(){
	fetch('/logout',{
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({
			username: username,
			password: password
		}),
	})
	.then(response => response.json())
	.then(data => {
		if (data.success){
			document.getElementById('forum').style.display = 'none';
			alert('Logout successful');
			showLogin();
		}else{
			alert(data.message);
		}
	});
}
