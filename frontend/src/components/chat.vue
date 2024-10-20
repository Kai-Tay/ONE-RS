<template>
    <div class="chat-container">
    <div v-if="isLoadingPartners">Loading partners...</div>
    <div v-else-if="!currentUser">Please log in to use the chat.</div>
    <div v-else>

    <div v-if="!selectedPartner" class="partner-selection-view">
        <h2>Select a {{ currentUser.userType === 'supplier' ? 'Restaurant' : 'Supplier' }} to chat with:</h2>
        <ul>
        <li v-for="partner in availablePartners" :key="partner.id" class="partner-item">
            <span class="partner-name">{{ partner.userName }}</span>
            <button @click="selectPartner(partner)" class="chat-button">Chat</button>
        </li>
        </ul>
    </div>
    

    <div v-if="selectedPartner" class="chat-window-view">
        <h2>Chat with {{ selectedPartner.userName }}</h2>
        <div class="messages-container" ref="messagesContainer">
        <div v-for="group in groupedMessages" :key="group.date" class="message-group">
            <div class="date-header">{{ group.date }}</div>
            <ul class="messages">
            <li v-for="message in group.messages" :key="message.timestamp" 
                :class="{ 'sent': message.senderId === currentUser.uid, 'received': message.senderId !== currentUser.uid }">
                <strong>{{ getUserName(message.senderId) }}</strong>: {{ message.text }}
                <small>{{ formatTime(message.timestamp) }}</small>
            </li>
            </ul>
        </div>
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
    </div>
</template>

        
    <script setup>
    import { ref, computed, onMounted, watch, nextTick } from 'vue';
    import { auth, db } from '../firebase.js';
    import { getAuth, onAuthStateChanged } from 'firebase/auth';
    import { writeBatch, collection, setDoc, updateDoc, arrayUnion, onSnapshot, query, where, orderBy, serverTimestamp, getDoc, doc, getDocs } from 'firebase/firestore';
    
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

    const groupedMessages = computed(() => {
    const groups = {};
    messages.value.forEach(message => {
        const date = new Date(message.timestamp).toLocaleDateString();
        if (!groups[date]) {
        groups[date] = [];
        }
        groups[date].push(message);
    });
    return Object.entries(groups).map(([date, msgs]) => ({ date, messages: msgs }));
    });


