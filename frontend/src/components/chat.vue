    <template>
        <div class="chat-container">
        <div v-if="isLoadingPartners">Loading partners...</div>
        <div v-else-if="!currentUser">Please log in to use the chat.</div>
        <div v-else-if="!selectedPartner" class="partner-selection">
            <h2>Select a {{ currentUser.userType === 'supplier' ? 'Restaurant' : 'Supplier' }} to chat with:</h2>
            <ul>
            <li v-for="partner in availablePartners" :key="partner.id" class="partner-item">
                <span class="partner-name">{{ partner.userName }}</span>
                <button @click="selectPartner(partner)" class="chat-button">Chat</button>
            </li>
            </ul>
        </div>
        <div v-else class="chat-window">
            <h2>Chat with {{ selectedPartner.userName }}</h2>
            <div class="messages-container" ref="messagesContainer">
            <ul id="messages">
                <li v-for="message in filteredMessages" :key="message.id" :class="{ 'sent': message.userId === currentUser.uid, 'received': message.userId !== currentUser.uid }">
                <strong>{{ getUserName(message.userId) }}</strong>: {{ message.text }}
                </li>
            </ul>
            </div>
            <form @submit.prevent="sendMessage" class="message-form">
            <input
                :id="messageInputId"
                v-model="newMessage" 
                autocomplete="off" 
                placeholder="Type a message..." 
            />
            <button type="submit">Send</button>
            </form>
            <div v-if="error" class="error-message">{{ error }}</div>
        </div>
        </div>
    </template>
    
    <script setup>
    import { ref, computed, onMounted, watch, nextTick } from 'vue';
    import { auth, db } from '../firebase.js';
    import { onAuthStateChanged } from 'firebase/auth';
    import { collection, addDoc, onSnapshot, query, where, orderBy, serverTimestamp, getDoc, doc, getDocs } from 'firebase/firestore';
    
    const currentUser = ref(null);
    const messages = ref([]);
    const newMessage = ref('');
    const error = ref(null);
    const messagesContainer = ref(null);
    const userNames = ref({});
    const selectedPartner = ref(null);
    const availablePartners = ref([]);
    const loading = ref(true);
    const isLoadingPartners = ref(false);
    
    const conversationId = computed(() => {
        if (currentUser.value && selectedPartner.value) {
            console.log(conversationId,123)
        return [currentUser.value.uid, selectedPartner.value.id].sort().join('_');
        }
        return null;
    });
    
    const filteredMessages = computed(() => {
        return messages.value.filter(message => 
        message.conversationId === conversationId.value
        );
    });
    
    const sendMessage = async () => {
        error.value = null;
        if (newMessage.value && currentUser.value && selectedPartner.value) {
        try {
            await addDoc(collection(db, 'messages'), {
            text: newMessage.value,
            timestamp: serverTimestamp(),
            userId: currentUser.value.uid,
            conversationId: conversationId.value
            });
            newMessage.value = '';
        } catch (err) {
            console.error("Error sending message: ", err);
            error.value = "Failed to send message: " + err.message;
        }
        } else {
        error.value = newMessage.value ? "Please select a partner to chat with" : "Cannot send empty message";
        }
    };
    


    
        const loadMessages = () => {
    if (!conversationId.value) {
        console.error("No conversation ID available");
        return;
    }

    const messagesRef = collection(db, 'messages');
    const q = query(
        messagesRef,
        where('conversationId', '==', conversationId.value),
        orderBy('timestamp', 'asc')  // Make sure this matches the field name in your Firestore documents
    );

    const unsubscribe = onSnapshot(q, (snapshot) => {
        messages.value = snapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
        }));
        console.log("Updated messages:", messages.value);
        nextTick(() => {
        scrollToBottom();
        });

        messages.value.forEach(message => {
        if (!userNames.value[message.userId]) {
            fetchUserName(message.userId);
        }
        });
    }, (err) => {
        console.error("Error loading messages: ", err);
        if (err.code === 'failed-precondition' || err.code === 'resource-exhausted') {
        error.value = "Message loading is temporarily unavailable. Please try again later.";
        } else {
        error.value = "Failed to load messages: " + err.message;
        }
    });

    // Return the unsubscribe function
    return unsubscribe;
    };
    
    const fetchUserName = async (userId) => {
        try {
        const userDoc = await getDoc(doc(db, 'users', userId));
        if (userDoc.exists()) {
            const userData = userDoc.data();
            // console.log(userData, "abc")
            userNames.value[userId] = userData.userName || 'Unknown User';
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
    
    const selectPartner = (partner) => {
        selectedPartner.value = partner;
        loadMessages();
    };
    
    const scrollToBottom = () => {
    if (messagesContainer.value) {
        messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
    }
    };



    watch(filteredMessages, (newMessages) => {
    console.log("Filtered messages updated:", newMessages);
});

    
    onMounted(() => {
    console.log("Component mounted");

    onAuthStateChanged(auth, async (user) => {
        console.log("Auth state changed. User:", user);
        loading.value = true;
        if (user) {
            // console.log("User is authenticated. UID:", user.uid);
            try {
                const userDocRef = doc(db, 'users', user.uid);
                const userDoc = await getDoc(userDocRef);
                console.log(userDoc.data(), 456);
                if (userDoc.exists()) {
                    currentUser.value = { 
                        uid: user.uid, 
                        userName: userDoc.data().userName,
                        userType: userDoc.data().userType
                    };
                    console.log("Current user set:", currentUser.value);
                    loadAvailablePartners();
                } else {
                    console.error('User document not found in Firestore');
                    currentUser.value = null;
                }
            } catch (error) {
                console.error('Error fetching user document:', error);
                currentUser.value = null;
            }
        } else {
            console.log("No authenticated user");
            currentUser.value = null;
        }
        loading.value = false;
    });
});

    const loadAvailablePartners = async () => {
        // console.log("Loading partners for user type:", currentUser.value.userType, 12345);
        if (!currentUser.value) return;

        isLoadingPartners.value = true;
        const usersRef = collection(db, 'users');
        const partnerType = currentUser.value.userType === 'restaurant' ? 'supplier' : 'restaurant';
        console.log(partnerType, 123);
        const q = query(usersRef, where('userType', '==', partnerType), orderBy('userName'))
        
        try {
            const snapshot = await getDocs(q);
            availablePartners.value = snapshot.docs.map(doc => ({
            id: doc.id,
            userName: doc.data().userName,
            userType: doc.data().userType,
            }));
        console.log("Available partners:", availablePartners.value);
        } catch (err) {
            console.error("Error loading partners:", err);
            error.value = "Failed to load partners: " + err.message;
        } finally {
        isLoadingPartners.value = false;
        }
        };
    const messageInputId = 'message-input';
    </script>

    
    
    <style scoped>
    
    .partner-selection {
        padding: 1rem;
    }
    
    .partner-selection ul {
        list-style-type: none;
        padding: 0;
    }
    
    .partner-selection li {
        cursor: pointer;
        padding: 0.5rem;
        margin-bottom: 0.5rem;
        background-color: #f0f0f0;
        border-radius: 4px;
    }
    
    .partner-selection li:hover {
        background-color: #e0e0e0;
    }
    
    #messages li:not(.current-user) {
        background-color: white;
        border-radius: 18px 18px 18px 0;
        float: left;
        text-align: left;
    }
    
    #messages li.current-user {
        background-color: #e6f3ff;
        border-radius: 18px 18px 0 18px;
        float: right;
        text-align: right;
    }
    label {
    display: block;
    margin-bottom: 5px;
    }

    .message-form {
    display: flex;
    padding: 1rem;
    background-color: #f9f9f9;
    border-top: 1px solid #ddd;
    }

    .message-form input {
    flex-grow: 1;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px 0 0 4px;
    margin-right: 0;
    }

    .message-form button {
    padding: 10px 20px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 0 4px 4px 0;
    cursor: pointer;
    }

    .message-form button:hover {
    background-color: #45a049;
    }

    .partner-selection {
    padding: 1rem;
    }

    .partner-selection ul {
    list-style-type: none;
    padding: 0;
    }

    .partner-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem;
    margin-bottom: 0.5rem;
    background-color: #f0f0f0;
    border-radius: 4px;
    }

    .partner-name {
    font-weight: bold;
    }

    .chat-button {
    background-color: #4CAF50;
    border: none;
    color: white;
    padding: 8px 16px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 14px;
    margin: 4px 2px;
    cursor: pointer;
    border-radius: 4px;
    }

    .chat-button:hover {
    background-color: #45a049;
    }

    .chat-container {
    display: flex;
    flex-direction: column;
    height: 100vh;
    }

    .chat-window {
    display: flex;
    flex-direction: column;
    height: 100%;
    }

    .messages-container {
    flex-grow: 1;
    overflow-y: auto;
    padding: 1rem;
    }

    #messages {
    list-style-type: none;
    padding: 0;
    margin: 0;
    }

    #messages li {
    margin-bottom: 10px;
    padding: 8px 12px;
    border-radius: 18px;
    max-width: 70%;
    clear: both;
    }

    #messages li.sent {
    background-color: #e6f3ff;
    float: right;
    text-align: right;
    border-bottom-right-radius: 0;
    }

    #messages li.received {
    background-color: #f0f0f0;
    float: left;
    text-align: left;
    border-bottom-left-radius: 0;
    }

    .message-form {
    display: flex;
    padding: 1rem;
    background-color: #f9f9f9;
    border-top: 1px solid #ddd;
    }

    .message-form input {
    flex-grow: 1;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    margin-right: 10px;
    }

    .message-form button {
    padding: 10px 20px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    }

    .message-form button:hover {
    background-color: #45a049;
    }

        .no-messages {
    text-align: center;
    padding: 20px;
    color: #666;
    }

    .error-message {
    color: red;
    text-align: center;
    padding: 10px;
    }
    </style>