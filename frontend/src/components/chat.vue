    <template>
        <div class="chat-container">
        <div class="messages-container" ref="messagesContainer">
            <ul id="messages">
            <li v-for="(message, index) in messages" :key="message.id" :class="{ 'current-user': message.userId === currentUser.uid }">
                <strong>{{ getUserName(message.userId) }}</strong>: {{ message.text }}
            </li>
            </ul>
        </div>
        <form @submit.prevent="sendMessage" class="message-form">
            <input v-model="newMessage" autocomplete="off" placeholder="Type a message..." />
            <button type="submit">Send</button>
        </form>
        <p v-if="error" class="error-message">{{ error }}</p>
        </div>
    </template>
    
    <script setup>
    import { ref, onMounted, nextTick } from 'vue';
    import { auth, db } from '../firebase.js';
    import { onAuthStateChanged } from 'firebase/auth';
    import { collection, addDoc, onSnapshot, query, orderBy, serverTimestamp, getDoc, doc } from 'firebase/firestore';
    
    const currentUser = ref(null);
    const messages = ref([]);
    const newMessage = ref('');
    const error = ref(null);
    const messagesContainer = ref(null);
    const userNames = ref({});
    
    const sendMessage = async () => {
        error.value = null;
        if (newMessage.value && currentUser.value) {
        try {
            await addDoc(collection(db, 'messages'), {
            text: newMessage.value,
            timestamp: serverTimestamp(),
            userId: currentUser.value.uid
            });
            newMessage.value = '';
        } catch (err) {
            console.error("Error sending message: ", err);
            error.value = "Failed to send message: " + err.message;
        }
        } else {
        error.value = newMessage.value ? "Please log in to send messages" : "Cannot send empty message";
        }
    };
    
    const loadMessages = () => {
        const messagesRef = collection(db, 'messages');
        const q = query(messagesRef, orderBy('timestamp', 'asc'));
        
        onSnapshot(q, (snapshot) => {
        messages.value = snapshot.docs.map(doc => ({
            id: doc.id,
            ...doc.data()
        }));
        nextTick(() => {
            scrollToBottom();
        });
        // Fetch usernames for new users
        messages.value.forEach(message => {
            if (!userNames.value[message.userId]) {
            fetchUserName(message.userId);
            }
        });
        }, (err) => {
        console.error("Error loading messages: ", err);
        error.value = "Failed to load messages: " + err.message;
        });
    };
    
    const scrollToBottom = () => {
        if (messagesContainer.value) {
        messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
        }
    };
    
    const fetchUserName = async (userId) => {
        try {
        const userDoc = await getDoc(doc(db, 'users', userId));
        if (userDoc.exists()) {
            const userData = userDoc.data();
            userNames.value[userId] = userData.username || 'Unknown User';
        } else {
            userNames.value[userId] = 'Unknown User';
        }
        } catch (err) {
        console.error("Error fetching username: ", err);
        userNames.value[userId] = 'Unknown User';
        }
    };
    
    const getUserName = (userId) => {
        return userNames.value[userId] || 'Loading...';
    };
    
    onMounted(() => {
        onAuthStateChanged(auth, (user) => {
        currentUser.value = user;
        if (user) {
            loadMessages();
            fetchUserName(user.uid); // Fetch current user's name
        } else {
            error.value = "Please log in to use the chat";
        }
        });
    });
    </script>
    
    <style scoped>
    .chat-container {
        display: flex;
        flex-direction: column;
        height: 100vh;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    .messages-container {
        flex-grow: 1;
        overflow-y: auto;
        padding: 1rem;
        background-color: #f0f0f0;
    }
    
    #messages {
        list-style-type: none;
        margin: 0;
        padding: 0;
    }
    
    #messages li {
        padding: 0.5rem 1rem;
        margin-bottom: 0.5rem;
        background-color: white;
        border-radius: 5px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    
    #messages li.current-user {
        background-color: #e6f3ff;
        text-align: right;
    }
    
    .message-form {
        display: flex;
        padding: 1rem;
        background-color: white;
        border-top: 1px solid #ddd;
    }
    
    .message-form input {
        flex-grow: 1;
        border: 1px solid #ddd;
        padding: 0.5rem;
        border-radius: 4px;
        margin-right: 0.5rem;
    }
    
    .message-form button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        cursor: pointer;
    }
    
    .error-message {
        color: red;
        text-align: center;
        padding: 0.5rem;
    }
    </style>