const sendMessage = async () => {
    error.value = null;
    if (newMessage.value && currentUser.value && selectedPartner.value) {
        const messageObject = {
        senderId: currentUser.value.uid,
        text: newMessage.value,
        timestamp: Date.now()
        };

        try {
        const messagesRef = collection(db, 'messages');
        const userIds = [currentUser.value.uid, selectedPartner.value.id].sort();
        const chatId = userIds.join('_');

        const chatDocRef = doc(messagesRef, chatId);
        const chatDoc = await getDoc(chatDocRef);

        if (!chatDoc.exists()) {
            // Create a new message document
            await setDoc(chatDocRef, {
            participants: userIds,
            messages: [messageObject],
            lastUpdated: serverTimestamp()
            });
        } else {
            // Update existing message document
            await updateDoc(chatDocRef, {
            messages: arrayUnion(messageObject),
            lastUpdated: serverTimestamp()
            });
        }

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
    if (!currentUser.value || !selectedPartner.value) {
        console.error("No current user or selected partner");
        return;
    }

    const messagesRef = collection(db, 'messages');
    const userIds = [currentUser.value.uid, selectedPartner.value.id].sort();
    const chatId = userIds.join('_');
    const chatDocRef = doc(messagesRef, chatId);

    const unsubscribe = onSnapshot(chatDocRef, (doc) => {
        if (doc.exists()) {
        const data = doc.data();
        messages.value = data.messages || [];
        console.log("Updated messages:", messages.value);
        nextTick(() => {
            scrollToBottom();
        });

        messages.value.forEach(message => {
            if (!userNames.value[message.senderId]) {
            fetchUserName(message.senderId);
            }
        });
        }
    }, (err) => {
        console.error("Error loading messages: ", err);
        error.value = "Failed to load messages: " + err.message;
    });

    return unsubscribe;
    };

    const fetchUserName = async (userId) => {
        if (userNames.value[userId]) return;

        try {
        const userDoc = await getDoc(doc(db, 'users', userId));
        if (userDoc.exists()) {
            const userData = userDoc.data();
            userNames.value[userId] = userData.userName || 'Unknown User';
        } else {
            userNames.value[userId] = 'Unknown User';
        }
        } catch (err) {
        console.error("Error fetching username: ", err);
        userNames.value[userId] = 'Unknown User';
        }
    };
    
    // const getUserName = (userId) => {
    //     return userNames.value[userId] || 'Loading...';
    // };

    const getUserName = (userId) => {
    if (!userNames.value[userId]) {
    fetchUserName(userId);
    return 'Loading...';
    }
    return userNames.value[userId];
};
    
    const selectPartner = (partner) => {
        selectedPartner.value = partner;
        loadMessages();
    };

    const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    };  
    
    const scrollToBottom = () => {
    if (messagesContainer.value) {
        messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
    }
    };

    
    onMounted(() => {

    onAuthStateChanged(auth, async (user) => {
        loading.value = true;
        if (user) {
            try {
                const userDocRef = doc(db, 'users', user.uid);
                const userDoc = await getDoc(userDocRef);
                if (userDoc.exists()) {
                    currentUser.value = { 
                        uid: user.uid, 
                        userName: userDoc.data().userName,
                        userType: userDoc.data().userType
                    };
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
            currentUser.value = null;
        }
        loading.value = false;
    });
});

    const loadAvailablePartners = async () => {
        if (!currentUser.value) return;

        isLoadingPartners.value = true;
        const usersRef = collection(db, 'users');
        const partnerType = currentUser.value.userType === 'restaurant' ? 'supplier' : 'restaurant';
        // console.log(partnerType, 123);
        const q = query(usersRef, where('userType', '==', partnerType), orderBy('userName'))
        
        try {
            const snapshot = await getDocs(q);
            availablePartners.value = snapshot.docs.map(doc => ({
            id: doc.id,
            userName: doc.data().userName,
            userType: doc.data().userType,
            }));
        } catch (err) {
            console.error("Error loading partners:", err);
            error.value = "Failed to load partners: " + err.message;
        } finally {
        isLoadingPartners.value = false;
        }
        };

        watch(selectedPartner, (newPartner) => {
    if (newPartner) {
    messages.value = []; // Clear existing messages
    loadMessages(); // Load new messages
    }
});
    const messageInputId = 'message-input';

    
    </script>

    
    
    <style scoped>

.chat-container {
    display: flex;
    flex-direction: column;
    height: 100vh;
    padding: 1rem;
}

.chat-window-view {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;  
}

.messages-container {
    flex-grow: 1;  
    overflow-y: auto;
    padding: 1rem;
}

.date-header {
    position: sticky;
    top: 0;
    background-color: #f0f0f0;
    padding: 5px;
    text-align: center;
    font-weight: bold;
    z-index: 1;
}

.messages {
    list-style-type: none;
    padding: 0;
}

.message-group {
    margin-bottom: 20px;
}

.sent, .received {
    margin: 10px 0;
    padding: 10px;
    border-radius: 5px;
}

.sent {
    background-color: #dcf8c6;
    text-align: right;
}

.received {
    background-color: #f0f0f0;
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
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    box-sizing: border-box;
}

.message-form input {
    flex-grow: 1;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px 0 0 4px;  
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

.partner-selection-view {
    width: 100%;  
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

.error-message {
    color: red;
    text-align: center;
    padding: 10px;
}

label {
    display: block;
    margin-bottom: 5px;
}

    </style>